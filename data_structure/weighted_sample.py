"""
Two method to do weighted sample.

SumTree is from (https://github.com/MorvanZhou/Reinforcement-learning-with-
                 tensorflow/blob/master/contents/5.2_Prioritized_Replay_DQN/
                 RL_brain.py)
It's a good algorithm!
"""

import numpy as np


class WeightedSample(object):
    def __init__(self, capacity):
        self.index = 0
        self.capacity = capacity

    def add(self, w):
        raise NotImplementedError

    def update(self, indices, weights):
        assert len(indices) == len(weights)
        raise NotImplementedError

    def sample(self, n):
        raise NotImplementedError


# SumTree
class SumTree(WeightedSample):
    def __init__(self, capacity):
        super(SumTree, self).__init__(capacity)
        self.tree = np.zeros(2 * capacity - 1)
        # [--------------Parent nodes-------------]
        #             size: capacity - 1
        # [-------leaves to recode weights-------]
        #              size: capacity

    def add(self, w):
        self._update(self.index, w)
        self.index += 1
        self.index %= self.capacity

    def _update(self, idx, w):
        tree_idx = idx + self.capacity - 1
        change = w - self.tree[tree_idx]
        self.tree[tree_idx] = w
        while tree_idx != 0:
            tree_idx = (tree_idx - 1) // 2
            self.tree[tree_idx] += change

    def update(self, indices, weights):
        assert len(indices) == len(weights)
        for idx, w in zip(indices, weights):
            self._update(idx, w)

    def get_leaf(self, v):
        parent_idx = 0
        while True:
            cl_idx = 2 * parent_idx + 1
            cr_idx = cl_idx + 1
            if cl_idx >= len(self.tree):
                leaf_idx = parent_idx
                break
            else:
                if v <= self.tree[cl_idx]:
                    parent_idx = cl_idx
                else:
                    v -= self.tree[cl_idx]
                    parent_idx = cr_idx

        data_idx = leaf_idx - self.capacity + 1
        return data_idx

    def sample(self, n):
        total_p = self.tree[0]
        idx = []
        for i in range(n):
            v = np.random.uniform(0, total_p)
            idx.append(self.get_leaf(v))

        return np.array(idx).astype(np.uint32)


class SumBinTree(SumTree):
    def __init__(self, capacity):
        self._capacity = capacity
        self.depth = self._depth(capacity)
        super(SumBinTree, self).__init__(2**(self.depth))

    @staticmethod
    def _depth(n):
        k = 0
        power = 1
        while n > power:
            k += 1
            power *= 2
        return k

    def add(self, w):
        self._update(self.index, w)
        self.index += 1
        self.index %= self._capacity

    def get_leaf(self, v):
        idx = 0
        for _ in range(self.depth):
            cl_idx = 2 * idx + 1
            cr_idx = cl_idx + 1
            if v <= self.tree[cl_idx]:
                idx = cl_idx
            else:
                v -= self.tree[cl_idx]
                idx = cr_idx
        data_idx = idx - self.capacity + 1

        assert data_idx >= 0 and data_idx < self._capacity
        return data_idx

    def sample(self, n):
        total_p = self.tree[0]
        idx = []
        for i in range(n):
            v = np.random.uniform(0, total_p)
            idx.append(self.get_leaf(v))
        return np.array(idx).astype(np.uint32)


class SumBinTreeFast(SumBinTree):
    def get_leaves(self, values):
        leaf_indices = np.zeros(len(values), dtype=np.uint32)
        for _ in range(self.depth):
            leaf_indices <<= 1
            leaf_indices += 1

            cond = values > self.tree[leaf_indices]
            values -= cond * self.tree[leaf_indices]
            leaf_indices += cond
        leaf_indices -= self.capacity - 1

        assert (leaf_indices >= 0).all() and (leaf_indices <
                                              self._capacity).all()
        return leaf_indices

    def sample(self, n):
        total_p = self.tree[0]
        values = np.random.uniform(0, total_p, size=n)
        idx = self.get_leaves(values)
        return idx


class Multinomial(WeightedSample):
    def __init__(self, capacity):
        super(Multinomial, self).__init__(capacity)
        self.weights = np.zeros(capacity)

    def add(self, p):
        self.weights[self.index] = p
        self.index += 1
        self.index %= self.capacity

    def update(self, indices, weights):
        assert len(indices) == len(weights)
        self.weights[indices] = weights

    def sample(self, n):
        idx = []
        for i, m in enumerate(
                np.random.multinomial(n, self.weights / sum(self.weights))):
            idx.extend([i] * m)
        return np.array(idx).astype(np.uint32)

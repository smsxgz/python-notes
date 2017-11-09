"""
Two method to do weighted sample.

SumTree is from https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow/blob/master/contents/5.2_Prioritized_Replay_DQN/RL_brain.py
It's a good algorithm, but np.random.multinomial is faster and better.
"""
import time
import numpy as np


# SumTree
class SumTree(object):
    index = 0

    def __init__(self, capacity):
        self.capacity = capacity
        self.tree = np.zeros(2 * capacity - 1)
        # [--------------Parent nodes-------------]
        #             size: capacity - 1
        # [-------leaves to recode weights-------]
        #              size: capacity

    def add(self, p):
        tree_idx = self.index + self.capacity - 1
        self.update(tree_idx, p)

        self.index += 1
        if self.index >= self.capacity:
            self.index = 0

    def update(self, tree_idx, p):
        change = p - self.tree[tree_idx]
        self.tree[tree_idx] = p
        while tree_idx != 0:
            tree_idx = (tree_idx - 1) // 2
            self.tree[tree_idx] += change

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

        return idx


if __name__ == '__main__':
    cap = 2 ** 20
    start = time.time()
    t = SumTree(cap)
    for _ in range(cap):
        t.add(np.random.random())
    t.sample(256)
    print(time.time() - start)

    start = time.time()
    weights = []
    for _ in range(cap):
        weights.append(np.random.random())
    idx = []
    for i, n in enumerate(
            np.random.multinomial(256, np.array(weights) / sum(weights))):
        idx.extend([i] * n)

    print(time.time() - start)

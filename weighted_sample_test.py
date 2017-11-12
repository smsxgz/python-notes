import time
import numpy as np
import weighted_sample as ws


# Do I wrote codes correctly?
def l2_er(t, cap, sample_n):
    er = 0.0
    for _ in range(10):
        weights = np.random.uniform(0, 2, size=cap)
        for i in range(cap):
            t.add(weights[i])

        er += np.linalg.norm(
            np.bincount(t.sample(sample_n)) / sample_n -
            weights / np.sum(weights))

    return er / 10


cap = 10
sample_n = 1000000

print(l2_er(ws.SumTree(cap), cap, sample_n))
print(l2_er(ws.SumBinTree(cap), cap, sample_n))
print(l2_er(ws.SumBinTreeFast(cap), cap, sample_n))
print(l2_er(ws.Multinomial(cap), cap, sample_n))


# Speed
class StopWatch(object):
    def __enter__(self, *args):
        self.start = time.time()

    def __exit__(self, *args):
        print(time.time() - self.start)


cap = 2**20
sample_n = 256


# init and add weights
def init_and_add(t_callable, cap):
    with StopWatch():
        t = t_callable(cap)
        for _ in range(cap):
            t.add(np.random.uniform(0, 2))
    return t


t1 = init_and_add(ws.SumTree, cap)
t2 = init_and_add(ws.SumBinTree, cap)
t3 = init_and_add(ws.SumBinTreeFast, cap)
t4 = init_and_add(ws.Multinomial, cap)


# sample and update
def sample_and_update(t, sample_n):
    with StopWatch():
        for _ in range(32):
            idx = t.sample(sample_n)
            t.update(idx, np.random.uniform(0, 2, size=sample_n))
            for _ in range(256):
                t.add(np.random.uniform(0, 2))


sample_and_update(t1, sample_n)
sample_and_update(t2, sample_n)
sample_and_update(t3, sample_n)
sample_and_update(t4, sample_n)

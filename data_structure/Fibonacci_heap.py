# https://blog.csdn.net/yzf0011/article/details/60574388

from math import log2


class FibonacciNode:
    def __init__(self, key):
        self.key = key
        self.degree = 0

        self.left = self
        self.right = self

        self.parent = None
        self.child = None

        self.marked = False

    def __repr__(self):
        return '({})'.format(self.key)


class FibonacciHeap:
    def __init__(self, node=None):
        if node:
            self.num_key = 1
            self.min_node = node
        else:
            self.num_key = 0
            self.min_node = None

    def merge(self, h2):
        self.num_key += h2.num_key

        if self.min_node is None:
            self.min_node = h2.min_node

        elif h2.min_node:
            min_h1 = self.min_node
            min_right_h1 = min_h1.right
            min_h2 = h2.min_node
            min_right_h2 = min_h2.right

            min_h1.right = min_right_h2
            min_right_h2.left = min_h1

            min_h2.right = min_right_h1
            min_right_h1.left = min_h2

            if self.min_node.key > h2.min_node.key:
                self.min_node = h2.min_node

    def insertKey(self, key):
        h = FibonacciHeap(FibonacciNode(key))
        self.merge(h)

    def extractMin(self):
        z = self.min_node
        if z is None:
            return

        self.num_key -= 1

        firstChid = z.child
        if firstChid:
            sibling = firstChid.right
            min_right = z.right

            z.right = firstChid
            firstChid.left = z
            min_right.left = firstChid
            firstChid.right = min_right

            firstChid.parent = None
            min_right = firstChid
            while firstChid is not sibling:
                sibling_right = sibling.right

                z.right = sibling
                sibling.left = z
                sibling.right = min_right
                min_right.left = sibling

                min_right = sibling
                sibling = sibling_right

                sibling.parent = None

        z.left.right = z.right
        z.right.left = z.left

        if z is z.right:
            self.min_node = None
        else:
            self.min_node = z.right
            self.consolidate()

        return z.key

    @staticmethod
    def link(y, x):
        """Link node y to x. """
        y.left.right = y.right
        y.right.left = y.left

        child = x.child
        if child is None:
            x.child = y
            y.left = y
            y.right = y
        else:
            y.right = child.right
            child.right.left = y
            y.left = child
            child.right = y
        y.parent = x
        x.degree += 1
        y.marked = False

    def consolidate(self):
        dn = int(log2(self.num_key)) + 2
        A = [None for i in range(dn)]

        w = self.min_node
        f = w.left

        while w is not f:
            d = w.degree
            x = w
            w = w.right
            while A[d]:
                y = A[d]
                if x.key > y.key:
                    x, y = y, x
                self.link(y, x)
                A[d] = None
                d += 1
            A[d] = x

        d = w.degree
        x = w
        w = w.right
        while A[d]:
            y = A[d]
            if x.key > y.key:
                x, y = y, x
            self.link(y, x)
            A[d] = None
            d += 1
        A[d] = x

        min_key = 100000
        for i in range(dn):
            if A[i] and A[i].key < min_key:
                self.min_node = A[i]
                min_key = A[i].key

    def decreaseKey(self, x, key):
        if key >= x.key:
            return

        x.key = key
        y = x.parent
        if y and x.key < y.key:
            self.cut(x, y)
            self.cascadingCut(y)

        if x.key < self.min_node.key:
            self.min_node = x

    def cut(self, x, y):
        if y.degree == 1:
            y.child = None
        else:
            x.left.right = x.right
            x.right.left = x.left

            y.child = x.right

        x.left = self.min_node
        x.right = self.min_node.right
        self.min_node.right = x
        x.right.left = x

        x.parent = None
        x.marked = False
        y.degree -= 1

    def cascadingCut(self, y):
        z = y.parent
        if z:
            if not y.marked:
                y.marked = True
            else:
                self.cut(y, z)
                self.cascadingCut(z)


if __name__ == '__main__':
    h = FibonacciHeap()
    h.insertKey(3)
    h.insertKey(2)
    h.insertKey(15)
    h.insertKey(5)
    h.insertKey(4)
    h.insertKey(45)

    h.extractMin()

    h.decreaseKey(h.min_node.right, 0)
    h.extractMin()

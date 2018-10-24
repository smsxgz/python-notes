# https://www.geeksforgeeks.org/implementation-binomial-heap/


class BionomialTree:
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.child = self.parent = self.sibling = None

    def __repr__(self):
        return '({})'.format(self.key)


def merge_two_bionomial_trees(t1, t2):
    if t1.key > t2.key:
        t1, t2 = t2, t1

    t2.parent = t1
    t2.sibling = t1.child
    t1.child = t2
    t1.degree += 1

    return t1


class BinomialHeap:
    def __init__(self):
        self.head = None

    def merge(self, h2):
        p1 = self.head
        p2 = h2.head

        if p1 is None or p2 is None:
            if p1 is None:
                self.head = p2
            else:
                self.head = p1
            return

        if p1.degree < p2.degree:
            self.head = p1
            p = self.head
            p1 = p1.sibling
        else:
            self.head = p2
            p = self.head
            p2 = p2.sibling

        while p1 and p2:
            if p1.degree < p2.degree:
                p.sibling = p1
                p = p1
                p1 = p1.sibling
            else:
                p.sibling = p2
                p = p2
                p2 = p2.sibling

        if p1:
            p.sibling = p1
        else:
            p.sibling = p2

        prev = None
        x = self.head
        next = x.sibling

        while next:
            if (x.degree != next.degree
                    or (next.sibling and x.degree == next.sibling.degree)):
                prev = x
                x = next
            else:
                temp = next.sibling
                x = merge_two_bionomial_trees(x, next)
                x.sibling = temp
                if prev:
                    prev.sibling = x
                else:
                    self.head = x

            next = x.sibling
        return

    def insertKey(self, key):
        temp_tree = BionomialTree(key)
        temp_heap = BinomialHeap()
        temp_heap.head = temp_tree
        self.merge(temp_heap)

    def extractMin(self):
        p = self.head

        if p is None:
            return

        x = p
        min = p.key
        p_prev = p
        p = p.sibling
        while p:
            if p.key < min:
                x_prev = p_prev
                x = p
                min = p.key
            p_prev = p
            p = p.sibling

        if x is self.head:
            self.head = x.sibling
        elif x.sibling is None:
            x_prev.sibling = None
        else:
            x_prev.sibling = x.sibling

        child_x = x.child
        if child_x:
            h1 = BinomialHeap()
            child_x.parent = None
            h1.head = child_x
            p = child_x.sibling
            child_x.sibling = None
            while p:
                p_prev = p
                p = p.sibling
                p_prev.sibling = h1.head
                h1.head = p_prev
                p_prev.parent = None
            self.merge(h1)

        return min

    def decreaseKey(self, x, key):
        if x.key < key:
            return

        x.key = key

        y = x
        p = x.parent
        while p and y.key < p.key:
            y.key = p.key
            p.key = key
            y = p
            p = y.parent


def printHeap(heap):
    def printTree(h, prefix=0):
        while h:
            print(' ' * (2 * prefix) + str(h.key))
            printTree(h.child, prefix + 1)
            h = h.sibling

    printTree(heap.head)


if __name__ == '__main__':
    h = BinomialHeap()
    h.insertKey(3)
    h.insertKey(2)
    h.insertKey(15)
    h.insertKey(5)
    h.insertKey(4)
    h.insertKey(45)

    for i in range(15):
        h.insertKey(i)

    h.extractMin()
    printHeap(h)

    h.decreaseKey(h.head.sibling.child.child, -2)
    printHeap(h)

    h.extractMin()
    printHeap(h)

    h.extractMin()
    printHeap(h)

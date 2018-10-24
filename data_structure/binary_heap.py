# See https://www.geeksforgeeks.org/binary-heap/ for more details


class MinHeap:
    def __init__(self, capacity):
        self.capacity = capacity
        self.heap_size = 0
        self.harr = [None] * capacity

    @staticmethod
    def parent(i):
        return (i - 1) // 2

    @staticmethod
    def left(i):
        return 2 * i + 1

    @staticmethod
    def right(i):
        return 2 * i + 2

    def swap(self, i, j):
        self.harr[i], self.harr[j] = self.harr[j], self.harr[i]

    def insertKey(self, key):
        if self.heap_size == self.capacity:
            print('Overflow: Could not insertKey!')
            return

        self.heap_size += 1
        i = self.heap_size - 1
        self.harr[i] = key

        while i != 0 and self.harr[self.parent(i)] > self.harr[i]:
            self.swap(self.parent(i), i)
            i = self.parent(i)

    def extractMin(self):
        if self.heap_size == 0:
            print("Empty heap!")
            return
        elif self.heap_size == 1:
            self.heap_size -= 1
            return self.harr[0]

        root = self.harr[0]
        self.harr[0] = self.harr[self.heap_size - 1]
        self.heap_size -= 1
        self.MinHeapify(0)
        return root

    def MinHeapify(self, i):
        """
        A recursive method to heapify a subtree with the root at given index.
        This method assumes that the subtrees are already heapified.
        """
        l = self.left(i)
        r = self.right(i)
        smallest = i
        if l < self.heap_size and self.harr[l] < self.harr[i]:
            smallest = l
        if r < self.heap_size and self.harr[r] < self.harr[smallest]:
            smallest = r
        if smallest != i:
            self.swap(i, smallest)
            self.MinHeapify(smallest)


if __name__ == '__main__':
    h = MinHeap(11)
    h.insertKey(3)
    h.insertKey(2)
    h.insertKey(15)
    h.insertKey(5)
    h.insertKey(4)
    h.insertKey(45)
    print(h.extractMin())
    print(h.extractMin())
    print(h.extractMin())
    print(h.extractMin())

class LeftistNode:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.parent = None

        self.dist = 0
        self.key = key

    def fix(self):
        if self.left and self.right and self.left.dist < self.right.dist:
            self.left, self.right = self.right, self.left

        elif self.right and self.left is None:
            self.left = self.right
            self.right = None

        if self.right:
            self.dist = self.right.dist + 1
        else:
            self.dist = 0

    def __str__(self, level=0):
        ret = "\t" * level + repr(self.key) + "\n"
        if self.left:
            ret += 'L: ' + self.left.__str__(level + 1)
        if self.right:
            ret += 'R: ' + self.right.__str__(level + 1)
        return ret


def _merge(root1, root2):
    if root1 is None:
        return root2
    if root2 is None:
        return root1

    if root1.key > root2.key:
        root1, root2 = root2, root1

    tmp = _merge(root1.right, root2)
    tmp.parent = root1
    root1.right = tmp
    root1.fix()
    return root1


class LeftistHeap:
    def __init__(self, node=None):
        self.root = node

    def merge(self, h2):
        if h2.root is None:
            return

        if self.root is None:
            self.root = h2.root
            return

        self.root = _merge(self.root, h2.root)

    def insertKey(self, key):
        self.merge(LeftistHeap(LeftistNode(key)))

    def extractMin(self):
        if self.root is None:
            return

        key = self.root.key
        self.root = _merge(self.root.left, self.root.right)
        self.root.parent = None
        return key

    def decreaseKey(self, x, key):
        if x.key < key:
            return

        x.key = key
        y = x
        p = x.parent
        while p and y.key < p.key:
            print(self.root)
            y.key = p.key
            p.key = key
            y = p
            p = y.parent


if __name__ == '__main__':
    h = LeftistHeap()
    h.insertKey(3)
    h.insertKey(2)
    h.insertKey(15)
    h.insertKey(5)
    h.insertKey(4)
    h.insertKey(45)

    h.extractMin()
    print(h.root)

    h.decreaseKey(h.root.left.left, -1)
    print(h.root)

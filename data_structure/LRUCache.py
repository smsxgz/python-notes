class Node:
    def __init__(self, prev=None, next=None, key=None, value=None):
        self.prev = prev
        self.next = next
        self.key = key
        self.value = value

    def __repr__(self):
        res = '({}: {})'.format(self.key, self.value)
        node = self
        while node.next is not None:
            node = node.next
            res += '--> ({}: {})'.format(node.key, node.value)
        return res


class LRUCache(object):
    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.capacity = capacity
        self.head = Node()
        self.tail = self.head
        self.dict = dict()

    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        if key not in self.dict:
            return -1
        node = self.dict[key]
        if node.next is None:
            return node.value
        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev, node.next = self.tail, None
        self.tail.next = node
        self.tail = node
        return node.value

    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: void
        """
        if key in self.dict:
            self.get(key)
            self.tail.value = value
        else:
            node = Node(prev=self.tail, key=key, value=value)
            self.tail.next = node
            self.tail = node
            self.dict[key] = node
            if len(self.dict) > self.capacity:
                self.dict.pop(self.head.next.key)
                self.head.next = self.head.next.next
                self.head.next.prev = self.head


if __name__ == '__main__':
    for op, args in zip([
            "LRUCache", "put", "put", "get", "get", "get", "put", "put", "get",
            "get", "get", "get"
    ], [[3], [2, 2], [1, 1], [2], [1], [2], [3, 3], [4, 4], [3], [2], [1], [4]
        ]):
        if op == "LRUCache":
            cache = LRUCache(*args)
        elif op == "put":
            print(cache.put(*args))
        else:
            print(cache.get(*args))
        print(op, args, cache.head)

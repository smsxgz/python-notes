class SinglyLinkedListNode:
    def __init__(self, obj, next=None):
        self.obj = obj
        self.next = next


class SinglyLinkedList:
    def __init__(self):
        self.start = self.end = None
        self.size = 0

    def appendleft(self, obj):
        if self.start is None:
            self.start = self.end = SinglyLinkedListNode(obj)
        else:
            self.start = SinglyLinkedListNode(obj, self.start)
        self.size += 1

    def append(self, obj):
        if self.start is None:
            self.start = self.end = SinglyLinkedListNode(obj)
        else:
            temp = SinglyLinkedListNode(obj)
            self.end.next = temp
            self.end = temp
        self.size += 1

    def __len__(self):
        return self.size

    def __repr__(self):
        res = []
        temp = self.start
        while temp:
            res.append(str(temp.obj))
            temp = temp.next
        return '->'.join(res)

    def __iter__(self):
        temp = self.start
        while temp:
            yield temp.obj
            temp = temp.next


if __name__ == '__main__':
    linked_list = SinglyLinkedList()
    for i in range(5):
        linked_list.append(2 * i)
        linked_list.appendleft(2 * i + 1)
        print(linked_list)

    for obj in linked_list:
        print(obj)

class Node:
  def __init__(self, data):
    self.data = data
    self.next = None

class Queue:
    """Queue ADT implemented as a linked list."""

    def __init__( self, bound = None ):
        """ Queue starts out empty. If bound == None, the queue
        is unbounded. Otherwise set the capacity of the queue
        to be the integer value of bound. """
        self.head = None
        self.tail = None
        self.length = 0
        self.capacity = bound

    def __len__( self ):
        """ Return the current size of the queue. """
        count = 0
        cur = self.head
        while cur:
          count += 1
          cur = cur.next
        self.length = count
        return self.length

    def is_empty(self):
        """ Returns true if the queue is empty, false otherwise. """
        return self.head == None

    def enqueue(self, item):
        """ If full and bounded, return -1 to indicate failure. """
        
        new_node = Node(item)

        if self.is_empty():
          self.head = new_node
          self.tail = new_node
          self.length += 1


        else:
          self.tail.next = new_node
          self.tail = new_node
          self.length += 1



    def dequeue(self):
        """ DeQ and return item. If empty, return None. """
        
        if self.is_empty():
          return None
        
        temp = self.head
        self.head = self.head.next
        
        if self.is_empty():
          self.tail = None
        
        deQ_node = temp.data
        self.length -= 1
        return deQ_node



    def peek(self):
        """ Return the item that would be dequeue'd next.
            If empty, return None. """
        print(self.capacity)
        if self.is_empty():
          return None
        
        return self.head.data

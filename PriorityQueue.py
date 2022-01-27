"""
This class implements a linked priority queue with a head.
Priorities are positive integers where the highest priority is zero. This queue is a linked list. The base class Queue has been implemented as linked list.
"""

from Queue import Queue
from Queue import Node

class PNode(Node):
  def __init__(self, data, precedence):
    super().__init__(data)
    self.priority = precedence


class PriorityQueue( Queue ):

    def __init__( self, minPriority = 15 ):
        """Initialize the queue with a default number of priority classes."""
        super().__init__()

    def __str__( self ):
        """
        Returns the name of the queue
        """
        return "PriorityQueue"

    def enqueue( self, priority, item ):
        """
        Inserts an item with priority at the right place.
        """

        new_node = PNode(item, priority)
        
        if self.is_empty():
          self.head = new_node
          self.tail = new_node
          self.length += 1

        elif new_node.priority < self.head.priority:
          new_node.next = self.head
          self.head = new_node
          self.length += 1

        elif new_node.priority >= self.tail.priority:
          self.tail.next = new_node
          self.tail = self.tail.next
          self.length += 1

        else:          
          temp_node = self.head.next
          other_node = self.head

          while temp_node.priority <= new_node.priority:
            temp_node = temp_node.next
            other_node = other_node.next
          other_node.next = new_node
          new_node.next = temp_node
          self.length += 1


    #def dequeue( self ):
        """Remove the item with most preferred priority."""
        #super().dequeue()


"""This class should implement nodes for a singly linked list with a priority."""
import math
from node import Node_stack

# preserves last 25 actions
class Stack():
  def __init__(self):
    self.name = "Stack Actions"
    self.head = None
    self.default = Node_stack('team', 'player', 'stat', 0)

  def __str__(self):
    ret = ''
    if self.head is None:
      ret += 'Stack empty'
      return ret
    curr = self.head
    indx = 1
    while curr is not None:
      ret += f"\nStack {indx}: {curr.team}-{curr.player}-{curr.stat}-{curr.val}"
      curr = curr.next
    return ret
  
  def is_empty(self):
    return self.head is None
  
  def get_size(self):
    if self.is_empty:
      return self.default
    count = 0
    curr = self.head 
    while curr is not None:
      coutn += 1 
      curr = curr.next 
    return count
  
  def get_first(self):
    if self.is_empty:
      return self.default
    return self.head
  
  def get_last(self):
    if self.is_empty:
      return self.default
    curr = self.head 
    while curr.next is not None:
      curr = curr.next 
    return curr
    
  def add_node(self, team, player, stat, val):
    new_node = Node_stack(team, player, stat, val)
    if self.head is None:
      self.head = new_node 
    else:
      curr = self.head 
      while curr.next is not None:
        curr = curr.next 
      curr = new_node
  
  def remove_last(self):
    if self.is_empty:
      return 0
    prev = None
    curr = self.head 
    while curr.next is not None:
      prev = curr
      curr = curr.next
    prev.next = None



  
import math
from node import Node_stack

# preserves last 25 actions
class Stack():
  def __init__(self):
    self.name = "Stack Actions"
    self.lst = []

  def __str__(self):
    ret = ''
    if len(self.lst) > 0:
      return ret
    for el in self.lst:
      indx = self.lst.index(el) + 1
      ret += f'{indx}: {el}\n'
    return ret
  
  def is_empty(self):
    return len(self.lst) == 0
  
  def get_size(self):
    return len(self.lst)
  
  def get_first(self):
    if len(self.lst) > 0:
      return self.lst[0] 
  
  def get_last(self):
    if len(self.lst) > 0:
      return self.lst[-1]
    
  def add_node(self, team, player, stat, val):
    new_node = Node_stack(team, player, stat, val)
    self.lst.append(new_node)
  
  def remove_last(self):
    if len(self.lst) > 0:
      self.lst.pop()


  
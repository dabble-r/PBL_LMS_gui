import math

# preserves last 25 actions
class Stack():
  def __init__(self, name, max=25, lst=[]):
    self.name = name 
    self.max = max 
    self.lst = lst 

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
    
  def append(self, action):
    if len(self.lst) < self.max:
      self.lst.append(action)
    else:
      self.lst.pop(0)
      self.lst.append(action)
  
  def remove_last(self):
    if len(self.lst) > 0:
      self.lst.pop()

  def remove_first(self):
    if len(self.lst) > 0:
      self.lst.pop(0)


  
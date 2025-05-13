
class Node():
  def __init__(self, team, next=None):
    self.team = team
    self.next = next

class Node_stack():
  def __init__(self, team, player, stat, val, next=None):
    self.team = team 
    self.player = player
    self.stat = stat 
    self.val = val 
    self.next = next
from node import Node
#from team import beef, rougarou

class LinkedList():
  COUNT = 0

  @classmethod
  def get_count(cls):
    return cls.COUNT 
  
  @classmethod
  def set_count(cls):
    cls.COUNT += 1
  
  def __init__(self, name, head=None):
    self.name = name
    self.head = head  
  
  def add_team(self, val):
    new_node = Node(val)
    if self.head == None:
      self.head = new_node 
      self.head.next = None
      LinkedList.set_count()
      return
    curr = self.head
    while curr.next != None:
      curr = curr.next
    curr.next = new_node
    new_node.next = None
    LinkedList.set_count()
    return
  
  def remove_team(self, target):
    traverser = self.head 
    if traverser.team.name == target:
      self.head = None
      LinkedList.COUNT = 0
      #print(f'Removing {target}')
      return
    while traverser.next != None:
      #print('team name', traverser.team.name)
      if traverser.next.team.name == target:
        #print('found', target)
        traverser.next = traverser.next.next
        traverser.next = None
        LinkedList.COUNT -= 1
        #print(f'Removing {target}')
        return
      else:
        traverser = traverser.next 
    #print('end of list')
  
  def find_team(self, target):
    traverser = self.head
    if traverser == None:
      #print('No teams in league\n')
      return None
    if traverser.team.name == target:
      return traverser.team
    else:
      while traverser.next != None:
        if traverser.next.team.name == target:
          return traverser.next.team
        traverser = traverser.next 
    #print('Team not found')
    return None
  
  def view_all(self):
    if LinkedList.COUNT == 0:
      print('No teams in league')
      return ''
    else:
      ret = ''
      traverser = self.head 
      while traverser != None:
        ret += f'\nTeam: {traverser.team.name}\nPlayers: {[{x.name: x.positions[0]} for x in traverser.team.players]}'
        traverser = traverser.next
      return ret
    
  def __str__(self):
    if LinkedList.COUNT == 0:
      print('No teams in league')
      return ''
    else:
      ret = ""
      traverser = self.head
      while traverser.next != None:
        tmp = f'Team: {traverser.team.name}\n'
        ret += tmp
        tmp = ''
        traverser = traverser.next
      ret += f'Team: {traverser.team.name}\n'
      return ret

# create league
#PBL = LinkedList('People\'s Baseball League')

#add team to league
#PBL.add_team(beef)
#PBL.add_team(rougarou)

# view all players
#all_players_league = PBL.view_all()
#print(all_players_league)

#find existing team in league
#team_search = PBL.find_team('Rougarou')
#print(team_search)

# curr state of league, view all teams
#print(PBL)



  

  


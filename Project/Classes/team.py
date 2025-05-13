from Classes.player import Player
import math

class Team():
  def __init__(self, name, max=math.inf):
    self.name = name  
    self.players = []
    self.lineup = {}
    self.positions = {
        'catcher': None,
        'pitcher': None,
        'first base': None,
        'second base': None,
        'third base': None,
        'shortstop': None,
        'left field': None,
        'center field': None,
        'right field': None
        }
    self.max = max
  
  def __str__(self): 
    ret = ''
    #print(self.players)
    ret += f'Team: {self.name}\nRoster: {self.get_size()} / {self.max if self.max < 50 else "No Max"}\nPlayers: {[x.name for x in self.players]}'
    return ret
  
  def set_max(self, val):
    self.max = val

  def get_size(self):
    return len(self.players)
  
  def set_lineup(self, order, name):
    if order > self.get_size():
      print(f'No position {order} in batting order. Try number less than {self.get_size() + 1}\n')
      return
    if order in self.lineup:
      flag_action = input(f'Would you like to replace {self.lineup[order]} at spot {order}? y/n ').lower() == 'y'
      if not flag_action:
        return 
      self.lineup[order] = name 
    else:
      self.lineup[order] = name
     
  def get_lineup(self):
    ret = ''
    for el in self.lineup:
      ret += f'{el}: {self.lineup[el]}\n' 
    return ret
      
  def set_positions(self, name, position):
    if self.positions[position] != None:
      flag_action = input(f'Would you like to replace {self.positions[position]} at {position}? y/n ').lower() == 'y'
      if not flag_action:
        return 
      self.positions[position] = name 
    else:
      self.positions[position] = name
    
  def get_positions(self):
    ret = ''
    for el in self.positions:
      ret += f'{el}: {self.positions[el]}\n'
    return ret 

  def get_player(self, target):
    for el in self.players:
      if el.name == target:
        #print(el)
        return el
    #print('Player not found')
    return

  def add_player(self, new_player):
    if len(self.players) < self.max:
      self.players.append(new_player)
    else:
      print('Roster is full')
      return

  def remove_player(self, player):
    indx = None
    for i in range(len(self.players)):
      if self.players[i].name == player:
        #print(self.players)
        #print('index', i)
        #print('player found\n', self.players[i])
        #print('player found\n', self.players[i].name)
        indx = i
    self.players.pop(indx)
    return self.players

'''
# create rougarou sliders team isntance
beef = Team('Beef Sliders')
beef.set_max(15)

# populate team with players
beef.add_player('Nick', 18, 'Beef Sliders', ['second base', 'pitcher', 'left field'])
beef.add_player('Jeremy', 12, 'Beef Sliders', ['pitcher', 'shortstop'])
beef.add_player('Justin', 6, 'Beef Sliders', ['left field', 'second base'])
beef.add_player('Chance', 4, 'Beef Sliders', ['catcher'])
beef.add_player('Nashon', 2, 'Beef Sliders', ['first base', 'center field'])
beef.add_player('John', 35, 'Beef Sliders', ['first base', 'second base'])
beef.add_player('Andrew', 74, 'Beef Sliders', ['second base', 'pitcher', 'left field'])
beef.add_player('Ben', 0, 'Beef Sliders', ['pitcher', 'shortstop'])
beef.add_player('Gavin M', 0, 'Beef Sliders', ['pitcher', 'shortstop'])
beef.add_player('Josh', 0, 'Beef Sliders', ['lfet field', 'right field'])
beef.add_player('Patrick', 0, 'Beef Sliders', ['right field', 'left field'])
beef.add_player('Ryan', 0, 'Beef Sliders', ['right field', 'left field'])
beef.add_player('Joe', 13, 'Beef Sliders', ['shortstop'])
beef.add_player('Gavin P', 0, 'Beef Sliders', ['first base', 'center field'])
beef.add_player('Freddie', 0, 'Beef Sliders', ['right field', 'center field'])

roster_size = beef.get_size()
#print(roster_size)

# set team batting order
beef.set_lineup(1, 'Nick')
beef.set_lineup(2, 'Justin')
beef.set_lineup(3, 'Jeremy')
beef.set_lineup(4, 'Chance')
beef.set_lineup(5, 'Nashon')
beef.set_lineup(6, 'John')
beef.set_lineup(7, 'Andrew')
beef.set_lineup(8, 'Ben')
beef.set_lineup(9, 'Gavin M')
beef.set_lineup(10, 'Josh')
beef.set_lineup(11, 'Patrick')
beef.set_lineup(12, 'Ryan')
beef.set_lineup(13, 'Joe')
beef.set_lineup(14, 'Gavin P')
beef.set_lineup(15, 'Freddie')
#beef.set_lineup(16, 'Freddie')
lineup = beef.get_lineup()
#print(lineup)

# set team defense positions
beef.set_positions('Chance', 'catcher')
beef.set_positions('John', 'first base')
beef.set_positions('Nick', 'second base')
beef.set_positions('Andrew', 'third base')
beef.set_positions('Joe', 'shortstop')
beef.set_positions('Patrick', 'right field')
beef.set_positions('Nashon', 'center field')
beef.set_positions('Justin', 'left field')
beef.set_positions('Jeremy', 'pitcher')
#beef.set_positions('Andrew', 'second base')
positions = beef.get_positions()
#print(positions)

#print(beef)

# create rougarou team instance
rougarou = Team('Rougarou')
rougarou.set_max(15)

# populate team with players
rougarou.add_player('Nick', 18, 'Rougarou', ['second base', 'pitcher', 'left field'])
rougarou.add_player('Jeremy', 12, 'Rougarou', ['pitcher', 'shortstop'])
rougarou.add_player('Justin', 6, 'Rougarou', ['left field', 'second base'])
rougarou.add_player('Chance', 4, 'Rougarou', ['catcher'])
rougarou.add_player('Nashon', 2, 'Rougarou', ['first base', 'center field'])
rougarou.add_player('John', 35, 'Rougarou', ['first base', 'second base'])
rougarou.add_player('Andrew', 74, 'Rougarou', ['second base', 'pitcher', 'left field'])
rougarou.add_player('Ben', 0, 'Rougarou', ['pitcher', 'shortstop'])
rougarou.add_player('Gavin M', 0, 'Rougarou', ['pitcher', 'shortstop'])
rougarou.add_player('Josh', 0, 'Rougarou', ['lfet field', 'right field'])
rougarou.add_player('Patrick', 0, 'Rougarou', ['right field', 'left field'])
rougarou.add_player('Ryan', 0, 'Rougarou', ['right field', 'left field'])
rougarou.add_player('Joe', 13, 'Rougarou', ['shortstop'])
rougarou.add_player('Gavin P', 0, 'Rougarou', ['first base', 'center field'])
rougarou.add_player('Freddie', 0, 'Rougarou', ['right field', 'center field'])

roster_size = rougarou.get_size()
#print(roster_size)

# set team batting order
rougarou.set_lineup(1, 'Nick')
rougarou.set_lineup(2, 'Justin')
rougarou.set_lineup(3, 'Jeremy')
rougarou.set_lineup(4, 'Chance')
rougarou.set_lineup(5, 'Nashon')
rougarou.set_lineup(6, 'John')
rougarou.set_lineup(7, 'Andrew')
rougarou.set_lineup(8, 'Ben')
rougarou.set_lineup(9, 'Gavin M')
rougarou.set_lineup(10, 'Josh')
rougarou.set_lineup(11, 'Patrick')
rougarou.set_lineup(12, 'Ryan')
rougarou.set_lineup(13, 'Joe')
rougarou.set_lineup(14, 'Gavin P')
rougarou.set_lineup(15, 'Freddie')
#rougarou.set_lineup(16, 'Freddie')
lineup = rougarou.get_lineup()
#print(lineup)

# set team defense positions
rougarou.set_positions('Chance', 'catcher')
rougarou.set_positions('John', 'first base')
rougarou.set_positions('Nick', 'second base')
rougarou.set_positions('Andrew', 'third base')
rougarou.set_positions('Joe', 'shortstop')
rougarou.set_positions('Patrick', 'right field')
rougarou.set_positions('Nashon', 'center field')
rougarou.set_positions('Justin', 'left field')
rougarou.set_positions('Jeremy', 'pitcher')
#rougarou.set_positions('Andrew', 'second base')
positions = rougarou.get_positions()
#print(positions)

#print(rougarou)
'''

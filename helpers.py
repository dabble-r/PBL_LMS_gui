from team import Team
from menu import Menu

# simple helpers

def user_continue(flag):
  if flag:
    action = input('Would you like to perform another action? y/n \n').lower().strip()
    if action == 'y' or action == 'n':
      return action == 'y'
    else:
      print('Session terminated')  
      return False
  else:
    action = input('Would you like to perform another action? y/n \n').lower().strip()

def user_update_continue(flag, inst):
  if flag:
    action = input(f'Would you like to continue updating {inst.name}?: y/n \n').lower().strip()
    if action == 'y' or action == 'n':
      return action == 'y' 
    else:
      print('Enter valid response:\n') 
      action = input(f'Would you like to continue updating {inst.name}?: y/n \n').lower().strip()
  else:
    user_continue(True)

def curr_menu(action):
  menu = action[1]
  return menu

def user_add_re():
  action = input('Would you like to add values or reassign stat to new value?: add/reassign ').lower().strip()
  if action == 'add' or action == 'reassign':
    #print('action', action)
    return action == 'add' 
  action = input('Would you like to add values or reassign stat to new value?: add/reassign ').lower().strip()

def user_start(league):
  #action = menu_1(league)
  action = menus.select_option(1)(league)
  #print('menu 1/usr cont - action', action)
  test = range(1,11)
  try:
    if int(action) in test:
      #print('user action', action)
      return action
  except:
    print(f'\nError: enter valid response\n')   
    action = menus.select_option(1)(league)
 
def is_None(val):
  return val is None

def not_found(val):
  print(f'{val} not found')

def found(val):
  print(f'\nFound:\n{val}')

def input_error(lst, num):
  ret = 'Input error:\n'
  for el in lst:
    ret += f'{el}\n'
  ret += f'Required input length: {num}'
  print(ret)

def no_teams():
  print('Player can\'t be searched or created. No teams exist')

def show_AVG(val):
  print(f'Curr avg:\n{val.get_AVG()}')

def input_len(lst, num):
  return len(lst) == num

def player_state(inst=None):
  #print('Player', inst)
  if inst is not None:
    return inst 
  return None

# prompts user to save progress
# returns boolean True if user wants to save
def save_action():
  action = input('Would you like to save progress: y/n ?\n ').lower().strip()
  if action == 'y' or action == 'n':
    return action == 'y' 
  else:
    action = input('Would you like to save progress: y/n ?\n ').lower().strip()

#------------------------------------------------------------------------#

# complex helpers

# if league has no teams, returns false
# handles invalid input types/erros
def league_empty_initial(league, action):
    if not isinstance(action, int):
        try:
            action = int(action)
        except (ValueError, TypeError):
            return False  # Handle invalid action inputs safely
    
    if action in range(1, 5):  # Explicitly checks action validity
        return league.get_count() == 0

    return False

def save_progress():
  pass

def hide_menu(frame):
  frame.pack_forget()
#------------------------------------------------------------------------#

# menu functionality

# search existing player
def search_player(league):
  #print('search pl\n')
  player_raw = input('Enter the player name and player team name to search in a comma separated list: ')
  player_data = player_raw.split(',')
  if len(player_data) != 2:
    input_error(player_data, 2)
  else:
    name = player_data[0].strip()
    team = player_data[1].strip()  
    find_team = league.find_team(team) 
    if is_None(find_team):
      not_found(team) 
      print('Available Teams:\n',league)
    else:
      find_player = find_team.get_player(name)  
      if is_None(find_player):
        not_found(name)
      else:
        print(f'Searching {find_player.name}')
        found(find_player)

# general stat update
def update_stat(update_player):
  try:
    stat, val = map(lambda x: x.strip(), input('Enter stat to update and value in a comma separated list: ').split(',')) 
  except ValueError:
    print('Error: must enter stat and value')
    stat, val = map(lambda x: x.strip(), input('Enter stat to update and value in a comma separated list: ').split(',')) 
  attr = f'set_{stat}'
  if hasattr(update_player, attr):
    method = getattr(update_player, attr)
    if callable(method):
      print('callable', method)
      set_stat(method, int(val))

# 
def set_stat(method, val):
  try:
    method(val)
  except Exception as e:
    print(f'Error: {e}')

# update existing player
def update_player(league, update_raw, stat, val):
  player_data = update_raw.split(',')
  name, team = player_data
  find_team = league.find_team(team.strip())
  find_player = find_team.get_player(name.strip())
  print(f'Updating Player: {find_player}')
  print('update stat', stat)
  match stat:
    case 'at_bats':
      at_bats_int = val
      find_player.set_at_bat(at_bats_int)
      find_player.set_AVG()
      
    case 'hits':
      hits_int = int(val)
      find_player.set_hit(hits_int)
      find_player.set_AVG()
       
    case 'walks':
      walks_int = int(val)
      find_player.set_bb(walks_int)
      find_player.set_AVG()

    case 'SO':
      so_int = int(val)
      find_player.set_so(so_int)
      find_player.set_AVG()

    case 'HR':
      hr_int = int(val)
      find_player.set_hr(hr_int)
      find_player.set_AVG()
      
    case 'RBI':
      rbi_int = int(val)
      find_player.set_rbi(rbi_int)
      find_player.set_AVG()
      
    case 'runs':
      runs_int = int(val)
      find_player.set_runs(runs_int)
      find_player.set_AVG()
     
    case 'singles':
      singles_int = int(val)
      find_player.set_singles(singles_int)
      find_player.set_AVG()
      
    case 'doubles':
      doubles_int = int(val)
      find_player.set_doubles(doubles_int)
      find_player.set_AVG()
      
    case 'triples':
      triples_int = int(val)
      find_player.set_triples(triples_int)
      find_player.set_AVG()

    case 'sac_fly':
      sac_fly_int = int(val)
      find_player.set_sac_fly(sac_fly_int)
      find_player.set_AVG()

  print(find_player) 
  return find_player

# remove exisiting player
def remove_player(league):
  print('remove player\n')
  player_raw = input('Enter a name and a team in a comma separated list: ')
  player_data = player_raw.split(',')
  name = player_data[0].strip()
  team = player_data[1].strip()
  find_team = league.find_team(team)
  if is_None(find_team):
    not_found(team)
    print('Available Teams:\n',league)
  else:
    find_player = find_team.get_player(name)
    if is_None(find_player):
      not_found(name)
    else:
      #found(name)
      print(f'Removing {name}')
      find_team.remove_player(name)

# create new player
def create_player(league, player_raw):    
  #new_player_raw = input('Enter new player name, number, team, and positions played separated by a comma: ')  
  ret = None
  new_player_data = player_raw.split(',')
  if len(new_player_data) < 4:
    print('Enter name, number, team, and at least one position')
    ret = 'Enter name, number, team, and at least one position'
    return ret
    #new_player_raw = input('Enter new player name, number, team, and positions played separated by a comma: ') 
    #flag_action = input('Would you like to perform another action? y/n ').lower().strip() == 'y'
  else:
    name = new_player_data[0].strip()
    number = new_player_data[1].strip()
    team = new_player_data[2].strip()
    #print('team', team)
    positions = [x.strip() for x in new_player_data[3:]]
    #print('new player',new_player)
    find_team = league.find_team(team)
    #print('find team', find_team.team)
    if is_None(find_team):
      ret = f'Team {team} not found'
      return ret
      #not_found(team)
      #print('Available Teams:\n',league)
      #new_player_raw = input('Enter new player name, number, team, and positions played separated by a comma: ') 
      #flag_action = input('Would you like to perform another action? y/n ').lower().strip() == 'y'
    elif find_team:
      #print(f'Creating player:\n {name}\n {number}\n {team}\n {positions}')
      find_team.add_player(name, number, team, positions)
      ret = [name, number, team, positions]
      #print('raw', new_player_raw)
      #print('split', new_player)
      #print(name, number, positions)
      #print('new player', new_player)
      #print('team', find_team)
      return ret

# view all team in league
def view_all(league):
  #print('view all teams')
  all_players = league.view_all()
  print(all_players)

# create new team in league
def create_team(league, team_raw):
  #print('create t\n')
  #hide_menu(menu)
  #new_team_raw = input('Enter a team name and an optional max number of players in a comma separated list: ')
  new_team_list = team_raw.split(',')
  name = new_team_list[0]
  new_team = None
  if len(new_team_list) == 2:
    max = int(new_team_list[1])
    new_team = Team(name, max)
  else:
    new_team = Team(name)
  league.add_team(new_team)
  print(f'Creating {new_team}')
  print(league.COUNT)

# remove one team in league
def remove_team(league):
  #print('remove t\n')
  team = input('Enter a team to remove: ').strip()
  if is_None(team):
    not_found(team)
    print('Available Teams:\n',league)
    team = input('Enter a team to remove: ').strip()
  league.remove_team(team)
  print(f'Removing team {team}\n')

# search one team in league
def search_team(league):
  team_raw = input('Enter a team to search: \n').strip()
  team = league.find_team(team_raw)
  if is_None(team):
    not_found(team)
    print('Available Teams:\n',league)
    team_raw = input('Enter a team to search: \n').strip()
  print(f'\n{team}\n')
  return team

def quit():
  print("Session terminated\n")
  return
#------------------------------------------------------------------------#

# user menus

# initial menu

def menu_1(league):
  print(f'Welcome to the {league.name}\n')
  user_action = input('Please select action:\n   1) Create Player\n   2) Search Player\n   3) Update Player\n   4) Remove Player\n\
   5) View all players\n   6) Create Team\n   7) Search Team\n   8) View all teams\n   9) Remove Team\n   10) Quit\nResponse: ')
  return user_action

# initial player stat update menu

def menu_2(player):
  print(f'{player.name} stats update:\n')
  user_action = input('Please select action:\n   1) Update offensive stats\n   2) Update defensive stats\n   3) Quit\nResponse: ')
  return user_action

# offensive player stats update menu

def menu_3(player):
  print(f'{player.name} stats update:\n')
  user_action = input('Please select action:\n   1) At Bats\n   2) Hits\n   3) Walks\n   4) SO\n   5) HR\n\
   6) RBI:\n   7) Runs:\n   8) Singles:\n   9) Doubles:\n   10) Triples:\n   11) Sac Fly:\n\
   12) Quit\nResponse: ')
  return user_action

# Menu options

options = [
    {"name": "menu 1", "action": menu_1},
    {"name": "menu 2", "action": menu_2},
    {"name": "menu 3", "action": menu_3}
]

# all menus in Class instance

menus = Menu('All Menus', options)
#print(menus)

#-------------------------------------------------------------------------#

# saving progress

def save():
  pass
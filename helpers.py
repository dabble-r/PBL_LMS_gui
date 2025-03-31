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

def set_stat(method, val):
  try:
    method(val)
  except Exception as e:
    print(f'Error: {e}')
    
# update existing player
def update_player(league):
  # print('update player\n')
  # flag to break out of Player Update Menu
  update_flag = True
  # player to be updated
  player_to_update = player_state()
  if is_None(player_to_update):
    player_raw = input('Enter the player name and team in a comma separated list: ')
    player_data = player_raw.split(',')
    if not input_len(player_data, 2):
      input_error(player_data, 2)
      player_raw = input('Enter the player name and team in a comma separated list: ')
    name = player_data[0].strip()
    team = player_data[1].strip()
    find_team = league.find_team(team)
    if find_team == None:
      not_found(team)
      print('Available Teams:\n',league)
      player_raw = input('Enter the player name and team in a comma separated list: ')
    else:
      find_player = find_team.get_player(name)
      if find_player == None:
        not_found(name)
        player_raw = input('Enter the player name and team in a comma separated list: ')
      else:
        # reassign player state, if find_player exists (not None)
        player_to_update = player_state(find_player)
        #print(f'Updating {find_player.name}')
        #find_player.set_at_bat(at_bats, flag_val)
        #find_player.set_AVG()
        #show_AVG()
  user_action_2 = menus.select_option(2)(player_to_update)
  #stack.append(user_action_2)
  #print(stack)
  #print('action 2', user_action_2)
  while update_flag:
    flag_val = True
    match user_action_2:
      case '1':
        # print('flag val', flag_val)
        # print(player_to_update)
        # print('Update offense\n')
        # flag val for suer stat update
        # flag default is True. stat value update default is to add val to curr state
        # flag = False, stat value replaces curr state
        user_action_3 = menus.select_option(3)(player_to_update)
        #stack.append(user_action_3)
        #print('action 3', user_action_3)
        match user_action_3:
          case '1':
            # print(player_to_update)
            # print('at bats\n')
            # check if user wants to add or reassign stat value
            # if user choice = 'add', func returns True
            user_action_val = user_add_re()
            if user_action_val == False:
              flag_val = False
            at_bats_raw = input('Enter value for at bat: ').strip()
            at_bats_data = int(at_bats_raw)
            player_to_update.set_at_bat(at_bats_data, flag_val)
            player_to_update.set_AVG()
            update_stat(player_to_update)
            '''
            #player_raw = input('Enter the player name, team, and at-bats to update in a comma separated list: ')
            #player_data = player_raw.split(',')
            #if not input_len(player_data, 3):
              #input_error(player_data, 3)
            #else:
              #name = player_data[0].strip()
              #team = player_data[1].strip()
            #find_team = league.find_team(team)
            # print(find_team)
            #if find_team == None:
              #not_found(team)
            #else:
              #find_player = find_team.get_player(name)
              #if find_player == None:
                #not_found(name)
              #else:
                # reassign player state, if find_player exists (not None)
                #player_to_update = player_state(player_to_update, find_player)
                #print(f'Updating {find_player.name}')
                #find_player.set_at_bat(at_bats, flag_val)
                #find_player.set_AVG()
                #show_AVG()
            '''
          case '2':
            # print(player_to_update)
            #print('flag val', flag_val)
            # print('hits\n')
            user_action_val = user_add_re()
            if user_action_val == False:
              flag_val = False
            hits_raw = input('Enter the hits to update: ').strip()
            hits_data = int(hits_raw)
            player_to_update.set_hit(hits_data, flag_val)
            player_to_update.set_AVG()
            # show_AVG()  
          case '3':
            # print('walks\n')
            # print(player_to_update)
            user_action_val = user_add_re()
            if user_action_val == False:
              flag_val = False
            walks_raw = input('Enter the walks to update: ').strip()
            walks_data = int(walks_raw)
            player_to_update.set_bb(walks_data, flag_val)
            player_to_update.set_AVG()
            '''
            # show_AVG() 
            #user_action_val = user_add_re()
            #if user_action_val == False:
              #flag_val = False
            #player_raw = input('Enter the player name and walks to update in a comma separated list: ')
            #player_data = player_raw.split(',')
            #if not input_len(player_data, 3):
              #input_error(player_data, 3)
            #else:
              #name = player_data[0].strip()
              #team = player_data[1].strip()
              #bb = int(player_data[2].strip())
              #find_team = league.find_team(team)
              # print(find_team)
              #if is_None(find_team):
                #not_found(team)
              #else:
                #find_player = find_team.get_player(name)
                #if is_None(find_player):
                  #not_found(name)
                #else:
                  #print(f'Updating {find_player.name}')
                  #find_player.set_bb(bb)
                  #find_player.set_AVG()
                  # show_AVG()
            '''
          case '4':
            # print('SO\n')
            # print(player_to_update)
            user_action_val = user_add_re()
            if user_action_val == False:
              flag_val = False
            so_raw = input('Enter the So\'s to update: ').strip()
            so_data = int(so_raw)
            player_to_update.set_so(so_data, flag_val)
            player_to_update.set_AVG()
            '''
            user_action_val = user_add_re()
            if user_action_val == False:
              flag_val = False
            player_raw = input('Enter the player name and SO\'s to update in a comma separated list: ')
            player_data = player_raw.split(',')
            if not input_len(player_data, 3):
              input_error(player_data, 3)
            else:
              name = player_data[0].strip()
              team = player_data[1].strip()
              so = int(player_data[2].strip())
              find_team = league.find_team(team)
              # print(find_team)
              if is_None(find_team):
                not_found(team)
              else:
                find_player = find_team.get_player(name)
                if is_None(find_player):
                  not_found(name)
                else:
                  print(f'Updating {find_player.name}')
                  find_player.set_so(so)
                  find_player.set_AVG()
                  # show_AVG()
            '''
          case '5':
            # print('HR\n')
            # print(player_to_update)
            user_action_val = user_add_re()
            if user_action_val == False:
              flag_val = False
            hr_raw = input('Enter the HR\'s to update: ').strip()
            hr_data = int(hr_raw)
            player_to_update.set_hr(hr_data, flag_val)
            player_to_update.set_AVG()
            '''
            user_action_val = user_add_re()
            if user_action_val == False:
              flag_val = False
            player_raw = input('Enter the player name and HR\'s to update in a comma separated list: ')
            player_data = player_raw.split(',')
            if not input_len(player_data, 3):
              input_error(player_data, 3)
            else:
              name = player_data[0].strip()
              team = player_data[1].strip()
              hr = int(player_data[2].strip())
              find_team = league.find_team(team)
              # print(find_team)
              if is_None(find_team):
                not_found(team)
              else:
                find_player = find_team.get_player(name)
                if is_None(find_player):
                  not_found(name)
                else:
                  print(f'Updating {find_player.name}')
                  find_player.set_hr(hr)
                  find_player.set_AVG()
                  # show_AVG()
            '''
          case '6':
            # print('rbi\n')
            # print(player_to_update)
            user_action_val = user_add_re()
            if user_action_val == False:
              flag_val = False
            rbi_raw = input('Enter the RBI\'s to update: ').strip()
            rbi_data = int(rbi_raw)
            player_to_update.set_rbi(rbi_data, flag_val)
            player_to_update.set_AVG()
            '''
            user_action_val = user_add_re()
            if user_action_val == False:
              flag_val = False
            player_raw = input('Enter the player name and RBI\'s to update in a comma separated list: ')
            player_data = player_raw.split(',')
            if not input_len(player_data, 3):
              input_error(player_data, 3)
            else:
              name = player_data[0].strip()
              team = player_data[1].strip()
              rbi = int(player_data[2].strip())
              find_team = league.find_team(team)
              # print(find_team)
              if is_None(find_team):
                not_found(team)
              else:
                find_player = find_team.get_player(name)
                if is_None(find_player):
                  not_found(name)
                else:
                  print(f'Updating {find_player.name}')
                  find_player.set_rbi(rbi)
                  find_player.set_AVG()
                  # show_AVG()
            '''
          case '7':
            # print('runs'\n)
            # print(player_to_update)
            user_action_val = user_add_re()
            if user_action_val == False:
              flag_val = False
            rbi_raw = input('Enter the RBI\'s to update: ').strip()
            rbi_data = int(rbi_raw)
            player_to_update.set_rbi(rbi_data, flag_val)
            player_to_update.set_AVG()
            '''
            user_action_val = user_add_re()
            if user_action_val == False:
              flag_val = False
            player_raw = input('Enter the player name and runs\'s to update in a comma separated list: ')
            player_data = player_raw.split(',')
            if not input_len(player_data, 3):
              input_error(player_data, 3)
            else:
              name = player_data[0].strip()
              team = player_data[1].strip()
              runs = int(player_data[2].strip())
              find_team = league.find_team(team)
              # print(find_team)
              if is_None(find_team):
                not_found(team)
              else:
                find_player = find_team.get_player(name)
                if is_None(find_player):
                  not_found(name)
                else:
                  print(f'Updating {find_player.name}')
                  find_player.set_runs(runs)
                  find_player.set_AVG()
                  # show_AVG()
            '''
          case '8':
            # print('singles\n')
            # print(player_to_update)
            user_action_val = user_add_re()
            if user_action_val == False:
              flag_val = False
            singles_raw = input('Enter the singles\'s to update: ').strip()
            singles_data = int(singles_raw)
            player_to_update.set_singles(singles_data, flag_val)
            player_to_update.set_AVG()
            '''
            user_action_val = user_add_re()
            if user_action_val == False:
              flag_val = False
            player_raw = input('Enter the player name and RBI\'s to update in a comma separated list: ')
            player_data = player_raw.split(',')
            if not input_len(player_data, 3):
              input_error(player_data, 3)
            else:
              name = player_data[0].strip()
              team = player_data[1].strip()
              singles = int(player_data[2].strip())
              find_team = league.find_team(team)
              # print(find_team)
              if is_None(find_team):
                not_found(team)
              else:
                find_player = find_team.get_player(name)
                if is_None(find_player):
                  not_found(name)
                else:
                  print(f'Updating {find_player.name}')
                  find_player.set_singles(singles)
                  find_player.set_AVG()
                  # show_AVG()
            '''
          case '9':
            # print('doubles\n')
            # print(player_to_update)
            user_action_val = user_add_re()
            if user_action_val == False:
              flag_val = False
            doubles_raw = input('Enter the doubles\'s to update: ').strip()
            doubles_data = int(doubles_raw)
            player_to_update.set_doubles(doubles_data, flag_val)
            player_to_update.set_AVG()
            '''
            user_action_val = user_add_re()
            if user_action_val == False:
              flag_val = False
            player_raw = input('Enter the player name and RBI\'s to update in a comma separated list: ')
            player_data = player_raw.split(',')
            if not input_len(player_data, 3):
              input_error(player_data, 3)
            else:
              name = player_data[0].strip()
              team = player_data[1].strip()
              doubles = int(player_data[2].strip())
              find_team = league.find_team(team)
              # print(find_team)
              if is_None(find_team):
                not_found(team)
              else:
                find_player = find_team.get_player(name)
                if is_None(find_player):
                  not_found(name)
                else:
                  print(f'Updating {find_player.name}')
                  find_player.set_doubles(doubles)
                  find_player.set_AVG()
                  # show_AVG()
            '''
          case '10':
            # print('triples\n')
            # print(player_to_update)
            user_action_val = user_add_re()
            if user_action_val == False:
              flag_val = False
            triples_raw = input('Enter the triples\'s to update: ').strip()
            triples_data = int(triples_raw)
            player_to_update.set_triples(triples_data, flag_val)
            player_to_update.set_AVG()
            '''
            user_action_val = user_add_re()
            if user_action_val == False:
              flag_val = False
            player_raw = input('Enter the player name and RBI\'s to update in a comma separated list: ')
            player_data = player_raw.split(',')
            if not input_len(player_data, 3):
              input_error(player_data, 3)
            else:
              name = player_data[0].strip()
              team = player_data[1].strip()
              triples = int(player_data[2].strip())
              find_team = league.find_team(team)
              # print(find_team)
              if is_None(find_team):
                not_found(team)
              else:
                find_player = find_team.get_player(name)
                if is_None(find_player):
                  not_found(name)
                else:
                  print(f'Updating {find_player.name}')
                  find_player.set_triples(triples)
                  find_player.set_AVG()
                  # show_AVG()
            '''
          case '11':
            # print('sac fly\n')
            # print(player_to_update)
            user_action_val = user_add_re()
            if user_action_val == False:
              flag_val = False
            sac_fly_raw = input('Enter the sac_flies to update: ').strip()
            sac_fly_data = int(sac_fly_raw)
            player_to_update.set_sac_fly(sac_fly_data, flag_val)
            player_to_update.set_AVG()
            '''
            user_action_val = user_add_re()
            if user_action_val == False:
              flag_val = False
            player_raw = input('Enter the player name and RBI\'s to update in a comma separated list: ')
            player_data = player_raw.split(',')
            if not input_len(player_data, 3):
              input_error(player_data, 3)
            else:
              name = player_data[0].strip()
              team = player_data[1].strip()
              sac_fly = int(player_data[2].strip())
              find_team = league.find_team(team)
              # print(find_team)
              if is_None(find_team):
                not_found(team)
              else:
                find_player = find_team.get_player(name)
                if is_None(find_player):
                  not_found(name)
                else:
                  print(f'Updating {find_player.name}')
                  find_player.set_sac_fly(sac_fly)
                  find_player.set_AVG()
                  # show_AVG()
            '''
          case '12':
            print('Quitting menu\n')
            # print(player_to_update)
            # print('return to last menu')
            # update_flag = user_update_continue(update_flag, find_player)
      case '2':
        print('update defense')
        # flag_action = input('Would you like to perform another action? y/n ').lower().strip() == 'y'
      case '3':
        print('Quitting menu\n')
    update_flag = user_update_continue(update_flag, find_player)
    #update_flag = input(f'Would you like to continue updating {find_player.name}?: y/n \n').lower().strip() == 'y'
    '''
    def remove_player(league):
      #print('remove pl\n')
      player_raw = input('Enter the player name and player team name to remove: ')
      player_data = player_raw.split(',')
      if not input_len(player_data, 2):
        input_error(player_data, 2)
      else:
        name = player_data[0]
        team = player_data[1].strip()   
        find_team = league.find_team(team) 
        find_team.remove_player(name)
        #print(find_team)
      else:
        print('Must enter player name and team name')
        flag_action = input('Would you like to perform another action? y/n ').lower().strip() == 'y'
    '''

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
def create_player(league):    
  new_player_raw = input('Enter new player name, number, team, and positions played separated by a comma: ')  
  new_player_data = new_player_raw.split(',')
  if len(new_player_data) < 4:
    #print('Enter name, number, team, and at least one position')
    new_player_raw = input('Enter new player name, number, team, and positions played separated by a comma: ') 
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
      not_found(team)
      print('Available Teams:\n',league)
      new_player_raw = input('Enter new player name, number, team, and positions played separated by a comma: ') 
      #flag_action = input('Would you like to perform another action? y/n ').lower().strip() == 'y'
    elif find_team:
      print(f'Creating player:\n {name}\n {number}\n {team}\n {positions}')
      find_team.add_player(name, number, team, positions)
      #print('raw', new_player_raw)
      #print('split', new_player)
      #print(name, number, positions)
      #print('new player', new_player)
      #print('team', find_team)

# view all team in league
def view_all(league):
  #print('view all teams')
  all_players = league.view_all()
  print(all_players)

# create new team in league
def create_team(league):
  #print('create t\n')
  new_team_raw = input('Enter a team name and an optional max number of players in a comma separated list: ')
  new_team_list = new_team_raw.split(',')
  name = new_team_list[0]
  new_team = None
  if len(new_team_list) == 2:
    max = int(new_team_list[1])
    new_team = Team(name, max)
  else:
    new_team = Team(name)
  league.add_team(new_team)
  print(f'Creating {new_team}')
  print(league)

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
import tkinter as tk
from helpers import *
from linked_list import *

# Create the main window
root = tk.Tk()
root.title("Dynamic Menu Example")

league = LinkedList('PBL')

# Create frames for different menus
menu1_frame = tk.Frame(root, name='menu1', padx=50, pady=25, borderwidth=2, relief='solid')
menu2_frame = tk.Frame(root, name='menu2', padx=50, pady=25, borderwidth=2, relief='solid')
menu3_frame = tk.Frame(root, name='menu3', padx=50, pady=25, borderwidth=2, relief='solid')
create_menu = tk.Frame(root, name='create_menu', padx=50, pady=25, borderwidth=2, relief='solid')


# populate menu 1
def populate_menu1():
  # Menu 1 contents
  tk.Label(menu1_frame, text="Menu 1", font=("Arial", 14)).pack(pady=10)
  items_1 = [
      {"name": "create player", "action": lambda: populate_create_player_menu(league)},
      {"name": "search player", "action": lambda: search_player(league)},
      {"name": "update player", "action": lambda: populate_update_player_menu_search(league)},
      {"name": "remove player", "action": lambda: remove_player(league)},
      {"name": "view all players", "action": lambda: view_all(league)},
      {"name": "create team", "action": lambda: populate_create_team_menu(league)},
      {"name": "search team", "action": lambda: search_team(league)},
      {"name": "view all teams", "action": lambda: print(league)},
      {"name": "remove team", "action": lambda: remove_team(league)},
      {"name": "quit", "action": lambda: hide_all()}
    ]
  for item in items_1:
    name = item['name']
    action = item['action']
    tk.Button(menu1_frame, text=name, command=action).pack(pady=5)      
    name = action = None
  tk.Button(menu1_frame, text="Switch to Menu 2", command=lambda: show_menu(menu2_frame, 2)).pack(pady=5)

# populate menu 2
def populate_menu2():
  # Menu 2 contents
  tk.Label(menu2_frame, text="Menu 2", font=("Arial", 14)).pack(padx=5, pady=5)
  items_2 = [
      {"name": "offense", "action": lambda: print("1")},
      {"name": "defense", "action": lambda: print("2")},
      {"name": "back", "action": lambda: print("3")},
    ]
  for item in items_2:
    tmp = item['action']
    tk.Button(menu2_frame, text=item['name'], command=tmp).pack(pady=5)
    tmp = None
  tk.Button(menu2_frame, text="Switch to Menu 3", command=lambda: show_menu(menu3_frame, 3)).pack(padx=5, pady=5)

# populate menu 3
def populate_menu3():
  # Menu 3 contents
  tk.Label(menu3_frame, text="Menu 3", font=("Arial", 14)).pack(padx=5, pady=5)
  items_3 = [
      {"name": "At Bats", "action": lambda: "1"},
      {"name": "Hits", "action": lambda: print("2")},
      {"name": "Walks", "action": lambda: print("3")},
      {"name": "SO", "action": lambda: print("4")},
      {"name": "HR", "action": lambda: print("5")},
      {"name": "RBI", "action": lambda: print("6")},
      {"name": "Runs", "action": lambda: print("7")},
      {"name": "Singles", "action": lambda: print("8")},
      {"name": "Doubles", "action": lambda: print("9")},
      {"name": "Triples", "action": lambda: print("10")},
      {"name": "Sac Fly", "action": lambda: print("11")},
      {"name": "back", "action": lambda: print("12")},
    ]
  for item in items_3:
    tmp = item['action']
    tk.Button(menu3_frame, text=item['name'], command=tmp).pack(pady=5)
    tmp = None
  tk.Button(menu3_frame, text="Switch to Menu 1", command=lambda: show_menu(menu1_frame, 1)).pack(pady=5)

# populate menu - create team
def populate_create_team_menu(league):
  clear_widgets(create_menu)
  show_menu(create_menu, 4)
  create_team = tk.Frame(create_menu, name="create team", bd=100, height=250, width=500)
  create_team.pack(pady=5)
  label = tk.Label(create_team, text="Enter team and max (optional) in comma separated list", font=("Arial", 14))
  label.pack(pady=5)
  entry = tk.Entry(create_team, insertwidth=15, font=('Arial', 14))
  entry.pack(padx=5, pady=5)
  button_create = tk.Button(create_team, text="Create", height=2, width=5, command=lambda: get_create_team(entry, league))
  button_create.pack(pady=5)
  button_exit = tk.Button(create_team, text='Back', command= lambda: show_menu(menu1_frame, 1))
  button_exit.pack(pady=5)

# populate menu - create team
def populate_create_player_menu(league):
  clear_widgets(create_menu)
  show_menu(create_menu, 4)
  create_player = tk.Frame(create_menu, name="create player", bd=100, height=250, width=500)
  create_player.pack(pady=5)
  label = tk.Label(create_player, text="Enter player name, number, team, and positions in comma separated list", font=("Arial", 14))
  label.pack(pady=5)
  entry = tk.Entry(create_player, insertwidth=15, font=('Arial', 14))
  entry.pack(padx=5, pady=5)
  button_create = tk.Button(create_player, text="Create", height=2, width=5, command=lambda: get_create_player(entry, league))
  button_create.pack(pady=5)
  button_exit = tk.Button(create_player, text='Back', command= lambda: show_menu(menu1_frame, 1))
  button_exit.pack(pady=5)

def populate_update_player_menu_search(league):
  clear_widgets(create_menu)
  show_menu(create_menu, 4)
  player = team = None
  label = tk.Label(create_menu, text="Enter player name and team in comma separated list", font=("Arial", 14))
  label.pack(pady=5)
  entry = tk.Entry(create_menu, insertwidth=15, font=('Arial', 14))
  entry.pack(padx=5, pady=5) 
  if entry.get():
    player = get_entry(entry)[0]
    team = get_entry(entry)[1]
    print(player, team)
  button = tk.Button(create_menu, text='Search', command=lambda: populate_update_player_menu_stat(player, team))
  button.pack(pady=5)

def populate_update_player_menu_stat(player, team):
  clear_widgets(create_menu)
  show_menu(create_menu, 4)
  find_team = league.find_team(team)
  print('find team', find_team)
  find_player = find_team.get_player(player)
  items_update = [
    {"name": "at bats", "action": lambda: get_update_stat("at bats", find_player)},
    {"name": "hits", "action": lambda: get_update_stat("hits", find_player)},
    {"name": "walks", "action": lambda: get_update_stat('walks', find_player)},
    {"name": "SO", "action": lambda: get_update_stat("SO", find_player)},
    {"name": "HR", "action": lambda: get_update_stat("HR", find_player)},
    {"name": "RBI", "action": lambda: get_update_stat("RBI", find_player)},
    {"name": "runs", "action": lambda: get_update_stat("runs", find_player)},
    {"name": "singles", "action": lambda: get_update_stat("singles", find_player)},
    {"name": "doubles", "action": lambda: get_update_stat("doubles", find_player)},
    {"name": "triples", "action": lambda: get_update_stat("triples", find_player)},
    {"name": "back", "action": lambda: show_menu(menu1_frame, 1)}
  ]
  for item in items_update:
    name = item['name']
    action = item['action']
    tk.Button(create_menu, text=name, command=action).pack(pady=5)
    name = action = None
  label = tk.Label(create_menu, text=f"Enter stat", font=("Arial", 14))
  label.pack(pady=5)
  entry = tk.Entry(create_menu, insertwidth=15, font=('Arial', 14))
  entry.pack(padx=5, pady=5)
  val = int(entry.get())
  button = tk.Button(create_menu, text='Search Player', command=lambda: find_player.set_at_bat(val, True))
  button.pack(pady=5)
  
  
  

  '''
  update_player = tk.Frame(create_menu, name="update player", bd=100, height=250, width=500)
  update_player.pack(pady=5)
  label = tk.Label(update_player, text="Enter player name and team in comma separated list", font=("Arial", 14))
  label.pack(pady=5)
  entry = tk.Entry(update_player, insertwidth=15, font=('Arial', 14))
  entry.pack(padx=5, pady=5)
  button_create = tk.Button(update_player, text="Update", height=2, width=5, command=lambda: get_update_player(entry, league))
  button_create.pack(pady=5)
  button_exit = tk.Button(update_player, text='Back', command= lambda: show_menu(menu1_frame, 1))
  button_exit.pack(pady=5)
  '''
  
def get_update_stat(stat, player, team):
  clear_widgets(create_menu)
  flag = True
  update_player = tk.Frame(create_menu, name=f"update {player} {stat}", bd=100, height=250, width=500)
  update_player.pack(pady=5)
  label = tk.Label(update_player, text=f"Enter {stat}", font=("Arial", 14))
  label.pack(pady=5)
  entry = tk.Entry(update_player, insertwidth=15, font=('Arial', 14))
  entry.pack(padx=5, pady=5)
  button_flag_add = tk.Button(update_player, text='add', command=lambda: flag)
  button_flag_add.pack(pady=5)
  button_flag_reassign = tk.Button(update_player, text='reassign', command=lambda: not flag)
  button_flag_reassign.pack(pady=5) 
  button_create = tk.Button(update_player, text=f"Update {player} {stat}", height=2, width=10, command=lambda: get_update_val(entry, player, team, league, flag))
  button_create.pack(pady=5)
  button_exit = tk.Button(update_player, text='Back', command= lambda: show_menu(menu3_frame, 3))
  button_exit.pack(pady=5)

def get_update_val(entry, player, team, league, flag):
  val = int(entry.get())
  find_team = league.find_team(team)
  find_player = find_team.get_player(player)

  #print('stat val', val)

def get_create_team(entry, league):
  team_raw = entry.get()
  try: 
    create_team(league, team_raw)
    tk.Label(create_menu, text='Team created!').pack(pady=5)
    print(league)
  except Exception as e:
    tk.Label(create_menu, text=f'Error: {e}').pack(pady=5)
  clear_entry(entry)

def get_create_player(entry, league):
  player_raw = entry.get()
  try:
    name, number, team, positions = create_player(league, player_raw)
    tk.Label(create_menu, text=f'{name}\n{number}\n{team}\n{[*positions]}\ncreated!').pack(pady=5)
  except Exception as e:
    tk.Label(create_menu, text=f'Error: {e}').pack(pady=5)
  clear_entry(entry)

def get_update_player(stat, league):
  update_raw = entry.get()
  try:
    update_player(league, update_raw)
    tk.Label(create_menu, text='Player updated').pack(pady=5)
  except Exception as e:
    tk.Label(create_menutext=f'Error: {e}').pack(pady=5)
  clear_entry(entry)

# Function to switch between menus
def show_menu(menu_frame, val):
    match val:
      case 1:
        menu2_frame.pack_forget()
        menu3_frame.pack_forget()
        create_menu.pack_forget()
        menu_frame.pack(pady=10)
      case 2:
        menu1_frame.pack_forget()
        menu3_frame.pack_forget()
        create_menu.pack_forget()
        menu_frame.pack(pady=10)
      case 3: 
        menu1_frame.pack_forget()
        menu2_frame.pack_forget()
        create_menu.pack_forget()
        menu_frame.pack(pady=10)
      case 4:
        menu1_frame.pack_forget()
        menu2_frame.pack_forget()
        menu3_frame.pack_forget()
        menu_frame.pack(pady=10)

def hide_all():
  root.quit()

def clear_widgets(frame):
  for widget in frame.winfo_children():
    widget.destroy()

def clear_entry(entry):
  entry.delete(0, tk.END)

def get_entry(entry):
  ret = tuple(map(lambda x: x.strip(), entry.get().split(',')))
  return ret

def hide_menu_specific(*args):
  menus = [*args]
  for el in menus:
    el.pack_forget()

def get_action():
  pass

# populate menus
populate_menu1()
populate_menu2()
populate_menu3()

# Start with Menu 1
show_menu(menu1_frame, 1)

# Run the application
root.mainloop()
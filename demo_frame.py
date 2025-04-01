import tkinter as tk
from helpers import *
from linked_list import *

# Create the main window
root = tk.Tk()
root.title("Dynamic Menu Example")

league = LinkedList('PBL')

# Create frames for different menus
menu1_frame = tk.Frame(root, padx=50, pady=25, borderwidth=2, relief='solid')
menu2_frame = tk.Frame(root, padx=50, pady=25, borderwidth=2, relief='solid')
menu3_frame = tk.Frame(root, padx=50, pady=25, borderwidth=2, relief='solid')
create_menu = tk.Frame(root, padx=50, pady=25, borderwidth=2, relief='solid')


# populate menu 1
def populate_menu1():
  # Menu 1 contents
  tk.Label(menu1_frame, text="Menu 1", font=("Arial", 14)).pack(pady=10)
  items_1 = [
      {"name": "create playe", "action": lambda: populate_create_player_menu(league)},
      {"name": "search player", "action": lambda: search_player(league)},
      {"name": "update player", "action": lambda: update_player(league)},
      {"name": "remove player", "action": lambda: remove_player(league)},
      {"name": "view all players", "action": lambda: view_all(league)},
      {"name": "create team", "action": lambda: populate_create_team_menu(league)},
      {"name": "search team", "action": lambda: search_team(league)},
      {"name": "view all teams", "action": lambda: print(league)},
      {"name": "remove team", "action": lambda: remove_team(league)},
      {"name": "quit", "action": lambda: hide_all()}
    ]
  for item in items_1:
    tmp = item['action']
    tk.Button(menu1_frame, text=item['name'], command=tmp).pack(pady=5)
    tmp = None
  tk.Button(menu1_frame, text="Switch to Menu 2", command=lambda: show_menu(menu2_frame, 2)).pack(pady=5)

# populate menu 2
def populate_menu2():
  # Menu 2 contents
  tk.Label(menu2_frame, text="Menu 2", font=("Arial", 14)).pack(padx=5, pady=5)
  items_2 = [
      {"name": "offense", "action": lambda: print("1")},
      {"name": "defense", "action": lambda: print("2")},
      {"name": "quit", "action": lambda: print("3")},
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
      {"name": "Quit", "action": lambda: print("12")},
    ]
  for item in items_3:
    tmp = item['action']
    tk.Button(menu3_frame, text=item['name'], command=tmp).pack(pady=5)
    tmp = None
  tk.Button(menu3_frame, text="Switch to Menu 1", command=lambda: show_menu(menu1_frame, 1)).pack(pady=5)

# populate menu - create team
def populate_create_team_menu(league):
  # Menu 2 contents
  clear_widgets(create_menu)
  show_menu(create_menu, 4)
  create_team = tk.Frame(create_menu, name="create team", bd=100, height=250, width=500)
  create_team.pack(pady=5)
  label = tk.Label(create_team, text="Enter team and max (optional) in comma separated list", font=("Arial", 10))
  label.pack(pady=5)
  entry = tk.Entry(create_team, insertwidth=15)
  entry.pack(padx=5, pady=5)
  button_create = tk.Button(create_team, text="Create", height=2, width=5, command=lambda: get_create_team(entry, league))
  button_create.pack(pady=5)
  button_exit = tk.Button(create_team, text='Quit', command= lambda: show_menu(menu1_frame, 1))
  button_exit.pack(pady=5)

# populate menu - create team
def populate_create_player_menu(league):
  # Menu 2 contents
  clear_widgets(create_menu)
  show_menu(create_menu, 4)
  create_player = tk.Frame(create_menu, name="create Player", bd=100, height=250, width=500)
  create_player.pack(pady=5)
  label = tk.Label(create_player, text="Enter player name, number, team, and positions in comma separated list", font=("Arial", 10))
  label.pack(pady=5)
  entry = tk.Entry(create_player, insertwidth=15)
  entry.pack(padx=5, pady=5)
  button_create = tk.Button(create_player, text="Create", height=2, width=5, command=lambda: get_create_player(entry, league))
  button_create.pack(pady=5)
  button_exit = tk.Button(create_player, text='Quit', command= lambda: show_menu(menu1_frame, 1))
  button_exit.pack(pady=5)

def get_create_team(entry, league):
  team_raw = entry.get()
  try: 
    create_team(league, team_raw)
    print(league)
  except Exception as e:
    tk.Label(create_menu, text=f'Error: {e}')

def get_create_player(entry, league):
  player_raw = entry.get()
  try:
    create_player(league, player_raw)
    print()
  except Exception as e:
    tk.Label(create_menu, text=f'Error: {e}')

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
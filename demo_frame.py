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
create_team_menu = tk.Frame(root, padx=50, pady=25, borderwidth=2, relief='solid')

# populate menu 1
def populate_menu1():
  # Menu 1 contents
  tk.Label(menu1_frame, text="Menu 1", font=("Arial", 14)).pack(pady=10)
  items_1 = [
      {"name": "create playe", "action": lambda: create_player(league)},
      {"name": "search player", "action": lambda: search_player(league)},
      {"name": "update player", "action": lambda: update_player(league)},
      {"name": "remove player", "action": lambda: remove_player(league)},
      {"name": "view all players", "action": lambda: view_all(league)},
      {"name": "create team", "action": lambda: populate_creat_team_menu()},
      {"name": "search team", "action": lambda: search_team(league)},
      {"name": "view all teams", "action": lambda: print(league)},
      {"name": "remove team", "action": lambda: remove_team(league)},
      {"name": "quit", "action": lambda: quit()}
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
def populate_creat_team_menu():
  # Menu 2 contents
  show_menu(create_team_menu, 4)
  tk.Label(root, text="Create New Team", font=("Arial", 14)).pack(pady=5)
  tk.Button(root, text="Create", command=lambda: get_create_team(entry)).pack(pady=5)
  entry = tk.Entry(create_team_menu, width=10)
  entry.pack(padx=5, pady=5)
 
def get_create_team(entry):
  team, max = entry.get().split(' ')
  print(team, max)
  
# Function to switch between menus
def show_menu(menu_frame, val):
    match val:
      case 1:
        menu2_frame.pack_forget()
        menu3_frame.pack_forget()
        create_team_menu.pack_forget()
        menu_frame.pack(pady=10)
      case 2:
        menu1_frame.pack_forget()
        menu3_frame.pack_forget()
        create_team_menu.pack_forget()
        menu_frame.pack(pady=10)
      case 3: 
        menu1_frame.pack_forget()
        menu2_frame.pack_forget()
        create_team_menu.pack_forget()
        menu_frame.pack(pady=10)
      case 4:
        menu1_frame.pack_forget()
        menu2_frame.pack_forget()
        menu3_frame.pack_forget()
        menu_frame.pack(pady=10)

def hide_menus_except(menu):
  menu1_frame.pack_forget()
  menu2_frame.pack_forget()
  menu3_frame.pack_forget()
  create_team_menu.pack_forget()

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
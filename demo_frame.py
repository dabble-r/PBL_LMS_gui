import tkinter as tk
from helpers import *
from linked_list import *

# Create the main window
root = tk.Tk()
root.title("Dynamic Menu Example")

league = LinkedList('PBL')

# Create frames for different menus
menu1_frame = tk.Frame(root)
menu2_frame = tk.Frame(root)
menu3_frame = tk.Frame(root)

# populate menu 1
def populate_menu1():
  # Menu 1 contents
  tk.Label(menu1_frame, text="Menu 1", font=("Arial", 14)).pack(pady=10)
  items_1 = [
      {"name": "create player", "action": lambda: create_team(league)},
      {"name": "search player", "action": lambda: search_player(league)},
      {"name": "update player", "action": lambda: update_player(league)},
      {"name": "remove player", "action": lambda: remove_player(league)},
      {"name": "view all players", "action": lambda: view_all(league)},
      {"name": "create team", "action": lambda: create_team(league)},
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
  tk.Label(menu2_frame, text="Menu 2", font=("Arial", 14)).pack(pady=10)
  items_2 = [
      {"name": "offense", "action": lambda: print("1")},
      {"name": "defense", "action": lambda: print("2")},
      {"name": "quit", "action": lambda: print("3")},
    ]
  for item in items_2:
    tmp = item['action']
    tk.Button(menu2_frame, text=item['name'], command=tmp).pack(pady=5)
    tmp = None
  tk.Button(menu2_frame, text="Switch to Menu 3", command=lambda: show_menu(menu3_frame, 3)).pack(pady=5)

# populate menu 3
def populate_menu3():
  # Menu 3 contents
  tk.Label(menu3_frame, text="Menu 3", font=("Arial", 14)).pack(pady=10)
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

# Function to switch between menus
def show_menu(menu_frame, val):
    if val == 3:
      menu1_frame.pack_forget()
      menu2_frame.pack_forget()
      menu_frame.pack(pady=10)
    elif val == 2:
      menu1_frame.pack_forget()
      menu3_frame.pack_forget()
      menu_frame.pack(pady=10)
    else:
      menu2_frame.pack_forget()
      menu3_frame.pack_forget()
      menu_frame.pack(pady=10)

def get_action(val):
  pass

# populate menus
populate_menu1()
populate_menu2()
populate_menu3()

# Start with Menu 1
show_menu(menu1_frame, 1)

# Run the application
root.mainloop()
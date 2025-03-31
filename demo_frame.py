import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Dynamic Menu Example")

# Create frames for different menus
menu1_frame = tk.Frame(root)
menu2_frame = tk.Frame(root)

# Menu 1 contents
tk.Label(menu1_frame, text="Menu 1", font=("Arial", 14)).pack(pady=10)
items_1 = [
    {"name": "create player", "action": lambda: print("1")},
    {"name": "search player", "action": lambda: print("2")},
    {"name": "update player", "action": lambda: print("3")},
    {"name": "remove player", "action": lambda: print("4")},
    {"name": "view all players", "action": lambda: print("5")},
    {"name": "create team", "action": lambda: print("6")},
    {"name": "search team", "action": lambda: print("7")},
    {"name": "view all teams", "action": lambda: print("8")},
    {"name": "remove team", "action": lambda: print("9")},
    {"name": "quit", "action": lambda: print("10")}
    ]
for item in items_1:
  tk.Button(menu1_frame, text=item['name'], command=lambda: print("Option 1 selected")).pack(pady=5)
  #tk.Button(menu1_frame, text="Option 2", command=lambda: print("Option 2 selected")).pack(pady=5)
  tk.Button(menu1_frame, text="Switch to Menu 2", command=lambda: show_menu(menu2_frame)).pack(pady=5)

# Menu 2 contents
tk.Label(menu2_frame, text="Menu 2", font=("Arial", 14)).pack(pady=10)
tk.Button(menu2_frame, text="Option A", command=lambda: print("Option A selected")).pack(pady=5)
tk.Button(menu2_frame, text="Option B", command=lambda: print("Option B selected")).pack(pady=5)
tk.Button(menu2_frame, text="Switch to Menu 1", command=lambda: show_menu(menu1_frame)).pack(pady=5)

# Function to switch between menus
def show_menu(menu_frame):
    menu1_frame.pack_forget()
    menu2_frame.pack_forget()
    menu_frame.pack(pady=10)

# Start with Menu 1
show_menu(menu1_frame)

# Run the application
root.mainloop()
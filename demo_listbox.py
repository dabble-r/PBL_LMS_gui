#from linked_list import LinkedList
#from player import Player 
#from team import Team
#from stack import Stack

'''
#league
PBL = LinkedList('People\'s Baseball League')

#teams
beef_sliders = Team('Beef Sliders')
rougarou = Team('Rougarou')

#sliders - roster
'''
#nick = Player('Nick Broussard', 18, ['second base', 'pitcher', 'left field'])
#jeremy = Player('Jeremy', 19, ['pitcher', 'shortstop', 'left field']) 
#justin = Player('Justin', 20, ['left field', 'second base']) 
#andrew = Player('Andrew', 21, ['third base', 'manager']) 
#chance = Player('Chance', 22, ['catcher']) 
#nashon = Player('Nashon', 23, ['center field', 'first base'])
#john = Player('John', 24, ['first base', 'second base'])
#garrett = Player('Garrett', 25, ['pitcher', 'first base']) 
#joe = Player('Joe', 26, ['shortstop'])
#luke = Player('Luke', 27, ['right field', 'second base'])
'''

#rougarou - roster
'''
#player_1 = Player('Ken', 1, ['right field', 'second base'])
#player_2 = Player('Jason', 2, ['right field', 'second base'])
#player_3 = Player('Albert', 3, ['right field', 'second base'])
'''

#sliders - add players
beef_sliders.add_player('Nick', 18, ['second base'])
beef_sliders.add_player('Jeremy', 19, ['second base'])
beef_sliders.add_player('Justin', 20, ['second base'])
beef_sliders.add_player('Andrew', 21, ['second base'])
beef_sliders.add_player('Chance', 22, ['second base'])
beef_sliders.add_player('Nashon', 23, ['second base'])
beef_sliders.add_player('John', 24, ['second base'])
beef_sliders.add_player('Garrett', 25, ['second base'])
beef_sliders.add_player('Joe', 26, ['second base'])
beef_sliders.add_player('Luke', 27, ['second base'])

#rougarou - add players 
rougarou.add_player('Albert', 1, ['left field'])
rougarou.add_player('Frank', 2, ['left field'])
rougarou.add_player('Ken', 3, ['left field'])
rougarou.add_player('Jose', 4, ['left field'])

#league - roster
PBL.add_node(beef_sliders)
PBL.add_node(rougarou)

# print out - tests 

#print(beef_sliders)
#print(rougarou)
#print(PBL)
'''

'''
test = Stack('test stack')
def fill():
  i = 1
  while i <= 50:
    test.append(i)
    i += 1
'''

#fill()
#print(test)
#print(test.get_first())
#print(test.get_last())

# menu test
#from menu import *
#from helpers import menu_1, menu_2, menu_3
#from linked_list import LinkedList

# Example functions
# initial menu

# user_action = input('Please select action:\n   1) Create Player\n   2) Search Player\n   3) Update Player\n   4) Remove Player\n\
# 5) View all players\n   6) Create Team\n   7) Search Team\n   8) View all teams\n   9) Remove Team\n   10) Quit\nResponse: ')
  


# Create and use the menu

#test_menu = Menu('Test Menus', menus)
#val = LinkedList('PBL')

#print(test_menu)

# breezy python GUI
from breezypythongui import *
from tkinter import Listbox, END
from main import * 
from linked_list import *
from menu import *
from helpers import *
from player import Player 
from team import Team

class Root(EasyFrame):
    def __init__(self):
      EasyFrame.__init__(self, title=f'Welcome.....', width=500, height=500)
      self.addLabel(text='Test Label', row=1, column=1)
      self.addButton(text='display menu 1', row=2, column=5, command=self.display_menu_1)
      self.addButton(text='display menu 2', row=3, column=5, command=self.display_menu_2)
      self.menu_1 = Menu_1()
      self.menu_2 = Menu_2()

    def display_menu_1(self):
      self.menu_1.show()
      self.menu_2.hide()

    def display_menu_2(self):
      self.menu_2.show()
      self.menu_1.hide()
      
class Menu_1(EasyFrame):
  def __init__(self):
    EasyFrame.__init__(self, title='menu 1 listbox')
    self.addLabel(text="Select an item from the list:", row=0, column=0)
    self.listbox = Listbox(self, width=50, height=10, selectmode="single")
    self.listbox.grid(row=1, column=0, padx=10, pady=5)
    self.items = [
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

    for item in self.items:
      self.listbox.insert(END, item['name'])
    
    self.addButton(text='Choice...', row=2, column=0, command=self.call_selection)

    self.resultLabel = self.addLabel(text="", row=3, column=0)

  def show(self):
    self.listbox.grid(row=1, column=0, padx=10, pady=5)

  def hide(self):
    self.listbox.grid_forget()

  def call_selection(self):
    # Getting the selected item from the listbox
    selected = self.listbox.curselection()  # Returns a tuple of indices
    #print('selected', selected)
    if selected:  # Check if something is selected
        item = self.listbox.get(selected[0])
        #print('item', item)
        self.resultLabel["text"] = f"You selected: {item}"
        self.call_button_text = item
        func_call = [x['action'] for x in self.items if x['name'] == item][0]
        func_call()
    else:
        self.resultLabel["text"] = "No item selected."

class Menu_2(EasyFrame):
  def __init__(self):
    EasyFrame.__init__(self, title='menu 2 listbox')
    self.addLabel(text="Select an item from the list:", row=0, column=0)
    self.listbox = Listbox(self, width=50, height=10, selectmode="single")
    self.listbox.grid(row=1, column=0, padx=10, pady=5)
    self.items = [
      {"name": "Update offensive stats", "action": lambda: print("1")},
      {"name": "Update defensive stats", "action": lambda: print("2")},
      {"name": "Quit", "action": lambda: print("3")}
    ]

    for item in self.items:
      self.listbox.insert(END, item['name'])
    
    self.addButton(text='Choice...', row=2, column=0, command=self.call_selection)

    self.resultLabel = self.addLabel(text="", row=3, column=0)

  def show(self):
    self.listbox.grid(row=1, column=0, padx=10, pady=5)

  def hide(self):
    self.listbox.grid_forget()

  def call_selection(self):
    # Getting the selected item from the listbox
    selected = self.listbox.curselection()  # Returns a tuple of indices
    #print('selected', selected)
    if selected:  # Check if something is selected
        item = self.listbox.get(selected[0])
        #print('item', item)
        self.resultLabel["text"] = f"You selected: {item}"
        self.call_button_text = item
        func_call = [x['action'] for x in self.items if x['name'] == item][0]
        func_call()
    else:
        self.resultLabel["text"] = "No item selected."

root = Root()
root.mainloop()

# -------------------------------------------------------------------------- #

# take menus in, iterate over menus object/list
# take each menu item, add to menus lst of root gui instance 

# menu = Menu("Main Menu", options)
# menu.add_option('Say Hello 2', say_hello_2)
# test_menu.display()
# action = test_menu.select_option()
# action(val)
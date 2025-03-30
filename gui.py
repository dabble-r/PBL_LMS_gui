from breezypythongui import *

# breezy python GUI
from breezypythongui import *
from tkinter import Listbox, END
from main import * 
from linked_list import *
from menu import *
from helpers import *
from player import Player 
from team import Team

# Menu options
menus = [
    {"name": "menu 1", "action": menu_1},
    {"name": "menu 2", "action": menu_2},
    {"name": "menu 3", "action": menu_3}
]

def menu_1():
  #print(f'Welcome to the {league.name}\n')
  display = [
     {'name': '1) Create Player', 'action': lambda: print('create player')}, 
     {'name': '2) Search Player', 'action': lambda: print('search player')},
     {'name': '3) Update Player', 'action': lambda: print('update player')},
     {'name': '4) Remove Player', 'action': lambda: print('remove player')} ,
     {'name': '5) View All Players', 'action': lambda: print('view all players')},
     {'name': '6) Create Team', 'action': create_team},
     {'name': '7) Search Team', 'action': lambda: print('search team')},
     {'name': '8) View All Teams', 'action': lambda: print('uview all teams')},
     {'name': '9) Remove Team', 'action': lambda: print('remove team')},
     {'name': '10) Quit', 'action': lambda: print('quit')} 
  ]
  return display

def menu_2():
  #print(f'{player.name} stats update:\n')
  #user_action = input('Please select action:\n   1) Update offensive stats\n   2) Update defensive stats\n   3) Quit\nResponse: ')
  display = [
     {'name': '1) Update offensive stats', 'action': update_player}, 
     {'name': '2) Update defensive stats', 'action': lambda: print('defense')},
     {'name': '3) Quit', 'action': lambda: print('quit')} 
  ]

  return display

class Root(EasyFrame):
    def __init__(self, league=None, player=None, menus=None):
      EasyFrame.__init__(self, title=f'Welcome to the...', width=500, height=500)
      self.menus = menus 
      self.league = league 
      self.player = player
      self.addLabel(text='Test Label', row=1, column=1)
      self.addButton(text='Menu 1', row=1, column=2, command=self.menu_list_1)
      self.addButton(text='Menu 2', row=2, column=2, command=self.menu_list_2)
      self.addButton(text='Menu 3', row=3, column=2, command=self.menu_list_3)

    def menu_list_1(self):
      self.listbox = ListBox(menu_1(), 0, league)
    
    def menu_list_2(self):
      # create listbox instance
      # pass display list from menu_2 to instance
      self.listbox = ListBox(menu_2(), 1, league)

    def menu_list_3(self):
      self.listbox = ListBox(menu_3(), 2, league)
    
class ListBox(EasyFrame):
    def __init__(self, menu_options, menu_indx, league):
        self.menu_options = menu_options
        self.menu_indx = menu_indx
        self.league = league
        EasyFrame.__init__(self, title="Menu - Test - ListBox")

        # Adding a label to explain the list box
        self.addLabel(text="Select an item from the list:", row=0, column=0)

        # Creating the Listbox widget
        self.listbox = Listbox(self, height=5, selectmode="single")
        self.listbox.grid(row=1, column=0, padx=10, pady=5)

        # Adding items to the Listbox
        for item in self.menu_options:
          self.listbox.insert(END, item['name'])
        
        # Adding a button to display selected item
        self.addButton(text="Show Selection", row=2, column=0, command=self.showSelection)

        # Adding a label to display the result
        self.resultLabel = self.addLabel(text="", row=3, column=0)

    def showSelection(self):
        # Getting the selected item from the listbox
        selected = self.listbox.curselection()  # Returns a tuple of indices
        if selected:  # Check if something is selected
            item = self.listbox.get(selected[0])
            self.resultLabel["text"] = f"You selected: {item}"
            func = [x['action'] for x in self.menu_options if x['name'] == item][0]
            func(self.league)
            
        else:
            self.resultLabel["text"] = "No item selected."

league = LinkedList('PBL')
root = Root()
root.mainloop()
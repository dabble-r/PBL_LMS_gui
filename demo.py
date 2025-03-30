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
  
def say_hello_2():
    print("Hello 2!")

def say_goodbye():
    print("Goodbye!")

def show_time():
    from datetime import datetime
    print(f"Current time: {datetime.now()}")


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
from helpers import menu_1, menu_2, menu_3
from player import Player 
from team import Team

# Menu options
menus = [
    {"name": "menu 1", "action": menu_1},
    {"name": "menu 2", "action": menu_2},
    {"name": "menu 3", "action": menu_3}
]

class Root(EasyFrame):
    def __init__(self, league=None, player=None, menus=None):
      EasyFrame.__init__(self, title=f'Welcome to the {league.name}', width=500, height=500)
      self.menus = menus 
      self.league = league 
      self.player = player
      self.addLabel(text='Test Label', row=1, column=1)
      self.addButton(text='Test Button - 1', row=1, column=2, command=self.menu_1)
      self.addButton(text='Test Button - 2', row=2, column=2, command=self.menu_2)
      self.addButton(text='Test Button - 3', row=3, column=2, command=self.menu_3)

    def menu_1(self):
      menu_1(self.league)
    
    def menu_2(self):
      menu_2(self.player)

    def menu_3(self):
      menu_3()

league = LinkedList('PBL')
player = Player('Nick Broussard', 18, 'Beef Sliders', 'second base')
root = Root(league, player, menus)
root.mainloop()

# -------------------------------------------------------------------------- #
# take menus in, iterate over menus object/list
# take each menu item, add to menus lst of root gui instance 

# menu = Menu("Main Menu", options)
# menu.add_option('Say Hello 2', say_hello_2)
# test_menu.display()
# action = test_menu.select_option()
# action(val)
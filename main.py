from node import Node 
from player import Player 
from team import Team 
from stack import Stack
from linked_list import LinkedList 
from helpers import is_None, not_found, found, no_teams, show_AVG, league_empty_initial, create_player,\
                    search_player, update_player, user_continue, remove_player, menu_1, menu_2, menu_3, user_start,\
                    view_all, create_team, remove_team, search_team
from breezypythongui import *


def main():
  flag_action = True 
  while flag_action:
    #user_action = menu_1()
    user_action = user_start(league)
    # use complex helper - league size
    if league_empty_initial(league, user_action):
      no_teams()
      user_action = '6'
    #print('menu 1/main - action', user_action)
    match user_action:
      case '1':
        create_player(league)
      case '2':
        search_player(league)
      case '3':
        update_player(league)
      case '4':
        remove_player(league)
      case '5':
        view_all(league)
      case '6':
        create_team(league)
      case '7':
        #print('search team\n')
        search_team(league)
      case '8':
        #print('view all\n')
        print(league)
      case '9':
        remove_team(league)
      case '10':
        print('\nSession terminated\n')
        return
    flag_action = user_continue(flag_action)
  #print('session terminated\n')

if __name__ == '__main__':
  league = LinkedList(input('Enter name of league: '))
  stack = Stack('Last 25 actions...')
  main()
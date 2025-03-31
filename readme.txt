create player class
  - each player starts with basic info
create team class
  - each team starts with empty list
  - add player, appends new player instance to team list
  - each team is a node
  - next pointer points to next team
create league class
  - league starts with no head
  - add new team isntance, create new head or append as last node

  Update Player:
    1 user enters choice of stat t

GUI Layout:

Display Initial (1):
- user has access to list of menu 1 options

Display User Action (2):
- user has access to list of menu options
  - if Update 
    - user has access to list of menu 2 options 
  - else 
    - user has access to functionality of user action (create team/player, remove team/player, etc.)

Display User Action/Continue: 
- if user wishes to continue updating curr player
  - user has access to menu 2 
else:
  - if user wants to continue with another action 
    - user has access to menu 1
  - else 
    - user quits program

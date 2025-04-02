import tkinter as tk
from tkinter import ttk, messagebox 
from linked_list import LinkedList
from team import Team
from player import Player

class BaseballApp():
  # initialize
  def __init__(self, root, league=None):
    self.root = root
    self.root.title = 'PBL'
    self.league = league 

    # Team Management Frame
    self.team_frame = tk.Frame(root, padx=10, pady=10)
    self.team_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    tk.Label(self.team_frame, text="Team Name:").grid(row=0, column=0)
    self.team_entry = tk.Entry(self.team_frame)
    self.team_entry.grid(row=0, column=1)
    tk.Button(self.team_frame, text="Add Team", command=self.add_team).grid(row=0, column=2)

    self.team_listbox = tk.Listbox(self.team_frame, height=10)
    self.team_listbox.grid(row=1, column=0, columnspan=3)

    # Player Management Frame
    self.player_frame = tk.Frame(root, padx=10, pady=10)
    self.player_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    tk.Label(self.player_frame, text="Player Name:").grid(row=0, column=0)
    self.player_entry = tk.Entry(self.player_frame)
    self.player_entry.grid(row=0, column=1)
    
    tk.Label(self.player_frame, text="Team:").grid(row=1, column=0)

    self.team_select = tk.StringVar()
    self.team_dropdown = ttk.Combobox(self.player_frame, textvariable=self.team_select)
    self.team_dropdown.grid(row=1, column=1)
    
    tk.Button(self.player_frame, text="Add Player", command=self.add_player).grid(row=2, column=1)

    self.player_tree = ttk.Treeview(self.player_frame, columns=("Player", "Team"), show="headings")
    self.player_tree.heading("Player", text="Player Name")
    self.player_tree.heading("Team", text="Team")
    self.player_tree.grid(row=3, column=0, columnspan=2)

  # add team function 
  def add_team(self):
    team = self.team_entry.get()
    if team:
      self.team_listbox.insert(tk.END, team)
      self.team_dropdown["values"] = self.team_listbox.get(0, tk.END)
      #print('team', team)
      new_team = Team(team)
      #print('team node', new_team)
      self.league.add_team(new_team)
      #print('league', self.league)
    self.team_entry.delete(0, tk.END)
  
  # add player function
  def add_player(self):
    player = self.player_entry.get()
    team = self.team_select.get()
    # print(team)
    if player:
      # print('new player', player)
      raw_lst = list(map(lambda x: x.strip(), player.split(',')))
      raw_lst.insert(0, team)
      #print(raw_lst)
      new_player = Player.format_player(self, raw_lst)
      self.add_player_team(new_player, team)
      print('new player', new_player)
      team = self.team_dropdown.get()
    self.player_entry.delete(0, tk.END)
  
  # add player to team roster
  def add_player_team(self, new_player, team):
    find_team = self.league.find_team(team)
    find_team.add_player(new_player)
    # print('player', new_player.name)
    # print('team', find_team.name)
    self.player_tree.insert("", tk.END, values=(new_player.name, find_team.name))
    print('league', self.league)
    print('players', self.league.view_all())

if __name__ == "__main__":
  root = tk.Tk()
  PBL = LinkedList('PBL')
  app = BaseballApp(root, PBL)
  root.mainloop()



  

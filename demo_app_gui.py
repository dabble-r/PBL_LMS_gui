import tkinter as tk
from tkinter import ttk, messagebox 
from linked_list import LinkedList
from team import Team
from player import Player
from helpers import update_player
import random
from bisect import bisect_left, bisect_right, insort
from stack import Stack
import sqlite3

# Database Setup
def init_db():
    conn = sqlite3.connect("baseball_league_gui.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS teams (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    team_id INTEGER,
                    batting_avg REAL DEFAULT 0.0,
                    FOREIGN KEY(team_id) REFERENCES teams(id))''')
    conn.commit()
    conn.close()

# Functions
def add_team(team_entry, teams_list):
    team_name = team_entry.get()
    if not team_name:
        messagebox.showwarning("Input Error", "Please enter a team name.")
        return
    try:
        conn = sqlite3.connect("baseball_league_gui.db")
        c = conn.cursor()
        c.execute("INSERT INTO teams (name) VALUES (?)", (team_name,))
        conn.commit()
        conn.close()
        team_entry.delete(0, tk.END)
        load_teams(teams_list)
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Team already exists.")

def load_teams(teams_list, teams_listbox):
    #all_teams = teams_list.get(0, tk.END)
    teams_list['values'] = []
    conn = sqlite3.connect("baseball_league_gui.db")
    c = conn.cursor()
    c.execute("SELECT name FROM teams")
    teams = [row[0] for row in c.fetchall()]
    conn.close()
    teams_list["values"] = teams
    for team in teams:
      teams_listbox.insert(tk.END, team)

class LeagueView():
  def __init__(self, parent, leaderboard=[]):
    self.frame = tk.Frame(parent)
    self.frame.pack()
    self.leaderboard = leaderboard
    
    # define leage view - leading players
    tk.Label(self.frame, text='Leaderboard', padx=2, pady=2).pack()
    self.tree = ttk.Treeview(self.frame, columns=('Player', 'Team', 'AVG'), show='headings')
    
    # display heading names
    self.tree.heading('Player', text='Player')
    self.tree.heading('Team', text='Team')
    self.tree.heading('AVG', text='AVG')

    # Define Column Widths
    self.tree.column("Player", width=150)
    self.tree.column("Team", width=150)
    self.tree.column("AVG", width=75, anchor="center")

    self.tree.pack()

  # add player to leaderboard 
  def add_leaderboard(self, player):
    # player arg should have name, team, batting avg 
    #print(player, type(player))
    #print('name attr', player.name)
    num = player.AVG
    name = player.name
    team = player.team
    avg = "{:.3f}".format(num)
    print('add ledaerboard - avg', avg)
    self.update_leaderboard(name, team, avg)
    for i in range(len(self.leaderboard)-1,-1,-1):
      #print(el)
      el = self.leaderboard[i]
      self.tree.insert('', tk.END, values=(el[0], el[1], el[2]))
  
  # clear all tree vals for new sorted leaderboard  
  def clear_tree(self):
    for el in self.tree.get_children():
      self.tree.delete(el)

  # insort - sort avgs in leaderbaord, find indx of new avg
  def insort_leaderboard(self, new_avg):
    avgs = [x[2] for x in self.leaderboard]
    indx = bisect_right(avgs, new_avg)
    return indx
  
  # insert_leaderbaord
  def update_leaderboard(self, name, team, avg):
    indx = self.insort_leaderboard(avg)
    self.leaderboard.insert(indx, (name, team, avg))
    self.clear_tree()

class BaseballApp():
  # initialize
  def __init__(self, root, app, league=None):
    self.root = root
    self.root.title = 'PBL'
    self.app = app
    self.league = league 
    self.stack = Stack()

    # Team Management Frame
    self.team_frame = tk.Frame(root, padx=10, pady=10)
    self.team_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    tk.Label(self.team_frame, text="Team Name:").grid(row=0, column=0)

    self.team_entry = tk.Entry(self.team_frame)
    self.team_entry.grid(row=0, column=1)

    tk.Button(self.team_frame, text="Add Team", command=self.add_team_db).grid(row=0, column=2)

    self.team_listbox = tk.Listbox(self.team_frame, height=10, justify='center')
    self.team_listbox.grid(row=1, column=0, columnspan=3)

    # Player Management Frame
    self.player_frame = tk.Frame(root, padx=10, pady=10)
    self.player_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    tk.Label(self.player_frame, text="Player Name:\n(Name, Number, Positions)").grid(row=0, column=0)

    self.player_entry = tk.Entry(self.player_frame)
    self.player_entry.grid(row=0, column=1)
    
    tk.Label(self.player_frame, text="Team:").grid(row=1, column=0)

    self.team_select = tk.StringVar()
    self.team_dropdown = ttk.Combobox(self.player_frame, textvariable=self.team_select)
    self.team_dropdown.grid(row=1, column=1)
    
    tk.Button(self.player_frame, text="Add Player)", command=self.add_player).grid(row=2, column=1)

    self.player_tree = ttk.Treeview(self.player_frame, columns=("Player", "Team"), show="headings")
    self.player_tree.heading("Player", text="Player Name")
    self.player_tree.heading("Team", text="Team")
    self.player_tree.grid(row=3, column=0, columnspan=2)

    # Player update frame
    options = ['at_bats', 'hits', 'walks', 'SO', 'HR', 'RBI', 'runs', 'singles', 'doubles', 'triples', 'sac_fly']

    self.update_frame = tk.Frame(root, padx=10, pady=10)
    self.update_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    tk.Label(self.update_frame, text="Update Player:").grid(row=0, column=1)

    self.update_name = tk.Entry(self.update_frame)
    self.update_name.grid(row=0, column=2)

    tk.Label(self.update_frame, text="Stat:").grid(row=1, column=1)

    self.update_val = tk.Entry(self.update_frame)
    self.update_val.grid(row=1, column=2)

    self.selected = tk.StringVar(value='at bat')

    tk.Button(self.update_frame, text='Update', command=self.update_stat).grid(row=2, column=2)

    # Player reset functionality

    tk.Button(self.update_frame, text="Undo", command=self.undo_update).grid(row=3, column=2)

    # populate radio buttons
    row = 2
    for el in options:
      tmp = el
      tk.Radiobutton(self.update_frame, text=tmp, textvariable=tmp, value=tmp, variable=self.selected, command=self.selected_option).grid(row=row, column=1, sticky='w')
      tmp = None
      row += 1

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
      add_team(self.team_entry, self.team_dropdown)
      #print('league', self.league)
    self.team_entry.delete(0, tk.END)
  
  # add team function - sqlite DB functionality
  def add_team_db(self):
    team_name = self.team_entry.get()
    load_teams(self.team_dropdown, self.team_listbox)
    if not team_name:
        messagebox.showwarning("Input Error", "Please enter a team name.")
        return
    try:
        conn = sqlite3.connect("baseball_league_gui.db")
        c = conn.cursor()
        c.execute("INSERT INTO teams (name) VALUES (?)", (team_name,))
        conn.commit()
        conn.close()
        self.team_entry.delete(0, tk.END)
        #self.team_listbox.insert(tk.END, team_name)
        new_team = Team(team_name)
        self.league.add_team(new_team)
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Team already exists.")
      
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
      #print('new player - avg', new_player.AVG)
      self.add_player_team(new_player, team)
      self.app.add_leaderboard(new_player)
      print('new player', new_player)
    self.player_entry.delete(0, tk.END)

  # update player stat
  def update_stat(self):
    stat = self.selected_option()
    name = self.update_name.get().strip()
    team = self.team_dropdown.get()
    val = int(self.update_val.get())
    ret_stat = f'{name}, {team}'
    print(team, name, stat, val)

    ret_board = update_player(self.league, ret_stat, stat, val)
    avg = "{:.3f}".format(float(ret_board.AVG))
   
    for indx, el in enumerate(self.app.leaderboard):
      if el[0] == name:
        self.app.leaderboard.pop(indx)
        self.app.update_leaderboard(name, team, avg)
        print('update stat - avg', avg)
        for i in range(len(self.app.leaderboard)-1, -1, -1):
          #print(el)
          el = self.app.leaderboard[i]
          self.app.tree.insert('', tk.END, values=(el[0], el[1], el[2]))
    self.stack.add_node(team, name, stat, val)
    self.update_name.delete(0, tk.END)
    self.update_val.delete(0, tk.END)
  
  def undo_update(self):
    stat = self.stack.get_last().stat 
    val = int(self.stack.get_last().val)
    print('type val - undo', type(val))
    player = self.stack.get_last().player
    team = self.stack.get_last().team
    print(team, player, stat, val)

    find_team = self.league.find_team(team)
    find_player = find_team.get_player(player)
    #print('team', find_team, '\nplayer', player)

    print('before', find_player)
    match stat:
      case 'at_bats':
        find_player.set_at_bat(-val)
      case 'hits':
        find_player.set_hit(-val)
      case 'walks':
        find_player.set_bb(-val)
      case 'SO':
        find_player.set_so(-val)
      case 'HR':
        find_player.set_hr(-val)
      case 'RBI':
        find_player.set_rbi(-val)
      case 'runs':
        find_player.set_runs(-val)
      case 'singles':
        find_player.set_singles(-val)
      case 'doubles':
        find_player.set_doubles(-val)
      case 'triples':
        find_player.set_triples(-val)
      case 'sac_fly':
        find_player.set_sac_fly(-val)
    #print(team, stat, val)
    print('after', find_player)    
   
  def selected_option(self):
    print(self.selected.get())
    return self.selected.get()
  
  # add player to team roster
  def add_player_team(self, new_player, team):
    find_team = self.league.find_team(team)
    try:
      find_team.add_player(new_player)
      # print('player', new_player.name)
      # print('team', find_team.name)
      self.player_tree.insert("", tk.END, values=(new_player.name, find_team.name))
      print('league', self.league)
      print('players', self.league.view_all())
    except Exception as e:
      print(f'Error: {e}')
      return

if __name__ == "__main__":
  root = tk.Tk()
  PBL = LinkedList('PBL')
  league_view = LeagueView(root)
  app = BaseballApp(root, league_view, PBL)
  init_db()
  root.mainloop()



  

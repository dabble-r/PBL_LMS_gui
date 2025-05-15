import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from linked_list import LinkedList
from team import Team
from player import Player
from helpers import update_player
import random
from bisect import bisect_left, bisect_right, insort
from stack import Stack
import sqlite3
import json
from decimal import Decimal

# Database Setup
def init_db(load_teams, load_players_tree, load_players, load_leaderboard):
    #print('league:', PBL)
    conn = sqlite3.connect("baseball_league_gui.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS teams (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL)''')
    # Create players table with full stat fields
    c.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            number INTEGER,
            team_id INTEGER,
            positions TEXT,
            at_bats INTEGER DEFAULT 0,
            hits INTEGER DEFAULT 0,
            walks INTEGER DEFAULT 0,
            so INTEGER DEFAULT 0,
            hr INTEGER DEFAULT 0,
            rbi INTEGER DEFAULT 0,
            runs INTEGER DEFAULT 0,
            singles INTEGER DEFAULT 0,
            doubles INTEGER DEFAULT 0,
            triples INTEGER DEFAULT 0,
            sac_fly INTEGER DEFAULT 0,
            BABIP REAL DEFAULT 0.000,
            SLG REAL DEFAULT 0.000,
            AVG REAL DEFAULT 0.000,
            ISO REAL DEFAULT 0.000,
            FOREIGN KEY(team_id) REFERENCES teams(id)
        )
    ''')
    conn.commit()
    load_teams()
    load_players_tree()
    load_players()
    load_leaderboard()
    conn.close()

# Functions
def add_team(team_entry):
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
        #load_teams(teams_list)
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Team already exists.")

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
    ##print(player, type(player))
    ##print('name attr', player.name)
    num = player.AVG
    name = player.name
    team = player.team
    avg = "{:.3f}".format(num)
    #print('add leaderboard', name,team,num,avg)
    self.update_leaderboard(name, team, avg)
    #print('leaderboard after update', self.leaderboard)
    for i in range(len(self.leaderboard)-1,-1,-1):
      ##print(el)
      el = self.leaderboard[i]
      #print('leaderboard el', el)
      self.tree.insert('', tk.END, values=(el[0], el[1], el[2]))
  
  # clear all tree vals for new sorted leaderboard  
  def clear_tree(self):
    for el in self.tree.get_children():
      self.tree.delete(el)

  # insort - sort avgs in leaderboard, find indx of new avg
  def insort_leaderboard(self, new_avg):
    avgs = [x[2] for x in self.leaderboard]
    indx = bisect_right(avgs, new_avg)
    return indx
  
  # insert_leaderbaord
  def update_leaderboard(self, name, team, avg):
    indx = self.insort_leaderboard(avg)
    #print('up leader indx', indx)
    self.leaderboard.insert(indx, (name, team, avg))
    #print('lyst insert', lyst)
    #self.clear_tree()

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
    tk.Button(self.team_frame, text="Remove", command=self.remove_team_db).grid(row=1, column=2)

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
    
    tk.Button(self.player_frame, text="Add", command=self.add_player_db).grid(row=2, column=0, padx=(0,4), pady=2, sticky="ew")

    self.player_tree = ttk.Treeview(self.player_frame, columns=("Player", "Team"), show="headings")
    self.player_tree.heading("Player", text="Player Name")
    self.player_tree.heading("Team", text="Team")
    self.player_tree.grid(row=3, column=0, columnspan=2)

    # remove player button
    tk.Button(self.player_frame, text="Remove", command=self.remove_player_all_locs).grid(row=2, column=1, padx=(4,0), pady=2, sticky="ew")

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

    tk.Button(self.update_frame, text='Update', command=self.update_stat_db).grid(row=2, column=2)

    # Player reset functionality
    tk.Button(self.update_frame, text="Undo", command=self.undo_update).grid(row=3, column=2)

    # populate radio buttons
    row = 2
    for el in options:
      tmp = el
      tk.Radiobutton(self.update_frame, text=tmp, textvariable=tmp, value=tmp, variable=self.selected, command=self.selected_option).grid(row=row, column=1, sticky='w')
      tmp = None
      row += 1
    
    # save progress
    tk.Button(self.update_frame, text="Save", command=self.save_prompt).grid(row=15, column=2)

  def load_teams(self):
    #all_teams = teams_list.get(0, tk.END)
    #print(all_teams)
    self.team_dropdown['values'] = []
    conn = sqlite3.connect("baseball_league_gui.db")
    c = conn.cursor()
    c.execute("SELECT name FROM teams")
    teams = [row[0] for row in c.fetchall()]
    conn.close()
    self.team_dropdown["values"] = teams
    teams_listbox_curr = self.team_listbox.get(0, tk.END)
    for team in teams:
      db_team = Team(team)
      db_team = Team(team)
      PBL.add_team(db_team)
      if team not in teams_listbox_curr:
        self.team_listbox.insert(tk.END, team)
    #print(self.league)
  
  def load_players_tree(self):
    #all_players = self.player_tree.get_children()
    #print(all_players)
    conn = sqlite3.connect("baseball_league_gui.db")
    c = conn.cursor()
    #c.execute("SELECT name, team_id FROM players")
    c.execute("""
      SELECT players.name, teams.name, players.AVG
      FROM players
      JOIN teams on players.team_id = teams.id
    """
    )
    results = c.fetchall()
    #players = [(row[0], row[1]) for row in c.fetchall()]
    #print(players)
    #print(results)
    player = None
    team = None 
    avg = None
    for el in results:
      player, team, avg = el
      # league view players/teams (unsorted)
      self.player_tree.insert("", tk.END, values=(player, team))
    print('load player res', results)

  def remove_one_player_tree(self, target_player):
    players = self.player_tree.get_children()
    for el in players:
      player = self.player_tree.item(el, "values")
      if player[0] == target_player:
        self.player_tree.delete(el)
        print("deleted player")
      #print(el)
      #print(player)
    #print('player not found in tree')
      
  
  def load_players(self):
    conn = sqlite3.connect("baseball_league_gui.db")
    c = conn.cursor()
    #c.execute("SELECT name, team_id FROM players")
    c.execute("""
      SELECT players.name, teams.name, players.AVG, players.number, players.positions
      FROM players
      JOIN teams on players.team_id = teams.id
    """
    )
    results = c.fetchall()
    results.sort(key=self.my_sort, reverse=True)
    return results

  # sorting purpose for refresh self.leaderboard on start
  # ----------- NOT FUNCTIONING ----------------- #
  def my_sort(self, x):
    # sort by player avg
    return x[2]
  
  def load_leaderboard(self):
    
    try:
      self.app.clear_tree()
      results = self.load_players()
      #print('league\n', PBL)
      #print('players\n', PBL.view_all())
      print('db results', results)

      if results:
        tmp = []
        for el in results:
          #print(el)
          player, team, avg, number, positions = el
          load_team = PBL.find_team(team)
          if load_team:
            load_player = Player(player, number, team, positions)
            load_team.add_player(load_player)
          self.app.tree.insert('', tk.END, values=(player, team, avg))

    except:
      print('error accessing results')
    finally:
      #print(PBL.view_all())
      print('completed loading players/team')

                                   # ----------------------------------------------------------------- #

  # add team function 
  # deprecated #
  def add_team(self):
    team = self.team_entry.get()
    if team:
      self.team_listbox.insert(tk.END, team)
      self.team_dropdown["values"] = self.team_listbox.get(0, tk.END)
      ##print('team', team)
      new_team = Team(team)
      ##print('team node', new_team)
      self.league.add_team(new_team)
      add_team(self.team_entry, self.team_dropdown)
      ##print('league', self.league)
    self.team_entry.delete(0, tk.END)
                                      # ----------------------------------------------------------------- #
  
  # add team function - sqlite DB functionality
  def add_team_db(self):
    team_name = self.team_entry.get()
    if not team_name:
        messagebox.showwarning("Input Error", "Please enter a team name.")
        return
    try:
        conn = sqlite3.connect("baseball_league_gui.db")
        c = conn.cursor()
        c.execute("INSERT INTO teams (name) VALUES (?)", (team_name,))
        conn.commit()
        conn.close()
        #self.team_listbox.insert(tk.END, team_name)
        new_team = Team(team_name)
        self.league.add_team(new_team)
        self.load_teams()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Team already exists.")
    finally:
      self.team_entry.delete(0, tk.END)
  
  def remove_team_db(self):
    team_name = self.team_entry.get()
    if not team_name:
        messagebox.showwarning("Input Error", "Please enter a team name.")
        return
    try:
        conn = sqlite3.connect("baseball_league_gui.db")
        c = conn.cursor()
        # delete from sqlite db
        c.execute("DELETE FROM teams WHERE name = (?)", (team_name,))
        conn.commit()

        # delete from GUI
        for idx in range(self.team_listbox.size()):
          if self.team_listbox.get(idx) == team_name:
            self.team_listbox.delete(idx)
            break 

        #remove from league object
        self.league.remove_team(team_name)

        # refresh gui 
        self.load_teams()

    except sqlite3.Error as e:
        messagebox.showerror("DB Error:", f"An error occurred: {e}.")
    finally:
      conn.close()
      self.team_entry.delete(0, tk.END)
      #print(self.league)

  # db - add player function
  def add_player_db(self):
    player = self.player_entry.get()
    team = self.team_select.get()
    #print('team get:', team)
    # #print(team)
    if not player:
      messagebox.showwarning("Input Error", "Please enter a player name.")
      return
    try:
      #print('adding new player...\n')
      raw_lst = list(map(lambda x: x.strip(), player.split(',')))
      raw_lst.insert(0, team)
      #print(raw_lst)
      team_name = raw_lst[0]
      player_name = raw_lst[1]
      number = int(raw_lst[2])
      positions_raw = raw_lst[3:]
      positions_json = json.dumps(positions_raw)
      #print(player_name, team_name, number, positions_json)

      new_player = Player.format_player(self, raw_lst)
      ##print('new player - avg', new_player.AVG)

      self.add_player_team(new_player, team)
      #self.app.add_leaderboard(new_player)
      ##print('new player:', new_player)

      conn = sqlite3.connect("baseball_league_gui.db")
      c = conn.cursor()
      c.execute("SELECT id FROM teams WHERE name = ?", (team_name,))
      team_id = c.fetchone()

      if team_id:
        #print(f"Found team: {team_id[0]}")
        c.execute("INSERT INTO players (name, number, positions, team_id) VALUES (?, ?, ?, ?)", (player_name, number, positions_json, team_id[0],))
        conn.commit()
        self.load_leaderboard()
      else:
        print(f"No id found for team {team}")
        conn.close()

    except:
      print('error adding new player')

    finally:
      print('completed adding new player')
      self.player_entry.delete(0, tk.END)

                                              # ------------------------------------------------------------------------------------ #
  # deprecated
  # add player function
  def add_player(self):
    player = self.player_entry.get()
    team = self.team_select.get()
    # #print(team)
    if player:
      # #print('new player', player)
      raw_lst = list(map(lambda x: x.strip(), player.split(',')))
      raw_lst.insert(0, team)
      ##print(raw_lst)
      new_player = Player.format_player(self, raw_lst)
      ##print('new player - avg', new_player.AVG)
      self.add_player_team(new_player, team)
      self.app.add_leaderboard(new_player)
      #print('new player', new_player)
    self.player_entry.delete(0, tk.END)
                                              # ------------------------------------------------------------------------------------ #
  
  # update player stat
  def update_stat_db(self):
    stat = self.selected_option()
    player = self.update_name.get().strip()
    team = self.team_dropdown.get()
    val = int(self.update_val.get())
    ret_stat = f'{player}, {team}'
    print(team, player, stat, val)

    if not player:
      messagebox.showwarning("Input Error", "Please enter a player name.")
      return
    
    conn = sqlite3.connect("baseball_league_gui.db")
    try:
      # sqlite db update
      c = conn.cursor()
      c.execute("SELECT id, at_bats, hits, walks, so, hr, rbi, runs, singles, doubles, triples, sac_fly, SLG, AVG FROM players WHERE name = ?", (player,))
      result = c.fetchone()
      print('result', result)

      if result:
        player_id, at_bats, hits, walks, so, hr, rbi, runs, singles, doubles, triples, sac_fly, slg, avg_db = result
        new_BABIP = self.update_BABIP(hits, hr, at_bats, so, sac_fly)
        new_SLG = self.update_SLG(singles, doubles, triples, hr, at_bats)
        new_ISO = self.update_ISO(doubles, triples, hr, slg, avg_db)
        new_AVG = self.update_AVG(at_bats, hits)
        #print('new avg', new_AVG, type(new_AVG))
        #print('new slg', new_SLG, type(new_SLG))
        #print('new BABIP', new_BABIP, type(new_BABIP))
        #print('new ISO', new_ISO, type(new_ISO))
        #print('avg db', avg_db, type(avg_db))
        #print('avg - format', self.format_decimal(avg_db))

        # user manual update
        query = f"""
          UPDATE players 
          SET {stat} = {stat} + ?, 
            BABIP = ?, 
            SLG = ?, 
            ISO = ?, 
            AVG = ?
          WHERE id = ?
        """
        params = (val, new_BABIP, new_SLG, new_ISO, new_AVG, player_id)
        c.execute(query, params)
        conn.commit()

        '''# GUI update
        ret_board = update_player(self.league, ret_stat, stat, val)
        avg = "{:.3f}".format(float(ret_board.AVG))
    
        for indx, el in enumerate(self.app.leaderboard):
          if el[0] == player:
            self.app.leaderboard.pop(indx)
            self.app.update_leaderboard(player, team, avg)
            #print('update stat - avg', avg)
            for i in range(len(self.app.leaderboard)-1, -1, -1):
              ##print(el)
              el = self.app.leaderboard[i]
              self.app.tree.insert('', tk.END, values=(el[0], el[1], el[2]))
        self.stack.add_node(team, player, stat, val)'''

      else:
        print(f"No id found for team {player}")

    except:
      print(f'Error updating {stat} for {player}')

    finally:
      conn.close()
      print('completed player updates')
      #self.update_name.delete(0, tk.END)
      self.update_val.delete(0, tk.END)
      # GUI update stat
      self.load_leaderboard()
  
  # remove player from db, league, and GUI
  def remove_player_all_locs(self):
    select_player = self.player_tree.selection()
    print('remove player - selection', select_player)
    if select_player:
      name, team = self.player_tree.item(select_player[0], "values")
      #print(name, team)

      # remove from league
      find_team = PBL.find_team(team)
      if find_team:
        #print('found team', find_team)
        find_team.remove_player(name)
      else:
        print('remove team not found!')

      # remove from DB
      conn = sqlite3.connect("baseball_league_gui.db")
      try:
        # sqlite db update
        c = conn.cursor()
        c.execute("SELECT * FROM players WHERE name = ?", (name,))
        result = c.fetchall()[0]
        #print('result', result)
        if result:
          name = result[1]
          #print('remove name DB', name)
          query = "DELETE FROM players where name = ?"
          c.execute(query, (name,))
          conn.commit()
          print('player removed from DB!')
      except:
        print('remove player not deleted!')

      # remove from GUI
      self.load_leaderboard()
      self.remove_one_player_tree(name)


  def update_AVG(self, at_bats, hits):
    if at_bats == 0:
      return 0
    ret = hits / at_bats
    #print(self.at_bat, self.hit)
    return float(self.format_decimal(ret))
    
  def update_BABIP(self, hits, hr, at_bats, so, sac_fly):
    if (at_bats - so - hr + sac_fly) <= 0:
      return 0
    ret = (hits - hr) / (at_bats - so - hr + sac_fly)
    return float(self.format_decimal(ret))

  def update_SLG(self, singles, doubles, triples, hr, at_bats):
    if at_bats == 0:
      return 0
    ret = (singles + (2 * doubles) + (3 * triples) + (4 * hr) ) / at_bats
    return float(self.format_decimal(ret))

  def update_ISO(self, doubles, triples, hr, slg, avg):
    if slg - avg <= 0:
      return 0
    ret = ( (1 * doubles) + (2 * triples) + (3 * hr ) ) / slg - avg
    return float(self.format_decimal(ret))

  def format_decimal(self, num):
    #print('fromat type', type("{:.3f}".format(num)))
    dec_num = Decimal(f"{num}")
    format_num = dec_num.quantize(Decimal("0.000"))
    #print('formatted num', format_num, type(format_num))
    return format_num

                                        # --------------------------------------------------------------------------------------- #
  
  # deprecated
  # update player stat
  def update_stat(self):
    stat = self.selected_option()
    name = self.update_name.get().strip()
    team = self.team_dropdown.get()
    val = int(self.update_val.get())
    ret_stat = f'{name}, {team}'
    #print(team, name, stat, val)

    ret_board = update_player(self.league, ret_stat, stat, val)
    avg = "{:.3f}".format(float(ret_board.AVG))
   
    for indx, el in enumerate(self.app.leaderboard):
      if el[0] == name:
        self.app.leaderboard.pop(indx)
        self.app.update_leaderboard(name, team, avg, self.app.leaderboard)
        #print('update stat - avg', avg)
        for i in range(len(self.app.leaderboard)-1, -1, -1):
          ##print(el)
          el = self.app.leaderboard[i]
          self.app.tree.insert('', tk.END, values=(el[0], el[1], el[2]))
    self.stack.add_node(team, name, stat, val)
    self.update_name.delete(0, tk.END)
    self.update_val.delete(0, tk.END)
                                          # --------------------------------------------------------------------------------------- #
  
  def undo_update(self):
    stat = self.stack.get_last().stat 
    val = int(self.stack.get_last().val)
    #print('type val - undo', type(val))
    player = self.stack.get_last().player
    team = self.stack.get_last().team
    #print(team, player, stat, val)

    find_team = self.league.find_team(team)
    find_player = find_team.get_player(player)
    ##print('team', find_team, '\nplayer', player)

    #print('last:',find_player)
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
    ##print(team, stat, val)
    #print('after', find_player)    
   
  def selected_option(self):
    #print(self.selected.get())
    return self.selected.get()
  
  # add player to team roster
  def add_player_team(self, new_player, team):
    find_team = self.league.find_team(team)
    try:
      find_team.add_player(new_player)
      # #print('player', new_player.name)
      # #print('team', find_team.name)
      self.player_tree.insert("", tk.END, values=(new_player.name, find_team.name))
      #print('league', self.league)
      #print('players', self.league.view_all())
    except Exception as e:
      #print(f'Error: {e}')
      return
  
  def save_prompt(self):
    save_frame = Save()

class Save():
  def __init__(self):
    # Ask the user to choose where to save the file
    self.file_path = self.user_path() 
  
  def user_path(self):
    self.file_path = filedialog.asksaveasfilename(
      defaultextension=".db",
      filetypes=[("SQLite Database", "*.db")],
      title="Save Progress"
    )

    # Only continue if the user selected a path
    if self.file_path:
      # Connect to the source database (e.g., in-memory or existing)
      source_conn = sqlite3.connect("baseball_league_gui.db")
      cursor = source_conn.cursor()
      cursor.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT);")
      cursor.execute("INSERT INTO test (name) VALUES ('Alice');")
      source_conn.commit()
      # Create the destination database at chosen path
      dest_conn = sqlite3.connect(self.file_path)
      with dest_conn:
          source_conn.backup(dest_conn)
      source_conn.close()
      dest_conn.close()
      print(f"Database saved to: {self.file_path}")
    else:
      print("Save aborted.")

if __name__ == "__main__":
  root = tk.Tk()
  PBL = LinkedList('PBL')
  league_view = LeagueView(root)
  app = BaseballApp(root, league_view, PBL)
  init_db(app.load_teams, app.load_players_tree, app.load_players, app.load_leaderboard)
  root.mainloop()



  

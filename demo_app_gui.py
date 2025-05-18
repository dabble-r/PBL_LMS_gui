import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from ttkthemes import ThemedTk
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
import asyncio
import aiosqlite

# Database Setup
async def init_db(load_teams, load_players_tree, load_players, load_leaderboard):
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
    await load_players()
    await load_leaderboard()
    conn.close()

# ------------------------------------------------------------------------------------#
# Functions
# wtf if this function doing here???
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
# ------------------------------------------------------------------------------------#

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
    new_avg = float(new_avg)
    indx = bisect_right(avgs, new_avg)
    return indx
  
  # insert_leaderbaord
  def update_leaderboard(self, name, team, avg, flag=False):
    """
    Updates the leaderboard with the given player information.

    Parameters:
      name (str): The name of the player.
      team (str): The name of the team.
      avg (float): The player's average.
      flag (bool): False when adding a new player.
                    True when updating an existing player's entry.
    """
    # If updating an existing player, remove any prior record for that player.
    if flag:
        self.leaderboard = [entry for entry in self.leaderboard if entry[0] != name]

    # Use the insort_leaderboard helper to get the index for insertion based on avg.
    insertion_index = self.insort_leaderboard(avg)
    self.leaderboard.insert(insertion_index, (name, team, avg))

    # Refresh the tree (GUI) to display the updated leaderboard.
    self.refresh_leaderboard_tree()

  def refresh_leaderboard_tree(self):
    """
    Clears the current tree view and repopulates it from the sorted leaderboard.
    """
    self.clear_tree()
    # Assuming you want a descending order display, iterate in reverse.
    for entry in reversed(self.leaderboard):
      self.tree.insert('', tk.END, values=entry)

  async def refresh_treeview(self):
    self.clear_tree()

    query = """
    SELECT p.name, p.avg, t.name
    FROM players AS p
    JOIN teams AS t ON p.team_id = t.id
    """
    async with aiosqlite.connect("baseball_league_gui.db") as conn:
      async with conn.execute(query) as cursor:
        results = await cursor.fetchall()

      for row in results:
        name, avg, team = row
        self.tree.insert('', 'end', values=(name, team, avg))
    await conn.close()

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
    
    tk.Button(self.player_frame, text="Add", command=self.run_async_add_player).grid(row=2, column=0, padx=(0,4), pady=4)

    self.player_tree = ttk.Treeview(self.player_frame, columns=("Player", "Team"), show="headings", height=15)
    self.player_tree.heading("Player", text="Player")
    self.player_tree.heading("Team", text="Team")
    self.player_tree.grid(row=3, column=0, columnspan=4, padx=50)

    # remove player button
    # command=self.run_async_remove_player_all_locs
    tk.Button(self.player_frame, text="Remove", command=self.run_async_remove_player_all_locs).grid(row=2, column=1, padx=(4,0), pady=4)

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

    tk.Button(self.update_frame, text='Update', command=self.run_async_update_player_2).grid(row=2, column=2)

    # Player reset functionality
    tk.Button(self.update_frame, text="Undo", command=self.undo_update).grid(row=3, column=2)

    # populate radio buttons
    row = 2
    for el in options:
      tmp = el
      tk.Radiobutton(self.update_frame, text=tmp, textvariable=tmp, value=tmp, variable=self.selected, command=self.selected_option).grid(row=row, column=3, sticky='w')
      tmp = None
      row += 1
    
    # save progress
    tk.Button(self.update_frame, text="Save", command=self.save_prompt, width=5, height=2, font=('Arial', 12)).place(relx=0.8, rely=0.9)

    # populate individual player stat button for each player
    x = 455
    y = 250
    tk.Button(self.player_frame, text='Stats', command=self.run_async_display_individual_players).place(x=x, y=y)

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
      #db_team = Team(team)
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
    #print(results)

    player = None
    team = None 
    avg = None

    for el in results:
      player, team, avg = el
      self.player_tree.insert("", tk.END, values=(player, team))
      
    #print('load player res', results)

  def remove_one_player_tree(self, target_player):
    players = self.player_tree.get_children()
    for el in players:
      player = self.player_tree.item(el, "values")
      name = player[0]
      if name == target_player:
        self.player_tree.delete(el)
        #print("deleted player")
      else:
        print('player not found in tree')
      
  async def load_players(self):
    async with aiosqlite.connect("baseball_league_gui.db") as conn:
      async with conn.execute("""
        SELECT players.name, teams.name, players.AVG, players.number, players.positions
        FROM players
        JOIN teams on players.team_id = teams.id
        """) as cursor:
          results = await cursor.fetchall()
          results.sort(key=self.my_sort, reverse=True)
          return results

  # sorting purpose for refresh self.leaderboard on start
  
  def my_sort(self, x):
    # sort by player avg
    return x[2]
  
  async def load_leaderboard(self):
    
    try:
      self.app.clear_tree()
      results = await self.load_players()
      #print('league\n', PBL)
      #print('players\n', PBL.view_all())
      #print('db results', results)

      if results:
        
        for el in results:
          #print('load leaderboard - player in db', el)
          player, team, avg, number, positions = el
          load_team = PBL.find_team(team)
          if load_team:
            load_player = Player(player, number, team, positions)
            load_player.AVG = avg
            load_team.add_player(load_player)
            self.app.tree.insert('', tk.END, values=(player, team, avg))
            self.app.update_leaderboard(player, team, load_player.AVG, flag=True)
          
    except:
      print('error accessing results')

    finally:
      #print(PBL.view_all())
      print('completed loading players/team')
      
  async def load_one_player(self, target_player):
    query = """
    SELECT p.name, t.name AS team_name, p.avg
    FROM players AS p
    JOIN teams AS t ON p.team_id = t.id
    WHERE p.name = ?
    """
    
    async with aiosqlite.connect("baseball_league_gui.db") as conn:
        async with conn.execute(query, (target_player,)) as cursor:
            result = await cursor.fetchone()
            if result is None:
                print(f"No player found with the name: {target_player}")
            else:
                print("load_one - Updated player:", result)
            return result
        
  async def load_one_player_all_stats(self, target_player):
    query = """
    SELECT *
    FROM players AS p
    JOIN teams AS t ON p.team_id = t.id
    WHERE p.name = ?
    """
    
    async with aiosqlite.connect("baseball_league_gui.db") as conn:
        async with conn.execute(query, (target_player,)) as cursor:
            result = await cursor.fetchone()
            if result is None:
                print(f"No player found with the name: {target_player}")
            else:
                print("load_one - Updated player:", result)
            return result

  async def update_leaderboard(self, target_player, flag):
    #print('update leaderboard')
    result = await self.load_one_player(target_player)
    #print('after update:', result)
    if result:
      name, team, avg = result 
      #print('update leaderboard:', (name, team, avg, type(avg)))
      self.app.update_leaderboard(name, team, avg, flag)
      
                                  # ----------------------------------------------------------------- #

  
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
      
                                              # ------------------------------------------------------------------------------------ #
  
  # db - add player
  # async - AI assist
  # currently in use
  async def add_player_db_1(self):
    player = self.player_entry.get()
    team = self.team_select.get()

    if not player:
        messagebox.showwarning("Input Error", "Please enter a player name.")
        return

    try:
        #print('Adding new player...\n')
        # Parse player details
        raw_lst = list(map(lambda x: x.strip(), player.split(',')))

        if len(raw_lst) < 3:
          messagebox.showwarning("Input Error", "Please enter a player name, team name, and at least one position.")
          return
        
        raw_lst.insert(0, team)
        team_name = raw_lst[0]
        player_name = raw_lst[1]
        number = int(raw_lst[2])
        positions_raw = raw_lst[3:]
        positions_json = json.dumps(positions_raw)

        # Format and add player to the team
        new_player = Player.format_player(self, raw_lst)
        avg = new_player.AVG
        self.add_player_team(new_player, team)
        #print('add new player:\n', new_player)

        # Async database operations
        async with aiosqlite.connect("baseball_league_gui.db") as conn:
            # Fetch team ID
            async with conn.execute("SELECT id FROM teams WHERE name = ?", (team_name,)) as cursor:
              team_id = await cursor.fetchone()

              if team_id:
                  
                  # check if player name already exists
                  async with conn.execute("SELECT 1 FROM players WHERE name = ?", (player_name,)) as cursor:
                    player_exists = await cursor.fetchone()
                    #print('player exsits:', player_exists)

                    if not player_exists:
                       
                      # Insert player data
                      await conn.execute(
                          "INSERT INTO players (name, number, positions, team_id, AVG) VALUES (?, ?, ?, ?, ?)",
                          (player_name, number, positions_json, team_id[0], avg)
                      )
                      
                      await conn.commit()
                    
                    else:
                      messagebox.showwarning("Input Error", "Player name already exists. Try using full name.")
                      return
                  
              else:
                  print(f"No ID found for team {team}")

    except Exception as e:
        print(f"Error adding new player: {e}")

    finally:
        print("Completed adding new player")
        #await conn.close()
        self.player_entry.delete(0, tk.END)
    #self.app.add_leaderboard(new_player)
    await self.app.refresh_treeview()

  # run async for tkinter
  # currently in use as button command func
  def run_async_add_player(self):
    asyncio.run(self.add_player_db_1())  # Runs the async function safely

                                              # ------------------------------------------------------------------------------------ #

  # run async for tkinter
  # currently in use as button command func
  def run_async_update_player_2(self):
    asyncio.run(self.update_stat_db_1())  # Runs the async function safely

  # AI assist
  # currently in use
  async def update_stat_db_1(self):
    stat = self.selected_option()
    player = self.update_name.get().strip()
    team = self.team_dropdown.get()
    val = int(self.update_val.get())
    #print(team, player, stat, val)

    if not player:
        messagebox.showwarning("Input Error", "Please enter a player name.")
        return

    try:
        async with aiosqlite.connect("baseball_league_gui.db") as conn:
            # Fetch player stats
            async with conn.execute(
                "SELECT id, at_bats, hits, walks, so, hr, rbi, runs, singles, doubles, triples, sac_fly, SLG, AVG FROM players WHERE name = ?",
                (player,)) as cursor:
                result_orig = await cursor.fetchone()
                #print("before update:", result_orig)

            if result_orig:
                player_id, at_bats, hits, walks, so, hr, rbi, runs, singles, doubles, triples, sac_fly, slg, avg_db = result_orig

                # Perform the initial update query (update stat)
                await conn.execute(
                    f"""
                    UPDATE players 
                    SET {stat} = {stat} + ?
                    WHERE id = ?
                    """,
                    (val, player_id)
                )

                await conn.commit()

                async with conn.execute(
                  "SELECT id, at_bats, hits, walks, so, hr, rbi, runs, singles, doubles, triples, sac_fly, SLG, AVG FROM players WHERE name = ?",
                  (player,)) as cursor:

                  result_upd = await cursor.fetchone()
                  #print('after update:', result_upd)
                
                  if result_upd:
                    player_id, at_bats, hits, walks, so, hr, rbi, runs, singles, doubles, triples, sac_fly, slg, avg_db = result_upd
                    
                    # Calculate updated stats
                    new_BABIP = self.update_BABIP(hits, hr, at_bats, so, sac_fly)
                    new_SLG = self.update_SLG(singles, doubles, triples, hr, at_bats)
                    new_ISO = self.update_ISO(doubles, triples, hr, slg, avg_db)
                    new_AVG = self.update_AVG(at_bats, hits)

                  await conn.execute(
                    f"""
                    UPDATE players
                    SET BABIP = ?, SLG = ?, ISO = ?, AVG = ?
                    WHERE id = ?
                    """,
                    (new_BABIP, new_SLG, new_ISO, new_AVG, player_id))  # Proper parameter tuple
                    
                  await conn.commit()
                
            else:
                print(f"No id found for player {player}")

    except Exception as e:
        print(f"Error updating {stat} for {player}: {e}")

    finally:
        print("Completed player updates")
        #await conn.close()
        self.update_val.delete(0, tk.END)
        # creates unsorted leaderboard
        #self.app.refresh_treeview()
        #self.app.add_leaderboard(player)
        await self.update_leaderboard(player, flag=True)
  
  # remove player message prompt
  def remove_player_prompt(self):
    selection = self.player_tree.selection()
    name, team = self.player_tree.item(selection, "values")
    response = messagebox.askquestion(title="Remove Options", message=f"Would you like to permanently remove {name}?")
    # print('response:', response)
    return response
  
  # remove player from db, league, and GUI
  async def remove_player_all_locs(self):
    select_player = self.player_tree.selection()
    name, team = self.player_tree.item(select_player, "values")
    #print('remove player - selection', select_player)
    user_response = self.remove_player_prompt()

    if user_response == 'yes':
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
        result = c.fetchall()
        #print('remove result', result)
        
        if result:
          for el in result:
            name = el[1]
            #print('remove name DB', name)
            #print('remove result el', el[1])
            query = "DELETE FROM players where name = ?"
            c.execute(query, (name,))
            conn.commit()
            print('player removed from DB!')

      except:
        print('remove player not deleted!')

      finally:
        # remove from GUI
        self.remove_one_player_tree(name)
        #self.load_leaderboard()
        await self.app.refresh_treeview()

    else:
      # remove selected player from leaderboard
      self.app.leaderboard = [x for x in self.app.leaderboard if x[0] != name]
      self.app.refresh_leaderboard_tree()
  
  # run async for tkinter
  # currently in use as button command func
  def run_async_remove_player_all_locs(self):
    asyncio.run(self.remove_player_all_locs())  # Runs the async function safely

  def run_async_display_individual_players(self):
    asyncio.run(self.display_individual_player())  # Runs the async function safely
    
  # display individual player stats in message box popup
  # not functional - testing
  async def display_individual_player(self):
    selection = self.player_tree.selection()
    if selection:
      name, team = self.player_tree.item(selection, "values")
      #print('display player:', name, team)
      await self.show_player_stats(name)
      
  # load player and display
  async def show_player_stats(self, name):
    def unpack_positions(str):
      ret = ''
      unpack = json.loads(str)
      ret += f"\nPrimary: {unpack[0]}"
      if len(unpack) == 1:
        return ret
      #print(type(unpack), unpack)
      for el in unpack:
         ret += f"\n  Pos: {el}"
      return ret
          
    result = await self.load_one_player_all_stats(name)
    ret = ''
    if result:
      #print('display one player all stats:', result)
      #(15., 'Test2'., 1., 3., '["abc"]'., 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0, 0.0, 1.0, 0.0, 3, 'Rougarou') -- 22 values
      player_id, name, number, team_id_1, positions, at_bats, hits, walks, so, hr, rbi, runs, singles, doubles, triples, sac_fly, babip, slg, avg_db, iso, team_id_2, team = result
      ret += f"Name: {name}\nNumber: {number}\nId: {player_id}\nTeam: {team}\nTeam Id: {team_id_1}\nAVG: {avg_db}\nSLG: {slg}\nBABIP: {babip}\nISO: {iso}\nPositions: {unpack_positions(positions)}\nAt Bats: {at_bats}\nHits: {hits}\nWalks: {walks}\nSO: {so}\nHR: {hr}\nRuns: {rbi}\nRuns: {runs}\nSingles: {singles}\nDoubles: {doubles}\nTriples: {triples}\nSac Fly: {sac_fly}\n"
      messagebox.showinfo(f'{name} stats', ret)

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

  def find_partial_tuple_index(self, lst):
    for i, t in enumerate(lst):
      print('search tuple', i, t)
        #if isinstance(t, tuple) and len(t) >= 2 and t[0] == value1 and t[1] == value2:
            #return i
    #raise ValueError("No matching tuple found")
  
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
  # AI assist - mount all elemtns on root
  # Initialize themed root window
  root = ThemedTk(theme="radiance")

  # Create a single container frame to hold all program elements
  main_frame = ttk.Frame(root)
  main_frame.pack(fill="both", expand=True)  # Ensure it scales properly

  # Initialize objects with the root window as their parent
  PBL = LinkedList('PBL')
  league_view = LeagueView(main_frame)  # Mount on the main frame
  app = BaseballApp(main_frame, league_view, PBL)  # Also mount here

  # Initialize database asynchronously
  asyncio.run(init_db(app.load_teams, app.load_players_tree, app.load_players, app.load_leaderboard))

  root.mainloop()

  # original code
  #root = tk.Tk()
  #root = ThemedTk(theme="radiance")
  #PBL = LinkedList('PBL')
  #league_view = LeagueView(root)
  #app = BaseballApp(root, league_view, PBL)
  #asyncio.run(init_db(app.load_teams, app.load_players_tree, app.load_players, app.load_leaderboard))
  #root.mainloop()



  

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

# deprecated
# not in use
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


# run asycn for tkinter
# deprecated
# not in use
def run_async_update_player_1(self):
  try:
      loop = asyncio.get_running_loop()  # Get the current event loop
  except RuntimeError:
      loop = asyncio.new_event_loop()  # Create a new loop if none exists
      asyncio.set_event_loop(loop)  # Set the new loop as the active one

  loop.create_task(self.update_stat_db_1())  # Schedule the async function

  # Ensure the event loop runs by processing async tasks
  loop.run_until_complete(asyncio.sleep(0))

# update player stat
# not currently in use
async def update_stat_db(self):
  
  stat = self.selected_option()
  player = self.update_name.get().strip()
  team = self.team_dropdown.get()
  val = int(self.update_val.get())
  ret_stat = f'{player}, {team}'
  print(team, player, stat, val)

  if not player:
    messagebox.showwarning("Input Error", "Please enter a player name.")
    return
  
  try:
    # sqlite db update
    async with aiosqlite.connect("baseball_league_gui.db") as conn:
      c = conn.cursor()
      await c.execute("SELECT id, at_bats, hits, walks, so, hr, rbi, runs, singles, doubles, triples, sac_fly, SLG, AVG FROM players WHERE name = ?", (player,))
      result = await c.fetchone()
      print('update result', result)

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
      await c.execute(query, params)
      await conn.commit()

    else:
      print(f"No id found for team {player}")

  except:
    print(f'Error updating {stat} for {player}')

  finally:
    await conn.close()
    print('completed player updates')
    #self.update_name.delete(0, tk.END)
    self.update_val.delete(0, tk.END)
    # GUI update stat
    #self.load_leaderboard()
  await self.update_leaderboard(player)

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
      # commented out - function not in use
      # self.app.update_leaderboard(name, team, avg, self.app.leaderboard)
      #print('update stat - avg', avg)
      for i in range(len(self.app.leaderboard)-1, -1, -1):
        ##print(el)
        el = self.app.leaderboard[i]
        self.app.tree.insert('', tk.END, values=(el[0], el[1], el[2]))
  self.stack.add_node(team, name, stat, val)
  self.update_name.delete(0, tk.END)
  self.update_val.delete(0, tk.END)

# db - add player function
  # not in use
  async def add_player_db(self):
    player = self.player_entry.get()
    team = self.team_select.get()
    #print('team get:', team)
    # #print(team)
    if not player:
      messagebox.showwarning("Input Error", "Please enter a player name.")
      return
    try:
      conn = sqlite3.connect("baseball_league_gui.db")
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
      print('add new player', new_player)

      self.add_player_team(new_player, team)
      #self.app.add_leaderboard(new_player)
      #print('new player:', new_player)

      c = conn.cursor()
      c.execute("SELECT id FROM teams WHERE name = ?", (team_name,))
      team_id = c.fetchone()

      if team_id:
        #print(f"Found team: {team_id[0]}")
        c.execute("INSERT INTO players (name, number, positions, team_id) VALUES (?, ?, ?, ?)", (player_name, number, positions_json, team_id[0],))
        conn.commit()
        
      else:
        print(f"No id found for team {team}")

    except:
      print('error adding new player')

    finally:
      conn.close()
      print('completed adding new player')
      self.player_entry.delete(0, tk.END)
    await self.load_leaderboard()
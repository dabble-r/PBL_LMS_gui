import tkinter as tk
from tkinter import ttk, messagebox
from helpers import *
from linked_list import *
import sqlite3

# Database Setup
def init_db():
    conn = sqlite3.connect("baseball_league.db")
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
def add_team():
    team_name = team_entry.get()
    if not team_name:
        messagebox.showwarning("Input Error", "Please enter a team name.")
        return
    try:
        conn = sqlite3.connect("baseball_league.db")
        c = conn.cursor()
        c.execute("INSERT INTO teams (name) VALUES (?)", (team_name,))
        conn.commit()
        conn.close()
        team_entry.delete(0, tk.END)
        load_teams()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Team already exists.")

def load_teams():
    team_menu['values'] = []
    conn = sqlite3.connect("baseball_league.db")
    c = conn.cursor()
    c.execute("SELECT name FROM teams")
    teams = [row[0] for row in c.fetchall()]
    conn.close()
    team_menu["values"] = teams

def add_player():
    player_name = player_entry.get()
    team_name = team_menu.get()
    if not player_name or not team_name:
        messagebox.showwarning("Input Error", "Please enter a player name and select a team.")
        return
    conn = sqlite3.connect("baseball_league.db")
    c = conn.cursor()
    c.execute("SELECT id FROM teams WHERE name=?", (team_name,))
    team_id = c.fetchone()
    if team_id:
        c.execute("INSERT INTO players (name, team_id) VALUES (?, ?)", (player_name, team_id[0]))
        conn.commit()
    conn.close()
    player_entry.delete(0, tk.END)
    load_players()

def load_players():
    for item in player_tree.get_children():
        player_tree.delete(item)
    conn = sqlite3.connect("baseball_league.db")
    c = conn.cursor()
    c.execute("SELECT players.id, players.name, teams.name, players.batting_avg FROM players JOIN teams ON players.team_id = teams.id")
    for row in c.fetchall():
        player_tree.insert("", tk.END, values=row)
    conn.close()

def update_stat():
    selected = player_tree.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a player.")
        return
    try:
        stat_value = float(stat_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number.")
        return
    player_id = player_tree.item(selected)['values'][0]
    conn = sqlite3.connect("baseball_league.db")
    c = conn.cursor()
    c.execute("UPDATE players SET batting_avg = ? WHERE id = ?", (stat_value, player_id))
    conn.commit()
    conn.close()
    load_players()

# UI Setup
root = tk.Tk()
root.title("Baseball League Manager")

frame = tk.Frame(root)
frame.pack(pady=10)

# Team Section
tk.Label(frame, text="Team Name:").grid(row=0, column=0)
team_entry = tk.Entry(frame)
team_entry.grid(row=0, column=1)
tk.Button(frame, text="Add Team", command=add_team).grid(row=0, column=2)

# Player Section
tk.Label(frame, text="Player Name:").grid(row=1, column=0)
player_entry = tk.Entry(frame)
player_entry.grid(row=1, column=1)
team_menu = ttk.Combobox(frame, state="readonly")
team_menu.grid(row=1, column=2)
tk.Button(frame, text="Add Player", command=add_player).grid(row=1, column=3)

# Update Player Stats
tk.Label(frame, text="New Batting Avg:").grid(row=2, column=0)
stat_entry = tk.Entry(frame)
stat_entry.grid(row=2, column=1)
tk.Button(frame, text="Update Stat", command=update_stat).grid(row=2, column=2)

# Player Table
player_tree = ttk.Treeview(root, columns=("ID", "Name", "Team", "Batting Avg"), show="headings")
player_tree.heading("ID", text="ID")
player_tree.heading("Name", text="Name")
player_tree.heading("Team", text="Team")
player_tree.heading("Batting Avg", text="Batting Avg")
player_tree.pack()

init_db()
load_teams()
load_players()

root.mainloop()


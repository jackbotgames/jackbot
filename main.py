#!/usr/bin/env python3

from re import A
from sys import argv as cliargs
import json
import discord # discord library
from discord.ext import commands  # discord library extension to make stuff easier
from discord_slash import SlashCommand
from discord_slash.context import SlashContext
from libs import extra
import sqlite3

import games
import fun
import meta

# Load prefix from -p or --prefix argument, else it is "j!"
tokenfilename = ""
for parameter in cliargs:
	if parameter == "-t":
		tokenfilename = cliargs[cliargs.index(parameter) + 1]
	elif parameter.startswith("--tokenfile"):
		x = parameter.split("=")
		tokenfilename = x[1]
tokenfilename = "tokenfile" if tokenfilename == "" else tokenfilename

# read token
with open(tokenfilename,"r") as tokenfile: token = tokenfile.read()

if not extra.file_exists("analytics.json"):
	with open("analytics.json","w") as analyticsfile:
		analytics = {}
		for i in ["rps","connectfour","tictactoe","minesweeper","coinflip"]:
			analytics[i] = 0
		analyticsfile.write(json.dumps(analytics))

with open("analytics.json","r") as analyticsfile:
	analytics = json.loads(analyticsfile.read())
with open("themes.json", "r") as themesfile: themes = json.load(themesfile)
print(f"prefix:/")

client = commands.Bot(command_prefix=" ",activity=discord.Game("starting up..."),intents=discord.Intents.default())
slash = SlashCommand(client,sync_commands=True,debug_guild=None if tokenfilename == "tokenfile" else 775406605906870302)
log_channel = None

client.add_cog(games.Games(client))
client.add_cog(meta.Meta(client))
client.add_cog(fun.Fun(client))

con = sqlite3.connect("users.db")
cur = con.cursor()
try: cur.execute("CREATE TABLE users (id text PRIMARY KEY, money int, username text)")
except sqlite3.OperationalError: pass
con.commit()

# print message when bot turns on and also print every guild that its in
@client.event
async def on_ready():
	print(f"logged in as {client.user}")
	print(f"https://discord.com/oauth2/authorize?client_id={client.user.id}&permissions=0&scope=bot%20applications.commands")
	for guild in client.guilds:
		print(f"In guild: {guild.name}")
	print(f"In {len(client.guilds)} guilds")
	print(f"Debug guild: {slash.debug_guild}")
	global log_channel
	log_channel = client.get_channel(784583344188817428)
	await log_channel.send("waking up")
	await client.change_presence(activity=discord.Game("games"))

# and also print every time it joins a guild
@client.event
async def on_guild_join(guild:discord.Guild):
	print(f"Joined guild: {guild.name}")
	await log_channel.send("joined a guild")

@client.event
async def on_slash_command(ctx:SlashContext):
	bonus = 1
	if ctx.cog.qualified_name == "Games":
		bonus = 3
	user = list(cur.execute("SELECT * FROM users WHERE id = ?",(str(ctx.author_id),)))[0]
	cur.execute("UPDATE users SET money = ? WHERE id = ?",(user[1] + bonus,str(ctx.author_id)))
	cur.execute("UPDATE users SET username = ? WHERE id = ?",(f"{ctx.author}",str(ctx.author_id)))
	con.commit()

client.run(token)

# vim: noet ci pi sts=0 sw=4 ts=4:
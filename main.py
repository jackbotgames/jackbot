#!/usr/bin/env python3

from re import A
from sys import argv as cliargs
import json
import discord # pycord
# from discord_slash import SlashCommand
# from discord_slash.context import SlashContext
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

client = discord.Bot(command_prefix=" ",activity=discord.Game("starting up..."),intents=discord.Intents.default(),debug_guilds=[None if tokenfilename == "tokenfile" else 775406605906870302])
# slash = SlashCommand(client,sync_commands=True,debug_guild=None if tokenfilename == "tokenfile" else 775406605906870302)
log_channel = None

client.add_cog(games.Games(client))
client.add_cog(meta.Meta(client))
client.add_cog(fun.Fun(client))

con = sqlite3.connect("users.db")
cur = con.cursor()
try: con.execute("CREATE TABLE users (id text PRIMARY KEY, money int)")
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
	print(f"Debug guild: {client.debug_guilds}")
	global log_channel
	log_channel = client.get_channel(784583344188817428)
	await log_channel.send("waking up")
	await client.change_presence(activity=discord.Game("games"))

# and also print every time it joins a guild
@client.event
async def on_guild_join(guild:discord.Guild):
	print(f"Joined guild: {guild.name}")
	await log_channel.send(f"joined a guild, **{guild.name}**, with **{guild.member_count}** members\nthis brings us to a total of {1} members in {len(client.guilds)} guilds")

@client.event
async def on_application_command(ctx:discord.ApplicationContext):
	bonus = None
	if ctx.cog.qualified_name == "Games":
		bonus = 3
	if ctx.cog.qualified_name == "Fun":
		bonus = 2
	if bonus is None:
		return
	if len(list(con.execute("SELECT id FROM users WHERE id = ?",(str(ctx.interaction.user.id),)))) == 0:
		con.execute("INSERT INTO users VALUES (?,?)",(str(ctx.interaction.user.id),0))
	user = list(con.execute("SELECT * FROM users WHERE id = ?",(str(ctx.interaction.user.id),)))[0]
	con.execute("UPDATE users SET money = ? WHERE id = ?",(user[1] + bonus,str(ctx.interaction.user.id)))
	con.commit()

client.run(token)

# vim: noet ci pi sts=0 sw=4 ts=4:
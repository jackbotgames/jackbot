#!/usr/bin/env python3

import discord # discord library
from discord.ext import commands # discord library extension to make stuff easier
import random
from libs import minespy,tttpy,c4py,extra # libraries to make minesweeper boards, tic tac toe boards, connect four boards, and other stuff respecively
import re # regex
import json # json
import base64 # for save states
import asyncio # for async stuff and error exceptions
from math import ceil as ceiling # for ceiling
from sys import argv as cliargs

if not extra.file_exists("analytics.json"):
	with open("analytics.json","w") as analyticsfile:
		analytics = {}
		for i in ["rps","connectfour","tictactoe","minesweeper","coinflip"]:
			analytics[i] = 0
		analyticsfile.write(json.dumps(analytics))

with open("analytics.json","r") as analyticsfile:
	analytics = json.loads(analyticsfile.read())

prefix = ""
for parameter in cliargs:
	if parameter == "-p":
		prefix = cliargs[cliargs.index(parameter) + 1]
	elif parameter.startswith("--prefix"):
		x = parameter.split("=")
		prefix = x[1]
prefix = "j!" if prefix == "" else prefix

tokenfilename = ""
for parameter in cliargs:
	if parameter == "-t":
		tokenfilename = cliargs[cliargs.index(parameter) + 1]
	elif parameter.startswith("--tokenfile"):
		x = parameter.split("=")
		tokenfilename = x[1]
tokenfilename = "tokenfile" if tokenfilename == "" else tokenfilename

# read token
with open(tokenfilename,"r") as tokenfile:
	token = tokenfile.read()

print(f"prefix:{prefix}")

# Help command specification
# (declaring everything needed for the help command)
with open("help.json", "r") as helpfile:
	jsonhelp = json.loads(helpfile.read())
help_embed = discord.Embed(title="Help")
help_message_list = []
for category in jsonhelp:
	field_text = ""
	for command in jsonhelp[category]:
		syntax = jsonhelp[category][command]["syntax"]
		usage = jsonhelp[category][command]["usage"]
		field_text += f"**{command}**: {prefix}{command} {' '.join(syntax)}\n*{usage}*\n"
	help_message_list.append(field_text)
	help_embed.add_field(
		name=category, value=help_message_list[len(help_message_list) - 1])

with open("themes.json", "r") as themesfile:
	themes = json.loads(themesfile.read())

client = commands.Bot(command_prefix=prefix,activity=discord.Game("connect 4"))
client.remove_command("help")

repomsg = discord.Embed(title="Repo",description="https://github.com/jackbotgames/jackbot")

log_channel = None
bug_channel = None
suggestion_channel = None

# print message when bot turns on and also print every guild that its in
@client.event
async def on_ready():
	print(f"logged in as {client.user}")
	print(f"https://discord.com/oauth2/authorize?client_id={client.user.id}&permissions=8192&scope=bot")
	for guild in client.guilds:
		print(f"In guild: {guild.name}")
	print(f"In {len(client.guilds)} guilds")
	global log_channel, bug_channel, suggestion_channel
	log_channel = client.get_channel(784583344188817428)
	bug_channel = client.get_channel(775770636353011752)
	suggestion_channel = client.get_channel(775770609191616512)
	await log_channel.send("waking up")

# and also print every time it joins a guild
@client.event
async def on_guild_join(guild):
	print(f"Joined guild: {guild.name}")
	await log_channel.send("joined a guild")

@client.command()
async def minesweeper(ctx, length: int = 6, width: int = 6, mines: int = 7):
	global analytics
	analytics["minesweeper"] += 1
	extra.update_analytics(analytics)
	if length * width > 196:
		await ctx.send(embed=discord.Embed(title="Error",description="Board too large. Try something smaller."))
		return
	if mines >= (length * width):
		mines = (length * width) - 1
	gridstr = minespy.generategrid(length,width,mines)
	while "0" in gridstr or "1" in gridstr or "2" in gridstr or "3" in gridstr or "4" in gridstr or "5" in gridstr or "6" in gridstr or "7" in gridstr or "7" in gridstr or "B" in gridstr: # stole this from stackoverflow
		gridstr = gridstr.replace("0","||:zero:||")
		gridstr = gridstr.replace("1","||:one:||")
		gridstr = gridstr.replace("2","||:two:||")
		gridstr = gridstr.replace("3","||:three:||")
		gridstr = gridstr.replace("4","||:four:||")
		gridstr = gridstr.replace("5","||:five:||")
		gridstr = gridstr.replace("6","||:six:||")
		gridstr = gridstr.replace("7","||:seven:||")
		gridstr = gridstr.replace("8","||:eight:||")
		gridstr = gridstr.replace("B","||:boom:||")
	gridstr = extra.replacenth(gridstr,"||:zero:||",":zero:",random.randint(0,gridstr.count("||:zero:||")))
	embed = discord.Embed(title=f"{length}x{width} with {mines} mines",description=gridstr)
	await ctx.send(embed=embed)

@client.command()
async def rps(ctx,member):
	global analytics
	analytics["rps"] += 1
	extra.update_analytics(analytics)
	otherguy = ctx.message.mentions[0]
	if ctx.author.dm_channel == None:
		await ctx.author.create_dm()
	if otherguy.dm_channel == None:
		await otherguy.create_dm()
	authormsg = await ctx.author.dm_channel.send("Rock, paper, or scissors?")
	otherguymsg = await otherguy.dm_channel.send("Rock, paper, or scissors?")
	for i in u"\U0001f5ff\U0001f4f0\u2702": # rock/paper/scissors
		await authormsg.add_reaction(i)
		await otherguymsg.add_reaction(i)
	def check(reaction,user):
		return (user.id == ctx.author.id or user.id == otherguy.id) and (reaction.message == authormsg or reaction.message == otherguymsg)
	players = []
	winner = None
	while len(players) < 2:
		try:
			reaction,user = await client.wait_for('reaction_add', timeout=60.0, check=check)
		except asyncio.exceptions.TimeoutError:
			await ctx.send("Game closed due to inactivity.")
			return
		stop = False
		for i in players:
			if user in i:
				stop = True
		if stop:
			continue
		players.append([reaction,user])
	if str(players[0][0].emoji) == u"\U0001f5ff" and str(players[1][0].emoji) == u"\U0001f4f0": # rock < paper
		winner = players[1][1].name
	elif str(players[0][0].emoji) == u"\U0001f4f0" and str(players[1][0].emoji) == u"\U0001f5ff": # paper > rock
		winner = players[0][1].name
	elif str(players[0][0].emoji) == u"\u2702" and str(players[1][0].emoji) == u"\U0001f4f0":     # paper < scissors
		winner = players[0][1].name
	elif str(players[0][0].emoji) == u"\U0001f4f0" and str(players[1][0].emoji) == u"\u2702":     # scissors > paper
		winner = players[1][1].name
	elif str(players[0][0].emoji) == u"\u2702" and str(players[1][0].emoji) == u"\U0001f5ff":     # scissors < rock
		winner = players[1][1].name
	elif str(players[0][0].emoji) == u"\U0001f5ff" and str(players[1][0].emoji) == u"\u2702":     # rock > scissors
		winner = players[0][1].name
	else:
		description = f"{players[0][0].emoji}   v   {players[1][0].emoji}\n\nIts a tie!"
	if winner != None:
		description = f"{players[0][0].emoji}   v   {players[1][0].emoji}\n\n{winner} wins!"
	title = f"{players[0][1].name} v {players[1][1].name}"
	game_embed = discord.Embed(title=title,description=description)
	await ctx.send(embed=game_embed)
	await otherguy.dm_channel.send(embed=game_embed)
	await ctx.author.dm_channel.send(embed=game_embed)

valid_t_movements = ['w', 'a', 's', 'd', 'wa', 'wd', 'sa', 'sd', '.', 'q', 'aw', 'dw', 'as', 'sd']

@client.command()
async def tictactoe(ctx,member,save = None):
	global analytics
	analytics["tictactoe"] += 1
	extra.update_analytics(analytics)
	opponent = ctx.message.mentions[0]
	await ctx.send(f"playing tic tac toe with {opponent.display_name if opponent.id != 775408192242974726 else 'an AI'}")
	if save is not None:
		base = base64.b64decode(save.encode()).decode("utf-8").split("|")
		g = base[0]
		moves = int(base[1])
	else:
		g = tttpy.generategrid()
		moves = 1
	gs = g
	gs = gs.replace("X",":regional_indicator_x:")
	gs = gs.replace("O",":zero:")
	for i in gs:
		if str(i) in "123456789":
			gs = gs.replace(i,":blue_square:")
	title = f"Tic Tac Toe: *{ctx.author.display_name}*:regional_indicator_x: vs {opponent.display_name}:zero:" if moves % 2 == 1 else f"Connect 4: {ctx.author.display_name}:regional_indicator_x: vs *{opponent.display_name}*:zero:"
	msgembed = discord.Embed(title=title)
	msgembed.description = gs
	savestate = base64.b64encode(f"{g}|{moves}".encode()).decode("utf-8")
	msgembed.set_footer(text=savestate)
	bmsg = await ctx.send(embed=msgembed)
	def check(message):
		user = message.author
		return ((user == opponent if moves % 2 == 0 else user == ctx.author) and (message.content in valid_t_movements or message.content)) or message.content in ["q","r"]
	while moves <= 9:
		try:
			m = await client.wait_for('message',timeout=60.0,check=check)
		except asyncio.exceptions.TimeoutError:
			await ctx.send("Game closed due to inactivity.")
			return
		c = m.content.lower()
		if c in ["as","ds","aw","dw"]:
			c = c[::-1]
		og = g
		char = "X" if moves % 2 == 1 else "O"
		if c == "q":
			await ctx.send("Game closed.")
			return
		if c == "r":
			title = f"Tic Tac Toe: *{ctx.author.display_name}*:regional_indicator_x: vs {opponent.display_name}:zero:" if moves % 2 == 1 else f"Connect 4: {ctx.author.display_name}:regional_indicator_x: vs *{opponent.display_name}*:zero:"
			msgembed = discord.Embed(title=title)
			msgembed.description = gs
			bmsg = await ctx.send(embed=msgembed)
			savestate = base64.b64encode(f"{g}|{moves}".encode()).decode("utf-8")
			msgembed.set_footer(text=savestate)
			continue
		if c == "wa":
			g = g.replace("1",char)
		elif c == "w":
			g = g.replace("2",char)
		elif c == "wd":
			g = g.replace("3",char)
		elif c == "a":
			g = g.replace("4",char)
		elif c == ".":
			g = g.replace("5",char)
		elif c == "d":
			g = g.replace("6",char)
		elif c == "sa":
			g = g.replace("7",char)
		elif c == "s":
			g = g.replace("8",char)
		elif c == "sd":
			g = g.replace("9",char)
		else:
			continue
		if og != g:
			moves += 1
		try:
			await m.delete()
		except discord.Forbidden:
			pass
		gs = g
		gs = gs.replace("X",":regional_indicator_x:")
		gs = gs.replace("O",":zero:")
		for i in gs:
			if str(i) in "123456789":
				gs = gs.replace(i,":blue_square:")
		title = f"Tic Tac Toe: *{ctx.author.display_name}*:regional_indicator_x: vs {opponent.display_name}:zero:" if moves % 2 == 1 else f"Connect 4: {ctx.author.display_name}:regional_indicator_x: vs *{opponent.display_name}*:zero:"
		msgembed = discord.Embed(title=title)
		msgembed.description = gs
		savestate = base64.b64encode(f"{g}|{moves}".encode()).decode("utf-8")
		msgembed.set_footer(text=savestate)
		await bmsg.edit(embed=msgembed)
		glist = []
		for i in g.split("\n"):
			if i == "":
				continue
			gltmp = []
			for j in i:
				gltmp.append(j)
			glist.append(gltmp)
		if tttpy.checkWin(glist):
			winner = ctx.author.display_name if moves % 2 == 0 else opponent.display_name
			await ctx.send(f"{winner} has won!")
			return
		elif moves > 9:
			await ctx.send("Nobody won, the game is tied.")
			return

valid_c_movements = [ str(i) for i in range(1,8) ]; valid_c_movements.append("q"); valid_c_movements.append("r")
@client.command()
async def connectfour(ctx,member,save = None):
	tiles_list = themes[random.choice(list(themes))]
	global analytics
	analytics["connectfour"] += 1
	extra.update_analytics(analytics)
	opponent = ctx.message.mentions[0]
	await ctx.send(f"playing connect 4 with {opponent.display_name}")
	if save is not None:
		base = base64.b64decode(save.encode()).decode("utf-8").split("|")
		g = json.loads(base[0].replace("'",'"'))
		moves = int(base[1])
	else:
		g = ["       \n", "       \n", "       \n", "       \n", "       \n", "       \n"]
		moves = 1
	gridstr = "".join(g[::-1])
	theme = random.choice(list(themes))
	tiles_list = dict(themes[theme])
	nums_list = "".join(tiles_list["nums"])
	gridstr += nums_list
	tiles_list.pop("nums")
	for tile in tiles_list: gridstr = gridstr.replace(tile,tiles_list[tile])
	title = f"Connect 4: *{ctx.author.display_name}*{tiles_list['X']} vs {opponent.display_name}{tiles_list['O']}" if moves % 2 == 1 else f"Connect 4: {ctx.author.display_name}{tiles_list['X']} vs *{opponent.display_name}*{tiles_list['O']}"
	if len(gridstr) > 2048:
		await ctx.send("The grid is too big!")
		return
	msgembed = discord.Embed(title=title)
	msgembed.description = gridstr
	savestate = base64.b64encode(f"{json.dumps(g)}|{moves}".encode()).decode("utf-8")
	msgembed.set_footer(text=savestate)
	bmsg = await ctx.send(embed=msgembed)
	while moves <= 42:
		def check(message):
			user = message.author
			return ((user == opponent if moves % 2 == 0 else user == ctx.author) and (message.content in valid_t_movements or message.content)) or (message.content in ["q","r"] and (user == opponent or user == ctx.author))
		m = await client.wait_for('message',timeout=None,check=check)
		c = m.content
		if c not in valid_c_movements:
			continue
		if c == "q":
			await ctx.send("game ended")
			return
		elif c == "r":
			title = f"Connect 4: *{ctx.author.display_name}*{tiles_list['X']} vs {opponent.display_name}{tiles_list['O']}" if moves % 2 == 1 else f"Connect 4: {ctx.author.display_name}{tiles_list['X']} vs *{opponent.display_name}*{tiles_list['O']}"
			msgembed = discord.Embed(title=title)
			msgembed.description = gridstr
			savestate = base64.b64encode(f"{json.dumps(g)}|{moves}".encode()).decode("utf-8")
			msgembed.set_footer(text=savestate)
			bmsg = await ctx.send(embed=msgembed)
			continue
		bg = list(g)
		if c in "1234567":
			for y in g:
				# and not (y == g[0] and y[int(c) - 1] in ["X","O"])
				if not y[int(c) - 1] == " ": continue
				t = list(y)
				t[int(c) - 1] = "X" if moves % 2 == 1 else "O"
				g[g.index(y)] = "".join(t)
				break
			moves += 1 if bg != g else 0
		else:
			continue
		gridstr = "".join(g[::-1])
		for tile in tiles_list: gridstr = gridstr.replace(tile,tiles_list[tile])
		gridstr += nums_list
		title = f"Connect 4: *{ctx.author.display_name}*{tiles_list['X']} vs {opponent.display_name}{tiles_list['O']}" if moves % 2 == 1 else f"Connect 4: {ctx.author.display_name}{tiles_list['X']} vs *{opponent.display_name}*{tiles_list['O']}"
		msgembed = discord.Embed(title=title)
		msgembed.description = gridstr
		savestate = base64.b64encode(f"{json.dumps(g)}|{moves}".encode()).decode("utf-8")
		msgembed.set_footer(text=savestate)
		await bmsg.edit(embed=msgembed)
		await m.delete()
		glist = []
		for i in g:
			if i == "\n":
				continue
			gltmp = []
			for j in i:
				gltmp.append(j)
			glist.append(gltmp)
		if c4py.check_win(glist,"X") or c4py.check_win(glist,"O"):
			winner = ctx.author.display_name if moves % 2 == 0 else opponent.display_name
			await ctx.send(f"{winner} has won!")
			return
		elif moves > 42:
			await ctx.send("Nobody won, the game is tied. How did you manage to do that in connect 4?")
			return

@client.command()
async def roll(ctx, number_of_dice: int, number_of_sides: int):
	dice = [
		str(random.choice(range(1, number_of_sides + 1)))
		for _ in range(number_of_dice)
	]
	await ctx.send(', '.join(dice))

@client.command()
async def coinflip(ctx):
	global analytics
	analytics["coinflip"] += 1
	extra.update_analytics(analytics)
	await ctx.send(f"It landed on {'heads' if random.choice([0,1]) == 0 else 'tails'}!")

@client.command()
async def help(ctx,cmd = None):
	if cmd is None:
		await ctx.send(embed=help_embed)
	elif cmd == "tictactoe":
		await ctx.send("controls: ```aw w wd\na  .  d\nas s sd```")
	elif cmd == "connect4":
		await ctx.send(f"controls: {' '.join([ str(i) for i in range(1,8) ])}")

@client.command()
async def repo(ctx):
	await ctx.send(embed=repomsg)

@client.command()
async def invite(ctx):
	await ctx.send("join our support server for support and teasers into new features :)\nhttps://discord.gg/4pUj8vNFXY")

@client.command()
async def bugreport(ctx,*report):
	if ctx.guild.id == bug_channel.guild.id:
		return
	if report == ():
		await ctx.send("Provide a report please.")
		return
	txt = " ".join(report)
	guild = "Jackbot's DMs" if ctx.guild is None else ctx.guild.name
	await bug_channel.send(f"**{ctx.author.display_name}** from **{guild}**:\n{txt}",files=await extra.attachments_to_files(ctx.message.attachments))
	await log_channel.send("received a bug report")
	await ctx.message.add_reaction(b'\xe2\x9c\x85'.decode("utf-8"))

@client.command()
async def suggestion(ctx,*report):
	if ctx.guild.id == suggestion_channel.guild.id:
		return
	if report == ():
		await ctx.send("Provide a suggestion please.")
		return
	txt = " ".join(report)
	guild = "Jackbot's DMs" if ctx.guild is None else ctx.guild.name
	await suggestion_channel.send(f"**{ctx.author.display_name}** from **{guild}**:\n{txt}",files=await extra.attachments_to_files(ctx.message.attachments))
	await log_channel.send("received a suggestion")
	await ctx.message.add_reaction(b'\xe2\x9c\x85'.decode("utf-8"))

# aliases

@client.command()
async def ms(ctx, length: int = 6, width: int = 6, mines = 7):
	await minesweeper(ctx,length,width,mines)

@client.command()
async def ttt(ctx,member,save = None):
	await tictactoe(ctx,member,save)

@client.command()
async def c4(ctx,member,save = None):
	await connectfour(ctx,member,save)

client.run(token)

# vim: noet ci pi sts=0 sw=4 ts=4:
#!/usr/bin/env python3

import discord
from discord.ext import commands
import random
import minespy

# read token
with open("tokenfile","r") as tokenfile:
	token = tokenfile.read()

client = commands.Bot(command_prefix="m!")
client.remove_command("help")

helpmsg = discord.Embed(title="Help",description="m!minesweeper: create minefield\nm!ms: alias for minesweeper\nm!roll: roll dice")
nums = [":zero:",":one:",":two:",":three:",":four:",":five:",":six:",":seven:",":eight:"]
# print message when bot turns on and also print every guild that its in
@client.event
async def on_ready(): 
	print(f"logged in as {client.user}")
	print(f"https://discord.com/oauth2/authorize?client_id={client.user.id}&permissions=0&scope=bot")
	for guild in client.guilds:
		print(f"In guild: {guild.name}") 
# and also print every time it joins a guild
@client.event
async def on_guild_join(guild):
	print(f"Joined guild: {guild.name}")

@client.command() 
async def minesweeper(ctx, length: int = 6, width: int = 6, mines = 7):
	#if str(mines).endswith("%"):
	#	mines = (float(mines[:-1]) * 0.01) * (length * width)
	mines = int(mines)
	if mines >= (length * width):
		mines = (length * width) - 1
	#await ctx.send(f"generating minefield of {length} length, {width} width, and with {mines} mines")
	bombs = minespy.generatebombs(length,width,mines)
	x = [ (i + 1) for i in range(width)  ]
	y = [ (i + 1) for i in range(length) ]
	grid = [ [ 0 for i in range(length) ] for i in range(width) ]
	for i in x:
		for j in y:
			if [i,j] in bombs:
				grid[i - 1][j - 1] = "B"
	for bomb in bombs:
		try:
			grid[bomb[0] - 2][bomb[1] - 2] += 1 if bomb[0] - 2 > -1 and bomb[1] - 2 > -1 else 0
		except:
			None
		try:
			grid[bomb[0] - 0][bomb[1] - 2] += 1 if bomb[0] - 1 > -1 and bomb[1] - 2 > -1 else 0
		except:
			None
		try:
			grid[bomb[0] - 2][bomb[1] - 0] += 1 if bomb[0] - 2 > -1 and bomb[1] - 0 > -1 else 0
		except:
			None
		try:
			grid[bomb[0] - 0][bomb[1] - 0] += 1 if bomb[0] - 0 > -1 and bomb[1] - 0 > -1 else 0
		except:
			None
		try:
			grid[bomb[0] - 1][bomb[1] - 0] += 1 if bomb[0] - 1 > -1 and bomb[1] - 0 > -1 else 0
		except:
			None
		try:
			grid[bomb[0] - 0][bomb[1] - 1] += 1 if bomb[0] - 0 > -1 and bomb[1] - 1 > -1 else 0
		except:
			None
		try:
			grid[bomb[0] - 2][bomb[1] - 1] += 1 if bomb[0] - 2 > -1 and bomb[1] - 1 > -1 else 0
		except:
			None
		try:
			grid[bomb[0] - 1][bomb[1] - 2] += 1 if bomb[0] - 1 > -1 and bomb[1] - 2 > -1 else 0
		except:
			None
	gridstr = ""
	for i in grid:
		for j in i:
			gridstr += f"{j}"
		gridstr += "\n"
	gridstr_new = gridstr
	while "0" in gridstr_new or "1" in gridstr_new or "2" in gridstr_new or "3" in gridstr_new or "4" in gridstr_new or "5" in gridstr_new or "6" in gridstr_new or "7" in gridstr_new or "7" in gridstr_new or "B" in gridstr_new: # stole this from stackoverflow
		gridstr_new = gridstr_new.replace("0","||:zero:||")
		gridstr_new = gridstr_new.replace("1","||:one:||")
		gridstr_new = gridstr_new.replace("2","||:two:||")
		gridstr_new = gridstr_new.replace("3","||:three:||")
		gridstr_new = gridstr_new.replace("4","||:four:||")
		gridstr_new = gridstr_new.replace("5","||:five:||")
		gridstr_new = gridstr_new.replace("6","||:six:||")
		gridstr_new = gridstr_new.replace("7","||:seven:||")
		gridstr_new = gridstr_new.replace("8","||:eight:||")
		gridstr_new = gridstr_new.replace("B","||:boom:||")
	gridstr_new = gridstr_new.replace("||:zero:||",":zero:",1)
	embed = discord.Embed(title=f"{length}x{width} with {mines} mines",description=gridstr_new)
	await ctx.send(embed=embed)

@client.command() 
async def ms(ctx, length: int = 6, width: int = 6, mines = 7):
	await minesweeper(ctx,length,width,mines)
@client.command()
async def roll(ctx, number_of_dice: int, number_of_sides: int):
	dice = [
		str(random.choice(range(1, number_of_sides + 1)))
		for _ in range(number_of_dice)
	]
	await ctx.send(', '.join(dice))

@client.command()
async def help(ctx):
	await ctx.send(embed=helpmsg)

client.run(token)

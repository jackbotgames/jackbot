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

helpmsg = discord.Embed(title="Help",description="m!minesweeper: create minefield\nm!roll: roll dice")

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
async def minesweeper(ctx, length: int = 10, width: int = 10, mines = 10):
	#if str(mines).endswith("%"):
	#	mines = (float(mines[:-1]) * 0.01) * (length * width)
	mines = int(mines)
	if mines >= (length * width):
		mines = (length * width) - 1
	await ctx.send(f"generating minefield of {length} length, {width} width, and with {mines} mines")
	bombs = minespy.generatebombs(length,width,mines)
	x = [ (i + 1) for i in range(width)  ]
	y = [ (i + 1) for i in range(length) ]
	grid = [ [ "0" for i in range(length) ] for i in range(width) ]
	for i in x:
		for j in y:
			if [i,j] in bombs:
				grid[i - 1][j - 1] = "B"
	gridstr = ""
	for i in grid:
		for j in i:
			gridstr += j
		gridstr += "\n"

	gridstr_new = gridstr.replace("B",":boom:").replace("0",":zero:")
	while "B" in gridstr_new:
		gridstr_new = gridstr_new.replace("0",":zero:")
		gridstr_new = gridstr_new.replace("B",":bomb:")
	await ctx.send(f"{gridstr_new}")

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

#!/usr/bin/env python3

import discord
from discord.ext import commands
import random
import minespy
import re

def replacenth(string, sub, wanted, n):
	where = [m.start() for m in re.finditer(sub, string)][n-1]
	before = string[:where]
	after = string[where:]
	after = after.replace(sub, wanted, 1)
	new_string = before + after
	return new_string

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
async def minesweeper(ctx, length: int = 6, width: int = 6, mines: int = 7):
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
	gridstr = replacenth(gridstr,"||:zero:||",":zero:",random.randint(0,gridstr.count("||:zero:||")))
	embed = discord.Embed(title=f"{length}x{width} with {mines} mines",description=gridstr)
	await ctx.send(embed=embed)

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

# aliases

@client.command() 
async def ms(ctx, length: int = 6, width: int = 6, mines = 7):
	await minesweeper(ctx,length,width,mines)

@client.command() 
async def Ms(ctx, length: int = 6, width: int = 6, mines = 7):
	await minesweeper(ctx,length,width,mines)

@client.command() 
async def Minesweeper(ctx, length: int = 6, width: int = 6, mines = 7):
	await minesweeper(ctx,length,width,mines)

client.run(token)

#!/usr/bin/env python3

from datetime import datetime
from os import terminal_size
from sys import argv as cliargs
import json
import discord # discord library
from discord.ext import commands  # discord library extension to make stuff easier
from discord_slash import SlashCommand, SlashContext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option # slash commands
import random
from libs import *

import games
# import fun
# import meta
import traceback
import sys

# Load prefix from -p or --prefix argument, else it is "j!"
prefix = ""
tokenfilename = ""
for parameter in cliargs:
	if parameter == "-p":
		prefix = cliargs[cliargs.index(parameter) + 1]
	elif parameter.startswith("--prefix"):
		x = parameter.split("=")
		prefix = x[1]
	elif parameter == "-t":
		tokenfilename = cliargs[cliargs.index(parameter) + 1]
	elif parameter.startswith("--tokenfile"):
		x = parameter.split("=")
		tokenfilename = x[1]
prefix = "j!" if prefix == "" else prefix
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
print(f"prefix:{prefix}")

client = commands.Bot(command_prefix=prefix,activity=discord.Game("starting up..."),help_command=extra.MyHelpCommand(),intents=discord.Intents.default())
slash = SlashCommand(client,sync_commands=True,debug_guild=775406605906870302)
log_channel = None
bug_channel = None
suggestion_channel = None

repomsg = discord.Embed(title="Repo",description="https://github.com/jackbotgames/jackbot")
# print message when bot turns on and also print every guild that its in
@client.event
async def on_ready():
	print(f"logged in as {client.user}")
	print(f"https://discord.com/oauth2/authorize?client_id={client.user.id}&permissions=8192&scope=bot%20applications.commands")
	for guild in client.guilds:
		print(f"In guild: {guild.name}")
	print(f"In {len(client.guilds)} guilds")
	global log_channel, bug_channel, suggestion_channel, t0
	log_channel = client.get_channel(784583344188817428)
	bug_channel = client.get_channel(775770636353011752)
	suggestion_channel = client.get_channel(775770609191616512)
	await log_channel.send("waking up")
	await client.change_presence(activity=discord.Game("games"))
	client.add_cog(games.Games(client))
	# client.add_cog(meta.Meta(client))
	t0 = datetime.now()

# and also print every time it joins a guild
@client.event
async def on_guild_join(guild:discord.Guild):
	print(f"Joined guild: {guild.name}")
	await log_channel.send("joined a guild")

@client.event
async def on_command_completion(ctx:commands.Context):
	if ctx.cog == games.Games:
		await client.change_presence(activity=discord.Game(ctx.command.name))

@client.event
async def on_command_error(ctx:commands.Context, exception):
	embed = discord.Embed(color=discord.Color.red())
	if type(exception) is commands.errors.MissingRequiredArgument:
		embed.title = "You forgot an argument"
		embed.description = f"The syntax to `{client.command_prefix}{ctx.invoked_with}` is `{client.command_prefix}{ctx.invoked_with} {ctx.command.signature}`."
		await ctx.send(embed=embed)
	elif type(exception) is commands.CommandNotFound:
		embed.title = "Invalid command"
		embed.description = f"The command you just tried to use is invalid. Use `{client.command_prefix}help` to see all commands."
		await ctx.send(embed=embed)
	elif type(exception) is commands.errors.CommandInvokeError:
		embed.title = "Invalid permissions"
		embed.description = "Somebody tried to use me in a channel where I can't talk."
		for channel in ctx.guild.channels:
			try:
				await channel.send(embed=embed)
				break
			except: pass
	else:
		print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
		traceback.print_exception(type(exception), exception, exception.__traceback__, file=sys.stderr)

@slash.slash(name='minesweeper',description="generate minesweeper board")
async def minesweeper(ctx:SlashContext, length: int = 6, width: int = 6, mines: int = 7):
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

@slash.slash(description="show repo",name='repo')
async def repo(ctx:SlashContext):
	await ctx.send(embed=repomsg,hidden=True)

@slash.slash(description="give link to support server",name='invite')
async def invite(ctx:SlashContext):
	await ctx.send("join our support server for support and teasers into new features :)\nhttps://discord.gg/4pUj8vNFXY",hidden=True)

@slash.slash(description="send bug report to bugs channel in support discord",name='bugreport',options=[create_option(name='report',description='the bug',option_type=SlashCommandOptionType.STRING,required=True)])
async def bugreport(ctx:SlashContext,report):
	guild = "Unknown" if ctx.guild is None else ctx.guild.name
	await bug_channel.send(f"**{ctx.author.display_name}** from **{guild}**:\n{report}")
	await log_channel.send("received a bug report")
	await ctx.send("Report received!",hidden=True)

@slash.slash(description="send suggestion to feature requests channel in support discord",name='suggestion',options=[create_option(name='suggestion',description='the suggestion',option_type=SlashCommandOptionType.STRING,required=True)])
async def suggestion(ctx:SlashContext,suggestion):
	guild = "Unknown" if ctx.guild is None else ctx.guild.name
	await suggestion_channel.send(f"**{ctx.author.display_name}** from **{guild}**:\n{suggestion}")
	await log_channel.send("received a suggestion")
	await ctx.send("Suggestion received!",hidden=True)


@slash.slash(description="show statistics, including usage and amount of servers",name='stats')
async def stats(ctx:SlashContext):
	with open("analytics.json","r") as analyticsfile: analytics = json.loads(analyticsfile.read())
	embed = discord.Embed(title="Analytics")
	embed.add_field(name="Servers",value=f"{client.user.name} is in {len(client.guilds)} servers.")
	str_usage_stats = ""
	for cmd in analytics:
		str_usage_stats += f"{cmd}: {analytics[cmd]}\n"
	embed.add_field(name="Usage stats",value=str_usage_stats)
	embed.add_field(name="Uptime",value=str(datetime.now() - t0).split(".")[0])
	await ctx.send(embed=embed,hidden=True)

@slash.slash(description="show latency",name='ping')
async def ping(ctx:SlashContext):
	await ctx.send(f"Pong! {int(client.latency * 1000)}ms",hidden=True)

@slash.slash(description="roll a dice")
async def roll(ctx:SlashContext, number_of_dice: int, number_of_sides: int,hidden: bool = False):
	dice = [
		str(random.choice(range(1, number_of_sides + 1)))
		for _ in range(number_of_dice)
	]
	await ctx.send(", ".join(dice))

@slash.slash(description="flip a coin")
async def coinflip(ctx:SlashContext,hidden:bool = False):
	await ctx.send(f"It landed on {'heads' if random.choice([0,1]) == 0 else 'tails'}!",hidden=hidden)

@slash.slash(description="show jack")
async def jack(ctx:SlashContext,hidden:bool = False):
	await ctx.send("<:jack1:784513836375212052><:jack2:784513836408504360><:jack3:784513836321079326>\n<:jack4:784513836442189884><:jack5:784513836626477056><:jack6:784513836832522291>\n<:jack7:784513836660031518><:jack8:784513836865814588><:jack9:784513836434325535>",hidden=hidden)

client.run(token)

# vim: noet ci pi sts=0 sw=4 ts=4:
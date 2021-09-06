#!/usr/bin/env python3

from sys import argv as cliargs
import json
import discord # discord library
from discord.ext import commands  # discord library extension to make stuff easier
from discord_slash import SlashCommand
from libs import extra
import traceback
import sys

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

client = commands.Bot(command_prefix="/",activity=discord.Game("starting up..."),intents=discord.Intents.default())
slash = SlashCommand(client,sync_commands=True)
log_channel = None

client.add_cog(games.Games(client))
client.add_cog(meta.Meta(client))
client.add_cog(fun.Fun(client))

# print message when bot turns on and also print every guild that its in
@client.event
async def on_ready():
	print(f"logged in as {client.user}")
	print(f"https://discord.com/oauth2/authorize?client_id={client.user.id}&permissions=0&scope=bot%20applications.commands")
	for guild in client.guilds:
		print(f"In guild: {guild.name}")
	print(f"In {len(client.guilds)} guilds")
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

client.run(token)

# vim: noet ci pi sts=0 sw=4 ts=4:
#!/usr/bin/env python3

import json  # json
from datetime import datetime
from sys import argv as cliargs
import importlib

import discord
from discord.errors import GatewayNotFound  # discord library
from discord.ext import commands  # discord library extension to make stuff easier

from libs import extra

import games
import fun
import meta
import traceback
import sys

# Load prefix from -p or --prefix argument, else it is "j!"
prefix = ""
for parameter in cliargs:
	if parameter == "-p":
		prefix = cliargs[cliargs.index(parameter) + 1]
	elif parameter.startswith("--prefix"):
		x = parameter.split("=")
		prefix = x[1]
prefix = "j!" if prefix == "" else prefix

# Get the tokenfile name from -t or --tokenfile, else it is "tokenfile"
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

client = commands.Bot(command_prefix=prefix,activity=discord.Game("starting up..."),help_command=extra.MyHelpCommand())
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
	global log_channel, bug_channel, suggestion_channel, t0
	log_channel = client.get_channel(784583344188817428)
	bug_channel = client.get_channel(775770636353011752)
	suggestion_channel = client.get_channel(775770609191616512)
	await log_channel.send("waking up")
	await client.change_presence(activity=discord.Game("games"))
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
	elif type(exception) == commands.errors.NotOwner:
		app_info = await client.application_info()
		embed.title = "You do not have access to this command."
		embed.description = f"You must be the owner of this discord bot ({app_info.owner.name})."
		await ctx.send(embed=embed)
	else:
		print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
		traceback.print_exception(type(exception), exception, exception.__traceback__, file=sys.stderr)

@client.command(brief="Reloads all commands. Exclusive to owner of bot.")
@commands.is_owner()
async def reload(ctx,cog_to_reload = None):
	print(f"reloading {cog_to_reload if cog_to_reload in ['Games','Fun','Meta'] else ''}")
	if cog_to_reload in ["Games","Fun","Meta"]:
		if cog_to_reload == "Games":
			client.remove_cog("Games")
			importlib.reload(games)
			client.add_cog(games.Games(client))
		if cog_to_reload == "Fun":
			client.remove_cog("Fun")
			importlib.reload(fun)
			client.add_cog(games.Fun(client))
		if cog_to_reload == "Meta":
			client.remove_cog("Meta")
			importlib.reload(meta)
			client.add_cog(games.Meta(client))
	else:
		client.remove_cog("Games")
		client.remove_cog("Fun")
		client.remove_cog("Meta")
		importlib.reload(games)
		importlib.reload(fun)
		importlib.reload(meta)
		client.add_cog(games.Games(client))
		client.add_cog(fun.Fun(client))
		client.add_cog(meta.Meta(client))
	await ctx.send("Reload complete!")

client.add_cog(games.Games(client))
client.add_cog(fun.Fun(client))
client.add_cog(meta.Meta(client))
client.run(token)

# vim: noet ci pi sts=0 sw=4 ts=4:
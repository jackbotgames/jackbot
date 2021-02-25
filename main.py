#!/usr/bin/env python3

import asyncio  # for async stuff and error exceptions
import base64  # for save states
import json  # json
import random
import re  # regex
from datetime import datetime
from math import ceil as ceiling  # for ceiling
from sys import argv as cliargs

import discord  # discord library
from discord.ext import commands  # discord library extension to make stuff easier

from libs import (  # libraries to make minesweeper boards, tic tac toe boards, connect four boards, and other stuff respecively
	c4py, extra, minespy, tttpy
)

from games import Games
from fun import Fun


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
	global log_channel, bug_channel, suggestion_channel, t0
	log_channel = client.get_channel(784583344188817428)
	bug_channel = client.get_channel(775770636353011752)
	suggestion_channel = client.get_channel(775770609191616512)
	await log_channel.send("waking up")
	await client.change_presence(activity=discord.Game("games"))
	t0 = datetime.now()

# and also print every time it joins a guild
@client.event
async def on_guild_join(guild):
	print(f"Joined guild: {guild.name}")
	await log_channel.send("joined a guild")

class Meta(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None

	@commands.command(brief="show repo")
	async def repo(self, ctx):
		await ctx.send(embed=repomsg)

	@commands.command(brief="give link to support server")
	async def invite(self, ctx):
		await ctx.send("join our support server for support and teasers into new features :)\nhttps://discord.gg/4pUj8vNFXY")

	@commands.command(brief="send bug report to bugs channel in support discord")
	async def bugreport(self, ctx,*report):
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

	@commands.command(brief="send suggestion to feature requests channel in support discord")
	async def suggestion(self, ctx,*report):
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


	@commands.command(brief="show statistics, including usage and amount of servers")
	async def stats(self, ctx):
		with open("analytics.json","r") as analyticsfile: analytics = json.loads(analyticsfile.read())
		embed = discord.Embed(title="Analytics")
		embed.add_field(name="Servers",value=f"{client.user.name} is in {len(client.guilds)} servers.")
		str_usage_stats = ""
		for cmd in analytics:
			str_usage_stats += f"{cmd}: {analytics[cmd]}\n"
		embed.add_field(name="Usage stats",value=str_usage_stats)
		embed.add_field(name="Uptime",value=str(datetime.now() - t0).split(".")[0])
		await ctx.send(embed=embed)

	@commands.command(brief="show latency")
	async def ping(ctx): await ctx.send(f"Pong! {int(client.latency * 1000)}ms")

client.add_cog(Games(client))
client.add_cog(Fun(client))
client.add_cog(Meta(client))
client.run(token)

# vim: noet ci pi sts=0 sw=4 ts=4:
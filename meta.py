import discord
from discord.ext import commands
from discord_slash import cog_ext
import json
from datetime import datetime
from libs import extra

repomsg = discord.Embed(title="Repo",description="https://github.com/jackbotgames/jackbot")
guild_ids=[775406605906870302]

class Meta(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None
		self.log_channel = self.bot.get_channel(784583344188817428)
		self.bug_channel = self.bot.get_channel(775770636353011752)
		self.suggestion_channel = self.bot.get_channel(775770609191616512)
		self.t0 = datetime.now()

	@cog_ext.cog_slash(description="show repo",name='repo')
	async def repo(self, ctx:commands.Context):
		await ctx.send(embed=repomsg)

	@cog_ext.cog_slash(description="give link to support server",name='invite')
	async def invite(self, ctx:commands.Context):
		await ctx.send("join our support server for support and teasers into new features :)\nhttps://discord.gg/4pUj8vNFXY")

	@cog_ext.cog_slash(description="send bug report to bugs channel in support discord",name='bugreport')
	async def bugreport(self, ctx:commands.Context,*report):
		if ctx.guild.id == self.bug_channel.guild.id:
			return
		if report == ():
			await ctx.send("Provide a report please.")
			return
		txt = " ".join(report)
		guild = "Jackbot's DMs" if ctx.guild is None else ctx.guild.name
		await self.bug_channel.send(f"**{ctx.author.display_name}** from **{guild}**:\n{txt}",files=await extra.attachments_to_files(ctx.message.attachments))
		await self.log_channel.send("received a bug report")
		await ctx.message.add_reaction(b'\xe2\x9c\x85'.decode("utf-8"))

	@cog_ext.cog_slash(description="send suggestion to feature requests channel in support discord",name='suggestion')
	async def suggestion(self, ctx:commands.Context,*report):
		if ctx.guild.id == self.suggestion_channel.guild.id:
			return
		if report == ():
			await ctx.send("Provide a suggestion please.")
			return
		txt = " ".join(report)
		guild = "Jackbot's DMs" if ctx.guild is None else ctx.guild.name
		await self.suggestion_channel.send(f"**{ctx.author.display_name}** from **{guild}**:\n{txt}",files=await extra.attachments_to_files(ctx.message.attachments))
		await self.log_channel.send("received a suggestion")
		await ctx.message.add_reaction(b'\xe2\x9c\x85'.decode("utf-8"))


	@cog_ext.cog_slash(description="show statistics, including usage and amount of servers",name='stats')
	async def stats(self, ctx:commands.Context):
		with open("analytics.json","r") as analyticsfile: analytics = json.loads(analyticsfile.read())
		embed = discord.Embed(title="Analytics")
		embed.add_field(name="Servers",value=f"{self.bot.user.name} is in {len(self.bot.guilds)} servers.")
		str_usage_stats = ""
		for cmd in analytics:
			str_usage_stats += f"{cmd}: {analytics[cmd]}\n"
		embed.add_field(name="Usage stats",value=str_usage_stats)
		embed.add_field(name="Uptime",value=str(datetime.now() - self.t0).split(".")[0])
		await ctx.send(embed=embed)

	@cog_ext.cog_slash(description="show latency")
	async def ping(self,ctx:commands.Context):
		await ctx.send(f"Pong! {int(self.bot.latency * 1000)}ms")

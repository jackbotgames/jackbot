import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import json
from datetime import datetime

repomsg = discord.Embed(title="Repo",description="https://github.com/jackbotgames/jackbot")
guild_ids=[775406605906870302]

class Meta(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None
		self.t0 = datetime.now()
	
	@property
	def bug_channel(self): return self.bot.get_channel(775770636353011752)
	
	@property
	def log_channel(self): return self.bot.get_channel(784583344188817428)
	
	@property
	def suggestion_channel(self): return self.bot.get_channel(775770609191616512)
	
	@cog_ext.cog_slash(description="show repo",name='repo')
	async def repo(self,ctx:SlashContext):
		await ctx.send(embed=repomsg,hidden=True)

	@cog_ext.cog_slash(description="give link to support server",name='invite')
	async def invite(self,ctx:SlashContext):
		await ctx.send("join our support server for support and teasers into new features :)\nhttps://discord.gg/4pUj8vNFXY",hidden=True)

	@cog_ext.cog_slash(description="send bug report to bugs channel in support discord",name='bugreport')
	async def bugreport(self,ctx:SlashContext,report:str):
		guild = "Unknown" if ctx.guild is None else ctx.guild.name
		await self.bug_channel.send(f"**{ctx.author.display_name}** from **{guild}**:\n{report}")
		await self.log_channel.send("received a bug report")
		await ctx.send("Report received!",hidden=True)

	@cog_ext.cog_slash(description="send suggestion to feature requests channel in support discord",name='suggestion')
	async def suggestion(self,ctx:SlashContext,suggestion):
		guild = "Unknown" if ctx.guild is None else ctx.guild.name
		await self.suggestion_channel.send(f"**{ctx.author.display_name}** from **{guild}**:\n{suggestion}")
		await self.log_channel.send("received a suggestion")
		await ctx.send("Suggestion received!",hidden=True)

	@cog_ext.cog_slash(description="show statistics, including usage and amount of servers",name='stats')
	async def stats(self,ctx:SlashContext):
		with open("analytics.json","r") as analyticsfile: analytics = json.load(analyticsfile)
		embed = discord.Embed(title="Analytics")
		embed.add_field(name="Servers",value=f"{self.bot.user.name} is in {len(self.bot.guilds)} servers.")
		str_usage_stats = ""
		for cmd in analytics:
			str_usage_stats += f"{cmd}: {analytics[cmd]}\n"
		embed.add_field(name="Usage stats",value=str_usage_stats)
		embed.add_field(name="Uptime",value=str(datetime.now() - self.t0).split(".")[0])
		await ctx.send(embed=embed,hidden=True)

	@cog_ext.cog_slash(description="show latency",name='ping')
	async def ping(self,ctx:SlashContext):
		await ctx.send(f"Pong! {int(self.bot.latency * 1000)}ms",hidden=True)
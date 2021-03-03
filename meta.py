import discord
from discord.ext import commands
import json
from datetime import datetime
from libs import extra

repomsg = discord.Embed(title="Repo",description="https://github.com/jackbotgames/jackbot")


class Meta(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None
		self.log_channel = self.bot.get_channel(784583344188817428)
		self.bug_channel = self.bot.get_channel(775770636353011752)
		self.suggestion_channel = self.bot.get_channel(775770609191616512)
		self.t0 = datetime.now()

	@commands.command(brief="show repo")
	async def repo(self, ctx:commands.Context):
		await ctx.send(embed=repomsg)

	@commands.command(brief="give link to support server")
	async def invite(self, ctx:commands.Context):
		await ctx.send("join our support server for support and teasers into new features :)\nhttps://discord.gg/4pUj8vNFXY")

	@commands.command(brief="send bug report to bugs channel in support discord")
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

	@commands.command(brief="send suggestion to feature requests channel in support discord")
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


	@commands.command(brief="show statistics, including usage and amount of servers")
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

	@commands.command(brief="show latency")
	async def ping(self,ctx:commands.Context):
		await ctx.send(f"Pong! {int(self.bot.latency * 1000)}ms")

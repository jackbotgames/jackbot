from collections import OrderedDict
import discord
# from discord_slash import cog_ext, discord.ApplicationContext
import json
from datetime import datetime
import sqlite3

repomsg = discord.Embed(title="Repo",description="https://github.com/jackbotgames/jackbot")
guild_ids=[775406605906870302]

class Meta(discord.Cog):
	def __init__(self, bot:discord.Bot):
		self.bot = bot
		self._last_member = None
		self.t0 = datetime.now()
	
	@property
	def bug_channel(self): return self.bot.get_channel(775770636353011752)
	
	@property
	def log_channel(self): return self.bot.get_channel(784583344188817428)
	
	@property
	def suggestion_channel(self): return self.bot.get_channel(775770609191616512)
	
	@discord.command(description="show repo",name='repo')
	async def repo(self,ctx:discord.ApplicationContext):
		await ctx.respond(embed=repomsg,ephemeral=True)

	@discord.command(description="give link to support server",name='invite')
	async def invite(self,ctx:discord.ApplicationContext):
		await ctx.respond(f"join our support server for support and teasers into new features :)\nhttps://discord.gg/4pUj8vNFXY\nalso invite jackbot https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&permissions=0&scope=bot%20applications.commands",ephemeral=True)

	@discord.command(description="send bug report to bugs channel in support discord",name='bugreport')
	async def bugreport(self,ctx:discord.ApplicationContext,report:str):
		guild = "Unknown" if ctx.guild is None else ctx.guild.name
		await self.bug_channel.send(f"**{ctx.author.display_name}** from **{guild}**:\n{report}")
		await self.log_channel.send("received a bug report")
		await ctx.respond("Report received!",ephemeral=True)

	@discord.command(description="send suggestion to feature requests channel in support discord",name='suggestion')
	async def suggestion(self,ctx:discord.ApplicationContext,suggestion):
		guild = "Unknown" if ctx.guild is None else ctx.guild.name
		await self.suggestion_channel.send(f"**{ctx.author.display_name}** from **{guild}**:\n{suggestion}")
		await self.log_channel.send("received a suggestion")
		await ctx.respond("Suggestion received!",ephemeral=True)

	@discord.command(description="show statistics, including usage and amount of servers",name='stats')
	async def stats(self,ctx:discord.ApplicationContext):
		with open("analytics.json","r") as analyticsfile: analytics = json.load(analyticsfile)
		embed = discord.Embed(title="Analytics")
		embed.add_field(name="Servers",value=f"{self.bot.user.name} is in {len(self.bot.guilds)} servers.")
		str_usage_stats = ""
		for cmd in analytics:
			str_usage_stats += f"{cmd}: {analytics[cmd]}\n"
		embed.add_field(name="Usage stats",value=str_usage_stats)
		embed.add_field(name="Uptime",value=str(datetime.now() - self.t0).split(".")[0])
		await ctx.respond(embed=embed,ephemeral=True)

	@discord.command(description="show latency",name='ping')
	async def ping(self,ctx:discord.ApplicationContext):
		await ctx.respond(f"Pong! {int(self.bot.latency * 1000)}ms",ephemeral=True)
	
	@discord.command(name='shmeckles',description='Get the amount of shmeckles of a user')
	async def shmeckles(self,ctx:discord.ApplicationContext,member:discord.Member = None):
		if member is None:
			member = ctx.author
		con = sqlite3.connect("users.db")
		cur = con.cursor()
		con.commit()
		money = None
		for user in cur.execute("SELECT * FROM users"):
			if user[0] == str(member.id):
				money = user[1]
		await ctx.respond(f"{member.mention} has <a:goldcoin:801148801653276693>{money}.",ephemeral=True)

	@discord.command(name='give',description='Gives someone an amount of money')
	async def give(self,ctx:discord.ApplicationContext,member:discord.Member,amount:int):
		if member == ctx.author:
			await ctx.respond("You cannot give yourself money!",ephemeral=True)
			return
		if abs(amount) != amount:
			await ctx.respond("You cannot give someone negative money!",ephemeral=True)
			return
		con = sqlite3.connect("users.db")
		giver_money = list(con.execute("SELECT money FROM users WHERE id = ?",(ctx.author.id,)))[0][0]
		if giver_money < amount:
			await ctx.respond("You cannot give someone money you don't have!",ephemeral=True)
			return
		taker_money = list(con.execute("SELECT money FROM users WHERE id = ?",(member.id,)))[0][0]
		con.execute("UPDATE users SET money = ? WHERE id = ?",(giver_money - amount,ctx.author.id))
		con.execute("UPDATE users SET money = ? WHERE id = ?",(taker_money + amount,member.id))
		con.commit()
		await ctx.respond(f"Transferred <a:goldcoin:801148801653276693>{amount} to {member.display_name}!",ephemeral=True)
	@discord.command(name='leaderboard',description='checks the shmeckle leaderboard')
	async def leaderboard(self,ctx:discord.ApplicationContext):
		con = sqlite3.connect("users.db")
		users = dict()
		for entry in con.execute("SELECT * FROM users"):
			users[int(entry[0])] = int(entry[1])
		users = list(users.items())
		users.sort(key=lambda x: x[1],reverse=True)
		msg = ""
		for user in users[:10]:
			msg += f"<@{user[0]}> - <a:goldcoin:801148801653276693>{user[1]}\n"
		embed = discord.Embed(title="Shmeckle Leaderboard",description=msg)
		await ctx.respond(embeds=[embed],ephemeral=True)


if __name__ == "__main__":
	import main
from discord.ext import commands
from discord_slash import SlashContext, cog_ext

import random

class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None

	@cog_ext.cog_slash(name="roll",description="roll a dice")
	async def roll(self,ctx:SlashContext, number_of_dice: int, number_of_sides: int,hidden: bool = False):
		dice = [
			str(random.choice(range(1, number_of_sides + 1)))
			for _ in range(number_of_dice)
		]
		await ctx.send(", ".join(dice),hidden=hidden)

	@cog_ext.cog_slash(name="coinflip",description="flip a coin")
	async def coinflip(self,ctx:SlashContext,hidden:bool = False):
		await ctx.send(f"It landed on {'heads' if random.choice([0,1]) == 0 else 'tails'}!",hidden=hidden)

	@cog_ext.cog_slash(name="jack",description="show jack")
	async def jack(self,ctx:SlashContext,hidden:bool = False):
		await ctx.send("""\
		<:jack1:784513836375212052><:jack2:784513836408504360><:jack3:784513836321079326>
		<:jack4:784513836442189884><:jack5:784513836626477056><:jack6:784513836832522291>
		<:jack7:784513836660031518><:jack8:784513836865814588><:jack9:784513836434325535>""".replace("	",""),hidden=hidden)

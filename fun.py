from discord.ext import commands

class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None

	@commands.command(brief="roll a dice")
	async def roll(self, ctx, number_of_dice: int, number_of_sides: int):
		dice = [
			str(random.choice(range(1, number_of_sides + 1)))
			for _ in range(number_of_dice)
		]
		await ctx.send(", ".join(dice))

	@commands.command(brief="flip a coin")
	async def coinflip(self, ctx):
		await ctx.send(f"It landed on {'heads' if random.choice([0,1]) == 0 else 'tails'}!")

	@commands.command(brief="show jack")
	async def jack(self,ctx):
		await ctx.send("<:jack1:784513836375212052><:jack2:784513836408504360><:jack3:784513836321079326>\n<:jack4:784513836442189884><:jack5:784513836626477056><:jack6:784513836832522291>\n<:jack7:784513836660031518><:jack8:784513836865814588><:jack9:784513836434325535>")

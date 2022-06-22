import discord
# from discord.ext import commands
# from discord_slash import discord.ApplicationContext, cog_ext

import sqlite3
import random
# from discord_slash.model import SlashCommandOptionType
# from discord_slash.utils.manage_commands import create_choice, create_option

class Fun(discord.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None

	@discord.command(name="roll",description="roll a dice")
	async def roll(self,ctx:discord.ApplicationContext, number_of_dice: int, number_of_sides: int,hidden: bool = False):
		dice = [
			str(random.choice(range(1, number_of_sides + 1)))
			for _ in range(number_of_dice)
		]
		await ctx.respond(", ".join(dice),hidden=hidden)

	@discord.command(name="coinflip",description="flip a coin")
	# 	create_option("hidden",description="Whether to show the output of the message in chat",option_type=SlashCommandOptionType.BOOLEAN,required=False),
	# 	create_option("bet",description="How much you want to bet on the coin",option_type=SlashCommandOptionType.INTEGER,required=False),
	# 	create_option("choice",description="Which side you think the coin will land on",option_type=SlashCommandOptionType.STRING,required=False,choices=[
	# 		create_choice(name="Heads",value="h"),
	# 		create_choice(name="Tails",value="t"),
	# 	])
	# ])
	async def coinflip(
		self,
		ctx:discord.ApplicationContext,
		hidden:discord.Option(bool,"Whether to show the output of the message in chat",default=True),
		bet:discord.Option(int,"How much you want to bet on the coin",default=0),
		choice:discord.Option(str,"Which side you think the coin will land on",choices=[discord.OptionChoice("Heads","h"),discord.OptionChoice("Tails","t")],default="ha")):
		coin = "heads" if random.choice((0,1)) == 0 else "tails"
		# await ctx.respond(f"It landed on {coin}!" + ("" if choice == "ha" else f"\n\nYou were {'right' if choice == coin[0] else 'wrong'}!"),hidden=hidden)
		default = len(choice) == 2
		choice = choice[0]
		betmsg = ""
		if bet:
			if abs(bet) != bet:
				await ctx.respond("You cannot bet a negative amount!",ephemeral=True)
				return
			con = sqlite3.connect("users.db")
			money = list(con.execute("SELECT money FROM users WHERE id = ?",(ctx.interaction.user.id,)))[0][0]
			if bet > money:
				await ctx.respond("You are betting money you don't have!",ephemeral=True)
				return
			con.execute("UPDATE users SET money = ? WHERE id = ?",(money + (bet * (1 if choice == coin[0] else -1)),str(ctx.interaction.user.id)))
			con.commit()
			betmsg = f"\n\n{'+' if choice == coin[0] else '-'}<a:goldcoin:801148801653276693>{bet}."
		await ctx.respond(f"It landed on {coin}!" + ("" if default and not bet else f"\n\nYou were {'right' if choice == coin[0] else 'wrong'}!") + betmsg,ephemeral=hidden)

	@discord.command(name="jack",description="show jack")
	async def jack(self,ctx:discord.ApplicationContext):
		await ctx.respond("""\
	<:jack1:887072181262123090><:jack2:887072180951724103>
	<:jack4:887072181442457641><:jack5:887072180544884747><:jack6:887072180679114782>
	<:jack7:887072181262123088><:jack8:887072181752823858><:jack9:887072181505359893>""".replace("	",""))

if __name__ == "__main__":
	import main
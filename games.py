import asyncio
from re import T
import discord
from discord.ext import commands
from discord.ext.commands import cog
from discord_slash import SlashContext,cog_ext
from discord_slash.context import ComponentContext
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from discord_slash.model import ButtonStyle
import sqlite3

from libs import c4py, extra, minespy, tttpy
import random
import json
import base64

with open("themes.json", "r") as themesfile:
	themes = json.loads(themesfile.read())

if not extra.file_exists("analytics.json"):
	with open("analytics.json","w") as analyticsfile:
		analytics = {}
		for i in ["rps","connectfour","tictactoe","minesweeper","coinflip"]:
			analytics[i] = 0
		json.dump(analytics,analyticsfile)

with open("analytics.json","r") as analyticsfile: analytics = json.load(analyticsfile)
class Games(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None
		
	
	@cog_ext.cog_slash(name='minesweeper',description="generate minesweeper board")
	async def minesweeper(self,ctx:SlashContext, length: int = 6, width: int = 6, mines: int = 7,hidden:bool = False):
		global analytics
		analytics["minesweeper"] += 1
		extra.update_analytics(analytics)
		if length * width > 196:
			await ctx.send(embed=discord.Embed(title="Error",description="Board too large. Try something smaller."))
			return
		if mines >= (length * width):
			mines = (length * width) - 1
		gridstr = minespy.generategrid(length,width,mines)
		while "0" in gridstr or "1" in gridstr or "2" in gridstr or "3" in gridstr or "4" in gridstr or "5" in gridstr or "6" in gridstr or "7" in gridstr or "7" in gridstr or "B" in gridstr: # stole this from stackoverflow
			gridstr = gridstr.replace("0","||:zero:||")
			gridstr = gridstr.replace("1","||:one:||")
			gridstr = gridstr.replace("2","||:two:||")
			gridstr = gridstr.replace("3","||:three:||")
			gridstr = gridstr.replace("4","||:four:||")
			gridstr = gridstr.replace("5","||:five:||")
			gridstr = gridstr.replace("6","||:six:||")
			gridstr = gridstr.replace("7","||:seven:||")
			gridstr = gridstr.replace("8","||:eight:||")
			gridstr = gridstr.replace("B","||:boom:||")
		gridstr = extra.replacenth(gridstr,"||:zero:||",":zero:",random.randint(0,gridstr.count("||:zero:||")))
		embed = discord.Embed(title=f"{length}x{width} with {mines} mines",description=gridstr)
		await ctx.send(embed=embed,hidden=hidden)
	
	@cog_ext.cog_slash(name='rockpaperscissors',description="play rock paper scissors with someone")
	async def rps(self,ctx:SlashContext,member:discord.Member):
		global analytics
		analytics["rps"] += 1
		extra.update_analytics(analytics)
		components = create_actionrow(create_button(style=ButtonStyle.blue,label="Rock",emoji=u"\U0001f5ff"),create_button(style=ButtonStyle.green,label="Paper",emoji=u"\U0001f4f0"),create_button(style=ButtonStyle.red,label="Scissors",emoji=u"\u2702"))
		await ctx.send(f"{ctx.author.mention} {member.mention} Rock, paper, or scissors?",components=[components])
		button_ctx:ComponentContext = await wait_for_component(self.bot,components=components,check=lambda c_ctx:c_ctx.author == ctx.author or c_ctx.author == member)
		await button_ctx.send(f"Chosen {button_ctx.component['label']}",hidden=True)
		button_ctx_2:ComponentContext = await wait_for_component(self.bot,components=components,check=lambda c_ctx:(c_ctx.author == ctx.author or c_ctx.author == member) and c_ctx.author != button_ctx.author)
		# await button_ctx_2.send(f"{button_ctx_2.author.display_name} has chosen!")
		winner:discord.Member = None
		description = ""
		if button_ctx.component['label'] == "Paper" and button_ctx_2.component['label'] == "Rock": # paper > rock
			winner = button_ctx.author
		elif button_ctx.component['label'] == "Scissors" and button_ctx_2.component['label'] == "Paper": # scissors > paper
			winner = button_ctx.author
		elif button_ctx.component['label'] == "Rock" and button_ctx_2.component['label'] == "Scissors": # rock > scissors
			winner = button_ctx.author
		elif button_ctx.component['label'] == button_ctx_2.component['label']:
			description = f"{button_ctx.component['emoji']['name']}   v   {button_ctx_2.component['emoji']['name']}\n\n\nIt's a tie!"
		else:
			winner = button_ctx_2.author
		if not description:
			description = f"{button_ctx.component['emoji']['name']}   v   {button_ctx_2.component['emoji']['name']}\n\n\n{winner.display_name} won!"
		game_embed = discord.Embed(title=f"{button_ctx.author.display_name} v {button_ctx_2.author.display_name}",description=description)
		await button_ctx_2.send(embed=game_embed)
	
	@cog_ext.cog_slash(description="play tic tac toe with someone",name="tictactoe")
	async def tictactoe(self,ctx:SlashContext,opponent:discord.Member,save:str = None):
		global analytics
		analytics["tictactoe"] += 1
		extra.update_analytics(analytics)
		if save is not None:
			base = base64.b64decode(save.encode()).decode("utf-8").split("|")
			g = base[0]
			moves = int(base[1])
		else:
			g = tttpy.generategrid()
			moves = 1
		gs = g
		gs = gs.replace("X",":regional_indicator_x:")
		gs = gs.replace("O",":zero:")
		for i in gs:
			if str(i) in "123456789":
				gs = gs.replace(i,":blue_square:")
		title = f"Tic Tac Toe: *{ctx.author.display_name}*:regional_indicator_x: vs {opponent.display_name}:zero:" if moves % 2 == 1 else f"Connect 4: {ctx.author.display_name}:regional_indicator_x: vs *{opponent.display_name}*:zero:"
		msgembed = discord.Embed(title=title)
		msgembed.description = gs
		savestate = base64.b64encode(f"{g}|{moves}".encode()).decode("utf-8")
		msgembed.set_footer(text=savestate)
		components = [
			create_actionrow(
				create_button(style=ButtonStyle.gray,custom_id="wa",emoji="\u2196\uFE0F"),
				create_button(style=ButtonStyle.gray,custom_id="w",emoji="\u2B06\uFE0F"),
				create_button(style=ButtonStyle.gray,custom_id="wd",emoji="\u2197\uFE0F")
			),
			create_actionrow(
				create_button(style=ButtonStyle.gray,custom_id="a",emoji="\u2B05\uFE0F"),
				create_button(style=ButtonStyle.gray,custom_id=".",emoji="\u2B1C"),
				create_button(style=ButtonStyle.gray,custom_id="d",emoji="\u27A1\uFE0F")
			),
			create_actionrow(
				create_button(style=ButtonStyle.gray,custom_id="sa",emoji="\u2199\uFE0F"),
				create_button(style=ButtonStyle.gray,custom_id="s",emoji="\u2B07\uFE0F"),
				create_button(style=ButtonStyle.gray,custom_id="sd",emoji="\u2198\uFE0F")
			),
			create_actionrow(
				create_button(style=ButtonStyle.red,label="Exit",custom_id="q"),
			)
		]
		await ctx.send(embeds=[msgembed],components=components)
		while moves <= 9:
			button_ctx:ComponentContext = await wait_for_component(self.bot,components=components,check=lambda c_ctx: (c_ctx.author == ctx.author if moves % 2 == 1 else c_ctx.author == opponent) or c_ctx.component['custom_id'] == 'q')
			og = g
			char = "X" if moves % 2 == 1 else "O"
			if button_ctx.custom_id == "q":
				await button_ctx.send("Game closed.")
				return
			if button_ctx.custom_id == "wa":
				g = g.replace("1",char)
			elif button_ctx.custom_id == "w":
				g = g.replace("2",char)
			elif button_ctx.custom_id == "wd":
				g = g.replace("3",char)
			elif button_ctx.custom_id == "a":
				g = g.replace("4",char)
			elif button_ctx.custom_id == ".":
				g = g.replace("5",char)
			elif button_ctx.custom_id == "d":
				g = g.replace("6",char)
			elif button_ctx.custom_id == "sa":
				g = g.replace("7",char)
			elif button_ctx.custom_id == "s":
				g = g.replace("8",char)
			elif button_ctx.custom_id == "sd":
				g = g.replace("9",char)
			else:
				continue
			if og != g:
				moves += 1
			gs = g
			gs = gs.replace("X",":regional_indicator_x:")
			gs = gs.replace("O",":zero:")
			for i in gs:
				if str(i) in "123456789":
					gs = gs.replace(i,":blue_square:")
			title = f"Tic Tac Toe: *{ctx.author.display_name}*:regional_indicator_x: vs {opponent.display_name}:zero:" if moves % 2 == 1 else f"Connect 4: {ctx.author.display_name}:regional_indicator_x: vs *{opponent.display_name}*:zero:"
			msgembed = discord.Embed(title=title)
			msgembed.description = gs
			savestate = base64.b64encode(f"{g}|{moves}".encode()).decode("utf-8")
			msgembed.set_footer(text=savestate)
			await button_ctx.edit_origin(embed=msgembed)
			glist = []
			for i in g.split("\n"):
				if i == "":
					continue
				gltmp = []
				for j in i:
						gltmp.append(j)
				glist.append(gltmp)
			glist = []
			if tttpy.checkWin(glist):
				winner = ctx.author.display_name if moves % 2 == 0 else opponent.display_name
				await ctx.send(f"{winner} has won!")
				return
			elif moves > 9:
				await ctx.send("Nobody won, the game is tied.")
				return
	
	@cog_ext.cog_slash(name='connect4',description="play connect four with someone")
	async def connectfour(self,ctx:SlashContext,opponent:discord.Member,save:str = None):
		tiles_list = themes[random.choice(list(themes))]
		global analytics
		analytics["connectfour"] += 1
		extra.update_analytics(analytics)
		with open("c4layouts.json", "r") as c4layoutsfile:
			c4layouts = json.loads(c4layoutsfile.read())
		if (save in c4layouts):
			save = c4layouts[save]
		if save is not None:
			base = base64.b64decode(save.encode()).decode("utf-8").split("|")
			g = json.loads(base[0].replace("'",'"'))
			moves = int(base[1])
		else:
			g = ["       \n" for _ in range(6)]
			moves = 1
			base = None
		if base is not None:
			pass
		gridstr = "".join(g[::-1])
		theme = random.choice(list(themes))
		tiles_list = dict(themes[theme])
		nums_list = "".join(tiles_list["nums"])
		gridstr += nums_list
		tiles_list.pop("nums")
		for tile in tiles_list: gridstr = gridstr.replace(tile,tiles_list[tile])
		title = f"Connect 4: *{ctx.author.display_name}*{tiles_list['X']} vs {opponent.display_name}{tiles_list['O']}" if moves % 2 == 1 else f"Connect 4: {ctx.author.display_name}{tiles_list['X']} vs *{opponent.display_name}*{tiles_list['O']}"
		if len(gridstr) > 2048:
			await ctx.send("The grid is too big!")
			return
		components = [
			create_actionrow(
				create_button(style=ButtonStyle.blue,label="1",custom_id="1"),
				create_button(style=ButtonStyle.blue,label="2",custom_id="2"),
				create_button(style=ButtonStyle.blue,label="3",custom_id="3"),
			),
			create_actionrow(
				create_button(style=ButtonStyle.blue,label="4",custom_id="4"),
				create_button(style=ButtonStyle.blue,label="5",custom_id="5"),
				create_button(style=ButtonStyle.blue,label="6",custom_id="6"),
			),
			create_actionrow(
				create_button(style=ButtonStyle.red,label="Quit",custom_id="q"),
				create_button(style=ButtonStyle.blue,label="7",custom_id="7"),
			)
		]
		msgembed = discord.Embed(title=title)
		msgembed.description = gridstr
		savestate = base64.b64encode(f"{json.dumps(g)}|{moves}".encode()).decode("utf-8")
		msgembed.set_footer(text=savestate)
		await ctx.send(embed=msgembed,components=components)
	
		while moves <= 42:
			def check(message):
				user = message.author
				return user == opponent if moves % 2 == 0 else user == ctx.author
			button_ctx:ComponentContext = await wait_for_component(self.bot,components=components,check=check)
			if button_ctx.custom_id == "q":
				await ctx.send("game ended")
				return
			bg = list(g)
			for y in g:
				# and not (y == g[0] and y[int(c) - 1] in ["X","O"])
				if not y[int(button_ctx.custom_id) - 1] == " ": continue
				t = list(y)
				t[int(button_ctx.custom_id) - 1] = "X" if moves % 2 == 1 else "O"
				g[g.index(y)] = "".join(t)
				break
			moves += 1 if bg != g else 0
			gridstr = "".join(g[::-1])
			for tile in tiles_list: gridstr = gridstr.replace(tile,tiles_list[tile])
			gridstr += nums_list
			title = f"Connect 4: *{ctx.author.display_name}*{tiles_list['X']} vs {opponent.display_name}{tiles_list['O']}" if moves % 2 == 1 else f"Connect 4: {ctx.author.display_name}{tiles_list['X']} vs *{opponent.display_name}*{tiles_list['O']}"
			msgembed = discord.Embed(title=title)
			msgembed.description = gridstr
			savestate = base64.b64encode(f"{json.dumps(g)}|{moves}".encode()).decode("utf-8")
			msgembed.set_footer(text=savestate)
			await button_ctx.edit_origin(embed=msgembed)
			glist = []
			for i in g:
				if i == "\n":
					continue
				gltmp = []
				for j in i:
					gltmp.append(j)
				glist.append(gltmp)
			if c4py.check_win(glist,"X") or c4py.check_win(glist,"O"):
				winner = ctx.author.display_name if moves % 2 == 0 else opponent.display_name
				await ctx.send(f"{winner} has won!")
				return
			elif moves > 42:
				await ctx.send("Nobody won, the game is tied. How did you manage to do that in connect 4?")
				return
	@cog_ext.cog_slash(name='blackjack',description='Gamble away all of your shmeckles, or win the jackbot!')
	async def blackjack(self,ctx:SlashContext,bet:int):
		if abs(bet) != bet:
			await ctx.send("You cannot bet a negative amount!",hidden=True)
			return
		con = sqlite3.connect("users.db")
		money = list(con.execute("SELECT money FROM users WHERE id = ?",(ctx.author_id,)))[0][0]
		if bet > money:
			await ctx.send("You are betting money you don't have!",hidden=True)
			return
		components = [create_actionrow(create_button(style=ButtonStyle.blue,label="Hit",custom_id="h"),create_button(style=ButtonStyle.gray,label="Stand",custom_id="s"))]
		dealer_draws = 1
		player_cards = random.randint(1,10) + random.randint(1,10)
		dealer_cards = random.randint(1,10) + random.randint(1,10)
		embed = discord.Embed(title="Blackjack",description=f"Your cards: {player_cards}\nDealer's cards: {dealer_cards}\nDealer draws: {dealer_draws}")
		await ctx.send(embeds=[embed],components=components,hidden=True)
		while player_cards < 21:
			button_ctx = await wait_for_component(client=self.bot,components=components)
			if button_ctx.custom_id == "h":
				player_cards += random.randint(1,10)
				dealer_cards += 0 if dealer_cards >= 17 else random.randint(1,10)
				dealer_draws += 1
			elif button_ctx.custom_id == "s":
				while dealer_cards <= 17:
					dealer_cards += random.randint(1,10)
					dealer_draws += 1
			embed = discord.Embed(title=f"Blackjack for {bet} shmeckles",description=f"Your cards: {player_cards}\nDealer's cards: {dealer_cards}\nDealer draws: {dealer_draws}")
			await button_ctx.send(embeds=[embed],hidden=True,components=components)
			if player_cards > 21:
				await button_ctx.send("You lose!",hidden=True)
				win = -1
				break
			if dealer_cards > 21 or (dealer_cards >= 17 and player_cards > dealer_cards):
				await button_ctx.send("You win!",hidden=True)
				win = 1
				break
			if dealer_cards == 21 and (player_cards == dealer_cards):
				await button_ctx.send("It's a draw!",hidden=True)
				return
		money = list(con.execute("SELECT money FROM users WHERE id = ?",(ctx.author_id,)))[0][0]
		con.execute("UPDATE users SET money = ? WHERE id = ?",(money + (money * win),str(ctx.author_id)))
		con.commit()


if __name__ == "__main__":
	import main
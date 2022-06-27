# import asyncio
from re import T
import discord
# from discord_slash import discord.ApplicationContext,cog_ext
# from discord_slash.context import ComponentContext
# from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
# from discord_slash.model import discord.ButtonStyle
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
class Games(discord.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None
	
	@discord.command(name='minesweeper',description="generate minesweeper board")
	async def minesweeper(
		self,
		ctx:discord.ApplicationContext,
		length: discord.Option(int, min_value=2, max_value=10,default=6),
		width: discord.Option(int, min_value=2, max_value=10,default=6),
		mines: int = 7,
		hidden:bool = False
		):
		global analytics
		analytics["minesweeper"] += 1
		extra.update_analytics(analytics)
		if length * width > 196:
			await ctx.response(embed=discord.Embed(title="Error",description="Board too large. Try something smaller."))
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
		await ctx.respond(embed=embed,ephemeral=hidden)
	
	@discord.command(name='rockpaperscissors',description="play rock paper scissors with someone")
	async def rps(self,ctx:discord.ApplicationContext,member:discord.Member):
		global analytics
		analytics["rps"] += 1
		extra.update_analytics(analytics)
		view = extra.RPSView(player1=ctx.author,player2=member,timeout=None)
		await ctx.respond(f"{ctx.author.mention} {member.mention} Rock, paper, or scissors?",view=view)
		await view.wait()
		winner:discord.Member = None
		description = ""
		if view.player1_choice == extra.RPSChoices.PAPER and view.player2_choice == extra.RPSChoices.ROCK: # paper > rock
			winner = view.player1
		elif view.player1_choice == extra.RPSChoices.SCISSORS and view.player2_choice == extra.RPSChoices.PAPER: # scissors > paper
			winner = view.player1
		elif view.player1_choice == extra.RPSChoices.ROCK and view.player2_choice == extra.RPSChoices.SCISSORS: # rock > scissors
			winner = view.player2
		elif view.player1_choice == view.player2_choice:
			description = f"{extra.RPStoEMOJI[view.player1_choice]}   v   {extra.RPStoEMOJI[view.player2_choice]}\n\n\nIt's a tie!"
		else:
			winner = view.player2
		if not description:
			description = f"{extra.RPStoEMOJI[view.player1_choice]}   v   {extra.RPStoEMOJI[view.player2_choice]}\n\n\n{winner.display_name} won!"
		game_embed = discord.Embed(title=f"{view.player1.display_name} v {view.player2.display_name}",description=description)
		await ctx.send(embed=game_embed)
	
	@discord.command(description="play tic tac toe with someone",name="tictactoe")
	async def tictactoe(self,ctx:discord.ApplicationContext,opponent:discord.Member,save:str = None):
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
		title = f"Tic Tac Toe: *{ctx.author.display_name}*:regional_indicator_x: vs {opponent.display_name}:zero:" if moves % 2 == 1 else f"Tic Tac Toe: {ctx.author.display_name}:regional_indicator_x: vs *{opponent.display_name}*:zero:"
		msgembed = discord.Embed(title=title)
		msgembed.description = gs
		savestate = base64.b64encode(f"{g}|{moves}".encode()).decode("utf-8")
		msgembed.set_footer(text=savestate)
		view = extra.TTTView(ctx.author)
		await ctx.respond(embeds=[msgembed],view=view)
		while moves <= 9:
			# await wait_for_component(self.bot,components=components,check=lambda c_ctx: (c_ctx.author == ctx.author if moves % 2 == 1 else c_ctx.author == opponent) or c_ctx.component['custom_id'] == 'q')
			await view.wait()
			og = g
			char = "X" if moves % 2 == 1 else "O"
			if view.move == "q":
				await view.interaction.response.send_message("Game closed.")
				return
			if view.move == "wa":
				g = g.replace("1",char)
			elif view.move == "w":
				g = g.replace("2",char)
			elif view.move == "wd":
				g = g.replace("3",char)
			elif view.move == "a":
				g = g.replace("4",char)
			elif view.move == ".":
				g = g.replace("5",char)
			elif view.move == "d":
				g = g.replace("6",char)
			elif view.move == "sa":
				g = g.replace("7",char)
			elif view.move == "s":
				g = g.replace("8",char)
			elif view.move == "sd":
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
			title = f"Tic Tac Toe: *{ctx.author.display_name}*:regional_indicator_x: vs {opponent.display_name}:zero:" if moves % 2 == 1 else f"Tic Tac Toe: {ctx.author.display_name}:regional_indicator_x: vs *{opponent.display_name}*:zero:"
			msgembed = discord.Embed(title=title)
			msgembed.description = gs
			savestate = base64.b64encode(f"{g}|{moves}".encode()).decode("utf-8")
			msgembed.set_footer(text=savestate)
			old_view = view
			view = extra.TTTView(ctx.author if moves % 2 == 1 else opponent)
			await old_view.interaction.response.edit_message(embed=msgembed,view=view)
			glist = []
			for i in g.split("\n"):
				if i == "":
					continue
				gltmp = []
				for j in i:
						gltmp.append(j)
				glist.append(gltmp)
			if tttpy.checkWin(glist):
				winner = ctx.author.display_name if moves % 2 == 0 else opponent.display_name
				await view.interaction.response.send_message(f"{winner} has won!")
				return
			elif moves > 9:
				await view.interaction.response.send_message("Nobody won, the game is tied.")
				return
	
	@discord.command(name='connect4',description="play connect four with someone")
	async def connectfour(self,ctx:discord.ApplicationContext,opponent:discord.Member,save:str = None):
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
			await ctx.respond("The grid is too big!")
			return
		# components = [
		# 	create_actionrow(
		# 		create_button(style=discord.ButtonStyle.blue,label="1",custom_id="1"),
		# 		create_button(style=discord.ButtonStyle.blue,label="2",custom_id="2"),
		# 		create_button(style=discord.ButtonStyle.blue,label="3",custom_id="3"),
		# 	),
		# 	create_actionrow(
		# 		create_button(style=discord.ButtonStyle.blue,label="4",custom_id="4"),
		# 		create_button(style=discord.ButtonStyle.blue,label="5",custom_id="5"),
		# 		create_button(style=discord.ButtonStyle.blue,label="6",custom_id="6"),
		# 	),
		# 	create_actionrow(
		# 		create_button(style=discord.ButtonStyle.red,label="Quit",custom_id="q"),
		# 		create_button(style=discord.ButtonStyle.blue,label="7",custom_id="7"),
		# 	)
		# ]
		view = extra.C4View(ctx.author if moves % 2 == 1 else opponent)
		msgembed = discord.Embed(title=title)
		msgembed.description = gridstr
		savestate = base64.b64encode(f"{json.dumps(g)}|{moves}".encode()).decode("utf-8")
		msgembed.set_footer(text=savestate)
		await ctx.respond(embed=msgembed,view=view)
		while moves <= 42:
			def check(message):
				user = message.author
				return user == opponent if moves % 2 == 0 else user == ctx.author
			await view.wait()
			if view.move == "q":
				await view.interaction.response.send_message("game ended")
				return
			bg = list(g)
			for y in g:
				# and not (y == g[0] and y[int(c) - 1] in ["X","O"])
				if not y[int(view.move) - 1] == " ": continue
				t = list(y)
				t[int(view.move) - 1] = "X" if moves % 2 == 1 else "O"
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
			old_view = view
			view = extra.C4View(ctx.author if moves % 2 == 1 else opponent)
			await old_view.interaction.response.edit_message(embed=msgembed,view=view)
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
				await view.interaction.response.send_message(f"{winner} has won!")
				return
			elif moves > 42:
				await view.interaction.response.send_message("Nobody won, the game is tied. How did you manage to do that in connect 4?")
				return
	
	@discord.command(name='blackjack',description='Gamble away all of your shmeckles, or win the jackbot!')
	async def blackjack(self,ctx:discord.ApplicationContext,bet:int):
		if abs(bet) != bet:
			await ctx.respond("You cannot bet a negative amount!",ephemeral=True)
			return
		con = sqlite3.connect("users.db")
		money = list(con.execute("SELECT money FROM users WHERE id = ?",(ctx.author.id,)))[0][0]
		if bet > money:
			await ctx.respond("You are betting money you don't have!",ephemeral=True)
			return
		# components = [create_actionrow(create_button(style=discord.ButtonStyle.blue,label="Hit",custom_id="h"),create_button(style=ButtonStyle.gray,label="Stand",custom_id="s"))]
		view = extra.BJView()
		dealer_draws = 1
		player_cards = random.randint(1,10) + random.randint(1,10)
		dealer_cards = random.randint(1,10) + random.randint(1,10)
		embed = discord.Embed(title=f"Blackjack for <a:goldcoin:801148801653276693>{bet}",description=f"Your cards: {player_cards}\nDealer's cards: {dealer_cards}\nDealer draws: {dealer_draws}")
		await ctx.respond(embeds=[embed],view=view,ephemeral=True)
		while player_cards < 21:
			view.wait()
			if view.button_pressed.custom_id == "h":
				player_cards += random.randint(1,10)
				dealer_cards += 0 if dealer_cards >= 17 else random.randint(1,10)
				dealer_draws += 1
			elif view.button_pressed.custom_id == "s":
				while dealer_cards <= 17:
					dealer_cards += random.randint(1,10)
					dealer_draws += 1
			embed = discord.Embed(title=f"Blackjack for <a:goldcoin:801148801653276693>{bet}",description=f"Your cards: {player_cards}\nDealer's cards: {dealer_cards}\nDealer draws: {dealer_draws}")
			old_view = view
			view = extra.BJView()
			await old_view.interaction.response.send_message(embeds=[embed],ephemeral=True,view=view)
			if player_cards > 21:
				await old_view.interaction.response.send_message(f"You lose! -<a:goldcoin:801148801653276693>{bet}.",ephemeral=True)
				win = -1
				break
			if dealer_cards > 21 or (dealer_cards >= 17 and player_cards > dealer_cards):
				await old_view.interaction.response.send_message(f"You win! +<a:goldcoin:801148801653276693>{bet}.",hidden=True)
				win = 1
				break
			if dealer_cards == 21 and (player_cards == dealer_cards):
				await old_view.interaction.response.send_message("It's a draw!",hidden=True)
				return
		money = list(con.execute("SELECT money FROM users WHERE id = ?",(ctx.author.id,)))[0][0]
		await ctx.send(f"You now have a total of <a:goldcoin:801148801653276693>{money + (bet * win)}.",hidden=True)
		con.execute("UPDATE users SET money = ? WHERE id = ?",(money + (bet * win),str(ctx.author.id)))
		con.commit()


if __name__ == "__main__":
	import main
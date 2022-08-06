import enum
from pickle import NONE
import re
import json
import discord


async def attachments_to_files(attached):
	filelist = []
	for i in attached:
		file = await i.to_file()
		filelist.insert(len(filelist),file)
	return filelist

def replacenth(string, sub, wanted, n):
	where = [m.start() for m in re.finditer(sub, string)][n-1]
	before = string[:where]
	after = string[where:]
	after = after.replace(sub, wanted, 1)
	new_string = before + after
	return new_string

def isint(thing):
	try:
		int(thing)
	except ValueError:
		return False
	return True

def update_analytics(analytics: dict):
	with open("analytics.json","w") as analyticsfile:
		json.dump(analytics,analyticsfile)
	return analytics

def file_exists(filename:str):
	try:
		with open(filename,"r"):
			return True
	except FileNotFoundError:
		return False

def list_layouts(filename):
		with open(filename, "r") as c4layoutsfile:
			return json.loads(c4layoutsfile.read())

class RPSChoices(enum.Enum):
	ROCK		 = "Rock"
	PAPER		= "Paper"
	SCISSORS = "Scissors"

RPStoEMOJI = {RPSChoices.ROCK:":rock:",RPSChoices.PAPER:":newspaper:",RPSChoices.SCISSORS:":scissors:"}

class RPSView(discord.ui.View):
	def __init__(self,player1:discord.Member,player2:discord.Member,*items:discord.ui.Item,timeout:float = 180.0):
		self.player1 = player1
		self.player2 = player2
		self.player1_choice = None
		self.player2_choice = None
		super().__init__(*items,timeout=timeout)
	
	async def _choose(self,choice:RPSChoices,interaction:discord.Interaction):
		await interaction.response.send_message(f"Chosen {choice.value}",ephemeral=True)
		self.player1_choice = choice if interaction.user == self.player1 else self.player1_choice
		self.player2_choice = choice if interaction.user == self.player2 else self.player2_choice
		# self.player1_choice = RPSChoices.ROCK if not self.player1_choice else self.player1_choice
		# self.player2_choice = RPSChoices.ROCK if self.player1_choice else None
		if self.player1_choice and self.player2_choice:
			self.stop()
		
	@discord.ui.button(label="Rock",style=discord.ButtonStyle.blurple,emoji=u"\U0001f5ff")
	async def rock(self,button:discord.ui.Button,interaction:discord.Interaction):
		await self._choose(RPSChoices.ROCK,interaction)
	
	@discord.ui.button(label="Paper",style=discord.ButtonStyle.green,emoji=u"\U0001f4f0")
	async def paper(self,button:discord.ui.Button,interaction:discord.Interaction):
		await self._choose(RPSChoices.PAPER,interaction)

	@discord.ui.button(label="Scissors",style=discord.ButtonStyle.red,emoji=u"\u2702")
	async def scissors(self,button:discord.ui.Button,interaction:discord.Interaction):
		await self._choose(RPSChoices.SCISSORS,interaction)

class TTTView(discord.ui.View):
	def __init__(self, whose_move:discord.User,*items:discord.ui.Item):
		self.move = ""
		self.whose_move = whose_move
		self.interaction = None
		super().__init__(*items, timeout=None)
	
	async def _choose(self,move:str,interaction:discord.Interaction):
		if self.whose_move == interaction.user or move == "q":
			self.move = move
			self.interaction = interaction
			self.stop()
	
	@discord.ui.button(emoji="\u2B1C",row=0,style=discord.ButtonStyle.gray)
	async def top_left(self,button:discord.ui.Button,interaction:discord.Interaction):
		await self._choose("wa",interaction)
	@discord.ui.button(emoji="\u2B1C",row=0,style=discord.ButtonStyle.gray)
	async def top_mid(self,button:discord.ui.Button,interaction:discord.Interaction):
		await self._choose("w",interaction)
	@discord.ui.button(emoji="\u2B1C",row=0,style=discord.ButtonStyle.gray)
	async def top_right(self,button:discord.ui.Button,interaction:discord.Interaction):
		await self._choose("wd",interaction)
	@discord.ui.button(emoji="\u2B1C",row=1,style=discord.ButtonStyle.gray)
	async def mid_left(self,button:discord.ui.Button,interaction:discord.Interaction):
		await self._choose("a",interaction)
	@discord.ui.button(emoji="\u2B1C",row=1,style=discord.ButtonStyle.gray)
	async def mid_mid(self,button:discord.ui.Button,interaction:discord.Interaction):
		await self._choose(".",interaction)
	@discord.ui.button(emoji="\u2B1C",row=1,style=discord.ButtonStyle.gray)
	async def mid_right(self,button:discord.ui.Button,interaction:discord.Interaction):
		await self._choose("d",interaction)
	@discord.ui.button(emoji="\u2B1C",row=2,style=discord.ButtonStyle.gray)
	async def bot_left(self,button:discord.ui.Button,interaction:discord.Interaction):
		await self._choose("sa",interaction)
	@discord.ui.button(emoji="\u2B1C",row=2,style=discord.ButtonStyle.gray)
	async def bot_mid(self,button:discord.ui.Button,interaction:discord.Interaction):
		await self._choose("s",interaction)
	@discord.ui.button(emoji="\u2B1C",row=2,style=discord.ButtonStyle.gray)
	async def bot_right(self,button:discord.ui.Button,interaction:discord.Interaction):
		await self._choose("sd",interaction)
	@discord.ui.button(label="Exit",row=3,style=discord.ButtonStyle.red)
	async def exit(self,button:discord.ui.Button,interaction:discord.Interaction):
		await self._choose("q",interaction)

class C4View(discord.ui.View):
	def __init__(self, whose_turn:discord.User,*items: discord.ui.Item):
		self.whose_turn = whose_turn
		self.interaction = None
		self.move = ""
		super().__init__(*items, timeout=None)
	
	async def _choose(self,button:discord.ui.Button,interaction:discord.Interaction):
		move = button.label
		if self.whose_turn == interaction.user:
			self.move = move
			self.interaction = interaction
			self.stop()

	@discord.ui.button(label="1",row=0,style=discord.ButtonStyle.blurple)
	async def select_1(self,button:discord.ui.Button,interaction:discord.Interaction):
		await self._choose(button,interaction)
	@discord.ui.button(label="2",row=0,style=discord.ButtonStyle.blurple)
	async def select_2(self,button:discord.ui.Button,interaction:discord.Interaction):
		await self._choose(button,interaction)
	@discord.ui.button(label="3",row=0,style=discord.ButtonStyle.blurple)
	async def select_3(self,button:discord.ui.Button,interaction:discord.Interaction):
		await self._choose(button,interaction)
	@discord.ui.button(label="4",row=1,style=discord.ButtonStyle.blurple)
	async def select_4(self,button:discord.ui.Button,interaction:discord.Interaction):
		await self._choose(button,interaction)
	@discord.ui.button(label="5",row=1,style=discord.ButtonStyle.blurple)
	async def select_5(self,button:discord.ui.Button,interaction:discord.Interaction):
		await self._choose(button,interaction)
	@discord.ui.button(label="6",row=1,style=discord.ButtonStyle.blurple)
	async def select_6(self,button:discord.ui.Button,interaction:discord.Interaction):
		await self._choose(button,interaction)
	@discord.ui.button(label="q",row=2,style=discord.ButtonStyle.red)
	async def select_q(self,button:discord.ui.Button,interaction:discord.Interaction):
		await self._choose(button,interaction)
	@discord.ui.button(label="7",row=2,style=discord.ButtonStyle.blurple)
	async def select_7(self,button:discord.ui.Button,interaction:discord.Interaction):
		await self._choose(button,interaction)

class BJView(discord.ui.View):
	def __init__(self, *items: discord.ui.Item):
		self.button_pressed = None
		self.interaction = None
		super().__init__(*items, timeout=None)
	
	@discord.ui.button(label="Hit",custom_id="h",style=discord.ButtonStyle.blurple)
	async def hit(self,button:discord.ui.Button,interaction:discord.Interaction):
		self.button_pressed = button
		self.interaction = interaction
		self.stop()
	@discord.ui.button(label="Stand",custom_id="s",style=discord.ButtonStyle.gray)
	async def stand(self,button:discord.ui.Button,interaction:discord.Interaction):
		self.button_pressed = button
		self.interaction = interaction
		self.stop()

def ordinal(n:int,/): # https://codereview.stackexchange.com/q/41298
	"""
	Returns ordinal number string from int, e.g. 1, 2, 3 becomes 1st, 2nd, 3rd, etc.
	"""
	if 4 <= n <= 20:
		suffix = 'th'
	elif n == 1 or (n % 10) == 1:
		suffix = 'st'
	elif n == 2 or (n % 10) == 2:
		suffix = 'nd'
	elif n == 3 or (n % 10) == 3:
		suffix = 'rd'
	elif n < 100:
		suffix = 'th'
	ord_num = str(n) + suffix
	return ord_num

# vim: noet ci pi sts=0 sw=4 ts=4:
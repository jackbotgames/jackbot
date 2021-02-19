import re
import discord
from discord.ext import	commands
import json

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
# most code from this class was stolen from help.py in discord.py
class MyHelpCommand(commands.DefaultHelpCommand):
	def __init__(self, **options):
		self.paginator = commands.Paginator()
		super().__init__(**options)
		self.paginator.prefix = ""
		self.paginator.suffix = ""
		self.no_category = "Other"
	def add_indented_commands(self, commands, *, heading, max_size=None):
		if not commands:
			return
		self.paginator.add_line(f"**{heading}**")
		max_size = max_size or self.get_max_size(commands)
		get_width = discord.utils._string_width
		for command in commands:
			name = f"{command.name}"
			width = max_size - (get_width(name) - len(name))
			entry = '{0}{1:<{width}}: *{2}*'.format(self.indent * ' ', name, command.short_doc, width=width)
			self.paginator.add_line(self.shorten_text(entry))
	def get_ending_note(self):
		command_name = self.invoked_with
		return "Type `{0}{1} <command>` for more info on a command.\n".format(self.clean_prefix, command_name)
	def add_command_formatting(self, command):
		if command.description:
			self.paginator.add_line(command.description, empty=True)

		signature = self.get_command_signature(command)
		self.paginator.add_line(f"`{signature}`""", empty=True)

		if command.help:
			try:
				self.paginator.add_line(command.help, empty=True)
			except RuntimeError:
				for line in command.help.splitlines():
					self.paginator.add_line(line)
				self.paginator.add_line()
	async def send_pages(self):
		destination = self.get_destination()
		e = discord.Embed(color=discord.Color.blurple(), description='')
		for page in self.paginator.pages:
			e.description += page
		await destination.send(embed=e)


# vim: noet ci pi sts=0 sw=4 ts=4:
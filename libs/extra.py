import re
import discord
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

# vim: noet ci pi sts=0 sw=4 ts=4:
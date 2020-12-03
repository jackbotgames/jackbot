import re

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

# vim: noet ci pi sts=0 sw=4 ts=4:

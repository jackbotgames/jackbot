import random

def generatebombs(length: int, width: int, mines: int):
	bombs = []
	for i in range(mines):
		while True:
			bomblocation = [random.randint(1,width),random.randint(1,length)]
			if bomblocation not in bombs:
				bombs.append(bomblocation)
				break
	return bombs

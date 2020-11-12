#!/usr/bin/env python3

import random

def generatebombs(length: int, width: int, mines: int):
	bombs = []
	for _ in range(mines):
		while True:
			bomblocation = [random.randint(1,width),random.randint(1,length)]
			if bomblocation not in bombs:
				bombs.append(bomblocation)
				break
	return bombs

def generategrid(length: int, width: int, mines: int):
	bombs = generatebombs(length,width,mines)
	x = [ (i + 1) for i in range(width)  ]
	y = [ (i + 1) for i in range(length) ]
	grid = [ [ 0 for i in range(length) ] for i in range(width) ]
	for i in x:
		for j in y:
			if [i,j] in bombs:
				grid[i - 1][j - 1] = "B"
	for bomb in bombs:
		try:
			grid[bomb[0] - 2][bomb[1] - 2] += 1 if bomb[0] - 2 > -1 and bomb[1] - 2 > -1 else 0
		except:
			pass
		try:
			grid[bomb[0] - 0][bomb[1] - 2] += 1 if bomb[0] - 1 > -1 and bomb[1] - 2 > -1 else 0
		except:
			pass
		try:
			grid[bomb[0] - 2][bomb[1] - 0] += 1 if bomb[0] - 2 > -1 and bomb[1] - 0 > -1 else 0
		except:
			pass
		try:
			grid[bomb[0] - 0][bomb[1] - 0] += 1 if bomb[0] - 0 > -1 and bomb[1] - 0 > -1 else 0
		except:
			pass
		try:
			grid[bomb[0] - 1][bomb[1] - 0] += 1 if bomb[0] - 1 > -1 and bomb[1] - 0 > -1 else 0
		except:
			pass
		try:
			grid[bomb[0] - 0][bomb[1] - 1] += 1 if bomb[0] - 0 > -1 and bomb[1] - 1 > -1 else 0
		except:
			pass
		try:
			grid[bomb[0] - 2][bomb[1] - 1] += 1 if bomb[0] - 2 > -1 and bomb[1] - 1 > -1 else 0
		except:
			pass
		try:
			grid[bomb[0] - 1][bomb[1] - 2] += 1 if bomb[0] - 1 > -1 and bomb[1] - 2 > -1 else 0
		except:
			pass
	gridstr = ""
	for i in grid:
		for j in i:
			gridstr += f"{j}"
		gridstr += "\n"
	return gridstr

if __name__ == "__main__":
	print(generategrid(10,10,10))

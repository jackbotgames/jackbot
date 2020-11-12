#!/usr/bin/env python3
from numpy import transpose

def generategrid():
	grid = [[1,2,3],[4,5,6],[7,8,9]]
	gridstr = ""
	for i in grid:
		for j in i:
			gridstr += f"{j}"
		gridstr += "\n"
	return gridstr

if __name__ == "__main__":
	print(generategrid())

def checkRows(board):
	for row in board:
		if len(set(row)) == 1:
			return row[0]
	return 0

def checkDiagonals(board):
	if len(set([board[i][i] for i in range(len(board))])) == 1:
		return board[0][0]
	if len(set([board[i][len(board)-i-1] for i in range(len(board))])) == 1:
		return board[0][len(board)-1]
	return 0

def checkWin(board):
	#transposition to check rows, then columns
	for newBoard in [board, transpose(board)]:
		result = checkRows(newBoard)
		if result:
			return result
	return checkDiagonals(board) 

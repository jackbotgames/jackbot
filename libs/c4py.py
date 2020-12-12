
# https://stackoverflow.com/questions/29949169/python-connect-4-check-win-function
def check_win(board,tile):
	boardHeight = len(board[0])
	boardWidth = len(board)
	# check horizontal spaces
	for y in range(boardHeight):
		for x in range(boardWidth - 3):
			if board[x][y] == tile and board[x+1][y] == tile and board[x+2][y] == tile and board[x+3][y] == tile:
				return True
	# check vertical spaces
	for x in range(boardWidth):
		for y in range(boardHeight - 3):
			if board[x][y] == tile and board[x][y+1] == tile and board[x][y+2] == tile and board[x][y+3] == tile:
				return True
	# check / diagonal spaces
	for x in range(boardWidth - 3):
		for y in range(3, boardHeight):
			if board[x][y] == tile and board[x+1][y-1] == tile and board[x+2][y-2] == tile and board[x+3][y-3] == tile:
				return True
	# check \ diagonal spaces
	for x in range(boardWidth - 3):
		for y in range(boardHeight - 3):
			if board[x][y] == tile and board[x+1][y+1] == tile and board[x+2][y+2] == tile and board[x+3][y+3] == tile:
				return True
	return False


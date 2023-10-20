import turtle
import math
import copy

#click on the screen to play. If bot is on, click anywhere on the screen and the bot will play a move
#bot is only ever white player. 

# Constants
boardsize = 600
margin = 50

# Turtle Initialization
t = turtle.Turtle()
s = turtle.Screen()

s.bgcolor('forest green')
s.setup(boardsize, boardsize)
s.tracer(0, 0)


# Data Structure Setup
gameBoard = [[0 for x in range(8)] for y in range(8)]
gameBoard[3][3] = 1
gameBoard[3][4] = -1
gameBoard[4][4] = 1
gameBoard[4][3] = -1
currentPlayer = -1
robotOn = False
#robotOn defines whether the bot is on


def drawBoard():
	t.color('black')
	t.penup()
	t.goto(-200, 200)
	t.pendown()
	t.goto(-200, -200)
	for row in range(9):
		t.penup()
		t.goto(200, 200 - (row*(400/8)))
		t.pendown()
		t.goto(-200, 200 - (row*(400/8)))
		t.penup()
		t.goto(200 - (row*(400/8)), 200)
		t.pendown()
		t.goto(200- (row*(400/8)), -200)

def whichRow(y):
	for row in range (1,9):
		if (200 - ((row-1) * 400/8)) > y > (200 - ((row *(400/8)))):
			return row
			
def whichColumn(x):
	for column in range (1,9):
		if (-200 + ((column-1) * (400/8))) < x < (-200 + (column *(400/8))):
			return column
			
def xFromColumn(column):
	return -200 + (column *50) - 25
	
def yFromRow(row):
	return 200 - (row*50)+25
	
def stampPlayer(row, column, player):
	t.shape('circle')
	t.shapesize(2)
	t.penup
	t.goto(xFromColumn(column), yFromRow(row))
	if player == -1:
		t.color('black')
		t.stamp()
	if player == 1:
		t.color('white')
		t.stamp()
	
def updateBoard(board, player, row, col):
	board2 = copy.deepcopy(board)
	board2[row -1][col -1] = player
	return board2

def calculateScore(board, player):
	return abs(sum([sum([y for y in board[row] if y==player]) for row in range(8)]))
	
def updateScore():
	global robotOn
	if currentPlayer == -1:
		player = 'black'
	if currentPlayer ==1:
		player = 'white'
	t.penup()
	t.goto(-300,250)
	t.color('forest green')
	t.pensize(100)
	t.pendown()
	t.goto(300, 250)
	t.penup()
	t.color('black')
	t.goto(-75, 260)
	t.write('black:', font = 25)
	t.goto(-50, 230)
	t.write(calculateScore(gameBoard, -1), font = 25)
	t.goto(25, 260)
	t.write('white:', font = 25)
	t.goto(50, 230)
	t.write(calculateScore(gameBoard, 1), font = 25)
	t.goto(100, 250)
	t.write(player, font = 25)
	t.goto(135, 250)
	t.write('to play', font = 25)
	if robotOn==True:
		t.goto(-200, 250)
		t.write('white is bot', font = 25)
	
def initialize():
	drawBoard()
	t.penup()
	for r in range(8):
		for c in range(8):
			stampPlayer(r+1, c+1, gameBoard[r][c])
	updateScore()

def initializeBot():
	global robotOn
	robotOn = True
	initialize()
#type this into terminal if you want to play game with bot

def stampBoard():
	for r in range(8):
		for c in range(8):
			stampPlayer(r+1, c+1, gameBoard[r][c])
			if gameBoard[r][c]==0:
				t.color('forest green')
				t.goto(xFromColumn(c+1), yFromRow(r+1))
				t.stamp()

	
def validMove(board, player, row, col):
	a = []
	m=2
	n=2
	if row == 8:
		m = 1
	if col == 8:
		n = 1
	if not(board[row-1][col-1]==0):
		return False
	for h in range(-1, n):
		for v in range(-1, m):
			a += [validMoveDir(board, player, row, col, h, v)]
	return len([i for i in a if i ==True])>0

def validMoveDir(board, player, row, col, h, v):
	r = row -1
	c = col -1
	if r > 7 or r <0 or c > 7 or c <0:
		return False
	if r > 6 and v > 0 or c > 6 and h > 0 or r < 1 and v < 0 or c < 1 and h < 0:
		return False
	if board[r+v][c+h]== 0:
		return False
	if not(board[r][c]==player*-1) and board[r+v][c+h]== player:
		return False
	if board[r+v][c+h] == player:
		return True
	else:
		return validMoveDir(board, player, row+v, col+h, h, v)
# Returns whether or not there is a valid move given a move and direction of validity
# works specifically with validMove

def allMoves(board, player):
	moves = []
	for row in range(1, 9):
		for col in range(1, 9):
			if validMove(board, player, row, col):
				moves += [[row, col]]
	return moves
#returns all valid moves for a given player


def nextBoard(board, player, move):
	b = copy.deepcopy(board)
	for p in positions(board, currentPlayer):
		if p[0]>move[0]:
			v = 1
		if move[0]>p[0]:
			v = -1
		if p[0]==move[0]: 
			v=0
		if p[1]>move[1]:
			h = 1
		if move[1]>p[1]:
			h = -1
		if move[1]==p[1]:
			h=0
		if validMoveSpec(board, player, p, move, h, v):
			m = calcM(p, move, h, v)
			for n in range(m):
				b[(move[0] + v*n)-1][(move[1] + h*n)-1] = player
	return b
#changes a board in accordance with the rules after a valid move 


def validMoveSpec(board, player, pos1, pos2, h, v):
	r = pos2[0]-1
	c = pos2[1]-1
	if pos2[0]+v == pos1[0] and pos2[1]+h == pos1[1]:
		return True
	if pos2[0]+v > 8 or pos2[0]+v <0 or pos2[1]+h > 8 or pos2[1]+h <0:
		return False
	if board[r+v][c+h]== 0:
		return False
	if not(board[r][c]==player*-1) and pos2[0]+v == pos1[0] and pos2[1]+h == pos1[1]:
		return False
	if not(board[r+v][c+h]==player*-1):
		return False
	if pos2[0]+v == pos1[0] and pos2[1]+h == pos1[1]:
		return True
	else:
		return validMoveSpec(board, player, pos1, [pos2[0]+v, pos2[1]+h], h, v)
#is more specific than validMoveDir
#valid move that takes in a move and specific position as well as the direction of validity - useful for nextBoard
#h = horizontal shift, v = vertical shift, pos1 is an existing position, pos2 is the move in question

def calcM(p, move, h, v):
	if v == 1:
		m = p[0]-move[0]
	elif v == -1:
		m = move[0]-p[0]
	elif h == 1:
		m = p[1]-move[1]
	else:
		m = move[1] - p[1]
	return m
# gives number of opposing blocks involved in valid move (# of blocks between the two positions)

def positions(board, player):
	p = []
	for row in range(8):
		for col in range(8):
			if board[row][col] == player:
				p += [[row+1, col+1]]
	return p
#gives the positions of all players on the board 

def gameMove(x, y):
	global gameBoard
	global currentPlayer
	global robotOn
	t.shape('circle')
	t.shapesize(2)
	t.penup()
	for n in allMoves(gameBoard, currentPlayer):
		t.color('forest green')
		t.goto(xFromColumn(n[1]), yFromRow(n[0]))
		t.stamp()
	if gameOver(gameBoard, currentPlayer):
		currentPlayer = currentPlayer*-1
		updateScore()
		print ('no moves')
		if gameOver(gameBoard, currentPlayer):
			print('game over')
			return[]
	if robotOn == True:
		if currentPlayer == 1:
			move = minimax(gameBoard, 1, -1000, 1000, 7)[0]
			print(move)
			x = xFromColumn(move[1])
			y = yFromRow(move[0])
	if -200< x<200 and -200< y < 200:
		if validMove(gameBoard, currentPlayer, whichRow(y), whichColumn(x)):
			gameBoard = nextBoard(gameBoard, currentPlayer, [whichRow(y), whichColumn(x)])
			for r in range(8):
				for c in range(8):
					stampPlayer(r+1, c+1, gameBoard[r][c])
			currentPlayer=currentPlayer *-1
			updateScore()
			for m in allMoves(gameBoard, currentPlayer):
				t.color('red')
				t.goto(xFromColumn(m[1]), yFromRow(m[0]))
				t.stamp()
#algorithm for a click on screen

s.onscreenclick(gameMove)	
	
def evaluate(board, player):
		return calculateScore(board, 1) - calculateScore(board, -1)
#evaluation function gives difference in score

def gameOver(board, player):
	return len(allMoves(board, player)) == 0

def minimax(board, p, alpha, beta, i ):
	print('.')
	if gameOver(board, p):
		p = p *-1
		if gameOver(board, p):
			return [[], evaluate(board, p)*20]
	a = allMoves(board, p)
	if i==1 or len(a) == 1:
		return [allMoves(board, p)[0], evaluate(board, p)]
	elif p == 1:
		maxC = -1000
		for child in [[m, nextBoard(board, p, m)] for m in a]: 
			c = minimax(child[1], p*-1, alpha, beta, i-1)[1]
			if c >= maxC:
				maxC = c
				maxM = child[0]
			if c > alpha:
				alpha = c
			if beta <= alpha:
				return [[], maxC]
		return [maxM, c]
	elif p == -1:
		minC = 1000
		for child in [[m, nextBoard(board, p, m)] for m in a]:
			c = minimax(child[1], p*-1, alpha, beta, i-1)[1]
			if c <= minC:
				minC = c
				minM = child[0]
			if c < beta:
				beta = c
			if beta <= alpha:
				return [[], c]
		return [minM, minC]
# My minimax with alpha beta pruning. i = the number of rounds deep into the game the algorithm searches

initializeBot()
#starts game
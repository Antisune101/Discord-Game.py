import discord
from discord.ext import commands
import random

client = discord.Client()
client = commands.Bot(command_prefix='.')

games = {}

##variables
class game(object):
	def __init__(self, player, channel):
		self.board = {1: '#', 2: '#', 3: '#', 4: '#', 5: '#', 6: '#', 7: '#', 8: '#', 9: '#'}
		self.player_token = 'O'
		self.bot_token = 'X'
		self.botStarts = False
		self.gameOver = False
		self.player = player
		self.channel = channel
		self.playerTurn = False

	async def printBoard(self):
		board_message = '\n' + self.board[1] + '|' + self.board[2] + '|' + self.board[3] + '\n' + self.board[4] + '|' + self.board[5] + '|' + self.board[6] + '\n' + self.board[7] + '|' + self.board[8] + '|' + self.board[9]
		await self.channel.send(board_message)

	def spaceIsFree(self, position):
		if self.board[int(position)] == '#':
			return True
		else:
			return False

	async def insertLetter(self, letter, position):
		if self.spaceIsFree(position):
			self.board[position] = letter
			await self.printBoard()
			if self.checkDraw():
				print("It's a Draw")
				gameOver = True
				if self.requestRestart():
					self.startGame(True, 'draw')
				else:
					exit()
			if self.checkForWin():
				self.gameOver = False
				if letter == 'X':
					print("Bot wins!")
					if self.requestRestart():
						self.startGame(True, 'bot')
					else:
						exit()
				else:
					print("Player wins!")
					if self.requestRestart():
						self.startGame(True, 'player')
			return
		elif self.playerTurn:
			await self.channel.send("Position is not Available")
		
		else:
			print("Can't insert there!")
			position = int(input("Please enter new position:  "))
			await self.insertLetter(letter, position)
		return

	def checkForWin(self):
		if (self.board[1] == self.board[2] and self.board[1] == self.board[3] and self.board[1] != '#'):
			return True
		elif (self.board[4] == self.board[5] and self.board[4] == self.board[6] and self.board[4] != '#'):
			return True
		elif (self.board[7] == self.board[8] and self.board[7] == self.board[9] and self.board[7] != '#'):
			return True
		elif (self.board[1] == self.board[4] and self.board[1] ==self. board[7] and self.board[1] != '#'):
			return True
		elif (self.board[2] == self.board[5] and self.board[2] == self.board[8] and self.board[2] != '#'):
			return True	
		elif (self.board[3] == self.board[6] and self.board[3] == self.board[9] and self.board[3] != '#'):
			return True
		elif (self.board[1] == self.board[5] and self.board[1] == self.board[9] and self.board[1] != '#'):
			return True
		elif (self.board[7] == self.board[5] and self.board[7] == self.board[3] and self.board[7] != '#'):
			return True
		else:
			return False

	def checkWhichMarkWon(self, mark):
		if (self.board[1] == self.board[2] and self.board[1] == self.board[3] and self.board[1] != mark):
			return True
		elif (self.board[4] == self.board[5] and self.board[4] == self.board[6] and self.board[4] != mark):
			return True
		elif (self.board[7] == self.board[8] and self.board[7] == self.board[9] and self.board[7] != mark):
			return True
		elif (self.board[1] == self.board[4] and self.board[1] ==self. board[7] and self.board[1] != mark):
			return True
		elif (self.board[2] == self.board[5] and self.board[2] == self.board[8] and self.board[2] != mark):
			return True	
		elif (self.board[3] == self.board[6] and self.board[3] == self.board[9] and self.board[3] != mark):
			return True
		elif (self.board[1] == self.board[5] and self.board[1] == self.board[9] and self.board[1] != mark):
			return True
		elif (self.board[7] == self.board[5] and self.board[7] == self.board[3] and self.board[7] != mark):
			return True
		else:
			return False

	def checkDraw(self):
		for key in self.board.keys():
			if (self.board[key] == '#'):
				return False
		return True

	async def playerMove(self, position:int):
		if self.playerTurn:
			if position  in range(1, 9):
				await self.channel.send("Invalid Position")
				print("Hello")
				return
			await self.insertLetter(self.player_token, position)
			self.playerTurn = False
			return
		else:
			await self.channel.send("Its not your Turn {}".format(self.player))

	async def compMove(self):
		bestScore = -800
		bestMove = 0
		for key in self.board.keys():
			if (self.board[key] == '#'):
				self.board[key] = self.bot_token
				score = self.minimax(self.board, 0, False)
				self.board[key] = '#'
				if (score > bestScore):
					bestScore = score
					bestMove = key

		await self.insertLetter(self.bot_token, bestMove)
		self.playerTurn = True
		await self.channel.send("Bot plays {}".format(bestMove))
		return

	def minimax(self, board, depth, isMaximizing):
		if (self.checkWhichMarkWon(self.bot_token)):
			return 100
		elif (self.checkWhichMarkWon(self.player_token)):
			return -100
		elif (self.checkDraw()):
			return 0

		if (isMaximizing):
			bestScore = -800
			for key in self.board.keys():
				if (board[key] == '#'):
					self.board[key] = self.bot
					score = self.minimax(board, depth + 1, False)
					self.board[key] = '#'
					if (score > bestScore):
						bestScore = score
			return bestScore

		else:
			bestScore = 800
			for key in self.board.keys():
				if (self.board[key] == '#'):
					self.board[key] = self.player_token
					score = self.minimax(self.board, depth + 1, True)
					self.board[key] = '#'
					if (score < bestScore):
						bestScore = score
			return bestScore

	async def startGame(self):
		botStarts = bool(random.randint(0, 1))
		if botStarts:
				self.playerTurn = False
		else:
				self.playerTurn = True
		
		if not botStarts:
			await self.channel.send("{} goes first".format(self.player))
			await self.printBoard()
		else:
			await self.channel.send("Bot goes first againts {}".format(self.player))
		while not self.gameOver:
			while not self.playerTurn:
				await self.compMove()

@client.command()
async def play(ctx, position):
	print("pls Print")
	if (ctx.message.author in games):
		print("Me First")
		await games[ctx.message.author].playerMove(int(position))
		print("hello")
		return
	else:
		await ctx.send("You are not in a game use .start to start one")
		print("something")
		return

@client.command()
async def start(ctx):
	if (ctx.message.author not in games):
		games[ctx.message.author] = game(ctx.message.author, ctx.channel)
		await games[ctx.message.author].startGame()
		return
	else:
		await ctx.send("You are already in a game use .stop to stop the current game")

@client.event
async def on_ready():
    print("logged in")

client.run("ODIyMDgwODQ0ODk0MDQ0MTcx.YFNEcg.KrIGkmAIBQeifqWbi_JP5L3v0oM")
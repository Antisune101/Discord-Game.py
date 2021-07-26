import discord
from discord.ext import commands
import random
import asyncio

client = discord.Client()
client = commands.Bot(command_prefix='.')

##variables
class game(object):
	def __init__(self, player, channel):
		self.board = {1: ' ', 2: ' ', 3: ' ', 4: ' ', 5: ' ', 6: ' ', 7: ' ', 8: ' ', 9: ' '}
		self.player_token = 'O'
		self.bot_token = 'X'
		self.botStarts = False
		self.gameOver = False
		self.player = player
		self.startGame(False, 'player')
		self.channel = channel

	async def printBoard(self):
		board_message = ''
		board_message += self.board[1] + '|' + self.board[2] + '|' + self.board[3] + '\n'
		board_message += self.board[4] + '|' + self.board[5] + '|' + self.board[6] + '\n'
		board_message += self.board[7] + '|' + self.board[8] + '|' + self.board[9]

		await self.channel.send(board_message)

	def spaceIsFree(self, position):
		if self.board[position] == ' ':
			return True
		else:
			return False

	def insertLetter(self, letter, position):
		if self.spaceIsFree(position):
			self.board[position] = letter
			#self.printBoard()
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
		else:
			print("Can't insert there!")
			position = int(input("Please enter new position:  "))
			self.insertLetter(letter, position)
		return

	def checkForWin(self):
		if (self.board[1] == self.board[2] and self.board[1] == self.board[3] and self.board[1] != ' '):
			return True
		elif (self.board[4] == self.board[5] and self.board[4] == self.board[6] and self.board[4] != ' '):
			return True
		elif (self.board[7] == self.board[8] and self.board[7] == self.board[9] and self.board[7] != ' '):
			return True
		elif (self.board[1] == self.board[4] and self.board[1] ==self. board[7] and self.board[1] != ' '):
			return True
		elif (self.board[2] == self.board[5] and self.board[2] == self.board[8] and self.board[2] != ' '):
			return True	
		elif (self.board[3] == self.board[6] and self.board[3] == self.board[9] and self.board[3] != ' '):
			return True
		elif (self.board[1] == self.board[5] and self.board[1] == self.board[9] and self.board[1] != ' '):
			return True
		elif (self.board[7] == self.board[5] and self.board[7] == self.board[3] and self.board[7] != ' '):
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
			if (self.board[key] == ' '):
				return False
		return True

	def playerMove(self):
		position = 0
		while not position in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
			position = int(input("Enter the position for 'O':  "))
		self.insertLetter(self.player_token, position)
		return

	def compMove(self):
		bestScore = -800
		bestMove = 0
		for key in self.board.keys():
			if (self.board[key] == ' '):
				self.board[key] = self.bot_token
				score = self.minimax(self.board, 0, False)
				self.board[key] = ' '
				if (score > bestScore):
					bestScore = score
					bestMove = key

		self.insertLetter(self.bot_token, bestMove)
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
				if (board[key] == ' '):
					self.board[key] = self.bot
					score = self.minimax(board, depth + 1, False)
					self.board[key] = ' '
					if (score > bestScore):
						bestScore = score
			return bestScore

		else:
			bestScore = 800
			for key in self.board.keys():
				if (self.board[key] == ' '):
					self.board[key] = self.player_token
					score = self.minimax(self.board, depth + 1, True)
					self.board[key] = ' '
					if (score < bestScore):
						bestScore = score
			return bestScore

	async def startGame(self, isRematch, winner):
		self.gameOver = False
		self.board = {1: ' ', 2: ' ', 3: ' ', 4: ' ', 5: ' ', 6: ' ', 7: ' ', 8: ' ', 9: ' '}
		if isRematch:
			if (winner == 'player'):
				botStarts = False
			if (winner == 'bot'):
				botStarts = True
			if (winner == 'draw'):
				botStarts = bool(random.randint(0, 1))
		else:
			botStarts = bool(random.randint(0, 1))
		if botStarts:
			while not self.gameOver:
				self.compMove()
				self.playerMove()
		else:
			await self.printBoard()
			while not self.gameOver:
				self.playerMove()
				self.compMove()

@client.command()
async def start(ctx):
	session = game(ctx.message.author, ctx.channel)
	await session.printBoard()

@client.event
async def on_ready():
    print("logged in")


client.run("ODIyMDgwODQ0ODk0MDQ0MTcx.YFNEcg.KrIGkmAIBQeifqWbi_JP5L3v0oM")
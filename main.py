import discord
from discord.ext import commands
import random

client = discord.Client()
client = commands.Bot(command_prefix='.')

games = {}

def endGame(current_game):
	for keys in games.keys():
		if games[keys] == current_game:
			games.pop(keys)
			break
		else:
			continue
##variables
class game:
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
				self.gameOver = True
				await self.channel.send("It's a Draw")
				endGame(self)
			if self.checkForWin():
				self.gameOver = True
				if letter == self.bot_token:
					await self.channel.send("Bot wins!")
					endGame(self)
				else:
					self.gameOver = True
					await self.channel.send("Player wins!")
					endGame(self)
			if letter == self.player_token and not self.gameOver:
				await self.channel.send("{} plays {}".format(self.player, str(position)))
				await self.compMove()
			if letter == self.bot_token and not self.gameOver:
				await self.channel.send("Bot plays {} against {}".format(str(position), self.player))
		elif self.playerTurn:
			await self.channel.send("Position is not Available")
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
		if (self.board[1] == self.board[2] and self.board[1] == self.board[3] and self.board[1] == mark):
			return True
		elif (self.board[4] == self.board[5] and self.board[4] == self.board[6] and self.board[4] == mark):
			return True
		elif (self.board[7] == self.board[8] and self.board[7] == self.board[9] and self.board[7] == mark):
			return True
		elif (self.board[1] == self.board[4] and self.board[1] ==self. board[7] and self.board[1] == mark):
			return True
		elif (self.board[2] == self.board[5] and self.board[2] == self.board[8] and self.board[2] == mark):
			return True	
		elif (self.board[3] == self.board[6] and self.board[3] == self.board[9] and self.board[3] == mark):
			return True
		elif (self.board[1] == self.board[5] and self.board[1] == self.board[9] and self.board[1] == mark):
			return True
		elif (self.board[7] == self.board[5] and self.board[7] == self.board[3] and self.board[7] == mark):
			return True
		else:
			return False

	def checkDraw(self):
		for key in self.board.keys():
			if (self.board[key] == '#'):
				return False
		return True

	async def playerMove(self, position:int):
			if position not in range(1, 10):
				await self.channel.send("Invalid Position {}".format(position))
				return
			else:
				await self.insertLetter(self.player_token, position)
				self.playerTurn = False
				return

	async def compMove(self):
		bestScore = -800
		bestMove = 0
		for key in self.board.keys():
			if (self.board[key] == '#'):
				self.board[key] = self.bot_token
				score = self.minimax(False)
				self.board[key] = '#'
				if (score > bestScore):
					bestScore = score
					bestMove = key
		await self.insertLetter(self.bot_token, bestMove)
		return

	def minimax(self, isMaximizing):
		if (self.checkWhichMarkWon(self.bot_token)):
			return 100
		elif (self.checkWhichMarkWon(self.player_token)):
			return -100
		elif (self.checkDraw()):
			return 0

		if (isMaximizing):
			bestScore = -800
			for key in self.board.keys():
				if (self.board[key] == '#'):
					self.board[key] = self.bot_token
					score = self.minimax(False)
					self.board[key] = '#'
					if (score > bestScore):
						bestScore = score
			return bestScore

		else:
			bestScore = 800
			for key in self.board.keys():
				if (self.board[key] == '#'):
					self.board[key] = self.player_token
					score = self.minimax(True)
					self.board[key] = '#'
					if (score < bestScore):
						bestScore = score
			return bestScore

	async def startGame(self):
		botStarts = bool(random.randint(0, 1))
		if not botStarts:
			await self.channel.send("@{} goes first".format(self.player))
			await self.printBoard()
		else:
			await self.channel.send("Bot goes first againts {}".format(self.player))
			await self.compMove()

@client.command()
async def push(ctx, position):
	if (ctx.message.author in games.keys()):
		if ( not games[ctx.message.author].gameOver):
			await games[ctx.message.author].playerMove(int(position))
			return
	else:
		await ctx.send("You are not in a game use .start to start one")
		return

@client.command()
async def start(ctx):
	if (ctx.message.author not in games.keys()):
		games[ctx.message.author] = game(ctx.message.author, ctx.channel)
		print("Starting")
		await games[ctx.message.author].startGame()
	else:
		print("Not Starting")
		await ctx.send("You are already in a game use .stop to stop the current game")

@client.event
async def on_ready():
    print("logged in as {}".format(client.user))

client.run("ODIyMDgwODQ0ODk0MDQ0MTcx.YFNEcg.KrIGkmAIBQeifqWbi_JP5L3v0oM")
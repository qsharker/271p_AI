# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================
from AI import AI
from Action import Action
import traceback
import sys


class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
		self.rowDimension = rowDimension
		self.colDimension = colDimension
		self.totalMines = totalMines
		self.UncvrSet = set()
		self.flagSet = set()
		self.blckWClue = set()
		self.map = [[None for x in range(colDimension)] for y in range(rowDimension)]
		self.isStart = True
		self.x = startX
		self.y = startY
		self.action = AI.Action.UNCOVER

	def getAdjBlck(self, x, y):
		minx = max(x - 1, 0)
		maxX = min(x + 1 + 1, self.colDimension)
		minY = max(y - 1, 0)
		maxY = min(y + 1 + 1, self.colDimension)
		for _y in range(minY, maxY):
			for _x in range(minx, maxX):
				if not (_x == x and _y == y):
					yield (_x, _y)

	def markAllNghbrSafe(self, x, y):
		for (_x, _y) in self.getAdjBlck(x, y):
			if self.map[_y][_x] is None:
				self.UncvrSet.add((_x, _y))
		return


	def UncvrRandom(self):
		pass

	def getUncover(self)->('x', 'y'):
		if len(self.UncvrSet) != 0:
			return self.UncvrSet.pop()
		else:
			return self.UncvrRandom()

	def updateMap(self):
		if self.map[self.y][self.x] == 0:
			self.markAllNghbrSafe(self.x, self.y)
			return
		for x, y in self.blckWClue:
			self.solveClue(x, y)


	def markNgbrMine(self, x, y):
		for _x, _y in self.getAdjBlck(x, y):
			if self.map[_y][_x] is None:
				self.flagSet.add((_x, _y))
				self.map[_y][_x] = 'f'

	def solveClue(self, x, y):
		numUnopenBlck = 0
		numMine = 0
		for a_x, a_y in self.getAdjBlck(x, y):
			if (self.map[a_y][a_x] is None):
				numUnopenBlck += 1
			elif (self.map[a_y][a_x] is 'f'):
				numMine += 1 
		
		if self.map[y][x] == numMine:
			self.markAllNghbrSafe(x, y)
		elif self.map[y][x] == (numUnopenBlck + numMine):
			self.markNgbrMine(x, y)


	def getAction(self, number: int) -> "Action Object":
		try:
			if self.isStart:
				self.map[self.y][self.x] = number
				self.isStart = False

			elif (self.action == AI.Action.UNCOVER):
				self.map[self.y][self.x] = number
				if number > 0:
					self.blckWClue.add((self.x, self.y))

			elif self.action == AI.Action.FLAG:
				self.map[self.y][self.x] = "f"

			elif self.action == AI.Action.UNFLAG:
				self.map[self.y][self.x] = None

			self.updateMap()

			if len(self.UncvrSet) > 0:
				self.action = AI.Action.UNCOVER
				(self.x, self.y) = self.getUncover()

			elif len(self.flagSet) > 0:
				self.action = AI.Action.FLAG
				self.x, self.y = self.flagSet.pop()


			return Action(self.action, self.x, self.y)

		except:
			pass
			#exc_info = sys.exc_info()
			#traceback.print_exc(*exc_info)

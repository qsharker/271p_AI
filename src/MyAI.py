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
		self.uncvrSet = set()
		self.flagSet = set()
		self.unsolvedBlcks = set()	# the blocks with hints and in the boarder
		self.map = [[None for x in range(colDimension)] for y in range(rowDimension)]
		self.x = startX
		self.y = startY
		self.action = AI.Action.UNCOVER

	def getAdjBlck(self, x, y):
		minx = max(x - 1, 0)
		maxX = min(x + 1 + 1, self.colDimension)
		minY = max(y - 1, 0)
		maxY = min(y + 1 + 1, self.rowDimension)
		for _y in range(minY, maxY):
			for _x in range(minx, maxX):
				if not (_x == x and _y == y):
					yield (_x, _y)

	def markAllNghbrSafe(self, blcks):
		for _x, _y in blcks:
			self.uncvrSet.add((_x, _y))

	def UncvrRandom(self):
		pass

	def getUncover(self)->('x', 'y'):
		if len(self.uncvrSet) != 0:
			return self.uncvrSet.pop()
		else:
			return self.UncvrRandom()

	def updateMap(self, number):
		if number >= 0:
			# perceive a hint
			self.map[self.y][self.x] = number
			self.solveClue(self.x, self.y)
		else:
			# perceive -1 following a FLAG or UNFLAG
			self.map[self.y][self.x] = 'f' if self.action == AI.Action.FLAG else None

		for _x, _y in set(self.unsolvedBlcks):
			self.solveClue(_x, _y)

	def markMine(self, blcks):
		for _x, _y in blcks:
			self.flagSet.add((_x, _y))

	def solveClue(self, x, y):
		numUnopenBlck = set()
		numMine = set()
		clue = self.map[y][x]
		for a_x, a_y in self.getAdjBlck(x, y):
			if self.map[a_y][a_x] is None:
				numUnopenBlck.add((a_x, a_y))
			elif self.map[a_y][a_x] is 'f':
				numMine.add((a_x, a_y))

		if (x, y) in self.unsolvedBlcks:
			self.unsolvedBlcks.remove((x, y))
		if clue == len(numMine):
			self.markAllNghbrSafe(numUnopenBlck)
		elif clue == len(numUnopenBlck) + len(numMine):
			self.markMine(numUnopenBlck)
		else:
			self.unsolvedBlcks.add((x, y))

	def categorizeBorders(self):
		"""
		Categorize border blocks by their connectivity.
		The borders which connect with others will be grouped together
		:param blocks: List[coordinates]
		:return: List[connected borders]
		"""
		def dfs(map, x, y, ans):
			if x < 0 or x >= self.colDimension or \
				y < 0 or y >= self.rowDimension or \
				map[y][x] == 0:
					return
			map[y][x] = 0
			ans.append((x,y))
			dfs(map, x + 1, y, ans)
			dfs(map, x - 1, y, ans)
			dfs(map, x, y + 1, ans)
			dfs(map, x, y - 1, ans)

		ans = []
		map = [[0 for _x in range(self.colDimension)] for _y in range(self.rowDimension)]
		for x,y in self.unsolvedBlcks:
			map[y][x] = 1

		for i in range(self.rowDimension):
			for j in range(self.colDimension):
				if map[i][j] == 1:
					grp = []
					dfs(map, j, i, grp)
					ans.append(grp)
		return ans

	def getAction(self, number: int) -> "Action Object":
		try:
			self.updateMap(number)

			if len(self.uncvrSet) > 0:
				self.action = AI.Action.UNCOVER
				self.x, self.y = self.getUncover()
			elif len(self.flagSet) > 0:
				self.action = AI.Action.FLAG
				self.x, self.y = self.flagSet.pop()
			else:
				self.action = AI.Action.LEAVE

			return Action(self.action, self.x, self.y)

		except:
			#pass
			exc_info = sys.exc_info()
			traceback.print_exc(*exc_info)


if __name__ == '__main__':
	ai = MyAI(4,4,1,0,1)
	ai.unsolvedBlcks = {(0,1),(1,0),(1,1),(2,2),(2,3),(3,2)}
	print(ai.categorizeBorders())
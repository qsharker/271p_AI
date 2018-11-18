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
import numpy as np
#import pandas as pd


class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
		self.rowDimension = rowDimension
		self.colDimension = colDimension
		self.totalMines = totalMines
		self.uncvrSet = set()
		self.flagSet = set()
		self.foundMines = 0
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

	def solveMatrix(self, brds: []):
		# pd.set_option('display.expand_frame_repr', False)
		# m = pd.DataFrame(self.map)

		for b in brds:
			unOpenTile, eqMtx, resMtx = self.createMatrix(b)
			UnopnLoc = sorted(unOpenTile.items(), key=lambda x: x[1])
			getUnpnXY = lambda ind: UnopnLoc[ind][0]

			# def remvMtxElm(loc, val):
			# 	ind = unOpenTile[loc]
			# 	# instead of putting new clue in matrix how about make the col == 0 and subtract (val * col) to res

			for i in range(1, len(b)):
				eqDiff  =  eqMtx[i] - eqMtx[i - 1]  if resMtx[i] > resMtx[i - 1] else eqMtx[i - 1] - eqMtx[i]
				resDiff = resMtx[i] - resMtx[i - 1] if resMtx[i] > resMtx[i - 1] else resMtx[i - 1] - resMtx[i]

				lambda x: np.argwhere(x)
				isNeg 	= eqDiff <= 0
				isNegOne = eqDiff == -1
				isOne 	= eqDiff == 1
				isZero = eqDiff == 0
				diffInd = np.argwhere(eqMtx[i] != eqMtx[i - 1])

				if len(diffInd) == 1:
					### for situation of [ 1 0 0 0] = 1/ 0
					colInd = diffInd[0][0]
					loc = getUnpnXY(colInd)
					if (resMtx[i] - resMtx[i - 1]) == 0:
						self.uncvrSet.add(loc)
					else:
						self.flagSet.add(loc)

				if resDiff == 1:
					### for situation of [1 0 0 -1] = 1
					oneInd = np.argwhere(isOne)
					negOneInd = np.argwhere(isNegOne)

					if len(oneInd) == 1 and len(negOneInd) == 1:
						mine = getUnpnXY(oneInd[0][0])
						safe = getUnpnXY(negOneInd[0][0])
						self.flagSet.add(mine)
						self.uncvrSet.add(safe)
						# self.remvMtxElm(mine, 1)
						# self.remvMtxElm(safe, 0)

				elif resDiff == 0 and isNeg.sum() == 0:
					## for [0 1 1 1 0] = 0
					oneIndex = np.argwhere(isOne)[0]
					for oneI in oneIndex:
						loc = getUnpnXY(oneI)
						self.uncvrSet.add(loc)


	def createMatrix(self, b: []):
		unOpenTile = dict()
		nbrMine = dict()
		## count mine and unopen tile info for each border tile
		for x, y in b:
			for nbx, nby in self.getAdjBlck(x, y):
				if (self.map[nby][nbx] is None) and ((nbx, nby) not in unOpenTile):
					unOpenTile[(nbx, nby)] = len(unOpenTile)
				if self.map[nby][nbx] == 'f':
					nbrMine[(x, y)] = 1 if (x, y) not in nbrMine else nbrMine[(x, y)] + 1

		## Putting border info into matrix
		resMtx = np.zeros(len(b))
		eqMtx = np.zeros((len(b), len(unOpenTile)))
		for i, loc in enumerate(b):
			x, y = loc
			numMine = nbrMine[(x, y)] if (x, y) in nbrMine else 0
			resMtx[i] = self.map[y][x] - numMine
			for nbx, nby in self.getAdjBlck(x, y):
				if self.map[nby][nbx] is None:
					eqMtx[i][unOpenTile[(nbx, nby)]] = 1

		return unOpenTile, eqMtx, resMtx



					

			# if len(unOpenTile) <= totalEq:
			# 	for i, tile in enumerate(np.linalg.solve(eqMtx, resMtx)):
			# 		loc = sortTileOrd[i][0]
			# 		if tile == 1:
			# 			self.flagSet.add(loc)
			# 		else:
			# 			self.uncvrSet.add(loc)


			# 	resMtx = np.zero((len(b), 1))
			# 	eqMtx = np.zero((len(b), len(unOpenTile)))
			#
			# 	for i, loc in enumerate(b):
			# 		x, y = loc
			# 		resMtx[i] = self.map[y][x] - nbrMine[(x, y)]
			# 		for nbx, nby in self.getAdjBlck(x, y):
			# 			if self.map[nbx, nby] is None:
			# 				eqMtx[i][unOpenTile[(nbx, nby)]] = 1
			#
			# 	unopnTilOrd = sorted(unOpenTile.items(), lambda x: x[1])

	# def solveBy(self):
	# 	total_border_unOpen = set()
	# 	total_border_mineLeft = 0
	# 	for x, y in self.unsolvedBlcks:
	# 		unOpen = set()
	# 		mine = 0
	# 		for ngbrx, ngbry in self.getAdjBlck(x, y):
	# 			if self.map[ngbry][ngbrx] is None:
	# 				unOpen.add((ngbrx, ngbry))
	# 			elif self.map[ngbry][ngbrx] == 'f':
	# 				mine += 1
	# 		mineLeft = self.map[y][x] - mine
	# 		total_border_unOpen |= unOpen
	# 		total_border_mineLeft += mineLeft
	# 	total_unOpen = self.getAllunOpenBlck()
	# 	total_mineLeft = self.totalMines - self.foundMines
	# 	if total_mineLeft - total_border_mineLeft <= 0:
	# 		for _x, _y in total_unOpen - total_border_unOpen:
	# 			self.uncvrSet.add((_x, _y))


	def markAllNghbrSafe(self, blcks):
		for _x, _y in blcks:
			self.uncvrSet.add((_x, _y))

	def UncvrRandom(self):
		minPb = 1.
		for x, y in self.unsolvedBlcks:
			none = 0.
			mine = 0.
			for ngbrx, ngbry in self.getAdjBlck(x, y):
				if self.map[ngbry][ngbrx] is None:
					none += 1.
				elif self.map[ngbry][ngbrx] == 'f':
					mine += 1

			pb = (self.map[y][x] - mine) / none
			if pb < minPb:
				minPb = pb
				tile = (x, y)
		for ngbrx, ngbry in self.getAdjBlck(*tile):
			if self.map[ngbry][ngbrx] is None:
				return (ngbrx, ngbry)


	def getAllunOpenBlck(self):
		ans = set()
		for _y in range(self.rowDimension):
			for _x in range(self.colDimension):
				if self.map[_y][_x] is None:
					ans.add((_x, _y))
		return ans


	def getUncover(self)->('x', 'y'):
		if len(self.uncvrSet) != 0:
			return self.uncvrSet.pop()
		else:
			return self.UncvrRandom()

	def hasAction(self):
		return len(self.uncvrSet) > 0 or len(self.flagSet) > 0

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

		if not self.hasAction():
			brds = self.categorizeBorders()
			self.solveMatrix(brds)


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
		:return: List[List[(x,y)]]
		"""
		def dfs(visited, x, y, ans):
			if x < 0 or x >= self.colDimension or \
				y < 0 or y >= self.rowDimension or \
				(x, y) not in self.unsolvedBlcks or (x, y) in visited:
					return
			visited.add((x,y))
			ans.append((x,y))
			dfs(visited, x + 1, y, ans)
			dfs(visited, x - 1, y, ans)
			dfs(visited, x, y + 1, ans)
			dfs(visited, x, y - 1, ans)

		ans = []
		visited = set()
		for x,y in self.unsolvedBlcks:
			if (x,y) not in visited:
				grp = []
				dfs(visited, x, y, grp)
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
				self.foundMines += 1
			elif len(self.unsolvedBlcks) > 0:
				self.action = AI.Action.UNCOVER
				self.x, self.y = self.UncvrRandom()
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
	borders = ai.categorizeBorders()
	print(ai.createMatrix(borders[0]))
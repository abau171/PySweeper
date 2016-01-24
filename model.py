import random

class Items:
	MINE = -1
	DIRT = -2
	FLAG = -3
	UNSURE = -4

class Grid:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.grid = [[None for row in range(self.height)] for col in range(self.width)]
	def get(self, x, y):
		return self.grid[x][y]
	def has(self, x, y):
		return x >= 0 and x < self.width and y >= 0 and y < self.height
	def coords(self):
		for x in range(self.width):
			for y in range(self.height):
				yield (x, y)
	def surrounding(self, x, y):
		for dx in range(-1, 2):
			for dy in range(-1, 2):
				if dx == 0 and dy == 0:
					continue
				surrX = x + dx
				surrY = y + dy
				if self.has(surrX, surrY):
					yield (surrX, surrY)

class MineGrid(Grid):
	def __init__(self, width, height, numMines):
		Grid.__init__(self, width, height)
		self.populateGrid(numMines)
		self.calculateProximities()
	def populateGrid(self, numMines):
		for i in range(numMines):
			minePlanted = False
			while not minePlanted:
				col = random.randint(0, self.width - 1)
				row = random.randint(0, self.height - 1)
				if self.grid[col][row] == None:
					self.grid[col][row] = Items.MINE
					minePlanted = True
	def calculateProximities(self):
		for (x, y) in self.coords():
			if self.grid[x][y] == Items.MINE:
				continue
			self.grid[x][y] = self.calculateProximity(x, y)
	def calculateProximity(self, x, y):
		proximity = 0
		for (checkX, checkY) in self.surrounding(x, y):
			if self.grid[checkX][checkY] == Items.MINE:
				proximity += 1
		return proximity

class VisibilityGrid(Grid):
	def __init__(self, width, height, numMines):
		Grid.__init__(self, width, height)
		self.mineGrid = MineGrid(width, height, numMines)
		self.fillWithDirt()
	def fillWithDirt(self):
		for (x, y) in self.coords():
			self.grid[x][y] = Items.DIRT
	def get(self, x, y):
		mask = Grid.get(self, x, y)
		if mask == None:
			return self.mineGrid.get(x, y)
		else:
			return mask

class ModelState:
	PLAYING = 0
	SOLVED = 1
	FAILED = 2

class PySweeperModel(VisibilityGrid):
	"""Also keeps track of number of mines that exist, number of
	mines thought to be left, solve/fail state, etc."""
	def __init__(self, width, height, numMines):
		VisibilityGrid.__init__(self, width, height, numMines)
		self.numMines = numMines
		self.numFlags = 0
		self.numSlots = width * height
		self.numDug = 0
		self.state = ModelState.PLAYING
	def isPlaying(self):
		return self.state == ModelState.PLAYING
	def isSolved(self):
		return self.state == ModelState.SOLVED
	def isFailed(self):
		return self.state == ModelState.FAILED
	def getNumMines(self):
		return self.numMines
	def getNumMinesLeft(self):
		return self.numMines - self.numFlags
	def dig(self, x, y):
		if self.state == ModelState.PLAYING:
			if self.get(x, y) == Items.DIRT:
				self.uncover(x, y)
				dugUp = self.mineGrid.get(x, y)
				if dugUp == Items.MINE:
					self.state = ModelState.FAILED
				elif self.numDug == self.numSlots - self.numMines:
					self.state = ModelState.SOLVED
			else:
				pass
				# TODO raise can only dig dirt exception
		else:
			pass
			# TODO raise incorrect state exception
	def uncover(self, x, y):
		if self.grid[x][y] == Items.FLAG:
			self.numFlags -= 1
		self.numDug += 1
		self.grid[x][y] = None
		# TODO perform BFS to reduce number of recursive calls
		if self.mineGrid.get(x, y) == 0:
			for (surrX, surrY) in self.surrounding(x, y):
				if self.grid[surrX][surrY] != None:
					self.uncover(surrX, surrY)
	def toggleFlag(self, x, y):
		if self.state == ModelState.PLAYING:
			curr = self.grid[x][y]
			if curr == Items.DIRT:
				next = Items.FLAG
				self.numFlags += 1
			elif curr == Items.FLAG:
				next = Items.UNSURE
				self.numFlags -= 1
			elif curr == Items.UNSURE:
				next = Items.DIRT
			else:
				pass
				# TODO raise incorrect toggle exception
			self.grid[x][y] = next
		else:
			pass
			# TODO raise incorrect state exception
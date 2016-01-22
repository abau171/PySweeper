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
	def getWidth(self):
		return self.width
	def getHeight(self):
		return self.height
	def coords(self):
		return GridIter(self)
	def surrounding(self, x, y):
		return GridSurroundingIter(self, x, y)

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

class GridIter:
	def __init__(self, grid):
		self.grid = grid
		self.x = -1
		self.y = 0
	def __iter__(self):
		return self
	def __next__(self):
		self.x += 1
		if self.x >= self.grid.getWidth():
			self.x = 0
			self.y += 1
		if self.y >= self.grid.getHeight():
			raise StopIteration
		return (self.x, self.y)

class GridSurroundingIter:
	def __init__(self, grid, x, y):
		self.grid = grid
		self.x = x
		self.y = y
		self.dx = -2
		self.dy = -1
	def __iter__(self):
		return self
	def __next__(self):
		result = None
		while result == None:
			self.dx += 1
			if self.dx == 0 and self.dy == 0:
				self.dx += 1
			if self.dx > 1:
				self.dx = -1
				self.dy += 1
			if self.dy > 1:
				raise StopIteration
			surrX = self.x + self.dx
			surrY = self.y + self.dy
			if surrX >= 0 and surrX < self.grid.getWidth():
				if surrY >= 0 and surrY < self.grid.getHeight():
					result = (surrX, surrY)
		return result

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
		self.state = ModelState.PLAYING
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
			else:
				pass
				# TODO raise can only dig dirt exception
		else:
			pass
			# TODO raise incorrect state exception
	def uncover(self, x, y):
		self.grid[x][y] = None
		# TODO perform BFS to reduce number of recursive calls
		if self.mineGrid.get(x, y) == 0:
			for (surrX, surrY) in self.surrounding(x, y):
				if self.grid[surrX][surrY] != None:
					self.uncover(surrX, surrY)
	def toggleFlag(self, x, y):
		curr = self.grid[x][y]
		if curr == Items.DIRT:
			next = Items.FLAG
		elif curr == Items.FLAG:
			next = Items.UNSURE
		elif curr == Items.UNSURE:
			next = Items.DIRT
		self.grid[x][y] = next
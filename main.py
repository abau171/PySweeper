import tkinter
import random

class MineMap:
	def __init__(self, width, height, numMines):
		self.width = width
		self.height = height
		self.numMines = numMines
		self.map = [[0 for row in range(height)] for col in range(width)]
		for i in range(numMines):
			minePlanted = False
			while not minePlanted:
				col = random.randint(0, width - 1)
				row = random.randint(0, height - 1)
				if self.map[col][row] == 0:
					self.map[col][row] = -1
					minePlanted = True
		for (x, y) in self.coords():
			if self.map[x][y] != -1:
				for (checkX, checkY) in self.surrounding(x, y):
					if self.map[checkX][checkY] == -1:
						self.map[x][y] += 1
	def coords(self):
		return MineMapIter(self)
	def surrounding(self, x, y):
		return MineMapSurroundingCoordIter(self, x, y)
	def get(self, x, y):
		if x >= 0 and x < self.width and y >= 0 and y < self.height:
			return self.map[x][y]
		else:
			return None

class MineMapIter:
	def __init__(self, mineMap):
		self.mineMap = mineMap
		self.x = -1
		self.y = 0
	def __iter__(self):
		return self
	def __next__(self):
		self.x += 1
		if self.x >= len(self.mineMap.map):
			self.x = 0
			self.y += 1
		if self.y >= len(self.mineMap.map[self.x]):
			raise StopIteration
		return (self.x, self.y)

class MineMapSurroundingCoordIter:
	def __init__(self, mineMap, x, y):
		self.mineMap = mineMap
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
			if surrX >= 0 and surrX < len(self.mineMap.map):
				if surrY >= 0 and surrY < len(self.mineMap.map[surrX]):
					result = (surrX, surrY)
		return result

class PySweeperModel:
	def __init__(self, width, height, numMines):
		self.width = width
		self.height = height
		self.numMines = numMines
		self.dugMine = False
		self.mineMap = MineMap(self.width, self.height, self.numMines)
		self.maskMap = [[False for row in range(self.height)] for col in range(self.width)]
	def dig(self, x, y):
		if self.dugMine:
			return
		self.maskMap[x][y] = True
		if self.mineMap.get(x, y) == -1:
			self.dugMine = True
		elif self.mineMap.get(x, y) == 0:
			for dX in range(-1, 2):
				for dY in range(-1, 2):
					if not (dX == 0 and dY == 0):
						checkX = x + dX
						checkY = y + dY
						if checkX >= 0 and checkX < self.width and checkY >= 0 and checkY < self.height:
							if self.maskMap[checkX][checkY] == False:
								self.dig(checkX, checkY)

class PySweeper:
	def start(self, width=15, height=10, numMines=20):
		self.width = width
		self.height = height
		self.numMines = numMines
		self.model = PySweeperModel(width, height, numMines)
		self.root = tkinter.Tk()
		def digFunction(x, y):
			def dig():
				self.model.dig(x, y)
				self.updateButtonText()
			return dig
		self.buttons = [[None for row in range(self.height)] for col in range(self.width)]
		for row in range(self.height):
			for col in range(self.width):
				f = tkinter.Frame(self.root, width=24, height=24)
				f.pack_propagate(0)
				f.grid(row=row, column=col)
				b = tkinter.Button(f, command=digFunction(col, row))
				b.pack(fill=tkinter.BOTH, expand=tkinter.YES)
				self.buttons[col][row] = b
		self.updateButtonText()
		self.root.mainloop()
	def updateButtonText(self):
		for col in range(self.width):
			for row in range(self.height):
				self.buttons[col][row].config(text=self.model.mineMap.get(col, row) if self.model.maskMap[col][row] else "")

PySweeper().start()
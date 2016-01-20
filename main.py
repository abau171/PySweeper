import tkinter
import random

MINE = -1
UNKNOWN = -2
FLAG = -3
UNSURE = -4

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
					self.map[col][row] = MINE
					minePlanted = True
		for (x, y) in self.coords():
			if self.map[x][y] != MINE:
				for (checkX, checkY) in self.surrounding(x, y):
					if self.map[checkX][checkY] == MINE:
						self.map[x][y] += 1
	def getHeight(self):
		return self.height
	def getWidth(self):
		return self.width
	def coords(self):
		return MineMapIter(self)
	def surrounding(self, x, y):
		return MineMapSurroundingCoordIter(self, x, y)
	def get(self, x, y):
		if x >= 0 and x < self.width and y >= 0 and y < self.height:
			return self.map[x][y]
		return None

class MaskedMineMap:
	def __init__(self, mineMap):
		self.mineMap = mineMap
		self.maskMap = [[UNKNOWN for row in range(self.mineMap.height)] for col in range(self.mineMap.width)]
	def getHeight(self):
		return self.mineMap.getHeight()
	def getWidth(self):
		return self.mineMap.getWidth()
	def coords(self):
		return MineMapIter(self)
	def surrounding(self, x, y):
		return MineMapSurroundingCoordIter(self, x, y)
	def get(self, x, y):
		if x >= 0 and x < self.getWidth() and y >= 0 and y < self.getHeight():
			if self.maskMap[x][y] == None:
				return self.mineMap.get(x, y)
			return self.maskMap[x][y]
		return None
	def isMasked(self, x, y):
		return self.maskMap[x][y] != None
	def unmask(self, x, y):
		self.maskMap[x][y] = None
	def toggleFlag(self, x, y):
		mask = self.maskMap[x][y]
		if mask == UNKNOWN:
			mask = FLAG
		elif mask == FLAG:
			mask = UNSURE
		elif mask == UNSURE:
			mask = UNKNOWN
		self.maskMap[x][y] = mask

class MineMapIter:
	def __init__(self, mineMap):
		self.mineMap = mineMap
		self.x = -1
		self.y = 0
	def __iter__(self):
		return self
	def __next__(self):
		self.x += 1
		if self.x >= self.mineMap.getWidth():
			self.x = 0
			self.y += 1
		if self.y >= self.mineMap.getHeight():
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
			if surrX >= 0 and surrX < self.mineMap.getWidth():
				if surrY >= 0 and surrY < self.mineMap.getHeight():
					result = (surrX, surrY)
		return result

class PySweeperModel:
	def __init__(self, width, height, numMines):
		self.width = width
		self.height = height
		self.numMines = numMines
		self.dugMine = False
		self.mineMap = MineMap(self.width, self.height, self.numMines)
		self.maskMap = MaskedMineMap(self.mineMap)
	def dig(self, x, y):
		if self.dugMine or self.maskMap.get(x, y) != UNKNOWN:
			return
		self.forceDig(x, y)
	def forceDig(self, x, y):
		if self.maskMap.isMasked(x, y):
			self.maskMap.unmask(x, y)
			if self.mineMap.get(x, y) == MINE:
				self.dugMine = True
			elif self.mineMap.get(x, y) == 0:
				for (checkX, checkY) in self.mineMap.surrounding(x, y):
					if self.maskMap.get(checkX, checkY) != None:
						self.forceDig(checkX, checkY)
	def toggleFlag(self, x, y):
		if self.dugMine:
			return
		self.maskMap.toggleFlag(x, y)

class PySweeper:
	def start(self, width=15, height=10, numMines=20):
		self.width = width
		self.height = height
		self.numMines = numMines
		self.model = PySweeperModel(width, height, numMines)
		self.root = tkinter.Tk()
		def digFunction(x, y):
			def dig(event):
				self.model.dig(x, y)
				self.updateButtonText()
			return dig
		def flagFunction(x, y):
			def toggleFlag(event):
				self.model.toggleFlag(x, y)
				self.updateButtonText()
			return toggleFlag
		self.buttons = [[None for row in range(self.height)] for col in range(self.width)]
		for row in range(self.height):
			for col in range(self.width):
				f = tkinter.Frame(self.root, width=24, height=24)
				f.pack_propagate(0)
				f.grid(row=row, column=col)
				b = tkinter.Button(f)
				b.bind("<ButtonRelease-1>", digFunction(col, row))
				b.bind("<ButtonRelease-3>", flagFunction(col, row))
				b.pack(fill=tkinter.BOTH, expand=tkinter.YES)
				self.buttons[col][row] = b
		self.updateButtonText()
		self.root.mainloop()
	def updateButtonText(self):
		for col in range(self.width):
			for row in range(self.height):
				value = self.model.maskMap.get(col, row)
				if value >= 0:
					text = str(value)
				elif value == MINE:
					text = "X"
				elif value == UNKNOWN:
					text = ""
				elif value == FLAG:
					text = "P"
				elif value == UNSURE:
					text = "?"
				else:
					text = "MISSINGNO"
				self.buttons[col][row].config(text=text)

PySweeper().start()
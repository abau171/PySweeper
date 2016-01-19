import tkinter
import random

class PySweeperModel:
	def __init__(self, width, height, numMines):
		self.width = width
		self.height = height
		self.numMines = numMines
		self.dugMine = False
		# generate mines
		self.mineMap = [[0 for row in range(self.height)] for col in range(self.width)]
		for i in range(self.numMines):
			minePlanted = False
			while not minePlanted:
				col = random.randint(0, self.width - 1)
				row = random.randint(0, self.height - 1)
				if self.mineMap[col][row] == 0:
					self.mineMap[col][row] = -1
					minePlanted = True
		# find number of nearby mines
		for col in range(self.width):
			for row in range(self.height):
				if self.mineMap[col][row] != -1:
					for dCol in range(-1, 2):
						for dRow in range(-1, 2):
							if not (dCol == 0 and dRow == 0):
								checkCol = col + dCol
								checkRow = row + dRow
								if checkCol >= 0 and checkCol < self.width and checkRow >= 0 and checkRow < self.height:
									if self.mineMap[checkCol][checkRow] == -1:
										self.mineMap[col][row] += 1
		# initially, nothing is discovered
		self.maskMap = [[False for row in range(self.height)] for col in range(self.width)]
	def dig(self, x, y):
		if self.dugMine:
			return
		self.maskMap[x][y] = True
		if self.mineMap[x][y] == -1:
			self.dugMine = True
		elif self.mineMap[x][y] == 0:
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
				self.buttons[col][row].config(text=self.model.mineMap[col][row] if self.model.maskMap[col][row] else "")

PySweeper().start()
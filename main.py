import tkinter

import model

MINE = -1
UNKNOWN = -2
FLAG = -3
UNSURE = -4

numberColors = ["gray", "blue", "green", "red", "navy", "brown", "light sea green", "black", "gray17"]

# class PySweeperModel:
# 	def __init__(self, width, height, numMines):
# 		self.width = width
# 		self.height = height
# 		self.numMines = numMines
# 		self.dugMine = False
# 		self.mineMap = MineMap(self.width, self.height, self.numMines)
# 		self.maskMap = MaskedMineMap(self.mineMap)
# 	def dig(self, x, y):
# 		if self.dugMine or self.maskMap.get(x, y) != UNKNOWN:
# 			return
# 		self.forceDig(x, y)
# 	def forceDig(self, x, y):
# 		if self.maskMap.isMasked(x, y):
# 			self.maskMap.unmask(x, y)
# 			if self.mineMap.get(x, y) == MINE:
# 				self.dugMine = True
# 			elif self.mineMap.get(x, y) == 0:
# 				for (checkX, checkY) in self.mineMap.surrounding(x, y):
# 					if self.maskMap.get(checkX, checkY) != None:
# 						self.forceDig(checkX, checkY)
# 	def toggleFlag(self, x, y):
# 		if self.dugMine:
# 			return
# 		self.maskMap.toggleFlag(x, y)

class PySweeper:
	def start(self, width=15, height=10, numMines=20):
		self.width = width
		self.height = height
		self.numMines = numMines
		self.model = model.PySweeperModel(width, height, numMines)
		print("got model!")
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
				b = tkinter.Button(f, font=("helvetica", 10, "bold"))
				b.bind("<ButtonRelease-1>", digFunction(col, row))
				b.bind("<ButtonRelease-3>", flagFunction(col, row))
				b.pack(fill=tkinter.BOTH, expand=tkinter.YES)
				self.buttons[col][row] = b
		self.updateButtonText()
		self.root.mainloop()
	def updateButtonText(self):
		for col in range(self.width):
			for row in range(self.height):
				value = self.model.get(col, row)
				if value >= 0:
					text = str(value)
					color = numberColors[value]
				elif value == MINE:
					text = "X"
					color = "black"
				elif value == UNKNOWN:
					text = ""
					color = "black"
				elif value == FLAG:
					text = "P"
					color = "red"
				elif value == UNSURE:
					text = "?"
					color = "blue"
				else:
					text = "MISSINGNO"
					color = "red"
				self.buttons[col][row].config(text=text, fg=color)

PySweeper().start()
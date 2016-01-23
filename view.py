import tkinter

import model

class ButtonType:
	def __init__(self, text, textColor, digEnabled=False, toggleEnabled=False):
		self.text = text
		self.textColor = textColor
		self.digEnabled = digEnabled
		self.toggleEnabled = toggleEnabled

buttonTypes = dict()
buttonTypes[model.Items.MINE] = ButtonType("X", "black")
buttonTypes[model.Items.DIRT] = ButtonType("", "black", digEnabled=True, toggleEnabled=True)
buttonTypes[model.Items.FLAG] = ButtonType("P", "red", toggleEnabled=True)
buttonTypes[model.Items.UNSURE] = ButtonType("?", "blue", toggleEnabled=True)
buttonTypes[0] = ButtonType("0", "gray")
buttonTypes[1] = ButtonType("1", "blue")
buttonTypes[2] = ButtonType("2", "green")
buttonTypes[3] = ButtonType("3", "red")
buttonTypes[4] = ButtonType("4", "navy")
buttonTypes[5] = ButtonType("5", "brown")
buttonTypes[6] = ButtonType("6", "light sea green")
buttonTypes[7] = ButtonType("7", "black")
buttonTypes[8] = ButtonType("8", "gray17")

class SmileyState:
	HAPPY=0
	SCARED=1
	DEAD=2
	COOL=3

smileyTexts = dict()
smileyTexts[SmileyState.HAPPY] = ":)"
smileyTexts[SmileyState.SCARED] = ":o"
smileyTexts[SmileyState.DEAD] = "XD"
smileyTexts[SmileyState.COOL] = "B)"

class SmileyButton:
	def __init__(self, parent, callback):
		self.frame = tkinter.Frame(parent, width=30, height=30, bg="green")
		self.frame.pack_propagate(0)
		self.button = tkinter.Button(self.frame)
		self.updateState(SmileyState.HAPPY)
		self.button.pack(fill=tkinter.BOTH, expand=tkinter.YES)
		self.frame.pack()
		def doCallback(event):
			callback()
		self.button.bind("<ButtonRelease-1>", doCallback)
	def updateState(self, state):
		self.state = state
		self.button.config(text=smileyTexts[self.state])

class PySweeperView:
	def __init__(self, width, height, resetCallback):
		self.width = width
		self.height = height
		self.resetCallback = resetCallback
		self.model = None
		self.root = tkinter.Tk()
		self.initTopFrame()
		self.initGrid()
	def initGrid(self):
		self.gridFrame = tkinter.Frame(self.root)
		self.buttons = [[None for y in range(self.height)] for x in range(self.width)]
		for y in range(self.height):
			for x in range(self.width):
				f = tkinter.Frame(self.gridFrame, width=24, height=24)
				f.pack_propagate(0)
				f.grid(row=y, column=x)
				b = tkinter.Button(f, font=("helvetica", 10, "bold"))
				b.pack(fill=tkinter.BOTH, expand=tkinter.YES)
				self.buttons[x][y] = b
		self.updateButtons()
		self.updateStats()
		self.gridFrame.pack()
	def initTopFrame(self):
		self.topFrame = tkinter.Frame(self.root, padx=10, pady=10)
		self.minesLeftText = tkinter.Label(self.topFrame, text="0")
		self.minesLeftText.pack(side=tkinter.LEFT)
		self.smileyButton = SmileyButton(self.topFrame, self.resetCallback)
		self.topFrame.pack(fill=tkinter.X)
	def setModel(self, model):
		self.model = model
		self.updateButtons()
		self.updateStats()
	def digFunction(self, x, y):
		def dig(event):
			self.model.dig(x, y)
			self.updateButtons()
			self.updateStats()
		return dig
	def flagFunction(self, x, y):
		def toggleFlag(event):
			self.model.toggleFlag(x, y)
			self.updateButtons()
			self.updateStats()
		return toggleFlag
	def smileyFunction(self, state):
		def updateSmileyState(event):
			self.smileyButton.updateState(state)
		return updateSmileyState
	def updateButtons(self):
		for y in range(self.height):
			for x in range(self.width):
				button = self.buttons[x][y]
				button.unbind("<Button-1>")
				button.unbind("<ButtonRelease-1>")
				button.unbind("<ButtonRelease-3>")
				if self.model != None:
					value = self.model.get(x, y)
				else:
					value = model.Items.DIRT
				bType = buttonTypes[value]
				if self.model != None:
					if self.model.isPlaying() and bType.digEnabled:
						button.bind("<Button-1>", self.smileyFunction(SmileyState.SCARED))
						button.bind("<ButtonRelease-1>", self.digFunction(x, y))
					if self.model.isPlaying() and bType.toggleEnabled:
						button.bind("<ButtonRelease-3>", self.flagFunction(x, y))
				button.config(text=bType.text, fg=bType.textColor, activeforeground=bType.textColor)
	def updateStats(self):
		if self.model != None:
			minesLeft = self.model.getNumMinesLeft()
			solved = self.model.isSolved()
			failed = self.model.isFailed()
		else:
			minesLeft = 0
			solved = False
			failed = False
		self.minesLeftText.config(text=str(minesLeft))
		if solved:
			newSmiley = SmileyState.COOL
		elif failed:
			newSmiley = SmileyState.DEAD
		else:
			newSmiley = SmileyState.HAPPY
		self.smileyButton.updateState(newSmiley)
	def start(self):
		self.root.mainloop()
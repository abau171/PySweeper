import tkinter

class PySweeperView:
	def __init__(self, width, height, model):
		self.width = width
		self.height = height
		self.model = model
		self.root = tkinter.Tk()
		self.initGrid()
	def initGrid(self):
		self.buttons = [[None for y in range(self.height)] for x in range(self.width)]
		for y in range(self.height):
			for x in range(self.width):
				f = tkinter.Frame(self.root, width=24, height=24)
				f.pack_propagate(0)
				f.grid(row=y, column=x)
				b = tkinter.Button(f, font=("helvetica", 10, "bold"))
				b.pack(fill=tkinter.BOTH, expand=tkinter.YES)
				self.buttons[x][y] = b
		self.updateButtons()
	def digFunction(self, x, y):
		def dig(event):
			self.model.dig(x, y)
			self.updateButtons()
		return dig
	def flagFunction(self, x, y):
		def toggleFlag(event):
			self.model.toggleFlag(x, y)
			self.updateButtons()
		return toggleFlag
	def updateButtons(self):
		for y in range(self.height):
			for x in range(self.width):
				button = self.buttons[x][y]
				value = self.model.get(x, y)
				button.config(text=str(value))
				button.unbind("<ButtonRelease-1>")
				button.bind("<ButtonRelease-1>", self.digFunction(x, y))
				button.unbind("<ButtonRelease-3>")
				button.bind("<ButtonRelease-3>", self.flagFunction(x, y))
	def start(self):
		self.root.mainloop()
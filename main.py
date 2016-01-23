import model
import view

WIDTH = 9
HEIGHT = 9
NUM_MINES = 10

class PySweeperWindow:
	def __init__(self, width=9, height=9, numMines=10):
		self.width = width
		self.height = height
		self.numMines = numMines
		def doReset():
			self.reset()
		self.view = view.PySweeperView(self.width, self.height, doReset)
		self.reset()
	def start(self):
		self.view.start()
	def reset(self):
		self.model = model.PySweeperModel(self.width, self.height, self.numMines)
		self.view.setModel(self.model)

window = PySweeperWindow(width=WIDTH, height=HEIGHT, numMines=NUM_MINES).start()
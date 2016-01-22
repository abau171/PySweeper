import model
import view

class PySweeper:
	def start(self, width=15, height=10, numMines=20):
		self.model = model.PySweeperModel(width, height, numMines)
		self.view = view.PySweeperView(width, height, self.model)
		self.view.start()

PySweeper().start()
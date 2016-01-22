import model
import view

numberColors = ["gray", "blue", "green", "red", "navy", "brown", "light sea green", "black", "gray17"]

class PySweeper:
	def start(self, width=15, height=10, numMines=20):
		self.model = model.PySweeperModel(width, height, numMines)
		self.view = view.PySweeperView(width, height, self.model)

		# def digFunction(x, y):
		# 	def dig(event):
		# 		self.model.dig(x, y)
		# 		self.updateButtonText()
		# 	return dig
		# def flagFunction(x, y):
		# 	def toggleFlag(event):
		# 		self.model.toggleFlag(x, y)
		# 		self.updateButtonText()
		# 	return toggleFlag
		# 		b.bind("<ButtonRelease-1>", digFunction(col, row))
		# 		b.bind("<ButtonRelease-3>", flagFunction(col, row))

		self.view.start()
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
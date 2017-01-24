class GUI:
	def __init__(self):
		self.children = []

	def destroy(self):
		for child in self.children:
			child.destroy()
		self.children.clear()

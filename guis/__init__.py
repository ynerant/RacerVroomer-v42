_CURRENT_GUI = None

class GUI:
	def __init__(self):
		global _CURRENT_GUI
		if _CURRENT_GUI is not None:
			_CURRENT_GUI.destroy()
		self.children = []
		_CURRENT_GUI = self

	def destroy(self):
		for child in self.children:
			child.destroy()
		self.children.clear()

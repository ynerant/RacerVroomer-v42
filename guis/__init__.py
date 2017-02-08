CURRENT_GUI = None
OLD_GUI = None

class GUI:
	def __init__(self):
		global CURRENT_GUI, OLD_GUI
		if CURRENT_GUI is not None:
			CURRENT_GUI.destroy()
		self.children = []
		OLD_GUI = CURRENT_GUI.__class__
		CURRENT_GUI = self

	def destroy(self):
		for child in self.children:
			child.destroy()
		self.children.clear()

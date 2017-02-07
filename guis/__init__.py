CURRENT_GUI = None
OLD_GUIS = []

class GUI:
	def __init__(self):
		global CURRENT_GUI, OLD_GUIS
		if CURRENT_GUI is not None:
			CURRENT_GUI.destroy()
		self.children = []
		OLD_GUIS.insert(0, CURRENT_GUI.__class__)
		CURRENT_GUI = self

	def destroy(self):
		for child in self.children:
			child.destroy()
		self.children.clear()

def back(window):
	gui = OLD_GUIS.pop(0)(window)
	OLD_GUIS.pop(0)
	return gui

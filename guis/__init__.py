#coding : utf-8

from audio import AudioPlayer
import tkinter as tk

CURRENT_GUI = None
OLD_GUIS = []

class GUI:
	def __init__(self):
		global CURRENT_GUI, OLD_GUIS
		if CURRENT_GUI is not None:
			CURRENT_GUI.destroy()
		self._children = []
		OLD_GUIS.insert(0, CURRENT_GUI.__class__)
		CURRENT_GUI = self
	
	def appendChild(self, child):
		self._children.append(child)
		if type(child) is tk.Button:
			child.bind("<ButtonRelease-1>", lambda event : self.clickButton(child))

	def destroy(self):
		for child in self._children:
			try:
				child.destroy()
			except:
				pass
		self._children.clear()
	
	def clickButton(self, button):
		print("A button is clicked!")
		# Now play the sound
		#AudioPlayer.playSound(AudioPlayer.CLICK)

def back(window):
	gui = OLD_GUIS.pop(0)(window)
	OLD_GUIS.pop(0)
	return gui

#coding: utf-8

import tkinter as tk

# Initialize the window
# It is necessary to  create the window before anything, because when classes are imported, it mays load some window components
# noinspection PyProtectedMember
if tk._default_root is None:
	tk.Tk()

from guis.mainMenu import MainMenu

def main():
	"""
	Main method (invoked at launch)
	"""

	# noinspection PyProtectedMember
	window = tk._default_root #type: tk.Tk
	window.title("Racer Vroomer v42")
	# Maximize the window
	window.state("zoomed")
	width = 840
	height = 420
	# Placing window at the center of the screen (when not maximized)
	screenWidth = window.winfo_screenwidth()
	screenHeight = window.winfo_screenheight()
	window.geometry(str(width) + "x" + str(height) + "+" + str(int((screenWidth - width) / 2)) + "+" + str(int((screenHeight - height) / 2)))

	window.music_enabled = True
	window.sounds_enabled = True

	MainMenu(window)

	window.mainloop()

if __name__ == "__main__" :
	main()

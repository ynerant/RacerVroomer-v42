#coding: utf-8

import tkinter as tk

# Initialize the window
# It is necessary to  create the window before anything, because when classes are imported, it mays load some window components
# noinspection PyProtectedMember
if tk._default_root is None:
	tk.Tk()


# Import messages vars
import messages as msgs
# Import some useful content
import utils


def main():
	"""
	Main method (invoked at launch)
	"""

	# noinspection PyProtectedMember
	window = tk._default_root
	window.title("Racer Vroomer v42")
	# Maximize the window
	window.state("zoomed")
	width = 840
	height = 420
	# Placing window at the center of the screen (when not maximized)
	screenWidth = window.winfo_screenwidth()
	screenHeight = window.winfo_screenheight()
	window.geometry(str(width) + "x" + str(height) + "+" + str(int((screenWidth - width) / 2)) + "+" + str(int((screenHeight - height) / 2)))

	singleplayer = tk.Button(window, textvariable = msgs.SINGLE_PLAYER, font = ("Plantagenet Cherokee", 42), anchor = "center", width = 20, borderwidth = 10, relief = "groove")
	multiplayer = tk.Button(window, textvariable = msgs.MULTI_PLAYER, font = ("Plantagenet Cherokee", 42), anchor = "center", width = 20, borderwidth = 10 , relief = "groove", command = lambda: utils.showMessageDialog(msgs.SOON, msgs.FUTURE_FEATURE))
	options = tk.Button(window, textvariable = msgs.SETTINGS, font = ("Plantagenet Cherokee", 42), anchor = "center", width = 20, borderwidth = 10, relief = "groove", command = msgs.switchLanguage)
	quitGame = tk.Button(window, textvariable = msgs.QUIT, font = ("Plantagenet Cherokee", 42), anchor = "center", width = 20, borderwidth = 10, relief = "groove", command = window.quit)

	singleplayer.pack()
	multiplayer.pack()
	options.pack()
	quitGame.pack()

	window.mainloop()

if __name__ == "__main__":
	main()

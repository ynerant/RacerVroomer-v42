#coding: utf-8

import tkinter as tk
# Import messages vars
import messages as msgs
# Import some useful content
import utils
from . import GUI

class MainMenu(GUI):
	def __init__(self, window):
		GUI.__init__(self)
		singleplayer = tk.Button(window, textvariable = msgs.SINGLE_PLAYER, font = ("Plantagenet Cherokee", 42), anchor = "center", width = 20, borderwidth = 10, relief = "groove")
		multiplayer = tk.Button(window, textvariable = msgs.MULTI_PLAYER, font = ("Plantagenet Cherokee", 42), anchor = "center", width = 20, borderwidth = 10 , relief = "groove", command = lambda: utils.showMessageDialog(msgs.SOON, msgs.FUTURE_FEATURE))
		options = tk.Button(window, textvariable = msgs.SETTINGS, font = ("Plantagenet Cherokee", 42), anchor = "center", width = 20, borderwidth = 10, relief = "groove", command = msgs.switchLanguage)
		quitGame = tk.Button(window, textvariable = msgs.QUIT, font = ("Plantagenet Cherokee", 42), anchor = "center", width = 20, borderwidth = 10, relief = "groove", command = window.quit)

		singleplayer.pack()
		multiplayer.pack()
		options.pack()
		quitGame.pack()

		self.children.append(singleplayer)
		self.children.append(multiplayer)
		self.children.append(options)
		self.children.append(quitGame)

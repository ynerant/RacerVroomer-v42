#coding: utf-8

import tkinter as tk
# Import messages vars
import messages as msgs
# Import some useful content
import utils
from . import GUI, settings, singleplayer

class MainMenu(GUI):
	def __init__(self, window):
		GUI.__init__(self)
		onePlayerMode = tk.Button(window, textvariable = msgs.SINGLE_PLAYER, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 25, borderwidth = 10, relief = "groove", command = lambda  : singleplayer.Singleplayer(window))
		multiplayer = tk.Button(window, textvariable = msgs.MULTI_PLAYER, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 25, borderwidth = 10 , relief = "groove", command = lambda : utils.showMessageDialog(msgs.SOON, msgs.FUTURE_FEATURE))
		options = tk.Button(window, textvariable = msgs.SETTINGS, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 25, borderwidth = 10, relief = "groove", command = lambda : settings.Settings(window))
		quitGame = tk.Button(window, textvariable = msgs.QUIT, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 25, borderwidth = 10, relief = "groove", command = window.quit)

		onePlayerMode.pack()
		multiplayer.pack()
		options.pack()
		quitGame.pack()

		self.children.append(onePlayerMode)
		self.children.append(multiplayer)
		self.children.append(options)
		self.children.append(quitGame)

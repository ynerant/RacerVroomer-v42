#coding: utf-8

import tkinter as tk
import os
# Import messages vars
import messages as msgs
import utils
from . import GUI, settings, playerMode
from PIL import Image, ImageTk


class MainMenu(GUI):
	def __init__(self, window):
		GUI.__init__(self)

		def on_closing():
			os._exit(0) # Force closing process, killing all threads

		bg = Image.open("images/menu/minia.png")
		bgImage = ImageTk.PhotoImage(bg)
		labelImage = tk.Label(window, image = bgImage)
		labelImage.pack()

		window.protocol("WM_DELETE_WINDOW", on_closing)

		onePlayerMode = tk.Button(window, textvariable = msgs.SINGLE_PLAYER, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 15, borderwidth = 4, bg = utils.BUTTON_BACKGROUND, relief = "raise", command = lambda  : playerMode.SinglePlayer(window))
		multiplayer = tk.Button(window, textvariable = msgs.MULTI_PLAYER, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 15, borderwidth = 4, bg = utils.BUTTON_BACKGROUND, relief = "raise", command = lambda : playerMode.MultiPlayer(window))
		options = tk.Button(window, textvariable = msgs.SETTINGS, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 15, borderwidth = 4, bg = utils.BUTTON_BACKGROUND, relief = "raise", command = lambda : settings.Settings(window))
		quitGame = tk.Button(window, textvariable = msgs.QUIT, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 15, borderwidth = 4, bg = utils.BUTTON_BACKGROUND, relief = "raise", command = on_closing)

		onePlayerMode.place(relx = .025, rely = .30)
		multiplayer.place(relx = .025, rely = .42)
		options.place(relx = .025, rely = .54)
		quitGame.place(relx = .74, rely = .88)

		self.appendChild(onePlayerMode)
		self.appendChild(multiplayer)
		self.appendChild(options)
		self.appendChild(quitGame)

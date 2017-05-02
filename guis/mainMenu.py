#coding: utf-8

import tkinter as tk
import os
# Import messages vars
import messages as msgs
import utils
from . import GUI, settings, scores, playerMode


class MainMenu(GUI):
	def __init__(self, window):
		"""
		Constructeur par défaut de l'interface du menu principal (Fond d'écran actif)
		Prend comme argument la fenêtre
		"""
		GUI.__init__(self, window, True)

		# Lorsque la fenêtre est fermée, on force la fin du processus coupant ainsi tout processus
		# Cela peut être instable dans quelques rares cas, mais ici, ils restent très négligeables
		def on_closing():
			# noinspection PyProtectedMember
			os._exit(0)

		window.protocol("WM_DELETE_WINDOW", on_closing)

		# Création des boutons
		onePlayerMode = tk.Button(window, textvariable = msgs.SINGLE_PLAYER, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 15, borderwidth = 4, bg = utils.BUTTON_BACKGROUND, relief = "raise", command = lambda  : playerMode.SinglePlayer(window))
		multiplayer = tk.Button(window, textvariable = msgs.MULTI_PLAYER, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 15, borderwidth = 4, bg = utils.BUTTON_BACKGROUND, relief = "raise", command = lambda : playerMode.MultiPlayer(window))
		options = tk.Button(window, textvariable = msgs.SETTINGS, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 15, borderwidth = 4, bg = utils.BUTTON_BACKGROUND, relief = "raise", command = lambda : settings.Settings(window))
		scoresBtn = tk.Button(window, textvariable = msgs.SCORES, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 15, borderwidth = 4, bg = utils.BUTTON_BACKGROUND, relief = "raise", command = lambda : scores.Scores(window))
		quitGame = tk.Button(window, textvariable = msgs.QUIT, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 15, borderwidth = 4, bg = utils.BUTTON_BACKGROUND, relief = "groove", command = on_closing)

		# Placement des boutons dans le menu
		onePlayerMode.place(relx = .025, rely = .25, relwidth = .42, relheight = .11)
		multiplayer.place(relx = .025, rely = .37, relwidth = .42, relheight = .11)
		options.place(relx = .025, rely = .49, relwidth = .42, relheight = .11)
		scoresBtn.place(relx = .025, rely = .61, relwidth = .42, relheight = .11)
		quitGame.place(relx = .74, rely = .88, relwidth = .26, relheight = .12)

		# Ajout des boutons comme enfants
		self.appendChild(onePlayerMode)
		self.appendChild(multiplayer)
		self.appendChild(options)
		self.appendChild(scoresBtn)
		self.appendChild(quitGame)

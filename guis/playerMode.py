#coding : utf-8

import tkinter as tk
import messages as msgs
import utils
from guis import GUI, back
from guis.gameBuilder import CarChooser, MapChooser, GameBuilder

class SinglePlayer(GUI):
	def __init__(self, window):
		"""
		Constructeur par défaut de l’interface du menu un joueur
		Prend comme argument la fenêtre
		"""
		GUI.__init__(self, window, True)

		# builder représente le constructeur de partie actuel (créé si inexistant)
		builder = GameBuilder.CURRENT_GAME_BUILDER
		if builder is None:
			builder = GameBuilder.CURRENT_GAME_BUILDER = GameBuilder(GameBuilder.SINGLE_PLAYER_MODE)

		# Création des boutons
		car = tk.Button(window, textvariable = msgs.CAR_CHOICE, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 15, borderwidth = 4, bg = utils.BUTTON_BACKGROUND, relief = "raise", command = lambda : CarChooser(window, builder))
		chooseMap = tk.Button(window, textvariable = msgs.MAP_CHOICE, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 15, borderwidth = 4, bg = utils.BUTTON_BACKGROUND, relief = "raise", command = lambda : MapChooser(window, builder))
		start = tk.Button(window, textvariable = msgs.START, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 15, borderwidth = 4, bg = utils.BUTTON_BACKGROUND, relief = "raise", state = tk.DISABLED if builder.car is None or builder.map is None else tk.NORMAL, command = lambda : builder.start(window))
		backBtn = tk.Button(window, textvariable = msgs.BACK, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 15, borderwidth = 4, bg = utils.BUTTON_BACKGROUND, relief = "raise", command = lambda : back(window))

		# Positionnement des boutons sur l’interface
		car.place(relx = .025, rely = .30)
		chooseMap.place(relx = .025, rely = .42)
		start.place(relx = .025, rely = .54)
		backBtn.place(relx = .74, rely = .88)

		# Ajout des boutons comme enfants
		self.appendChild(car)
		self.appendChild(chooseMap)
		self.appendChild(start)
		self.appendChild(backBtn)

class MultiPlayer(GUI):
	def __init__(self, window):
		"""
		Constructeur par défaut de l’interface du menu multijoueur
		Prend comme argument la fenêtre
		
		Ce menu n’est absolument pas encore travaillé et n’est là qu’en prévision
		"""
		GUI.__init__(self, window, True)

		# Création des boutons
		local = tk.Button(window, textvariable = msgs.LOCAL, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 15, borderwidth = 4, bg = utils.BUTTON_BACKGROUND, relief = "raise", command = lambda : utils.showMessageDialog(msgs.SOON, msgs.FUTURE_FEATURE))
		online = tk.Button(window, textvariable = msgs.ONLINE, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 15, borderwidth = 4, bg = utils.BUTTON_BACKGROUND, relief = "raise", command = lambda : utils.showMessageDialog(msgs.SOON, msgs.FUTURE_FEATURE))
		backBtn = tk.Button(window, textvariable = msgs.BACK, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 15, borderwidth = 4, bg = utils.BUTTON_BACKGROUND, relief = "raise", command = lambda : back(window))

		# Affichage et positionnement des boutons sur l’interface
		local.place(relx = .025, rely = .35)
		online.place(relx = .025, rely = .47)
		backBtn.place(relx = .74, rely = .88)

		# Ajout des boutons comme enfants
		self.appendChild(local)
		self.appendChild(online)
		self.appendChild(backBtn)
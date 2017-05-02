#coding : utf-8

import tkinter as tk
import messages as msgs
from guis import GUI, back, game
import cars, maps, utils
from PIL import Image

class GameBuilder:
	CURRENT_GAME_BUILDER = None

	class Mode:
		def __init__(self, singleplayer):
			"""
			Constructeur par défaut d'un mode de jeu
			Deux modes existent : un joueur et multijoueur
			"""
			self.sp = singleplayer
			self.mp = not singleplayer

	SINGLE_PLAYER_MODE = Mode(True)
	MULTI_PLAYER_MODE = Mode(False)


	def __init__(self, mode : Mode):
		"""
		Constructeur par défaut d'un constructeur de partie
		Prend comme argument le mode de jeu précédemment défini
		"""
		self.car = None
		self.map = None
		self.mode = mode

	def start(self, window):
		"""
		Démarre la partie et détruit le constructeur
		N'est possible seulement si une voiture et une carte ont été choisies
		"""
		GameBuilder.CURRENT_GAME_BUILDER = None
		game.Game(window, self)

class CarChooser(GUI):
	def __init__(self, window : tk.Tk, gameBuilder : GameBuilder):
		"""
		Constructeur par défaut du sélecteur de voiture
		Prend comme argument la fenêtre et le constructeur de partie
		"""
		GUI.__init__(self, window)

		self.builder = gameBuilder

		# master représente un cadre dans lequel sera incorporé le sélecteur ainsi que les barres de défilement
		master = tk.Frame(window, width = window.winfo_screenwidth(), height = window.winfo_screenheight())
		master.place(x = 0, y = 0, relwidth = 1, relheight = 1)
		self.appendChild(master)

		# Création des barres de défilement
		vscrollbar = tk.Scrollbar(master, orient = tk.VERTICAL)
		hscrollbar = tk.Scrollbar(master, orient = tk.HORIZONTAL)
		vscrollbar.pack(side = tk.RIGHT, fill = tk.Y, expand = tk.FALSE)
		hscrollbar.pack(side = tk.BOTTOM, fill = tk.X, expand = tk.FALSE)
		self.appendChild(vscrollbar)
		self.appendChild(hscrollbar)

		# Afin de pouvoir déplacer la fenêtre, nécessité de passer par un canevas
		# x(y)scrollcommand : Contrôle la taille des barres de défilement
		# scrollregion : Définit la zone de défilement (pour des raisons obscrures, nécessité de définir cela de façon statique)
		canvas = tk.Canvas(master, xscrollcommand = hscrollbar.set, yscrollcommand = vscrollbar.set, width = window.winfo_screenwidth(), height = window.winfo_screenheight(), scrollregion = "0 0 %s %s" % (window.winfo_screenwidth() + 54, window.winfo_screenheight() - 100))
		# Création du cadre dans lequel seront déposés les composants
		frame = tk.Frame(canvas, width = window.winfo_screenwidth(), height = window.winfo_screenheight())
		# Placement du cadre dans le canevas
		canvas.create_window(0, 0, window = frame, anchor = tk.NW)
		# Placement du canevas
		canvas.pack(side = tk.LEFT, fill = tk.BOTH, expand = tk.FALSE)
		canvas.xview_moveto(0)
		canvas.yview_moveto(0)

		# Définition de l'action des barres de défilement (déplacer le canevas)
		vscrollbar.config(command = canvas.yview)
		hscrollbar.config(command = canvas.xview)

		for i in range(len(cars.CARS)):
			# Pour chaque voiture, affichae d'une ligne d'informations
			car = cars.CARS[i]
			# Chargement de l'image de miniature grâce au module PIL
			image = Image.open("images/thumbnails/" + car.thumbnail_file)
			# Redimensionnement de l'image en 100x100 avec anti-crénelage
			image = image.resize((100, 100), Image.ANTIALIAS)
			# Remplacement de l'image
			image.save("images/thumbnails/" + car.thumbnail_file, car.thumbnail_file[-3:])
			# Conversion de l'image en Tkinter
			thumbnail = tk.PhotoImage(file = "images/thumbnails/" + car.thumbnail_file)
			# Passage de l'image en Label et placement dans l'interface
			thumbnailLabel = tk.Label(frame, image = thumbnail)
			thumbnailLabel.image = thumbnail
			thumbnailLabel.grid(row = 5 * i, column = 0, rowspan = 4)
			# Affichage du nom de la voiture
			label = tk.Label(frame, textvariable = car.name, font = ("Plantagenet Cherokee", 30))
			label.grid(row = 5 * i, column = 1, rowspan = 4)
			# Affichage de la vitesse de la voiture
			speedLabel = tk.Label(frame, textvariable = msgs.MAX_SPEED.format(car.max_speed), font = ("Plantagenet Cherokee", 16))
			speedLabel.grid(row = 5 * i, column = 2)
			# Affichage de la capacité d'accélération de la voiture
			accelerateLabel = tk.Label(frame, textvariable = msgs.ACCELERATION.format(60 * car.acceleration), font = ("Plantagenet Cherokee", 16))
			accelerateLabel.grid(row = 5 * i + 1, column = 2)
			# Affichage de la taille de la voiture
			sizeLabel = tk.Label(frame, textvariable = msgs.SIZE.format(car.width, car.height), font = ("Plantagenet Cherokee", 16))
			sizeLabel.grid(row = 5 * i + 2, column = 2)
			# Affichage de la maniabilité de la voiture (présenté comme unité arbitraire sans réellement en être une)
			maniabilityLabel = tk.Label(frame, textvariable = msgs.MANIABILITY.format(car.maniability), font = ("Plantagenet Cherokee", 16))
			maniabilityLabel.grid(row = 5 * i + 3, column = 2)
			# Affichage du bouton de sélection
			choose = tk.Button(frame, textvariable = msgs.CHOOSE, bg = utils.BUTTON_BACKGROUND, font = ("Plantagenet Cherokee", 22))
			choose.grid(row = 5 * i, column = 3, rowspan = 4)

			# Si la voiture a déjà été choisie (pour modification), affichage d'un check à côté
			if self.builder.car == car:
				ok = tk.Label(frame, text = "ü", font = ("Wingdings", 42))
				ok.grid(row = 5 * i, column = 4, rowspan = 4)
				self.appendChild(ok)

			# Si ce n'est pas la dernière voiture, affichage d'une ligne grisée
			if i < len(cars.CARS) - 1:
				canvas = tk.Canvas(frame, width = window.winfo_screenwidth(), height = 5, bg = "lightgray")
				canvas.grid(row = 5 * i + 4, columnspan = 4)
				self.appendChild(canvas)

			# Inscription de l'écouteur pour le click du bouton de sélection
			self.registerChooseListener(window, choose, car)

			# Ajout de tous les composants comme enfants
			self.appendChild(frame)
			self.appendChild(thumbnailLabel)
			self.appendChild(label)
			self.appendChild(speedLabel)
			self.appendChild(accelerateLabel)
			self.appendChild(sizeLabel)
			self.appendChild(maniabilityLabel)
			self.appendChild(choose)

		# Ajout du bouton retour
		backBtn = tk.Button(frame, textvariable = msgs.BACK, bg = utils.BUTTON_BACKGROUND, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 20,
							borderwidth = 10, relief = "groove", command = lambda : back(window))
		backBtn.grid(row = 5 * (len(cars.CARS) + 1), columnspan = 4, pady = 100)
		self.appendChild(backBtn)

		# Configuration des poids (rapports de longueur) de chaque colonne
		frame.columnconfigure(0, weight = 1)
		frame.columnconfigure(1, weight = 2)
		frame.columnconfigure(2, weight = 3)
		frame.columnconfigure(3, weight = 2)
		frame.columnconfigure(4, weight = 1)

		# Mise à jour de la zone de scroll lorsque le cadre est redimensionné
		# En apparence mystérieusement non fonctionnel
		def _configure_frame(event):
			size = (frame.winfo_reqwidth(), frame.winfo_reqheight())
			canvas.config(scrollregion = "0 0 %s %s" % size)
			print(canvas.config("scrollregion"))
		frame.bind('<Configure>', _configure_frame)

	# Lorsqu'un clic est réalisé, retour au menu précédent et affectation au constructeur de la voiture
	def registerChooseListener(self, window, button, car):
		def choose_car():
			self.builder.car = car
			back(window)
		button.bind("<ButtonRelease-1>", lambda event : choose_car())

class MapChooser(GUI):
	def __init__(self, window : tk.Tk, gameBuilder : GameBuilder):
		"""
		Constructeur par défaut du sélecteur de carte
		Prend comme argument la fenêtre et le constructeur de partie
		"""
		GUI.__init__(self, window)

		self.builder = gameBuilder

		for i in range(len(maps.MAPS)):
			# Pour chaque carte, affiche une ligne d'informations et de sélection
			map = maps.MAPS[i]
			# Lecture de l'image de miniature grâce au module PIL
			image = Image.open("images/thumbnails/" + map.thumbnail)
			# Redimensionnement de l'image en 100x100 avec anti-crénelage
			image = image.resize((100, 100), Image.ANTIALIAS)
			# Remplacement de l'ancien fichier
			image.save("images/thumbnails/" + map.thumbnail, map.thumbnail[-3:])
			# Conversion de l'image en image Tkinter
			thumbnail = tk.PhotoImage(file = "images/thumbnails/" + map.thumbnail)
			# Placement de l'image dans un label et positionnement dans l'interface
			thumbnailLabel = tk.Label(window, image = thumbnail)
			thumbnailLabel.image = thumbnail
			thumbnailLabel.grid(row = i, column = 0, rowspan = 1)
			# Affichage du nom de la carte
			label = tk.Label(window, textvariable = map.name, font = ("Plantagenet Cherokee", 30))
			label.grid(row = i, column = 1, rowspan = 1)
			# Affichage de la taille (en pixels) de la carte
			sizeLabel = tk.Label(window, textvariable = msgs.SIZE.format(map.width, map.height), font = ("Plantagenet Cherokee", 22))
			sizeLabel.grid(row = i, column = 2)
			# Affichage du bouton de sélection de la carte
			choose = tk.Button(window, textvariable = msgs.CHOOSE, bg = utils.BUTTON_BACKGROUND, font = ("Plantagenet Cherokee", 22))
			choose.grid(row = i, column = 3, rowspan = 1)

			# Si une carte était déjà sélectionné, affichage d'un check à côté
			if self.builder.map == map:
				ok = tk.Label(window, text = "ü", font = ("Wingdings", 42))
				ok.grid(row = i, column = 4, rowspan = 1)
				self.appendChild(ok)

			# Inscription de l'écouteur pour le clic du bouton
			self.registerChooseListener(window, choose, map)

			# Ajout des enfants
			self.appendChild(thumbnailLabel)
			self.appendChild(label)
			self.appendChild(sizeLabel)
			self.appendChild(choose)

		# Configuration des poids des colonnes
		window.columnconfigure(0, weight = 1)
		window.columnconfigure(1, weight = 2)
		window.columnconfigure(2, weight = 3)
		window.columnconfigure(3, weight = 2)
		window.columnconfigure(4, weight = 1)

		# Affichage du bouton retour
		backBtn = tk.Button(window, textvariable = msgs.BACK, font = ("Plantagenet Cherokee", 30), bg = utils.BUTTON_BACKGROUND, anchor = "center",
							width = 20, borderwidth = 10, relief = "groove", command = lambda : back(window))
		backBtn.grid(row = len(cars.CARS) * 2 + 1, column = 0, columnspan = 5, pady = 100)
		self.appendChild(backBtn)

	# Lorsque la carte est sélectionnée, affectation au constructeur et retour au menu précédent
	def registerChooseListener(self, window, button, map):
		def choose_map():
			self.builder.map = map
			back(window)
		button.bind("<ButtonRelease-1>", lambda event : choose_map())

#coding : utf-8

import tkinter as tk
import messages as msgs
from guis import GUI, back
import utils, gzip, json, cars, maps

def loadScores():
	"""
	Chargement du fichier de scores JSON compressé en GZIP (scores.gz) et si absent, en crée un vierge
	"""
	try:
		# Décompression et lecture du fichier de scores compressé en gzip, écrit en JSON
		with gzip.open("scores.gz", "rb") as f:
			file_content = f.read()
		# Décodage binaire (tableau d'octets vers chaîne de caractères)
		jsoned = file_content.decode("UTF-8")
		# Traduction JSON -> liste Python
		l = json.loads(jsoned) #type: list
		for obj in l:
			car = cars.CARS[int(obj["car"])]
			map = maps.MAPS[int(obj["map"])]
			time_laps = obj["laps_time"]
			total_time = obj["total_time"]
			total_time_seconds = obj["total_time_seconds"]
			Score(car, map, time_laps, total_time, total_time_seconds, False)
	except FileNotFoundError:
		# Si le fichier n'a pas été trouvé, création d'un fichier vierge
		saveScores()
	except IOError:
		# Autre message d'erreur (fichier corrompu et irrécupérable) => Paramètres d'origine
		utils.showMessageDialog(msgs.MSG("Error occurred", "Une erreur est survenue"),
								msgs.MSG("An error occurred while loading scores. The file may be corrupted, all your score are deleted.",
										 "Une erreur est survenue lors de la lecture des scores. Le ficher est probablement corrompu, tous vos scores ont été supprimés."))
		saveScores()

def saveScores():
	"""
	Sauvegarde au sein d'un fichier JSON compressé en GZIP (scores.gz) les scores actuels
	"""
	# Création de scores sérialisés
	l = list()
	for score in utils.SCORES:
		# Pour chaque score, création d'un dictionnaire comprenant les informations des scores en convertissant voitures et cartes par leurs identifiants numériques
		obj = dict(car = cars.CARS.index(score.car), map = maps.MAPS.index(score.map), laps_time = score.laps_time, total_time = score.total_time, total_time_seconds = score.total_time_seconds)
		l.append(obj)
	# Traduction en JSON
	jsoned = json.dumps(l, sort_keys = True, indent = 4)

	# Écriture dans le fichier compressé en GZIP
	with gzip.open("scores.gz", "wb") as f:
		f.write(jsoned.encode("UTF-8"))

def getHighScore(map : maps.Map):
	"""
	Renvoie le plus gros score effectué sur une carte
	Renvoie None si aucun score n'existe
	"""
	highScore = None
	for score in utils.SCORES:
		if score.map is map and (highScore is None or score < highScore):
			highScore = score

	return highScore

class Score:
	def __init__(self, car = None, map = None, laps_time = list(), total_time = None, total_time_seconds = -1, save = True):
		"""
		Constructeur par défaut d'un score, comprenant la voiture de course, la carte, les temps à chaque tour ainsi que le temps global (formatté et numérique)
		"""
		self.car = car
		self.map = map
		self.laps_time = laps_time
		self.total_time = total_time
		self.total_time_seconds = total_time_seconds
		# Ajout du score à la liste des scores et sauvegarde si nécessaire
		utils.SCORES.append(self)
		if save:
			saveScores()

	def __lt__(self, other):
		"""
		Comparaison : renvoie True si le temps total de ce score est inférieur à celui d'un autre
		Permet d'effectuer des choses de la sorte my_score < my_other_score
		Nécessité d'avoir la même carte
		"""
		if other is None:
			return False
		if self.map is not other.map:
			raise Exception("Maps are different")
		return self.total_time_seconds < other.total_time_seconds

	def __le__(self, other):
		"""
		Comparaison : renvoie True si le temps total de ce score est inférieur ou égal à celui d'un autre
		Permet d'effectuer des choses de la sorte my_score <= my_other_score
		Nécessité d'avoir la même carte
		"""
		if other is None:
			return False
		if self.map is not other.map:
			raise Exception("Maps are different")
		return self.total_time_seconds <= other.total_time_seconds

	def __gt__(self, other):
		"""
		Comparaison : renvoie True si le temps total de ce score est supérieur à celui d'un autre
		Permet d'effectuer des choses de la sorte my_score > my_other_score
		Nécessité d'avoir la même carte
		"""
		if other is None:
			return False
		if self.map is not other.map:
			raise Exception("Maps are different")
		return self.total_time_seconds > other.total_time_seconds

	def __ge__(self, other):
		"""
		Comparaison : renvoie True si le temps total de ce score est supérieur à celui d'un autre
		Permet d'effectuer des choses de la sorte my_score >= my_other_score
		Nécessité d'avoir la même carte
		"""
		if other is None:
			return False
		if self.map is not other.map:
			raise Exception("Maps are different")
		return self.total_time_seconds >= other.total_time_seconds

class Scores(GUI):
	def __init__(self, window : tk.Tk):
		"""
		Constructeur par défaut du menu de scores
		Prend comme argument la fenêtre et le constructeur de partie
		"""
		GUI.__init__(self, window)

		# Création du bouton retour
		backBtn = tk.Button(window, textvariable = msgs.BACK, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 15, borderwidth = 4, bg = utils.BUTTON_BACKGROUND, relief = "groove", command = lambda : back(window))
		backBtn.place(relx = .74, rely = .88, relwidth = .26, relheight = .12)
		self.appendChild(backBtn)

		# Détermination du nombre de colonnes (1 colonne pour la carte, 1 colonne pour le temps, 1 colonne pour la voiture, autant de colonnes qui il y a de tours au maximum
		columns = 3
		for map in maps.MAPS:
			columns = max(columns, map.max_laps + 3)

		# Définition du poids de chaque colonne à 1
		for i in range(columns):
			window.columnconfigure(i, weight = 1)

		# Définition et affichage des en-têtes
		total_time_label = tk.Label(window, textvariable = msgs.TOTAL_TIME, font = ("Plantagenet Cherokee", 18, "bold"), relief = "groove")
		total_time_label.grid(row = 0, column = 1, sticky = "nsew")
		self.appendChild(total_time_label)
		car_label = tk.Label(window, textvariable = msgs.CAR, font = ("Plantagenet Cherokee", 18, "bold"), relief = "groove")
		car_label.grid(row = 0, column = columns - 1, sticky = "nsew")
		self.appendChild(car_label)

		# Affichage des en-têtes des temps par tour
		for lap in range(0, columns - 3):
			lap_time_label = tk.Label(window, textvariable = msgs.LAP_TIME.format(lap + 1), font = ("Plantagenet Cherokee", 18, "bold"), relief = "groove")
			lap_time_label.grid(row = 0, column = lap + 2, sticky = "nsew")
			self.appendChild(lap_time_label)

		# Curseur donnant la ligne actuelle du tableau
		row_index = 1

		for map_index in range(len(maps.MAPS)):
			# Pour chaque carte, récupérer la liste des scores triés par le temps effectués sur cette carte
			map = maps.MAPS[map_index]
			map_scores = list()
			for score in utils.SCORES:
				if score.map == map:
					map_scores.append(score)
			map_scores.sort()

			# Afficher le nom de la carte à gauche
			mapLabel = tk.Label(window, textvariable = map.name, font = ("Plantagenet Cherokee", 18, "bold"), relief = "groove")
			mapLabel.grid(row = row_index, column = 0, rowspan = max(1, len(map_scores)), sticky = "nsew")
			self.appendChild(mapLabel)

			for score in map_scores:
				# Pour chaque score, afficher le temps total et la voiture utilisée
				total_time_label = tk.Label(window, text = score.total_time, font = ("Plantagenet Cherokee", 18), relief = "groove")
				total_time_label.grid(row = row_index, column = 1, sticky = "nsew")
				self.appendChild(total_time_label)
				car_label = tk.Label(window, textvariable = score.car.name, font = ("Plantagenet Cherokee", 18), relief = "groove")
				car_label.grid(row = row_index, column = columns - 1, sticky = "nsew")
				self.appendChild(car_label)

				for lap in range(map.max_laps):
					# Pour chaque tour, afficher le temps effectué
					lap_time_label = tk.Label(window, text = score.laps_time[lap], font = ("Plantagenet Cherokee", 18), relief = "groove")
					lap_time_label.grid(row = row_index, column = lap + 2, sticky = "nsew")
					self.appendChild(lap_time_label)
				# Incrémenter le compteur de ligne
				row_index += 1

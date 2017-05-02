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
			Score(car, map, time_laps, total_time)
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
	l = list()
	for score in utils.SCORES:
		obj = dict(car = cars.CARS.index(score.car), map = maps.MAPS.index(score.map), laps_time = score.laps_time, total_time = score.total_time, total_time_seconds = score.total_time_seconds)
		l.append(obj)
	# Traduction en JSON
	jsoned = json.dumps(l, sort_keys = True, indent = 4)

	# Écriture dans le fichier compressé en GZIP
	with gzip.open("scores.gz", "wb") as f:
		f.write(jsoned.encode("UTF-8"))

class Score:
	def __init__(self, car = None, map = None, laps_time = list(), total_time = None, total_time_seconds = -1):
		self.car = car
		self.map = map
		self.laps_time = laps_time
		self.total_time = total_time
		self.total_time_seconds = total_time_seconds
		utils.SCORES.append(self)
		saveScores()

	def __lt__(self, other):
		if self.map is not other.map:
			raise Exception("Maps are different")
		return self.total_time_seconds < other.total_time_seconds

	def __gt__(self, other):
		if self.map is not other.map:
			raise Exception("Maps are different")
		return self.total_time_seconds > other.total_time_seconds

class Scores(GUI):
	def __init__(self, window : tk.Tk):
		"""
		Constructeur par défaut du menu de scores
		Prend comme argument la fenêtre et le constructeur de partie
		"""
		GUI.__init__(self, window)

		# Création du bouton retour
		backBtn = tk.Button(window, textvariable = msgs.BACK, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 15, borderwidth = 4, bg = utils.BUTTON_BACKGROUND, relief = "raise", command = lambda : back(window))
		backBtn.place(relx = .74, rely = .88)

		row_index = 0
		columns = 2
		for map in maps.MAPS:
			columns = max(columns, map.max_laps + 2)

		for i in range(columns):
			window.columnconfigure(i, weight = 1)

		for map_index in range(len(maps.MAPS)):
			map = maps.MAPS[map_index]
			map_scores = list()
			for score in utils.SCORES:
				if score.map == map:
					map_scores.append(score)
			map_scores.sort()

			mapLabel = tk.Label(window, textvariable = map.name, font = ("Plantagenet Cherokee", 30, "bold"))
			mapLabel.grid(row = row_index, column = 0, columnspan = columns, pady = 50)
			self.appendChild(mapLabel)
			row_index += 1

			total_time_label = tk.Label(window, textvariable = msgs.TIME, font = ("Plantagenet Cherokee", 24, "bold"))
			total_time_label.grid(row = row_index, column = 0)
			self.appendChild(total_time_label)
			car_label = tk.Label(window, textvariable = msgs.CAR, font = ("Plantagenet Cherokee", 24, "bold"))
			car_label.grid(row = row_index, column = columns - 1)
			self.appendChild(car_label)

			for lap in range(map.max_laps):
				lap_time_label = tk.Label(window, textvariable = msgs.LAP_TIME.format(lap + 1), font = ("Plantagenet Cherokee", 24, "bold"))
				lap_time_label.grid(row = row_index, column = lap + 1)
				self.appendChild(lap_time_label)

			row_index += 1

			for score in map_scores:
				total_time_label = tk.Label(window, text = score.total_time, font = ("Plantagenet Cherokee", 24))
				total_time_label.grid(row = row_index, column = 0)
				self.appendChild(total_time_label)
				car_label = tk.Label(window, textvariable = score.car.name, font = ("Plantagenet Cherokee", 24))
				car_label.grid(row = row_index, column = columns - 1)
				self.appendChild(car_label)

				for lap in range(map.max_laps):
					lap_time_label = tk.Label(window, text = score.laps_time[lap], font = ("Plantagenet Cherokee", 24))
					lap_time_label.grid(row = row_index, column = lap + 1)
					self.appendChild(lap_time_label)
				row_index += 1

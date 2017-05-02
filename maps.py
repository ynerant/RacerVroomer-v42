#coding : utf-8

import messages as msgs
import json

# Liste de toutes les cartes disponibles
MAPS = list()

class Map :
	def __init__(self, name : msgs.MSG, fileName):
		"""
		Constructeur par défaut des cartes
		Prend en paramètres le nom (localisé/traduit) de la carte ainsi que le fichier contenant toutes les informations
		"""
		self.name = name
		self.fileName = fileName

		# Chargement du fichier JSON
		try:
			with open("maps/" + fileName, "r") as f:
				jsoned = f.read()
		except:
			print("An error occured while loading the map called \"" + name.en + "\" with filename \"" + fileName + "\", map not loaded")
			return

		# Parcours du fichier JSON et conversion en un dictionnaire Python
		obj = json.loads(jsoned) #type: dict

		# Attribution de tous les paramètres (fichier d'image, de miniature, longueur, largeur, nombre de tours, ligne de départ et murs)
		self.img_file = obj["img_file"]
		self.thumbnail = obj["thumbnail"]
		self.width = int(obj["width"])
		self.height = int(obj["height"])
		self.max_laps = int(obj["max_laps"])
		# La ligne de départ peut être considérée comme un mur
		# Un mur est une ligne faisant obsctacle à la voiture
		self.start = Wall(obj["start"])
		raw_walls = obj["walls"]
		self.walls = []
		for raw_wall in raw_walls:
			self.walls.append(Wall(raw_wall))

		# Ajout à la liste MAPS
		MAPS.append(self)

	def __str__(self):
		return "{Map name=\"" + self.name.get() + "\", size=" + str(self.width) + "x" + str(self.height) + ", filename=\"" + self.fileName + "\", img_file=\"" + self.img_file \
			   + "\", max_laps=" + str(self.max_laps) + ", start=" + str(self.start) + ", walls=" + str(self.walls) + "}"

class Wall :
	def __init__(self, args):
		"""
		Constructeur par défaut d'un mur
		Prend en argument un tuple de taille 4 comprenant les coordonnées du mur
		Ces coordonnées sont dans l'ordre l'abscisse de début, celle de fin, l'ordonnée de début et celle de fin
		"""
		self.x_start = int(args[0])
		self.x_end = int(args[1])
		self.y_start = int(args[2])
		self.y_end = int(args[3])

	def length(self):
		"""
		Renvoie la taille du mur
		"""
		return ((self.x_end - self.x_start) ** 2 + (self.y_end - self.y_start) ** 2) ** 0.5

	def __str__(self):
		return "{Wall x=[" + str(self.x_start) + ", " + str(self.x_end) + "], y=[" + str(self.y_start) + ", " + str(self.y_end) + "]}"

TEST_LOOP = Map(msgs.TEST_LOOP, "test_loop.map")
PHANTOM_LABYRINTH = Map(msgs.PHANTOM_LABYRINTH, "phantom_labyrinth.map")

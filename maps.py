#coding : utf-8

import messages as msgs
import json

# Liste de toutes les cartes disponibles
MAPS = list()

class Map :
	def __init__(self, name : msgs.MSG, fileName):
		"""
		Constructeur par défaut des cartes
		:param name: Name in-game of the map (localized)
		:param fileName: Path relative to ./maps to find the JSON file containing map infos
		"""
		self.name = name
		self.fileName = fileName

		# Loading JSON file
		try:
			with open("maps/" + fileName, "r") as f:
				jsoned = f.read()
		except:
			print("An error occured while loading the map called \"" + name.en + "\" with filename \"" + fileName + "\", map not loaded")
			return

		# Parsing the JSON file into a dictionnary
		obj = json.loads(jsoned) #type: dict

		# Attributing all parameters (img file, thumbnail file, width, height, laps, start line and walls)
		self.img_file = obj["img_file"]
		self.thumbnail = obj["thumbnail"]
		self.width = int(obj["width"])
		self.height = int(obj["height"])
		self.max_laps = int(obj["max_laps"])
		# Start line is considered line a wall
		# A wall is a line
		self.start = Wall(obj["start"])
		raw_walls = obj["walls"]
		self.walls = []
		for raw_wall in raw_walls:
			self.walls.append(Wall(raw_wall))

		# Appending MAPS
		MAPS.append(self)

	def __str__(self):
		return "{Map name=\"" + self.name.get() + "\", size=" + str(self.width) + "x" + str(self.height) + ", filename=\"" + self.fileName + "\", img_file=\"" + self.img_file \
			   + "\", max_laps=" + str(self.max_laps) + ", start=" + str(self.start) + ", walls=" + str(self.walls) + "}"

class Wall :
	def __init__(self, args):
		"""
		Default wall constructor
		:param args: list or tuple, which length is 4.
		First value is the abscissa
		"""
		self.x_start = int(args[0])
		self.x_end = int(args[1])
		self.y_start = int(args[2])
		self.y_end = int(args[3])

	def length(self):
		return ((self.x_end - self.x_start) ** 2 + (self.y_end - self.y_start) ** 2) ** 0.5

	def __str__(self):
		return "{Wall x=[" + str(self.x_start) + ", " + str(self.x_end) + "], y=[" + str(self.y_start) + ", " + str(self.y_end) + "]}"

TEST_LOOP = Map(msgs.TEST_LOOP, "test_loop.map")
PHANTOM_LABYRINTH = Map(msgs.PHANTOM_LABYRINTH, "phantom_labyrinth.map")

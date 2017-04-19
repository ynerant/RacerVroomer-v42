#coding : utf-8

import messages as msgs
import json
#import tkinter as tk

MAPS = []

class Map :
	def __init__(self, name : msgs.MSG, fileName):
		self.name = name
		self.fileName = fileName

		try:
			with open("maps/" + fileName, "r") as f:
				jsoned = f.read()
		except:
			print("An error occured while loading the map called \"" + name.en + "\" with filename \"" + fileName + "\", map not loaded")
			return

		obj = json.loads(jsoned) #type: dict

		self.img_file = obj["img_file"]
		self.thumbnail = obj["thumbnail"]
		self.width = int(obj["width"])
		self.height = int(obj["height"])
		self.start = Wall(obj["start"])
		raw_walls = obj["walls"]
		self.walls = []
		for raw_wall in raw_walls:
			self.walls.append(Wall(raw_wall))

		MAPS.append(self)

	def __str__(self):
		return "{Map name=\"" + self.name.get() + "\", size=" + str(self.width) + "x" + str(self.height) + ", filename=\"" + self.fileName + "\", img_file=\"" + self.img_file \
			   + "\", start=" + str(self.start) + ", walls=" + str(self.walls) + "}"

class Wall :
	def __init__(self, args):
		self.x_start = int(args[0])
		self.x_end = int(args[1])
		self.y_start = int(args[2])
		self.y_end = int(args[3])

	def length(self):
		return ((self.x_end - self.x_start) ** 2 + (self.y_end - self.y_start) ** 2) ** 0.5

	def __str__(self):
		return "{Wall x=[" + str(self.x_start) + ", " + str(self.x_end) + "], y=[" + str(self.y_start) + ", " + str(self.y_end) + "]}"

BABY = Map(msgs.BABY, "baby.map")
CIRCUIT_8 = Map(msgs.CIRCUIT_8, "8_circuit.map")
TEST_LOOP = Map(msgs.TEST_LOOP, "test_loop.map")

#coding : utf-8

import tkinter as tk
import messages as msgs
from guis import GUI, back, game
import cars, maps
from PIL import Image

class GameBuilder:
	CURRENT_GAME_BUILDER = None

	class Mode:
		def __init__(self, singleplayer):
			self.sp = singleplayer
			self.mp = not singleplayer

	SINGLE_PLAYER_MODE = Mode(True)
	MULTI_PLAYER_MODE = Mode(False)


	def __init__(self, mode : Mode):
		self.car = None
		self.map = None
		self.mode = mode

	def start(self, window):
		game.Game(window, self)

class CarChooser(GUI):
	def __init__(self, window : tk.Tk, gameBuilder : GameBuilder):
		GUI.__init__(self)

		self.builder = gameBuilder

		for i in range(len(cars.CARS)):
			car = cars.CARS[i]
			label = tk.Label(window, textvariable = car.name, font = ("Plantagenet Cherokee", 30))
			label.grid(row = 2 * i, column = 0, rowspan = 2)
			speedLabel = tk.Label(window, textvariable = msgs.SPEED.format(car.speed), font = ("Plantagenet Cherokee", 22))
			speedLabel.grid(row = 2 * i, column = 1)
			sizeLabel = tk.Label(window, textvariable = msgs.SIZE.format(car.width, car.height), font = ("Plantagenet Cherokee", 22))
			sizeLabel.grid(row = 2 * i + 1, column = 1)
			choose = tk.Button(window, textvariable = msgs.CHOOSE, bg="#f8a1a1", font = ("Plantagenet Cherokee", 22))
			choose.grid(row = 2 * i, column = 2, rowspan = 2)

			if self.builder.car == car:
				ok = tk.Label(window, text = "ü", font = ("Wingdings", 42))
				ok.grid(row = 2 * i, column = 3, rowspan = 2)
				self.children.append(ok)

			self.registerChooseListener(window, choose, car)

			self.children.append(label)
			self.children.append(speedLabel)
			self.children.append(sizeLabel)
			self.children.append(choose)

		window.columnconfigure(0, weight = 3)
		window.columnconfigure(1, weight = 2)
		window.columnconfigure(2, weight = 2)
		window.columnconfigure(3, weight = 1)

		backBtn = tk.Button(window, textvariable = msgs.BACK, bg="#f8a1a1", font = ("Plantagenet Cherokee", 30), anchor = "center", width = 20, borderwidth = 10, relief = "groove", command = lambda : back(window))
		backBtn.grid(row = len(cars.CARS) * 2 + 1, column = 0, columnspan = 4, pady = 100)
		self.children.append(backBtn)

	def registerChooseListener(self, window, button, car):
		def choose_car():
			self.builder.car = car
			back(window)
		button.bind("<ButtonRelease-1>", lambda event : choose_car())

class MapChooser(GUI):
	def __init__(self, window : tk.Tk, gameBuilder : GameBuilder):
		GUI.__init__(self)

		self.builder = gameBuilder

		for i in range(len(maps.MAPS)):
			map = maps.MAPS[i]
			image = Image.open("images/thumbnails/" + map.thumbnail)
			image = image.resize((100, 100), Image.ANTIALIAS)
			image.save("images/thumbnails/" + map.thumbnail, "png")
			thumbnail = tk.PhotoImage(file = "images/thumbnails/" + map.thumbnail)
			thumbnailLabel = tk.Label(window, image = thumbnail)
			thumbnailLabel.image = thumbnail
			thumbnailLabel.grid(row = i, column = 0, rowspan = 1)
			label = tk.Label(window, textvariable = map.name, font = ("Plantagenet Cherokee", 30))
			label.grid(row = i, column = 1, rowspan = 1)
			sizeLabel = tk.Label(window, textvariable = msgs.SIZE.format(map.width, map.height), font = ("Plantagenet Cherokee", 22))
			sizeLabel.grid(row = i, column = 2)
			choose = tk.Button(window, textvariable = msgs.CHOOSE, bg="#f8a1a1", font = ("Plantagenet Cherokee", 22))
			choose.grid(row = i, column = 3, rowspan = 1)

			if self.builder.map == map:
				ok = tk.Label(window, text = "ü", font = ("Wingdings", 42))
				ok.grid(row = i, column = 4, rowspan = 1)
				self.children.append(ok)

			self.registerChooseListener(window, choose, map)

			self.children.append(thumbnailLabel)
			self.children.append(label)
			self.children.append(sizeLabel)
			self.children.append(choose)

		window.columnconfigure(0, weight = 1)
		window.columnconfigure(1, weight = 3)
		window.columnconfigure(2, weight = 2)
		window.columnconfigure(3, weight = 2)
		window.columnconfigure(4, weight = 1)

		backBtn = tk.Button(window, textvariable = msgs.BACK, font = ("Plantagenet Cherokee", 30), bg="#f8a1a1", anchor = "center", width = 20, borderwidth = 10, relief = "groove", command = lambda : back(window))
		backBtn.grid(row = len(cars.CARS) * 2 + 1, column = 0, columnspan = 5, pady = 100)
		self.children.append(backBtn)

	def registerChooseListener(self, window, button, map):
		def choose_map():
			self.builder.map = map
			back(window)
		button.bind("<ButtonRelease-1>", lambda event : choose_map())

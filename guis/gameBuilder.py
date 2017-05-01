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
			self.sp = singleplayer
			self.mp = not singleplayer

	SINGLE_PLAYER_MODE = Mode(True)
	MULTI_PLAYER_MODE = Mode(False)


	def __init__(self, mode : Mode):
		self.car = None
		self.map = None
		self.mode = mode

	def start(self, window):
		GameBuilder.CURRENT_GAME_BUILDER = None
		game.Game(window, self)

class CarChooser(GUI):
	def __init__(self, window : tk.Tk, gameBuilder : GameBuilder):
		GUI.__init__(self)

		self.builder = gameBuilder

		master = tk.Frame(window, width = window.winfo_screenwidth(), height = window.winfo_screenheight())
		master.place(x = 0, y = 0, relwidth = 1, relheight = 1)
		self.appendChild(master)

		vscrollbar = tk.Scrollbar(master, orient = tk.VERTICAL)
		hscrollbar = tk.Scrollbar(master, orient = tk.HORIZONTAL)
		vscrollbar.pack(side = tk.RIGHT, fill = tk.Y, expand = tk.FALSE)
		hscrollbar.pack(side = tk.BOTTOM, fill = tk.X, expand = tk.FALSE)
		self.appendChild(vscrollbar)
		self.appendChild(hscrollbar)

		canvas = tk.Canvas(master, bd = 0, highlightthickness = 0, xscrollcommand = hscrollbar.set, yscrollcommand = vscrollbar.set, width = window.winfo_screenwidth(), height = window.winfo_screenheight(), scrollregion = "0 0 %s %s" % (window.winfo_screenwidth() + 54, window.winfo_screenheight() - 100))
		frame = tk.Frame(canvas, width = window.winfo_screenwidth(), height = window.winfo_screenheight())
		canvas.create_window(0, 0, window = frame, anchor = tk.NW)
		canvas.pack(side = tk.LEFT, fill = tk.BOTH, expand = tk.FALSE)
		canvas.xview_moveto(0)
		canvas.yview_moveto(0)

		vscrollbar.config(command = canvas.yview)
		hscrollbar.config(command = canvas.xview)

		for i in range(len(cars.CARS)):
			car = cars.CARS[i]
			image = Image.open("images/thumbnails/" + car.thumbnail_file)
			image = image.resize((100, 100), Image.ANTIALIAS)
			image.save("images/thumbnails/" + car.thumbnail_file, "png")
			thumbnail = tk.PhotoImage(file = "images/thumbnails/" + car.thumbnail_file)
			thumbnailLabel = tk.Label(frame, image = thumbnail)
			thumbnailLabel.image = thumbnail
			thumbnailLabel.grid(row = 5 * i, column = 0, rowspan = 4)
			label = tk.Label(frame, textvariable = car.name, font = ("Plantagenet Cherokee", 30))
			label.grid(row = 5 * i, column = 1, rowspan = 4)
			speedLabel = tk.Label(frame, textvariable = msgs.MAX_SPEED.format(car.max_speed), font = ("Plantagenet Cherokee", 16))
			speedLabel.grid(row = 5 * i, column = 2)
			accelerateLabel = tk.Label(frame, textvariable = msgs.ACCELERATION.format(60 * car.acceleration), font = ("Plantagenet Cherokee", 16))
			accelerateLabel.grid(row = 5 * i + 1, column = 2)
			sizeLabel = tk.Label(frame, textvariable = msgs.SIZE.format(car.width, car.height), font = ("Plantagenet Cherokee", 16))
			sizeLabel.grid(row = 5 * i + 2, column = 2)
			maniabilityLabel = tk.Label(frame, textvariable = msgs.MANIABILITY.format(car.maniability), font = ("Plantagenet Cherokee", 16))
			maniabilityLabel.grid(row = 5 * i + 3, column = 2)
			choose = tk.Button(frame, textvariable = msgs.CHOOSE, bg = utils.BUTTON_BACKGROUND, font = ("Plantagenet Cherokee", 22))
			choose.grid(row = 5 * i, column = 3, rowspan = 4)

			if self.builder.car == car:
				ok = tk.Label(frame, text = "ü", font = ("Wingdings", 42))
				ok.grid(row = 5 * i, column = 4, rowspan = 4)
				self.appendChild(ok)

			if i < len(cars.CARS) - 1:
				canvas = tk.Canvas(frame, width = window.winfo_screenwidth(), height = 5, bg = "lightgray")
				canvas.grid(row = 5 * i + 4, columnspan = 4)
				self.appendChild(canvas)

			self.registerChooseListener(window, choose, car)

			self.appendChild(frame)
			self.appendChild(thumbnailLabel)
			self.appendChild(label)
			self.appendChild(speedLabel)
			self.appendChild(accelerateLabel)
			self.appendChild(sizeLabel)
			self.appendChild(maniabilityLabel)
			self.appendChild(choose)

		backBtn = tk.Button(frame, textvariable = msgs.BACK, bg = utils.BUTTON_BACKGROUND, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 20,
							borderwidth = 10, relief = "groove", command = lambda : back(window))
		backBtn.grid(row = 5 * (len(cars.CARS) + 1), columnspan = 4, pady = 100)
		self.appendChild(backBtn)

		frame.columnconfigure(0, weight = 1)
		frame.columnconfigure(1, weight = 2)
		frame.columnconfigure(2, weight = 2)
		frame.columnconfigure(3, weight = 2)
		frame.columnconfigure(4, weight = 1)

		def _configure_frame(event):
			# update the scrollbars to match the size of the inner frame
			size = (frame.winfo_reqwidth(), frame.winfo_reqheight())
			canvas.config(scrollregion = "0 0 %s %s" % size)
			print(canvas.config("scrollregion"))
		frame.bind('<Configure>', _configure_frame)

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
			choose = tk.Button(window, textvariable = msgs.CHOOSE, bg = utils.BUTTON_BACKGROUND, font = ("Plantagenet Cherokee", 22))
			choose.grid(row = i, column = 3, rowspan = 1)

			if self.builder.map == map:
				ok = tk.Label(window, text = "ü", font = ("Wingdings", 42))
				ok.grid(row = i, column = 4, rowspan = 1)
				self.appendChild(ok)

			self.registerChooseListener(window, choose, map)

			self.appendChild(thumbnailLabel)
			self.appendChild(label)
			self.appendChild(sizeLabel)
			self.appendChild(choose)

		window.columnconfigure(0, weight = 1)
		window.columnconfigure(1, weight = 2)
		window.columnconfigure(2, weight = 2)
		window.columnconfigure(3, weight = 2)
		window.columnconfigure(4, weight = 1)

		backBtn = tk.Button(window, textvariable = msgs.BACK, font = ("Plantagenet Cherokee", 30), bg = utils.BUTTON_BACKGROUND, anchor = "center",
							width = 20, borderwidth = 10, relief = "groove", command = lambda : back(window))
		backBtn.grid(row = len(cars.CARS) * 2 + 1, column = 0, columnspan = 5, pady = 100)
		self.appendChild(backBtn)

	def registerChooseListener(self, window, button, map):
		def choose_map():
			self.builder.map = map
			back(window)
		button.bind("<ButtonRelease-1>", lambda event : choose_map())

#coding : utf-8

import tkinter as tk
from PIL import Image, ImageTk
from guis import GUI
import math
from threading import Thread
import time

class Game(GUI):
	def __init__(self, window, builder):
		GUI.__init__(self)

		self.raw_car = builder.car
		self.map = builder.map

		self.canvas = tk.Canvas(window, width = window.winfo_screenwidth(), height = window.winfo_screenheight(), bg = "green")

		self.background_img = ImageTk.PhotoImage(file = "images/maps/" + self.map.img_file)
		self.background = self.canvas.create_image(window.winfo_screenwidth(), window.winfo_screenheight(), image = self.background_img)
		self.canvas.focus_set()
		self.canvas.pack()
		self.canvas.coords(self.background, window.winfo_screenwidth() / 2, window.winfo_screenheight() / 2)

		self.car = Car(window, self)

		self.children.append(self.canvas)

class Car:
	def __init__(self, window, game):
		self.game = game
		self.car = game.raw_car
		self.window = window

		start_line = game.map.start
		self.x = int((start_line.x_end + start_line.x_start) / 2) - 60
		self.y = int((start_line.y_end + start_line.y_start) / 2) - 120
		self.canvas = game.canvas
		img_temp = Image.open("images/cars/" + self.car.img_file)
		img_temp = img_temp.convert("RGBA")
		img_temp = img_temp.resize((self.car.width, self.car.height), Image.ANTIALIAS)
		self.img_img = ImageTk.PhotoImage(img_temp)
		self.img = self.canvas.create_image(0, 0, image = self.img_img)
		self.canvas.coords(self.img, self.x - self.car.width / 2, self.y - self.car.height / 2)

		self.speed = 0.0
		self.angle = 0.0
		self.vector = self.angle_to_normalized_vector()

		self.thread = CarThread(self)
		self.thread.start()

		window.bind("<KeyPress>", lambda event : self.catch_key_event(event))

	def angle_to_normalized_vector(self):
		return math.cos(self.angle), math.sin(self.angle)

	def catch_key_event(self, event):
		from utils import CONTROLS
		key = event.keysym.upper()
		if key == CONTROLS["forward"]:
			self.forward()
		elif key == CONTROLS["backward"]:
			self.backward()
		elif key == CONTROLS["left"]:
			self.left()
		elif key == CONTROLS["right"]:
			self.right()

	def forward(self):
		self.speed = min(self.speed + 1.0, float(self.car.speed))
		print("accelerate: " + str(self.speed))

	def backward(self):
		self.speed = max(self.speed - 1.0, float(-self.car.speed))
		print("break: " + str(self.speed))

	def left(self):
		self.angle -= math.pi / 16
		self.vector = self.angle_to_normalized_vector()
		img_temp = Image.open("images/cars/" + self.car.img_file)
		img_temp = img_temp.convert("RGBA")
		img_temp = img_temp.resize((self.car.width, self.car.height), Image.ANTIALIAS)
		img_temp = img_temp.rotate(-self.angle * 180 / math.pi, expand = 1)
		self.img_img = ImageTk.PhotoImage(img_temp)
		self.img = self.canvas.create_image(self.car.width, self.car.height, image = self.img_img)

	def right(self):
		self.angle += math.pi / 16
		self.vector = self.angle_to_normalized_vector()
		img_temp = Image.open("images/cars/" + self.car.img_file)
		img_temp = img_temp.convert("RGBA")
		img_temp = img_temp.resize((self.car.width, self.car.height), Image.ANTIALIAS)
		img_temp = img_temp.rotate(-self.angle * 180 / math.pi, expand = 1)
		self.img_img = ImageTk.PhotoImage(img_temp)
		self.img = self.canvas.create_image(self.car.width, self.car.height, image = self.img_img)

class CarThread(Thread):
	def __init__(self, car):
		Thread.__init__(self)
		self.car = car

	def run(self):
		car = self.car
		while True:
			car.x += car.speed * car.vector[0] / 60.0
			car.y += car.speed * car.vector[1] / 60.0
			car.speed *= 0.98
			car.canvas.coords(car.img, car.x - car.car.width / 2, car.y - car.car.height / 2)
			time.sleep(1.0 / 60.0)
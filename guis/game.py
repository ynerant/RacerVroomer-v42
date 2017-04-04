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

		window.wm_attributes("-topmost", True)
		window.wm_attributes("-disabled", True)
		window.wm_attributes("-transparentcolor", "purple")

		self.raw_car = builder.car
		self.map = builder.map
		self.background = tk.PhotoImage(file = "images/maps/" + self.map.img_file)

		background_label = tk.Label(window, image = self.background)
		background_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)
		background_label.image = self.background

		self.car = Car(window, self)

		self.children.append(background_label)

class Car:
	def __init__(self, window, game):
		self.game = game
		self.car = game.raw_car

		img_temp = Image.open("images/cars/" + self.car.img_file)
		img_temp = img_temp.convert("RGBA")
		img_temp = img_temp.resize((self.car.width, self.car.height), Image.ANTIALIAS)
		img_temp.save("images/cars/tmp." + self.car.img_file)
		img = ImageTk.PhotoImage(img_temp)
		start_line = game.map.start
		self.x = int((start_line.x_end + start_line.x_start) / 2) - 60
		self.y = int((start_line.y_end + start_line.y_start) / 2) - 120
		#self.frame = tk.Frame(window)
		#self.canvas = tk.Canvas(self.frame, width = self.car.width, height = self.car.height)
		#box = self.canvas.create_image(0, 0, image = img)
		#print(box)
		#self.frame.place(x = self.x, y = self.y)
		#self.canvas.pack()
		#game.children.append(self.frame)
		self.car_label = tk.Label(window, image = img, bg = "purple")
		self.car_label.image = img
		self.car_label.place(x = self.x, y = self.y)

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
		img_temp.save("images/cars/tmp." + self.car.img_file)
		self.car_label.destroy()
		self.car_label = tk.Label(self.car_label.winfo_parent(), image = ImageTk.PhotoImage(img_temp), bg = "purple")
		self.car_label.image = ImageTk.PhotoImage(img_temp)
		self.car_label.place(x = self.x, y = self.y)
		#self.canvas.create_image(0, 0, image = tk.PhotoImage(file = "images/cars/tmp." + self.car.img_file))

	def right(self):
		self.angle += math.pi / 16
		self.vector = self.angle_to_normalized_vector()

class CarThread(Thread):
	def __init__(self, car):
		Thread.__init__(self)
		self.car = car

	def run(self):
		car = self.car
		while True:
			car.x += car.speed * car.vector[0] / 60.0
			car.y += car.speed * car.vector[1] / 60.0
			car.speed *= 0.97
			car.car_label.place(x = int(car.x), y = int(car.y))
			time.sleep(1.0 / 60.0)
#coding : utf-8

import tkinter as tk
from PIL import Image, ImageTk
from guis import GUI, mainMenu
import messages as msgs
import math
from threading import Thread
import time

class Game(GUI):
	def __init__(self, window, builder):
		GUI.__init__(self)

		self.raw_car = builder.car
		self.map = builder.map

		self.canvas = tk.Canvas(window, width = window.winfo_screenwidth(), height = window.winfo_screenheight(), bg = "green")

		img_temp = Image.open("images/maps/" + self.map.img_file)
		img_temp = img_temp.convert("RGBA")
		img_temp = img_temp.resize((window.winfo_screenwidth(), window.winfo_screenheight()), Image.ANTIALIAS)
		self.background_img = ImageTk.PhotoImage(img_temp)
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
		self.window = window #type: tk.Tk

		start_line = game.map.start
		self.x = int((start_line.x_end + start_line.x_start) / 2)
		self.y = int((start_line.y_end + start_line.y_start) / 2)
		self.speed = 0.0
		start_line_length = start_line.length()
		dot_product = start_line.x_end - start_line.x_start
		cosinus = dot_product / start_line_length
		self.angle = -math.acos(cosinus) + math.pi / 2
		if start_line.y_start > start_line.y_end:
			self.angle += math.pi
		self.angle = int(16 * self.angle / math.pi) * math.pi / 16
		print(int(16 * self.angle / math.pi))
		self.vector = self.angle_to_normalized_vector()
		self.x -= self.vector[0] * self.car.width / 2
		self.y -= self.vector[1] * self.car.height / 2
		self.canvas = game.canvas
		img_temp = Image.open("images/cars/" + self.car.img_file)
		img_temp = img_temp.convert("RGBA")
		img_temp = img_temp.resize((self.car.width, self.car.height), Image.ANTIALIAS)
		img_temp = img_temp.rotate(-self.angle * 180 / math.pi, expand = 1)
		self.img_img = ImageTk.PhotoImage(img_temp)
		self.img = self.canvas.create_image(0, 0, image = self.img_img)

		self.keys_pressed = set()
		self.paused = False

		self.thread = CarThread(self)
		self.thread.start()

		window.bind("<KeyPress>", lambda event : self.catch_key_press_event(event))
		window.bind("<KeyRelease>", lambda event : self.catch_key_release_event(event))
		window.bind("<FocusOut>", lambda event : self.pause())

	def angle_to_normalized_vector(self):
		return math.cos(self.angle), math.sin(self.angle)

	def catch_key_press_event(self, event):
		if self.paused:
			return

		self.keys_pressed.add(event.keysym.upper())


	def catch_key_release_event(self, event):
		if event.keysym.upper() == "ESCAPE":
			self.pause()
			return

		if event.keysym.upper() in self.keys_pressed:
			self.keys_pressed.remove(event.keysym.upper())

	def pause(self):
		if self.paused:
			return
		self.keys_pressed.clear()
		print("PAUSE")
		self.paused = True

		canvas = self.canvas #type: tk.Canvas
		rectangle = canvas.create_rectangle(0, 0, self.window.winfo_screenwidth(), self.window.winfo_screenheight(), fill = "#F0F0F0", stipple = "gray50")

		def resume():
			self.paused = False
			canvas.delete(rectangle)
			if resumeButton in self.game.children:
				self.game.children.remove(resumeButton)
			if quitButton in self.game.children:
				self.game.children.remove(quitButton)
			resumeButton.destroy()
			quitButton.destroy()
			self.window.unbind("<KeyRelease-Escape>", resumeId)

		def quitGame():
			self.thread.stopped = True
			self.paused = False
			mainMenu.MainMenu(self.window)

		resumeButton = tk.Button(self.window, textvariable = msgs.RESUME, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 15, borderwidth = 10, bg="#f8a1a1", relief = "groove", command = resume)
		quitButton = tk.Button(self.window, textvariable = msgs.QUIT, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 15, borderwidth = 10, bg="#f8a1a1", relief = "groove", command = quitGame)

		fc = lambda event : resume()
		resumeId = self.window.bind("<KeyRelease-Escape>", fc)

		width, height = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
		resumeButton.place(x = width / 3, y = height / 4)
		quitButton.place(x = width / 3, y = height / 2)

		self.game.children.append(resumeButton)
		self.game.children.append(quitButton)

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
		self.stopped = False

	def run(self):
		car = self.car
		while True:
			if car.paused:
				continue

			if self.stopped:
				return

			from utils import CONTROLS
			for key in set(car.keys_pressed):
				if key == CONTROLS["forward"]:
					car.forward()
				elif key == CONTROLS["backward"]:
					car.backward()
				elif key == CONTROLS["left"]:
					car.left()
				elif key == CONTROLS["right"]:
					car.right()

			newX = car.x + car.speed * car.vector[0] / 60.0
			newY = car.y + car.speed * car.vector[1] / 60.0

			collision = False
			for wall in car.game.map.walls:
				dot_product = (wall.x_end - wall.x_start) * (newX - wall.x_start) + (wall.y_end - wall.y_start) * (newY - wall.y_start)
				line = (wall.x_end - wall.x_start, wall.y_end - wall.y_start)
				line_length = math.sqrt(line[0] ** 2 + line[1] ** 2)
				xH, yH = dot_product / (line_length ** 2) * line[0] + wall.x_start, dot_product / (line_length ** 2) * line[1] + wall.y_start

				if xH < min(wall.x_start, wall.x_end) or xH > max(wall.x_start, wall.x_end) or yH < min(wall.y_start, wall.y_end) or yH > max(wall.y_start, wall.y_end):
					continue

				diagonal = math.sqrt(car.car.width ** 2 + car.car.height ** 2) / 2
				if math.sqrt((xH - newX) ** 2 + (yH - newY) ** 2) < diagonal + 0.1:
					collision = True
					break

			if collision:
				car.x = car.x - car.speed * car.vector[0] / 10.0
				car.y = car.y - car.speed * car.vector[1] / 10.0
				if car.speed > 0:
					car.speed = -car.speed
				else:
					car.speed = 0.0
				continue

			car.x = newX
			car.y = newY
			car.speed *= 0.99
			car.canvas.coords(car.img, car.window.winfo_screenwidth() / car.game.map.width * car.x,
							  car.window.winfo_screenheight() / car.game.map.height * car.y)
			time.sleep(1.0 / 60.0)
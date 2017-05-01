#coding : utf-8

import messages as msgs
#import tkinter as tk

CARS = []

class Car :
	def __init__(self, name : msgs.MSG, max_speed : float, acceleration : float, maniability : float, width : int, height : int, img_file : str, thumbnail_file : str):
		self.name = name
		self.max_speed = max_speed
		self.acceleration = acceleration
		self.maniability = maniability
		self.width = width
		self.height = height
		self.img_file = img_file
		self.thumbnail_file = thumbnail_file
		CARS.append(self)

	def __str__(self):
		return "{Car name=\"" + self.name.get() + "\" speed=" + str(self.max_speed) + " size=" + str(self.width) + "x" + str(self.height) + "}"

RED_CAR = Car(msgs.RED_CAR, 42.0, 1.0, 42.0, 42, 42, "red_car.gif", "red_car.png")
BLUE_CAR = Car(msgs.BLUE_CAR, 34.0, 0.34, 34.0, 34, 34, "bluecar.gif", "bluecar.png")
GREEN_CAR = Car(msgs.GREEN_CAR, 10.0, 0.10, 10.0, 10, 10, "greencar.gif", "greencar.png")

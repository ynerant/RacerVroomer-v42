#coding : utf-8

import messages as msgs
#import tkinter as tk

CARS = []

class Car :
	def __init__(self, name : msgs.MSG, speed, width, height, imgFile):
		self.name = name
		self.speed = speed
		self.width = width
		self.height = height
		self.img = imgFile
		CARS.append(self)



	def __str__(self):
		return "{Car name=\"" + self.name.get() + "\" speed=" + str(self.speed) + " size=" + str(self.width) + "x" + str(self.height) + "}"

RED_CAR = Car(msgs.RED_CAR, 42, 42, 42,"rouge.svg")
BLUE_CAR = Car(msgs.BLUE_CAR, 34, 34, 34,"bleue.svg")
GREEN_CAR = Car(msgs.GREEN_CAR, 10, 10, 10,"verte.svg")

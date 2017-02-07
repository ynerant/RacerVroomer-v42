#coding : utf-8

import messages as msgs
#import tkinter as tk

class Car :
	def __init__(self, name : msgs.MSG, speed, width, heigth):
		self.name = name
		self.speed = speed
		self.width = width
		self.height = heigth

RED_CAR = Car(msgs.RED_CAR, 42, 42, 42)
#BLUE_CAR = Car(msgs.BLUE_CAR, 34, 34, 34)
#GREEN_CAR = Car(msgs.GREEN_CAR, 10, 10, 10)



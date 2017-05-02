#coding : utf-8

import messages as msgs
#import tkinter as tk

# Liste de toutes les voitures disponibles
CARS = []

class Car :
	def __init__(self, name : msgs.MSG, max_speed : float, acceleration : float, maniability : float, width : int, height : int, img_file : str, thumbnail_file : str):
		"""
		Constructeur par défaut d'une voiture
		Le nom est localisé
		La vitesse max est en px/s
		L'accélération est en px/s²
		L'angle d'orientation de la voiture est déterminé par la maniabilité; angle = 2pi / maniabilité
		Plus la maniabilité est élevée, moins la voiture va tourner vite
		width (longueur) et height (hauteur) représentent la taille de la voiture en pixels
		img_file (resp. thumbnail_file) est le chemin relatif à ./images/cars/ (resp. ./images/thumbnails/)
				de l'image de la voiture (resp. de la miniature du sélecteur de voiture)
		"""
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

RED_CAR = Car(msgs.RED_CAR, 420.0, .4, 42.0, 42, 38, "red_car.gif", "red_car.png")
BLUE_CAR = Car(msgs.BLUE_CAR, 340.0, 0.6, 34.0, 34, 29, "blue_car.gif", "blue_car.png")
GREEN_CAR = Car(msgs.GREEN_CAR, 190.0, 0.8, 10.0, 54, 46, "green_car.gif", "green_car.png")

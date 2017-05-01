#coding: utf-8

import sys

# Version inspection (only run with Python 3.0+)
if sys.version_info < (3, 0):
	print("This game can only run with Python 3.0+.")
	print("Ce jeu ne peut seulement tourner sous Python 3.0 ou une version supérieure.")
	exit(1)

# Dependencies inspection
try:
	import tkinter as tk
except:
	print("It seems you don't have tkinter installed on your machine. Please install it before running.")
	print("On dirait que tkinter n'est pas installé sur votre machine. Merci de l'installer avant de lancer le jeu.")
	exit(1)

import utils

try:
	import pygame
except:
	utils.showMessageDialog("Pygame not installed / Pygame non-installé", "It seems you don't have pygame installed on your machine. Please install it before running.\n" +
			"On dirait que pygame n'est pas installé sur votre machine. Merci de l'installer avant de lancer le jeu.")
	exit(1)

try:
	import PIL
except:
	utils.showMessageDialog("PIL not installed / PIL non-installé", "It seems you don't have PIL installed on your machine. Please install it before running.\n" +
			"On dirait que PIL n'est pas installé sur votre machine. Merci de l'installer avant de lancer le jeu.")
	exit(1)

# Initialize the window
# It is necessary to  create the window before anything, because when classes are imported, it mays load some window components
# noinspection PyProtectedMember
if tk._default_root is None:
	tk.Tk()

from guis.mainMenu import MainMenu
from guis import settings
import audio

def main():
	"""
	Main method (invoked at launch)
	"""

	# noinspection PyProtectedMember
	window = tk._default_root #type: tk.Tk
	window.title("Racer Vroomer v42")
	# Maximize the window
	if utils.isWindows():
		window.state("zoomed")
	else:
		window.attributes("-zoomed", True)
	width = 840
	height = 420
	# Placing window at the center of the screen (when not maximized)
	screenWidth = window.winfo_screenwidth()
	screenHeight = window.winfo_screenheight()
	window.geometry(str(width) + "x" + str(height) + "+" + str(int((screenWidth - width) / 2)) + "+" + str(int((screenHeight - height) / 2)))

	# noinspection PyUnusedLocal
	def catch_key_event(event):
		if window.attributes("-fullscreen"):
			window.attributes("-fullscreen", False)
		else:
			window.attributes("-fullscreen", True)
		settings.saveSettings()
	window.bind("<KeyPress-F11>", catch_key_event)

	settings.loadSettings()

	MainMenu(window)

	audio.AudioPlayer(window).start()

	window.mainloop()

if __name__ == "__main__" :
	main()

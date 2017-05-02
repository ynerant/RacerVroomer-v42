#coding: utf-8

import sys

# Inspection de la version de Python (ne tourne seulement avec Python 3.0+)
if sys.version_info < (3, 0):
	print("This game can only run with Python 3.0+.")
	print("Ce jeu ne peut seulement tourner sous Python 3.0 ou une version supérieure.")
	exit(1)

# Inspection des dépendances
# Pour chaque module requis, si ce dernier n’est pas trouvé, un message compréhensif est adressé à l’utilisateur, à la place d’une erreur
# Les modules sont : Tkinter (pour le graphique), pygame.mixer (pour le son), PIL (pour le traitement d’images)
try:
	import tkinter as tk
except:
	print("It seems you don’t have tkinter installed on your machine. Please install it before running.")
	print("On dirait que tkinter n’est pas installé sur votre machine. Merci de l’installer avant de lancer le jeu.")
	exit(1)

import utils

try:
	import pygame
except:
	utils.showMessageDialog("Pygame not installed / Pygame non-installé", "It seems you don’t have pygame installed on your machine. Please install it before running.\n" +
			"On dirait que pygame n’est pas installé sur votre machine. Merci de l’installer avant de lancer le jeu.")
	exit(1)

try:
	import PIL
except:
	utils.showMessageDialog("PIL not installed / PIL non-installé", "It seems you don’t have PIL installed on your machine. Please install it before running.\n" +
			"On dirait que PIL n’est pas installé sur votre machine. Merci de l’installer avant de lancer le jeu.")
	exit(1)

# Initialise la fenêtre
# Il est nécessaire de créer la fenêtre avant toute chose, puisque lorsque les classes sont importées, elles peuvent charger quelques composants
# noinspection PyProtectedMember
if tk._default_root is None:
	tk.Tk()

from guis.mainMenu import MainMenu
from guis import settings, scores
import audio

def main():
	"""
	Main method (invoked at launch)
	"""

	# noinspection PyProtectedMember
	window = tk._default_root #type: tk.Tk
	# Affectation du titre
	window.title("Racer Vroomer v42")
	# Affectation de l’icône
	window.iconbitmap("icon.ico")
	# Maximisation de la fenêtre
	if utils.isWindows():
		window.state("zoomed")
	else:
		window.attributes("-zoomed", True)
	# Résolution de base de 840x420 lorsque la fenêtre n’est pas maximisée
	width = 840
	height = 420
	# Placement de la fenêtre au centre de l’écran (quand non-maximisée)
	screenWidth = window.winfo_screenwidth()
	screenHeight = window.winfo_screenheight()
	window.geometry(str(width) + "x" + str(height) + "+" + str(int((screenWidth - width) / 2)) + "+" + str(int((screenHeight - height) / 2)))

	# Quand la touche F11 est pressée, la fenêtre passe en mode plein écran (la touche ne peut être modifiée directement dans le jeu)
	def catch_key_event(event):
		if window.attributes("-fullscreen"):
			window.attributes("-fullscreen", False)
		else:
			window.attributes("-fullscreen", True)
		settings.saveSettings()
	window.bind("<KeyPress-F11>", catch_key_event)

	# Chargement des paramètres
	settings.loadSettings()

	# Chargement des scores
	scores.loadScores()

	# Affichage du menu principal
	MainMenu(window)

	# Démarrage du processus audio, afin de ne pas interrompre le processus principal
	audio.AudioPlayer(window).start()

	# Affichage de la fenêtre et démarrage de la boucle principale
	window.mainloop()

# Démarrage du jeu
if __name__ == "__main__" :
	main()

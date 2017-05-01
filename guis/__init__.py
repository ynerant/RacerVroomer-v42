#coding : utf-8

from audio import AudioPlayer
import tkinter as tk
from PIL import Image, ImageTk

# Fenêtre actuelle
CURRENT_GUI = None
# Anciennes fenêtres affichées, pour un meilleur bouton retour
OLD_GUIS = []

class GUI:
	def __init__(self, window, bg = False):
		"""
		Constructeur par défaut d'une interface
		Prend en paramètre la fenêtre
		Paramètre bg : affichage du fond d'écran par défaut
		"""
		global CURRENT_GUI, OLD_GUIS
		# Si il y avait une ancienne interface (qui arrive tout le temps sauf au démarrage), on la détruit
		if CURRENT_GUI is not None:
			CURRENT_GUI.destroy()
		# La liste children contient tous les composants, facilitant leur future destruction
		self._children = []
		# On ajoute l'ancienne fenêtre à la liste
		OLD_GUIS.insert(0, CURRENT_GUI.__class__)
		# La nouvelle fenêtre remplace l'ancienne
		CURRENT_GUI = self

		# Mise en place du fond d'écran si nécessaire
		if bg:
			# Lecture de l'image avec le module PIL
			bg = Image.open("images/menu/minia.png")
			# Redimensionnement à l'écran avec anti-crénelage
			bg = bg.resize((window.winfo_screenwidth(), window.winfo_screenheight()), Image.ANTIALIAS)
			# Conversion en image Tkinter
			bgImage = ImageTk.PhotoImage(bg)
			# Mise en place de l'image dans un label et affichage de ce dernier
			labelImage = tk.Label(window, image = bgImage)
			labelImage.image = bgImage
			labelImage.pack()
			# Ajout de l'enfant
			self.appendChild(labelImage)
	
	def appendChild(self, child):
		"""
		Ajout d'un composant à la liste children
		"""
		self._children.append(child)
		# Si ce composant est un bouton, invocation de la fonction clickButton où le bouton prend la place d'argument
		if type(child) is tk.Button:
			child.bind("<Button-1>", lambda event : self.clickButton(child))

	def clickButton(self, button):
		"""
		Action effectuée lors d'un clic sur bouton
		Lors d'un clic sur un bouton, déclenchement du son de clic
		"""
		AudioPlayer.playSound(AudioPlayer.CLICK)

	def destroy(self):
		"""
		Destruction de l'interface et de tous ces composants
		"""
		for child in self._children:
			try:
				child.destroy()
			except:
				pass
		self._children.clear()

def back(window):
	"""
	Retour en arrière. Lorsqu'invoquée, la fenêtre précédente s'affiche
	"""
	gui = OLD_GUIS.pop(0)(window)
	OLD_GUIS.pop(0)
	return gui

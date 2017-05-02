#coding : utf-8

from tkinter import messagebox as mb
import sys

# Dictionnaire des contrôles
# Au contrôle est affecté la touche
CONTROLS = dict(forward = 'Z', left = 'Q', backward = 'S', right = 'D')
# Liste des scores
SCORES = list()
# Couleur de fond des boutons
BUTTON_BACKGROUND = "#f8a1a1"

def showMessageDialog(title, text):
	"""
	Affichage d’une boîte de dialogue d’informations
	title est le titre de la boîte et text le contenu
	Chaque argument peut soit être une chaîne de caractères (str), soit un message localisé (messages.MSG)
	"""
	mb.showinfo(title if type(title) is str else title.get(), text if type(text) is str else text.get())

def isWindows():
	"""
	Renvoie True ssi le jeu tourne sous Windows 
	"""
	return "win" in sys.platform.lower()

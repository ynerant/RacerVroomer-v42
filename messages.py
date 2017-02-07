# coding=utf-8
from tkinter import StringVar
import locale

if locale.getlocale(locale.LC_ALL) == (None, None):
	locale.setlocale(locale.LC_ALL, locale.getdefaultlocale()[0][:2])

LOCALE = StringVar(value = locale.getlocale()[0][:2])
if LOCALE.get() != "fr" and LOCALE.get() != "en":
	LOCALE.set("en")


class MSG(StringVar):
	def __init__(self, english_message : str, french_message : str):
		super().__init__()
		self.en = english_message
		self.fr = french_message

		if len(self.fr) == 0:
			self.fr = self.en
		if len(self.en) == 0:
			self.en = self.fr

		# noinspection PyUnusedLocal
		def callback(*kwargs):
			if isFrench():
				self.set(self.fr)
			else:
				self.set(self.en)

		LOCALE.trace_variable("w", callback)
		callback()

	def clone(self):
		return MSG(self.en, self.fr)

	def switch(self, msg):
		self.en = msg.en
		self.fr = msg.fr
		if isFrench():
			self.set(self.fr)
		else:
			self.set(self.en)


def isEnglish():
	return LOCALE.get() == "en"


def isFrench():
	return not isEnglish()

def setEnglish():
	LOCALE.set("en")

def setFrench():
	LOCALE.set("fr")

def switchLanguage():
	if isEnglish():
		setFrench()
	else:
		setEnglish()


####################################################################################
################################ Title screen menus ################################
####################################################################################

SINGLE_PLAYER = MSG("Singleplayer", "Un joueur")
MAP_CHOICE = MSG("Choose map", "Choisir la carte")
CAR_CHOICE = MSG("Choose car", "Choisir la voiture")
MULTI_PLAYER = MSG("Multiplayer", "Multijoueur")
SETTINGS = MSG("Settings", "Options")
QUIT = MSG("Don't quit :(", "Ne quittez pas :(")
BACK = MSG("Back", "Retour")
CHANGE_LANGUAGE = MSG("Changer en français", "Change to english")
DISABLE_MUSIC = MSG("Disable music", "Désactiver la musique")
ENABLE_MUSIC = MSG("Enable music", "Activer la musique")
DISABLE_SOUNDS = MSG("Disable sounds", "Désactiver les effets sonores")
ENABLE_SOUNDS = MSG("Enable sounds", "Activer les effets sonores")

####################################################################################
################################## Boxes messages ##################################
####################################################################################

SOON = MSG("Soon!", "Bientôt !")
FUTURE_FEATURE = MSG("This feature will (probably) be available later!", "Cette fonctionnalité sera (probablement) accessible plus tard !")

####################################################################################
################################## Cars names ##################################
####################################################################################

RED_CAR = MSG("Red Speedo", "La Fulgurante Rouge")

# coding=utf-8
from tkinter import StringVar
import locale
from guis import settings

if locale.getlocale(locale.LC_ALL) == (None, None):
	locale.setlocale(locale.LC_ALL, locale.getdefaultlocale()[0][:2])

LOCALE = StringVar(value = locale.getlocale()[0][:2])
if LOCALE.get() != "fr" and LOCALE.get() != "en":
	LOCALE.set("en")
LOCALE.trace_variable("w", lambda *args : settings.saveSettings())

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

	def format(self, *args):
		obj = self.clone()
		obj.en = obj.en.format(*list(args))
		obj.fr = obj.fr.format(*list(args))
		if isFrench():
			obj.set(obj.fr)
		else:
			obj.set(obj.en)
		return obj


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
START = MSG("Start!", "Démarrer !")
MULTI_PLAYER = MSG("Multiplayer", "Multijoueur")
SETTINGS = MSG("Settings", "Paramètres")
QUIT = MSG("Don't quit :(", "Ne quittez pas :(")
MAIN_MENU = MSG("Title screen", "Menu principal")
BACK = MSG("Back", "Retour")
CHANGE_LANGUAGE = MSG("Changer en français", "Change to english")
DISABLE_MUSIC = MSG("Disable music", "Désactiver la musique")
ENABLE_MUSIC = MSG("Enable music", "Activer la musique")
DISABLE_SOUNDS = MSG("Disable sounds", "Désactiver les effets sonores")
ENABLE_SOUNDS = MSG("Enable sounds", "Activer les effets sonores")
CHANGE_CONTROLS = MSG("Controls", "Contrôles")
WHAT_KEY_FOR = MSG("What key to {}?", "Quelle touche pour {} ?")
MAX_SPEED = MSG("Max speed : {:.1f} px/s", "Vitesse max : {:.1f} px/s")
ACCELERATION = MSG("Acceleration : {:.1f} px/s²", "Accélération : {:.1f} px/s²")
SIZE = MSG("Size : {}x{} px²", "Taille : {}x{} px²")
MANIABILITY = MSG("Maniability : {:.1f} %", "Maniabilité : {:.1f} %")
CHOOSE = MSG("Choose", "Choisir")
RESUME = MSG("Resume", "Reprendre")
LAP_NUMBER = MSG("Lap {}/{}", "Tour {}/{}")
YOU_WIN = MSG("You win in {}!", "Vous avez gagné en {} !")
LAP = MSG("Lap", "Tour")
TIME = MSG("Time", "Temps")


####################################################################################
################################## Controls names ##################################
####################################################################################

FORWARD = MSG("Accelerate", "Accélérer")
TURN_LEFT = MSG("Turn left", "Tourner à gauche")
BACKWARD = MSG("Brake", "Freiner")
TURN_RIGHT = MSG("Turn right", "Tourner à droite")
LOCAL = MSG("Local", "Local")
ONLINE = MSG("Online", "En ligne")

####################################################################################
################################## Boxes messages ##################################
####################################################################################

SOON = MSG("Soon!", "Bientôt !")
FUTURE_FEATURE = MSG("This feature will (probably) be available later!", "Cette fonctionnalité sera (probablement) accessible plus tard !")

####################################################################################
################################## Cars names ######################################
####################################################################################

RED_CAR = MSG("Red Speedo", "La Fulgurante Rouge")
BLUE_CAR = MSG("Blue car", "La voiture bleue")
GREEN_CAR = MSG("Green car", "La voiture verte")


####################################################################################
################################## Maps names ######################################
####################################################################################

BABY = MSG("Baby loop", "Circuit Baby")
CIRCUIT_8 = MSG("8-Circuit", "Circuit en 8")
TEST_LOOP = MSG("Test Loop", "Circuit de test")

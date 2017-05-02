# coding=utf-8
from tkinter import StringVar
import locale
from guis import settings
import utils

# Affectation de la langue par défaut si non présente
if utils.isWindows():
	if locale.getlocale(locale.LC_ALL) == (None, None):
		locale.setlocale(locale.LC_ALL, locale.getdefaultlocale()[0][:2])
else:
	if locale.getlocale(locale.LC_CTYPE) == (None, None):
		locale.setlocale(locale.LC_CTYPE, locale.getdefaultlocale()[0][:2])

# Affectation de la langue d'utilisation en fonction des paramètres ou du système d'exploitation (français ou anglais)
LOCALE = StringVar(value = locale.getlocale()[0][:2])
if LOCALE.get() != "fr" and LOCALE.get() != "en":
	LOCALE.set("en")
LOCALE.trace_variable("w", lambda *args : settings.saveSettings())

class MSG(StringVar):
	def __init__(self, english_message : str, french_message : str):
		"""
		Constructeur d'un message localisé
		Le premier argument est le message en anglais, le second est en français
		"""
		super().__init__()
		self.en = english_message
		self.fr = french_message

		# Si un des messages est vide, l'autre est choisi
		if len(self.fr) == 0:
			self.fr = self.en
		if len(self.en) == 0:
			self.en = self.fr

		# Changement du message d'utilisation lorsque la langue est changée
		# noinspection PyUnusedLocal
		def callback(*kwargs):
			if isFrench():
				self.set(self.fr)
			else:
				self.set(self.en)

		# Lorsque la valeur de la variable LOCALE est changée, la fonction callback est invoquée
		LOCALE.trace_variable("w", callback)
		callback()

	def clone(self):
		"""
		Clonage de l'objet
		Chaque modification sur l'une des instances de changera pas l'autre (notamment utile en cas de formattage ou de switch)
		"""
		return MSG(self.en, self.fr)

	def switch(self, msg):
		"""
		Change les textes à partir d'un autre message
		Utile pour changer le texte d'un bouton (notamment pour activer/désactiver les sons)
		"""
		self.en = msg.en
		self.fr = msg.fr
		if isFrench():
			self.set(self.fr)
		else:
			self.set(self.en)

	def format(self, *args):
		"""
		Formatte le message à partir d'arguments
		"""
		obj = self.clone()
		obj.en = obj.en.format(*list(args))
		obj.fr = obj.fr.format(*list(args))
		if isFrench():
			obj.set(obj.fr)
		else:
			obj.set(obj.en)
		return obj

def isEnglish():
	"""
	Renvoie True ssi le jeu est en anglais
	"""
	return LOCALE.get() == "en"


def isFrench():
	"""
	Renvoie True ssi le jeu est en français
	"""
	return not isEnglish()

def setEnglish():
	"""
	Changement de la langue vers l'anglais 
	"""
	LOCALE.set("en")

def setFrench():
	"""
	Changement de la langue vers le français
	"""
	LOCALE.set("fr")

def switchLanguage():
	"""
	Changement de langue (anglais -> français ou français -> anglais)
	"""
	if isEnglish():
		setFrench()
	else:
		setEnglish()


#########################################################################
########################### Messages généraux ###########################
#########################################################################

SINGLE_PLAYER = MSG("Singleplayer", "Un joueur")
MAP_CHOICE = MSG("Choose map", "Choisir la carte")
CAR_CHOICE = MSG("Choose car", "Choisir la voiture")
START = MSG("Start!", "Démarrer !")
MULTI_PLAYER = MSG("Multiplayer", "Multijoueur")
SETTINGS = MSG("Settings", "Paramètres")
SCORES = MSG("Scores", "Scores")
QUIT = MSG("Quit", "Quitter")
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
LAP_TIME = MSG("Time lap #{}", "Temps tour #{}")
CAR = MSG("Car", "Voiture")


#########################################################################
########################### Noms des contrôles ##########################
#########################################################################

FORWARD = MSG("Accelerate", "Accélérer")
TURN_LEFT = MSG("Turn left", "Tourner à gauche")
BACKWARD = MSG("Brake", "Freiner")
TURN_RIGHT = MSG("Turn right", "Tourner à droite")
LOCAL = MSG("Local", "Local")
ONLINE = MSG("Online", "En ligne")

##########################################################################
########################### Boîtes de dialogue ###########################
##########################################################################

SOON = MSG("Soon!", "Bientôt !")
FUTURE_FEATURE = MSG("This feature will (probably) be available later!", "Cette fonctionnalité sera (probablement) accessible plus tard !")

##########################################################################
########################### Noms des voitures ############################
##########################################################################

RED_CAR = MSG("Red Speedo", "La Fulgurante Rouge")
BLUE_CAR = MSG("Beauty Blue", "La Belle Bleue")
GREEN_CAR = MSG("E-Car", "E-Voiture")


##########################################################################
############################ Noms des cartes #############################
##########################################################################

BABY = MSG("Baby loop", "Circuit Baby")
CIRCUIT_8 = MSG("8-Circuit", "Circuit en 8")
TEST_LOOP = MSG("Test Loop", "Circuit de test")

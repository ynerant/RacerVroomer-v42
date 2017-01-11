from tkinter import StringVar
import locale

LOCALE = StringVar(value = locale.getlocale()[0][:2])
if LOCALE.get() != "fr" and LOCALE.get() != "en":
	LOCALE.set("en")


class MSG(StringVar):
	def __init__(self, english_message, french_message):
		super().__init__()
		self.en = english_message
		self.fr = french_message

		def callback(*kwargs):
			if LOCALE.get() == "fr":
				self.set(self.fr)
			else:
				self.set(self.en)

		LOCALE.trace_variable("w", callback)
		callback()


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

SINGLE_PLAYER = MSG("Singleplayer", "Un joueur")
MULTI_PLAYER = MSG("Multiplayer", "Multijoueur")
SETTINGS = MSG("Settings", "Options")
QUIT = MSG("Don't quit :(", "Ne quittez pas :(")

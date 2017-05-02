#coding: utf-8

import tkinter as tk
import json, gzip
# Import messages vars
import messages as msgs
import guis
import utils
from guis import GUI

def loadSettings():
	"""
	Chargement du fichier de paramètres JSON compressé en GZIP (settings.gz) et si absent, en crée un avec des paramètres par défaut
	"""
	# noinspection PyProtectedMember
	window = tk._default_root
	try:
		# Décompression et lecture du fichier de configuration compressé en gzip, écrit en JSON
		with gzip.open("settings.gz", "rb") as f:
			file_content = f.read()
		# Décodage binaire (tableau d’octets vers chaîne de caractères)
		jsoned = file_content.decode("UTF-8")
		# Traduction JSON -> dictionnaire Python
		obj = json.loads(jsoned) #type: dict
		# Attribution des paramètres par défaut
		# Paramètres : contrôles (dictionnaire), musique (booléen), effets sonores (booléen), plein écran (booléen), langue (chaîne)
		obj.setdefault("controls", utils.CONTROLS)
		obj.setdefault("music", True)
		obj.setdefault("sounds", True)
		obj.setdefault("fullscreen", False)
		obj.setdefault("locale", msgs.LOCALE.get())
		# Affectation des nouveaux contrôles
		utils.CONTROLS = obj["controls"]
		# (Dés)activation de la musique
		window.music_enabled = bool(obj["music"])
		# (Dés)activation des effets sonores
		window.sounds_enabled = bool(obj["sounds"])
		# Affichage (ou non) en mode plein écran
		window.attributes("-fullscreen", bool(obj["fullscreen"]))
		# Changement de langue
		locale = obj["locale"]
		if locale == "en" or locale == "fr":
			msgs.LOCALE.set(locale)
	except FileNotFoundError:
		# Si le fichier n’a pas été trouvé, conservation des paramètres par défaut
		# Création de deux nouvelles variables dans la variable de la fenêtre gérant musiques et sons
		# voir audio/__init__.py
		window.music_enabled = True
		window.sounds_enabled = True
	except IOError:
		# Autre message d’erreur (fichier corrompu et irrécupérable) => Paramètres d’origine
		utils.showMessageDialog(msgs.MSG("Error occurred", "Une erreur est survenue"),
								msgs.MSG("An error occurred while loading settings. The file may be corrupted, all your settings are resetted.",
										 "Une erreur est survenue lors de la lecture des paramètres. Le ficher est probablement corrompu, tous vos paramètres ont été réinitialisés."))
		window.music_enabled = True
		window.sounds_enabled = True

	# Sauvegarde des paramètres si le fichier est manquant, corrompu ou incomplet (peut arriver en cas de mise à jour ultérieure tout en conservant une compatibilité)
	saveSettings()

def saveSettings():
	"""
	Sauvegarde au sein d’un fichier JSON compressé en GZIP (settings.gz) les paramètres actuels
	"""
	# noinspection PyProtectedMember
	window = tk._default_root
	# Création d’un dictionnaire comprenant tous les paramètres
	settings = dict(music = window.music_enabled, sounds = window.sounds_enabled, locale = msgs.LOCALE.get(), fullscreen = bool(window.attributes("-fullscreen")), controls = utils.CONTROLS)
	# Traduction en JSON
	jsoned = json.dumps(settings, sort_keys = True, indent = 4)

	# Écriture dans le fichier compressé en GZIP
	with gzip.open("settings.gz", "wb") as f:
		f.write(jsoned.encode("UTF-8"))

# noinspection PyUnusedLocal
class Settings(GUI):
	def __init__(self, window):
		"""
		Constructeur par défaut de l’interface de paramètres (Fond d’écran actif)
		Prend en paramètre la fenêtre
		"""
		GUI.__init__(self, window, True)

		# Définition des textes des boutons de (dés)activation de la musique et des effets sonores en fonction des paramètres actuels
		switchMusicMsg = (msgs.DISABLE_MUSIC if window.music_enabled else msgs.ENABLE_MUSIC).clone()
		switchSoundsMsg = (msgs.DISABLE_SOUNDS if window.sounds_enabled else msgs.ENABLE_SOUNDS).clone()

		# Création des boutons
		music = tk.Button(window, bg = utils.BUTTON_BACKGROUND, textvariable = switchMusicMsg, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 22, borderwidth = 4, relief = "raise")
		sounds = tk.Button(window, bg = utils.BUTTON_BACKGROUND, textvariable = switchSoundsMsg, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 22, borderwidth = 4, relief = "raise")
		changeLanguage = tk.Button(window, bg = utils.BUTTON_BACKGROUND, textvariable = msgs.CHANGE_LANGUAGE,  font = ("Plantagenet Cherokee", 30), anchor = "center", width = 22, borderwidth = 4, relief = "raise", command = msgs.switchLanguage)
		controls = tk.Button(window, bg = utils.BUTTON_BACKGROUND, textvariable = msgs.CHANGE_CONTROLS, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 22, borderwidth = 4, relief = "raise", command = lambda : Controls(window))
		back = tk.Button(window, bg = utils.BUTTON_BACKGROUND, textvariable = msgs.BACK, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 15, borderwidth = 4, relief = "raise", command = lambda : guis.back(window))

		# Affichage des boutons
		music.place(relx = .025, rely = .25)
		sounds.place(relx = .025, rely = .37)
		changeLanguage.place(relx = .025, rely = .49)
		controls.place(relx = .025, rely = .61)
		back.place(relx = .74, rely = .88)

		def switchMusicState():
			"""
			Change l’état d’activation de la musique
			La musique est lancée dans le sous-module audio
			"""
			if window.music_enabled:
				switchMusicMsg.switch(msgs.ENABLE_MUSIC)
			else:
				switchMusicMsg.switch(msgs.DISABLE_MUSIC)
			window.music_enabled ^= True
			saveSettings()

		def switchSoundsState():
			"""
			Change l’état d’activation des effets sonores
			"""
			if window.sounds_enabled:
				switchSoundsMsg.switch(msgs.ENABLE_SOUNDS)
			else:
				switchSoundsMsg.switch(msgs.DISABLE_SOUNDS)
			window.sounds_enabled ^= True
			saveSettings()

		# Affectation des évenements de clics
		music.config(command = switchMusicState)
		sounds.config(command = switchSoundsState)

		# Ajout des enfants
		self.appendChild(music)
		self.appendChild(sounds)
		self.appendChild(changeLanguage)
		self.appendChild(controls)
		self.appendChild(back)

class Controls(GUI):
	def __init__(self, window):
		"""
		Constructeur par défaut de l’interface de changements des contrôles (fond d’écran actif)
		Prend en paramètre la fenêtre
		"""
		super().__init__(window, True)

		# Création des labels et des boutons
		forwardLabel = tk.Label(window, textvariable = msgs.FORWARD, font = ("Plantagenet Cherokee", 21),width = 10)
		forwardText = tk.StringVar(window, utils.CONTROLS["forward"].replace("_", " "))
		forward = tk.Button(window, bg = utils.BUTTON_BACKGROUND, textvariable = forwardText, font = ("Plantagenet Cherokee", 21), width = 10, relief ="raise")
		leftLabel = tk.Label(window, textvariable = msgs.TURN_LEFT, font = ("Plantagenet Cherokee", 21),width = 10)
		leftText = tk.StringVar(window, utils.CONTROLS["left"].replace("_", " "))
		left = tk.Button(window, bg = utils.BUTTON_BACKGROUND, textvariable = leftText, font = ("Plantagenet Cherokee", 21), width = 10, relief ="raise")
		backwardLabel = tk.Label(window, textvariable = msgs.BACKWARD, font = ("Plantagenet Cherokee", 21),width = 10)
		backwardText = tk.StringVar(window, utils.CONTROLS["backward"].replace("_", " "))
		backward = tk.Button(window, bg = utils.BUTTON_BACKGROUND, textvariable = backwardText, font = ("Plantagenet Cherokee", 21), width = 10, relief ="raise")
		rightLabel = tk.Label(window, textvariable = msgs.TURN_RIGHT, font = ("Plantagenet Cherokee", 21),width = 10)
		rightText = tk.StringVar(window, utils.CONTROLS["right"].replace("_", " "))
		right = tk.Button(window, bg = utils.BUTTON_BACKGROUND, textvariable = rightText, font = ("Plantagenet Cherokee", 21), width = 10, relief ="raise")

		# Création du bouton retour
		back = tk.Button(window, bg = utils.BUTTON_BACKGROUND, textvariable = msgs.BACK, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 15, borderwidth = 4, relief ="raise", command = lambda : guis.back(window))

		# Affichage des boutons sur l’interface
		forwardLabel.place(relx = .025, rely = .30)
		forward.place(relx = .225, rely = .30)
		leftLabel.place(relx = .025, rely = .38)
		left.place(relx = .225, rely = .38)
		backwardLabel.place(relx = .025, rely = .46)
		backward.place(relx = .225, rely = .46)
		rightLabel.place(relx = .025, rely = .54)
		right.place(relx = .225, rely = .54)
		back.place(relx = .74, rely = .88)

		def requestNewKey(index, buttonText, label):
			"""
			Affiche une boîte de dialogue demandant la nouvelle touche à affecter à l’action
			 Le paramètre index représente le numéro de l’action
			 Le paramètre buttonText représente l’affichage du bouton, soit le nom de la touche
			 Le paramètre label représente le nom de l’action (localisé/traduit)
			"""
			# Création d’une boîte de dialogue
			popup = tk.Toplevel(window)
			# Ajout du texte dans la boîte
			label = tk.Label(popup, textvariable = msgs.WHAT_KEY_FOR.format(label.get().lower()), font = ("Plantagenet Cherokee", 30))
			label.grid(row = 0, column = 0, padx = 10, pady = 10)
			# Définition de la géométrie de la boîte ainsi que son positionnement sur l’écran (centré)
			width = label.winfo_reqwidth() + 20
			height = label.winfo_height() + 80
			screenWidth = popup.winfo_screenwidth()
			screenHeight = popup.winfo_screenheight()
			popup.geometry(str(width) + "x" + str(height) + "+" + str(int((screenWidth - width) / 2)) + "+" + str(int((screenHeight - height) / 2) - 40))
			# Variable expliquée plus tard
			sound_started = tk.BooleanVar(False)
			def catch_key_event(event):
				"""
				Méthode invoquée lorsqu’une touche est pressée
				Paramètre : informations par rapport à l’évennemment "appuyer sur une touche"
				"""
				# event.keycode est le numéro de la touche dans la table ASCII
				key = event.keycode
				# La touche 27 est la touche ÉCHAP qui annule alors la modification de contrôle
				if key == 27:
					popup.destroy()
					return
				# On vérifie si la touche n’est pas déjà assignée et si ce n’est pas la touche F11 (utile pour le plein écran)
				if event.keysym.upper() in utils.CONTROLS.values() or event.keysym.upper() == "F11":
					# Si on est sous windows, le son d’erreur est alors déclenché
					# La variable sound_started permet alors de savoir si ce son a déjà été déclenché
					if utils.isWindows():
						import winsound, threading
						if not sound_started.get():
							def start_sound():
								sound_started.set(True)
								winsound.PlaySound("*", winsound.SND_ALIAS)
								sound_started.set(False)
							threading.Thread(target = start_sound).start()
					return
				# Changement du texte du bouton avec le nouveau contrôle
				buttonText.set(event.keysym.upper().replace("_", " "))
				# Affectation du nouveau contrôle
				utils.CONTROLS[index] = event.keysym.upper()
				# Fermeture de la boîte de dialogue
				popup.destroy()
				# Écriture des paramètres
				saveSettings()
			# Appelle la fonction catch_key_event lors de l’appui de n’importe quelle touche de clavier
			popup.bind("<KeyPress>", catch_key_event)
			# Force la mise en avant de la boîte de dialogue et la laisse en avant-plan
			popup.focus_force()
			popup.wm_attributes("-topmost", 1)
			popup.grab_set()

		forward.bind("<ButtonRelease-1>", lambda event : requestNewKey("forward", forwardText, msgs.FORWARD))
		left.bind("<ButtonRelease-1>", lambda event : requestNewKey("left", leftText, msgs.TURN_LEFT))
		backward.bind("<ButtonRelease-1>", lambda event : requestNewKey("backward", backwardText, msgs.BACKWARD))
		right.bind("<ButtonRelease-1>", lambda event : requestNewKey("right", rightText, msgs.TURN_RIGHT))

		window.columnconfigure(0, weight = 3)
		window.columnconfigure(1, weight = 2)

		# Ajout des enfants
		self.appendChild(forwardLabel)
		self.appendChild(forward)
		self.appendChild(leftLabel)
		self.appendChild(left)
		self.appendChild(backwardLabel)
		self.appendChild(backward)
		self.appendChild(rightLabel)
		self.appendChild(right)
		self.appendChild(back)
#coding: utf-8

import tkinter as tk
import json, gzip
# Import messages vars
import messages as msgs
import guis
import utils
from guis import GUI

def loadSettings():
	# noinspection PyProtectedMember
	window = tk._default_root
	try:
		with gzip.open("settings.gz", "rb") as f:
			file_content = f.read()
		jsoned = file_content.decode()
		obj = json.loads(jsoned) #type: dict
		obj.setdefault("controls", utils.CONTROLS)
		obj.setdefault("music", True)
		obj.setdefault("sounds", True)
		obj.setdefault("fullscreen", False)
		obj.setdefault("locale", msgs.LOCALE.get())
		utils.CONTROLS = obj["controls"]
		window.music_enabled = bool(obj["music"])
		window.sounds_enabled = bool(obj["sounds"])
		window.attributes("-fullscreen", bool(obj["fullscreen"]))
		locale = obj["locale"]
		if locale == "en" or locale == "fr":
			msgs.LOCALE.set(locale)
	except FileNotFoundError:
		window.music_enabled = True
		window.sounds_enabled = True
	except IOError:
		utils.showMessageDialog(msgs.MSG("Error occurred", ""), msgs.MSG("An error occurred while loading settings. The file may be corrupted, all yur settings are resetted.", ""))
		window.music_enabled = True
		window.sounds_enabled = True

	saveSettings()

def saveSettings():
	# noinspection PyProtectedMember
	window = tk._default_root
	settings = dict(music = window.music_enabled, sounds = window.sounds_enabled, locale = msgs.LOCALE.get(), fullscreen = bool(window.attributes("-fullscreen")), controls = utils.CONTROLS)
	jsoned = json.dumps(settings, sort_keys = True, indent = 4)

	with gzip.open("settings.gz", "wb") as f:
		f.write(jsoned.encode("UTF-8"))


# noinspection PyUnusedLocal
class Settings(GUI):
	def __init__(self, window):
		GUI.__init__(self)

		switchMusicMsg = (msgs.DISABLE_MUSIC if window.music_enabled else msgs.ENABLE_MUSIC).clone()
		switchSoundsMsg = (msgs.DISABLE_SOUNDS if window.sounds_enabled else msgs.ENABLE_SOUNDS).clone()

		music = tk.Button(window, bg = utils.BUTTON_BACKGROUND, textvariable = switchMusicMsg, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 25, borderwidth = 10, relief = "groove")
		sounds = tk.Button(window, bg = utils.BUTTON_BACKGROUND, textvariable = switchSoundsMsg, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 25, borderwidth = 10, relief = "groove")
		changeLanguage = tk.Button(window, bg = utils.BUTTON_BACKGROUND, textvariable = msgs.CHANGE_LANGUAGE,  font = ("Plantagenet Cherokee", 30), anchor = "center", width = 25, borderwidth = 10, relief = "groove", command = msgs.switchLanguage)
		controls = tk.Button(window, bg = utils.BUTTON_BACKGROUND, textvariable = msgs.CHANGE_CONTROLS, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 25, borderwidth = 10, relief = "groove", command = lambda : Controls(window))
		back = tk.Button(window, bg = utils.BUTTON_BACKGROUND, textvariable = msgs.BACK, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 25, borderwidth = 10, relief = "groove", command = lambda : guis.back(window))

		music.pack()
		sounds.pack()
		changeLanguage.pack()
		controls.pack()
		back.pack()

		def switchMusicState(*args):
			if window.music_enabled:
				switchMusicMsg.switch(msgs.ENABLE_MUSIC)
			else:
				switchMusicMsg.switch(msgs.DISABLE_MUSIC)
			window.music_enabled ^= True
			saveSettings()

		def switchSoundsState(*args):
			if window.sounds_enabled:
				switchSoundsMsg.switch(msgs.ENABLE_SOUNDS)
			else:
				switchSoundsMsg.switch(msgs.DISABLE_SOUNDS)
			window.sounds_enabled ^= True
			saveSettings()

		music.bind("<ButtonRelease-1>", switchMusicState)
		sounds.bind("<ButtonRelease-1>", switchSoundsState)

		self.appendChild(music)
		self.appendChild(sounds)
		self.appendChild(changeLanguage)
		self.appendChild(controls)
		self.appendChild(back)

class Controls(GUI):
	def __init__(self, window):
		super().__init__()

		forwardLabel = tk.Label(window, textvariable = msgs.FORWARD, font = ("Plantagenet Cherokee", 21))
		forwardText = tk.StringVar(window, utils.CONTROLS["forward"].replace("_", " "))
		forward = tk.Button(window, bg = utils.BUTTON_BACKGROUND, textvariable = forwardText, font = ("Plantagenet Cherokee", 21), width = 10)
		leftLabel = tk.Label(window, textvariable = msgs.TURN_LEFT, font = ("Plantagenet Cherokee", 21))
		leftText = tk.StringVar(window, utils.CONTROLS["left"].replace("_", " "))
		left = tk.Button(window, bg = utils.BUTTON_BACKGROUND, textvariable = leftText, font = ("Plantagenet Cherokee", 21), width = 10)
		backwardLabel = tk.Label(window, textvariable = msgs.BACKWARD, font = ("Plantagenet Cherokee", 21))
		backwardText = tk.StringVar(window, utils.CONTROLS["backward"].replace("_", " "))
		backward = tk.Button(window, bg = utils.BUTTON_BACKGROUND, textvariable = backwardText, font = ("Plantagenet Cherokee", 21), width = 10)
		rightLabel = tk.Label(window, textvariable = msgs.TURN_RIGHT, font = ("Plantagenet Cherokee", 21))
		rightText = tk.StringVar(window, utils.CONTROLS["right"].replace("_", " "))
		right = tk.Button(window, bg = utils.BUTTON_BACKGROUND, textvariable = rightText, font = ("Plantagenet Cherokee", 21), width = 10)

		back = tk.Button(window, bg = utils.BUTTON_BACKGROUND, textvariable = msgs.BACK, font = ("Plantagenet Cherokee", 21), anchor = "center", width = 50, borderwidth = 10, relief = "groove", command = lambda : guis.back(window))

		forwardLabel.grid(row = 0, column = 0)
		forward.grid(row = 0, column = 1)
		leftLabel.grid(row = 1, column = 0)
		left.grid(row = 1, column = 1)
		backwardLabel.grid(row = 2, column = 0)
		backward.grid(row = 2, column = 1)
		rightLabel.grid(row = 3, column = 0)
		right.grid(row = 3, column = 1)
		back.grid(row = 4, column = 0, columnspan = 2, pady = 50)

		def requestNewKey(index, buttonText, label):
			popup = tk.Toplevel(window)
			label = tk.Label(popup, textvariable = msgs.WHAT_KEY_FOR.format(label.get().lower()), font = ("Plantagenet Cherokee", 30))
			label.grid(row = 0, column = 0, padx = 10, pady = 10)
			width = label.winfo_reqwidth() + 20
			height = label.winfo_height() + 80
			screenWidth = popup.winfo_screenwidth()
			screenHeight = popup.winfo_screenheight()
			popup.geometry(str(width) + "x" + str(height) + "+" + str(int((screenWidth - width) / 2)) + "+" + str(int((screenHeight - height) / 2) - 40))
			sound_started = tk.BooleanVar(False)
			def catch_key_event(event):
				key = event.keycode
				if key == 27:
					popup.destroy()
					return
				if event.keysym.upper() in utils.CONTROLS.values():
					if utils.isWindows():
						import winsound, threading
						if not sound_started.get():
							def start_sound():
								sound_started.set(True)
								winsound.PlaySound("*", winsound.SND_ALIAS)
								sound_started.set(False)
							threading.Thread(target = start_sound).start()
					return
				buttonText.set(event.keysym.upper().replace("_", " "))
				utils.CONTROLS[index] = event.keysym.upper()
				popup.destroy()
				saveSettings()
			popup.bind("<KeyPress>", catch_key_event)
			popup.focus_force()
			popup.wm_attributes("-topmost", 1)
			popup.grab_set()

		forward.bind("<ButtonRelease-1>", lambda event : requestNewKey("forward", forwardText, msgs.FORWARD))
		left.bind("<ButtonRelease-1>", lambda event : requestNewKey("left", leftText, msgs.TURN_LEFT))
		backward.bind("<ButtonRelease-1>", lambda event : requestNewKey("backward", backwardText, msgs.BACKWARD))
		right.bind("<ButtonRelease-1>", lambda event : requestNewKey("right", rightText, msgs.TURN_RIGHT))

		window.columnconfigure(0, weight = 3)
		window.columnconfigure(1, weight = 2)

		self.appendChild(forwardLabel)
		self.appendChild(forward)
		self.appendChild(leftLabel)
		self.appendChild(left)
		self.appendChild(backwardLabel)
		self.appendChild(backward)
		self.appendChild(rightLabel)
		self.appendChild(right)
		self.appendChild(back)
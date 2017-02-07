#coding: utf-8

import tkinter as tk
import json, gzip
# Import messages vars
import messages as msgs
import guis
from guis import GUI

CONTROLS = dict(forward = 'Z', left = 'Q', backward = 'S', right = 'D', brake = 'SHIFT_L')

def loadSettings():
	global CONTROLS
	# noinspection PyProtectedMember
	window = tk._default_root
	with gzip.open("settings.gz", "rb") as f:
		file_content = f.read()
	jsoned = file_content.decode()
	obj = json.loads(jsoned)
	controlsTmp = obj["controls"]
	CONTROLS = controlsTmp if controlsTmp is not None else CONTROLS
	music = obj["music"]
	window.music_enabled = music if type(music) is bool else True
	sounds = obj["sounds"]
	window.sounds_enabled = sounds if type(sounds) is bool else True
	locale = obj["locale"]
	if locale == "en" or locale == "fr":
		msgs.LOCALE.set(locale)

	saveSettings()

def saveSettings():
	# noinspection PyProtectedMember
	window = tk._default_root
	settings = dict(music = window.music_enabled, sounds = window.sounds_enabled, locale = msgs.LOCALE.get(), controls = CONTROLS)
	jsoned = json.dumps(settings, sort_keys = True, indent = 4)

	with gzip.open("settings.gz", "wb") as f:
		f.write(jsoned.encode("UTF-8"))

class Settings(GUI):
	def __init__(self, window):
		GUI.__init__(self)

		switchMusicMsg = (msgs.DISABLE_MUSIC if window.music_enabled else msgs.ENABLE_MUSIC).clone()
		switchSoundsMsg = (msgs.DISABLE_SOUNDS if window.sounds_enabled else msgs.ENABLE_SOUNDS).clone()

		music = tk.Button(window, textvariable = switchMusicMsg, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 25, borderwidth = 10, relief = "groove")
		sounds = tk.Button(window, textvariable = switchSoundsMsg, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 25, borderwidth = 10, relief = "groove")
		changeLanguage = tk.Button(window, textvariable = msgs.CHANGE_LANGUAGE, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 25, borderwidth = 10, relief = "groove", command = msgs.switchLanguage)
		controls = tk.Button(window, textvariable = msgs.CHANGE_CONTROLS, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 25, borderwidth = 10, relief = "groove", command = lambda : Controls(window))
		back = tk.Button(window, textvariable = msgs.BACK, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 25, borderwidth = 10, relief = "groove", command = lambda : guis.back(window))

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

		music.bind("<Button-1>", switchMusicState)
		sounds.bind("<Button-1>", switchSoundsState)

		self.children.append(music)
		self.children.append(sounds)
		self.children.append(changeLanguage)
		self.children.append(controls)
		self.children.append(back)

class Controls(GUI):
	def __init__(self, window):
		super().__init__()

		forwardLabel = tk.Label(window, textvariable = msgs.FORWARD, font = ("Plantagenet Cherokee", 21))
		forwardText = tk.StringVar(window, CONTROLS["forward"].replace("_", " "))
		forward = tk.Button(window, textvariable = forwardText, font = ("Plantagenet Cherokee", 21), width = 10)
		leftLabel = tk.Label(window, textvariable = msgs.TURN_LEFT, font = ("Plantagenet Cherokee", 21))
		leftText = tk.StringVar(window, CONTROLS["left"].replace("_", " "))
		left = tk.Button(window, textvariable = leftText, font = ("Plantagenet Cherokee", 21), width = 10)
		backwardLabel = tk.Label(window, textvariable = msgs.BACKWARD, font = ("Plantagenet Cherokee", 21))
		backwardText = tk.StringVar(window, CONTROLS["backward"].replace("_", " "))
		backward = tk.Button(window, textvariable = backwardText, font = ("Plantagenet Cherokee", 21), width = 10)
		rightLabel = tk.Label(window, textvariable = msgs.TURN_RIGHT, font = ("Plantagenet Cherokee", 21))
		rightText = tk.StringVar(window, CONTROLS["right"].replace("_", " "))
		right = tk.Button(window, textvariable = rightText, font = ("Plantagenet Cherokee", 21), width = 10)
		brakeLabel = tk.Label(window, textvariable = msgs.BRAKE, font = ("Plantagenet Cherokee", 21))
		brakeText = tk.StringVar(window, CONTROLS["brake"].replace("_", " "))
		brake = tk.Button(window, textvariable = brakeText, font = ("Plantagenet Cherokee", 21), width = 10)

		back = tk.Button(window, textvariable = msgs.BACK, font = ("Plantagenet Cherokee", 21), anchor = "center", width = 50, borderwidth = 10, relief = "groove", command = lambda : guis.back(window))

		forwardLabel.grid(row = 0, column = 0)
		forward.grid(row = 0, column = 1)
		leftLabel.grid(row = 1, column = 0)
		left.grid(row = 1, column = 1)
		backwardLabel.grid(row = 2, column = 0)
		backward.grid(row = 2, column = 1)
		rightLabel.grid(row = 3, column = 0)
		right.grid(row = 3, column = 1)
		brakeLabel.grid(row = 4, column = 0)
		brake.grid(row = 4, column = 1)
		back.grid(row = 5, column = 0, columnspan = 2, pady = 50)

		def requestNewKey(index, buttonText, label):
			popup = tk.Toplevel(window)
			label = tk.Label(popup, textvariable = msgs.WHAT_KEY_FOR.format(label.get().lower()), font = ("Plantagenet Cherokee", 30))
			label.grid(row = 0, column = 0, padx = 10, pady = 10)
			def catch_key_event(event):
				print(event)
				key = event.keycode
				if key == 27:
					popup.destroy()
					return
				if event.keysym.upper() in CONTROLS.values():
					return
				buttonText.set(event.keysym.upper().replace("_", " "))
				CONTROLS[index] = event.keysym.upper()
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
		brake.bind("<ButtonRelease-1>", lambda event : requestNewKey("brake", brakeText, msgs.BRAKE))

		window.columnconfigure(0, weight = 3)
		window.columnconfigure(1, weight = 2)

		self.children.append(forwardLabel)
		self.children.append(forward)
		self.children.append(leftLabel)
		self.children.append(left)
		self.children.append(backwardLabel)
		self.children.append(backward)
		self.children.append(rightLabel)
		self.children.append(right)
		self.children.append(brakeLabel)
		self.children.append(brake)
		self.children.append(back)
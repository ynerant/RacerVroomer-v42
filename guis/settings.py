#coding: utf-8

import tkinter as tk
# Import messages vars
import messages as msgs
# Import some useful content
import utils
from . import GUI, mainMenu

class Settings(GUI):
	def __init__(self, window):
		GUI.__init__(self)

		switchMusicMsg = msgs.DISABLE_MUSIC.clone()
		switchSoundsMsg = msgs.DISABLE_SOUNDS.clone()

		music = tk.Button(window, textvariable = switchMusicMsg, font = ("Plantagenet Cherokee", 42), anchor = "center", width = 20, borderwidth = 10, relief = "groove")
		sounds = tk.Button(window, textvariable = switchSoundsMsg, font = ("Plantagenet Cherokee", 42), anchor = "center", width = 20, borderwidth = 10, relief = "groove")
		changeLanguage = tk.Button(window, textvariable = msgs.CHANGE_LANGUAGE, font = ("Plantagenet Cherokee", 42), anchor = "center", width = 20, borderwidth = 10, relief = "groove", command = msgs.switchLanguage)
		back = tk.Button(window, textvariable = msgs.BACK, font = ("Plantagenet Cherokee", 42), anchor = "center", width = 20, borderwidth = 10, relief = "groove", command = lambda : mainMenu.MainMenu(window))

		music.pack()
		sounds.pack()
		changeLanguage.pack()
		back.pack()

		def switchMusicState(*kwargs):
			if window.music_enabled:
				window.music_enabled = False
				switchMusicMsg.switch(msgs.ENABLE_MUSIC)
			else:
				window.music_enabled = True
				switchMusicMsg.switch(msgs.DISABLE_MUSIC)

		def switchSoundsState(*kwargs):
			print(window.sounds_enabled)
			if window.sounds_enabled:
				window.sounds_enabled = False
				switchSoundsMsg.switch(msgs.ENABLE_SOUNDS)
			else:
				window.sounds_enabled = True
				switchSoundsMsg.switch(msgs.DISABLE_SOUNDS)

		music.bind("<Button>", switchMusicState)
		sounds.bind("<Button>", switchSoundsState)

		self.children.append(music)
		self.children.append(sounds)
		self.children.append(changeLanguage)
		self.children.append(back)
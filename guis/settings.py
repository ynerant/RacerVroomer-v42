#coding: utf-8

import tkinter as tk
# Import messages vars
import messages as msgs
# Import some useful content
import utils
import guis
from guis import GUI

class Settings(GUI):
	def __init__(self, window):
		GUI.__init__(self)

		switchMusicMsg = msgs.DISABLE_MUSIC.clone()
		switchSoundsMsg = msgs.DISABLE_SOUNDS.clone()

		music = tk.Button(window, textvariable = switchMusicMsg, font = ("Plantagenet Cherokee", 42), anchor = "center", width = 20, borderwidth = 10, relief = "groove")
		sounds = tk.Button(window, textvariable = switchSoundsMsg, font = ("Plantagenet Cherokee", 42), anchor = "center", width = 20, borderwidth = 10, relief = "groove")
		changeLanguage = tk.Button(window, textvariable = msgs.CHANGE_LANGUAGE, font = ("Plantagenet Cherokee", 42), anchor = "center", width = 20, borderwidth = 10, relief = "groove", command = msgs.switchLanguage)
		controls = tk.Button(window, textvariable = msgs.CHANGE_CONTROLS, font = ("Plantagenet Cherokee", 42), anchor = "center", width = 20, borderwidth = 10, relief = "groove", command = lambda : Controls(window))
		back = tk.Button(window, textvariable = msgs.BACK, font = ("Plantagenet Cherokee", 42), anchor = "center", width = 20, borderwidth = 10, relief = "groove", command = lambda : guis.OLD_GUI(window))

		music.pack()
		sounds.pack()
		changeLanguage.pack()
		controls.pack()
		back.pack()

		def switchMusicState(*kwargs):
			if window.music_enabled:
				window.music_enabled = False
				switchMusicMsg.switch(msgs.ENABLE_MUSIC)
			else:
				window.music_enabled = True
				switchMusicMsg.switch(msgs.DISABLE_MUSIC)

		def switchSoundsState(*kwargs):
			if window.sounds_enabled:
				window.sounds_enabled = False
				switchSoundsMsg.switch(msgs.ENABLE_SOUNDS)
			else:
				window.sounds_enabled = True
				switchSoundsMsg.switch(msgs.DISABLE_SOUNDS)

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

		forwardLabel = tk.Label(window, textvariable = msgs.FORWARD, font = ("Plantagenet Cherokee", 42))
		forwardText = tk.StringVar(window, "Z")
		forward = tk.Button(window, textvariable = forwardText, font = ("Plantagenet Cherokee", 42))
		leftLabel = tk.Label(window, textvariable = msgs.TURN_LEFT, font = ("Plantagenet Cherokee", 42))
		leftText = tk.StringVar(window, "Q")
		left = tk.Button(window, textvariable = leftText, font = ("Plantagenet Cherokee", 42))
		backwardLabel = tk.Label(window, textvariable = msgs.BACKWARD, font = ("Plantagenet Cherokee", 42))
		backwardText = tk.StringVar(window, "S")
		backward = tk.Button(window, textvariable = backwardText, font = ("Plantagenet Cherokee", 42))
		rightLabel = tk.Label(window, textvariable = msgs.TURN_RIGHT, font = ("Plantagenet Cherokee", 42))
		rightText = tk.StringVar(window, "D")
		right = tk.Button(window, textvariable = rightText, font = ("Plantagenet Cherokee", 42))
		brakeLabel = tk.Label(window, textvariable = msgs.BRAKE, font = ("Plantagenet Cherokee", 42))
		brakeText = tk.StringVar(window, "Shift")
		brake = tk.Button(window, textvariable = brakeText, font = ("Plantagenet Cherokee", 42))

		back = tk.Button(window, textvariable = msgs.BACK, font = ("Plantagenet Cherokee", 42), anchor = "center", width = 20, borderwidth = 10, relief = "groove", command = lambda : guis.OLD_GUI(window))

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
		back.grid(row = 5, column = 0, columnspan = 2)

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
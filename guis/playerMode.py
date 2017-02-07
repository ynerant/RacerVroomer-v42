#coding : utf-8

import tkinter as tk
import messages as msgs
import utils
from . import GUI, mainMenu

class Singleplayer(GUI):
	def __init__(self, window):
		GUI.__init__(self)

		map = tk.Button(window, textvariable = msgs.MAP_CHOICE, font = ("Plantagenet Cherokee", 42), anchor = "center", width = 20, borderwidth = 10, relief = "groove")
		car = tk.Button(window, textvariable = msgs.CAR_CHOICE, font = ("Plantagenet Cherokee", 42), anchor = "center", width = 20, borderwidth = 10, relief = "groove")
		back = tk.Button(window, textvariable = msgs.BACK, font = ("Plantagenet Cherokee", 42), anchor = "center", width = 20, borderwidth = 10, relief = "groove", command = lambda : mainMenu.MainMenu(window))

		car.pack()
		map.pack()
		back.pack()

		self.children.append(map)
		self.children.append(car)
		self.children.append(back)

class Multiplayer(GUI):
	def __init__(self, window):
		GUI.__init__(self)

		local = tk.Button(window, textvariable = msgs.LOCAL, font = ("Plantagenet Cherokee", 42), anchor = "center", width = 20, borderwidth = 10, relief = "groove", command = lambda : utils.showMessageDialog(msgs.SOON, msgs.FUTURE_FEATURE))
		online = tk.Button(window, textvariable = msgs.ONLINE, font = ("Plantagenet Cherokee", 42), anchor = "center", width = 20, borderwidth = 10, relief = "groove", command = lambda : utils.showMessageDialog(msgs.SOON, msgs.FUTURE_FEATURE))
		back = tk.Button(window, textvariable = msgs.BACK, font = ("Plantagenet Cherokee", 42), anchor = "center", width = 20, borderwidth = 10, relief = "groove", command = lambda : mainMenu.MainMenu(window))

		local.pack()
		online.pack()
		back.pack()

		self.children.append(local)
		self.children.append(online)
		self.children.append(back)
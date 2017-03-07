#coding : utf-8

import messages as msgs
#import tkinter as tk

MAPS = []

class Map :
	def __init__(self, name : msgs.MSG, fileName):
	self.name = name
	self.fileName = fileName

	MAPS.append(self)

def __str__(self):
	return "{Map name=\"" + self.name.get() + ")"

BABY = Map(msgs.BABY, "baby.map")
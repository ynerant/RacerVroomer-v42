#coding : utf-8

from tkinter import messagebox as mb
import sys

CONTROLS = dict(forward = 'Z', left = 'Q', backward = 'S', right = 'D')
BUTTON_BACKGROUND = "#f8a1a1"

def showMessageDialog(title, text):
	mb.showinfo(title if type(title) is str else title.get(), text if type(text) is str else text.get())

def isWindows():
	return "win" in sys.platform.lower()

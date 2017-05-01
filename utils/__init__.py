#coding : utf-8

from tkinter import messagebox as mb
import sys

CONTROLS = dict(forward = 'Z', left = 'Q', backward = 'S', right = 'D')
BUTTON_BACKGROUND = "#f8a1a1"

def showMessageDialog(title, text):
	mb.showinfo(str(title), str(text))

def isWindows():
	return "win" in sys.platform.lower()

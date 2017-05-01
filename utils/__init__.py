#coding : utf-8

from tkinter import messagebox as mb

CONTROLS = dict(forward = 'Z', left = 'Q', backward = 'S', right = 'D')
BUTTON_BACKGROUND = "#f8a1a1"

def showMessageDialog(title, text):
	mb.showinfo(title.get(), text.get())

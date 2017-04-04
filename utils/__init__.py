#coding : utf-8

from tkinter import messagebox as mb

CONTROLS = dict(forward = 'Z', left = 'Q', backward = 'S', right = 'D')

def showMessageDialog(title, text):
	mb.showinfo(title.get(), text.get())

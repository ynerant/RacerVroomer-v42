from tkinter import messagebox as mb
from messages import MSG

CONTROLS = dict(forward = 'Z', left = 'Q', backward = 'S', right = 'D', brake = 'SHIFT_R')

def showMessageDialog(title: MSG, text: MSG):
	mb.showinfo(title.get(), text.get())

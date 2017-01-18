from tkinter import messagebox as mb
from messages import MSG

def showMessageDialog(title: MSG, text: MSG):
	mb.showinfo(title.get(), text.get())

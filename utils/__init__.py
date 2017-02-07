from tkinter import messagebox as mb

def showMessageDialog(title, text):
	mb.showinfo(title.get(), text.get())

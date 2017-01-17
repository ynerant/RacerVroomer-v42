import tkinter as tk
import locale


def main():
	if locale.getlocale(locale.LC_ALL) == (None, None):
		locale.setlocale(locale.LC_ALL, locale.getdefaultlocale()[0][:2])

	window = tk.Tk()
	window.title("Racer Vroomer v42")
	window.state("zoomed")
	width = 840
	height = 420
	screenWidth = window.winfo_screenwidth()
	screenHeight = window.winfo_screenheight()
	window.geometry(str(width) + "x" + str(height) + "+" + str(int((screenWidth - width) / 2)) + "+" + str(int((screenHeight - height) / 2)))

	import messages as msgs

	singleplayer = tk.Button(window, textvariable = msgs.SINGLE_PLAYER, font = ("Plantagenet Cherokee", 42), anchor = "center", width = 20, borderwidth = 10, relief = "groove")
	multiplayer = tk.Button(window, textvariable = msgs.MULTI_PLAYER, font = ("Plantagenet Cherokee", 42), anchor = "center", width = 20, borderwidth = 10 , relief = "groove")
	options = tk.Button(window, textvariable = msgs.SETTINGS, font = ("Plantagenet Cherokee", 42), anchor = "center", width = 20, borderwidth = 10, relief = "groove", command = lambda: msgs.switchLanguage())
	quit = tk.Button(window, textvariable = msgs.QUIT, font = ("Plantagenet Cherokee", 42), anchor = "center", width = 20, borderwidth = 10, relief = "groove", command = window.quit)

	singleplayer.pack()
	multiplayer.pack()
	options.pack()
	quit.pack()

	window.mainloop()


if __name__ == "__main__":
	main()

import tkinter


def main():
	window = tkinter.Tk()
	window.title("Racer Vrommer v42")
	window.state("zoomed")
	width = 840
	height = 420
	screenWidth = window.winfo_screenwidth()
	screenHeight = window.winfo_screenheight()
	window.geometry(str(width) + "x" + str(height) + "+" + str(int((screenWidth - width) / 2)) + "+" + str(int((screenHeight - height) / 2)))
	
	singleplayer = tkinter.Button(window, text="Un joueur", font=("Plantagenet Cherokee", 42), anchor="center", width=20)
	multiplayer = tkinter.Button(window, text="Multijoueur", font=("Plantagenet Cherokee", 42), anchor="center", width=20)
	options = tkinter.Button(window, text="Options", font=("Plantagenet Cherokee", 42), anchor="center", width=20)
	quit = tkinter.Button(window, text="Quitter", font=("Plantagenet Cherokee", 42), anchor="center", width=20)
	
	singleplayer.pack()
	multiplayer.pack()
	options.pack()
	quit.pack()
	
	window.mainloop()
	
	print(42)

if __name__ == "__main__":
	main()

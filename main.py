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
	
	label = tkinter.Label(window, text="42", font="\"Plantagenet Cherokee\" 42")
	label.pack()
	
	window.mainloop()
	
	print(42)

if __name__ == "__main__":
	main()

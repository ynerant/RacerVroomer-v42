#coding : utf-8

import tkinter as tk
from PIL import Image, ImageTk
from guis import GUI, mainMenu, scores

import cars, utils
import messages as msgs
from audio import AudioPlayer
import math
from threading import Thread

class Game(GUI):
	def __init__(self, window, builder):
		"""
		Constructeur par défaut de l’interface de jeu
		Prend en paramètres la fenêtre ainsi que le constructeur de partie
		"""
		GUI.__init__(self, window)

		# Affectation de quelques constantes
		self.window = window
		self.raw_car = builder.car
		self.map = builder.map

		# Création du canevas à la taille de la fenêtre
		self.width, self.height = window.winfo_reqwidth(), window.winfo_reqheight()
		if window.state() == "zoomed":
			self.width, self.height = window.winfo_screenwidth(), window.winfo_screenheight()
		self.canvas = tk.Canvas(window, width = window.winfo_screenwidth(), height = window.winfo_screenheight(), bg = "green")

		# Ouverture du fond de carte par le module PIL
		img_temp = Image.open("images/maps/" + self.map.img_file)
		# Convertit si nécessaire la carte en RGBA (Rouge-Vert-Bleu-Alpha)
		img_temp = img_temp.convert("RGBA")
		# Redimensionne le fond à la taile de la fenêtre
		img_temp = img_temp.resize((self.width, self.height), Image.ANTIALIAS)
		# Conversion de l’image en image Tkinter
		self.background_img = ImageTk.PhotoImage(img_temp)
		# Création de l’image dans le canevas
		self.background = self.canvas.create_image(self.width, self.height, image = self.background_img, anchor = tk.NW)
		# Affichage du canevas et positionnement
		self.canvas.focus_set()
		self.canvas.pack()
		# Lorsque la fenêtre est reconfigurée redimensionnée, réduite, ...), invocation de la fonction on_resize(voir plus bas)
		window.bind("<Configure>", lambda event : self.on_resize(event))

		# Affichage du chronomètre
		self.time_label = tk.Label(window, text = "00:00:00.000", font = ("Plantagenet Cherokee", 24), fg = "white", bg = "black")
		self.time_label.place(x = 0, y = 0)
		self.appendChild(self.time_label)

		# Affichage du compte-tours
		self.lap = 0
		self.lap_label = tk.Label(window, text = msgs.LAP_NUMBER.get().format(self.lap, self.map.max_laps), font = ("Plantagenet Cherokee", 24), fg ="white", bg ="black")
		self.lap_label.place(x = 0, y = self.time_label.winfo_reqheight(), width = self.time_label.winfo_reqwidth())
		self.appendChild(self.lap_label)

		# Création de l’objet Voiture (qui se déplacera sur la carte, ne contennant plus que les infos de base)
		self.car = Car(window, self)
		# Initialisation du temps de course à -1, il se mettra à 0 dès la première action de l’utilisateur
		self.time = -1

		# Ajout du canevas comme enfant
		self.appendChild(self.canvas)

		# Actualisation de la fenêtre
		window.config(width = window.winfo_reqwidth())

	def on_resize(self, event):
		"""
		Redimensionne le canevas lors d’un redimensionnement de fenêtre
		"""
		# Si le jeu est en pause ou terminé, rien ne se passe
		if self.car.paused or self.car.thread.stopped:
			return

		# Récupération de la nouvelle taille de fenêtre
		self.width, self.height = event.width, event.height
		# Suppression de l’ancien fond d’écran et rechargement de l’image
		self.canvas.delete(self.background)
		img_temp = Image.open("images/maps/" + self.map.img_file)
		img_temp = img_temp.convert("RGBA")
		img_temp = img_temp.resize((self.width, self.height), Image.ANTIALIAS)
		self.background_img = ImageTk.PhotoImage(img_temp)
		self.background = self.canvas.create_image(self.width, self.height, image = self.background_img)
		# Positionnement de l’image
		self.canvas.coords(self.background, self.width / 2, self.height / 2)
		# Remontée de la voiture au-dessus du fond de carte
		self.canvas.tag_raise(self.car.img)

class Car:
	def __init__(self, window, game):
		"""
		Constructeur par défaut de l’objet Voiture
		Prend en paramètre la fenêtre ainsi que la partie en cours
		"""
		self.game = game
		self.car = game.raw_car #type: cars.Car
		self.window = window #type: tk.Tk

		# Définition de la ligne de départ
		# La voiture se placera un peu derrière la ligne
		start_line = game.map.start
		self.x = int((start_line.x_end + start_line.x_start) / 2)
		self.y = int((start_line.y_end + start_line.y_start) / 2)
		self.speed = 0.0
		# Recherche de l’angle de départ
		start_line_length = start_line.length()
		dot_product = start_line.x_end - start_line.x_start
		cosinus = dot_product / start_line_length
		# Définition de l’angle de départ
		self.start_angle = -math.acos(cosinus) + math.pi / 2
		self.angle = self.start_angle
		if start_line.y_start > start_line.y_end:
			self.angle += math.pi
		# Définition de l’angle d’orientation lorsque la voiture tourne en fonction de la maniabilité (angle = 2pi / maniabilité)
		self.angle_division = self.car.maniability
		self.angle = int(self.angle_division * self.angle / math.pi) * math.pi / self.angle_division
		# Définition du vecteur d’avancée de la voiture en fonction de son angle
		self.vector = self.angle_to_normalized_vector()
		# Positionnement de la voiture derrière la ligne en fonction de son angle de départ
		self.x -= self.vector[0] * self.car.width / 2
		self.y -= self.vector[1] * self.car.height / 2
		self.canvas = game.canvas
		# Lecture de l’image de la voiture, redimensionnement et placement sur l’interface
		img_temp = Image.open("images/cars/" + self.car.img_file)
		img_temp = img_temp.convert("RGBA")
		img_temp = img_temp.resize((self.car.width, self.car.height), Image.ANTIALIAS)
		img_temp = img_temp.rotate(-self.angle * 180 / math.pi, expand = 1)
		self.img_img = ImageTk.PhotoImage(img_temp)
		self.img = self.canvas.create_image(0, 0, image = self.img_img)

		# keys_pressed représente l’ensemble des touches sur lesquelles l’utilisateur appuie actuellement
		self.keys_pressed = set()
		# Initialisation de l’état de pause
		self.paused = False
		# Création du tableau qui contiendra les temps pour effectuer chacun des tours
		self.lap_times = []

		# Création et démarrage du processus de jeu et d’avancée de la voiture
		self.thread = CarThread(self)
		self.thread.start()

		# Invocation de la fonction catck_key_press_event lors de l’appui d’une touche
		window.bind("<KeyPress>", lambda event : self.catch_key_press_event(event))
		# Invocation de la fonction catck_key_release_event lors du relâchement d’une touche
		window.bind("<KeyRelease>", lambda event : self.catch_key_release_event(event))
		# Met en pause la partie lorsque la fenêtre n’a plus la priorité
		window.bind("<FocusOut>", lambda event : self.pause())

	def angle_to_normalized_vector(self):
		"""
		Renvoie le vecteur de norme 1 dont l’angle avec un vecteur dirigeant l’axe horizontal est celui de la voiture.
		"""
		return math.cos(self.angle), math.sin(self.angle)

	def catch_key_press_event(self, event):
		"""
		Fonction invoquée lors de l’appui d’une touche, permettant de savoir quelle(s) touche(s) est/sont actuellement pressée(s)
		"""
		# Si le jeu est en pause, rien ne se passe
		if self.paused:
			return

		# Ajout de la touche dans la liste keys_pressed
		self.keys_pressed.add(event.keysym.upper())


	def catch_key_release_event(self, event):
		"""
		Fonction invoquée lors du relâchement d’une touche, permettant de savoir quelle(s) touche(s) est/sont actuellement pressée(s)
		"""
		# La touche Échap met en pause la partie
		if event.keysym.upper() == "ESCAPE":
			self.pause()
			return

		# Si la touche est effectivement pressée (on ne sait jamais), on retire cette touche de la liste
		if event.keysym.upper() in self.keys_pressed:
			self.keys_pressed.remove(event.keysym.upper())

	def pause(self):
		"""
		Mise en pause de la partie 
		"""
		# Si la partie est déjà en pause ou est stoppée, rien ne se passe
		if self.paused or self.thread.stopped:
			return
		# Plus aucune touche n’est pressée (afin d’éviter des bugs qui permettent d’avancer tout seul)
		self.keys_pressed.clear()
		# Changement du statut de pause
		self.paused = True

		# Dessin du menu de pause
		canvas = self.canvas #type: tk.Canvas
		# Rectangle blanc quadrillé, donnant l’impression de transparence
		rectangle = canvas.create_rectangle(0, 0, self.game.width, self.game.height, fill = "#F0F0F0", stipple = "gray50")

		# noinspection PyProtectedMember
		def resume():
			"""
			Fonction invoquée lorsque le bouton Reprendre est cliqué, reprenant alors la partie en cours 
			"""
			# Changement du statut de pause
			self.paused = False
			try:
				# Suppression du rectangle
				canvas.delete(rectangle)
			except:
				pass
			# Suppression des boutons des enfants
			if resumeButton in self.game._children:
				self.game._children.remove(resumeButton)
			if quitButton in self.game._children:
				self.game._children.remove(quitButton)
			# Destruction des boutons
			resumeButton.destroy()
			quitButton.destroy()
			# Suppression de l’écouteur de la touche Échap
			self.window.unbind("<KeyRelease-Escape>", resumeId)

		def quitGame():
			"""
			Fonction invoquée lorsque le bouton Menu principal est cliqué, quittant alors la partie
			"""
			# Fin du processus faisant avancer la voiture
			self.thread.stopped = True
			# Suppression de la mise en pause
			self.paused = False
			# Affichage du menu principal
			mainMenu.MainMenu(self.window)

		# Création des boutons de reprise et de fin de partie
		resumeButton = tk.Button(self.window, textvariable = msgs.RESUME, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 15, borderwidth = 10, bg = utils.BUTTON_BACKGROUND, relief = "groove", command = resume)
		quitButton = tk.Button(self.window, textvariable = msgs.MAIN_MENU, font = ("Plantagenet Cherokee", 30), anchor = "center", width = 15, borderwidth = 10, bg = utils.BUTTON_BACKGROUND, relief = "groove", command = quitGame)

		# La touche Échap permet de reprendre la partie
		fc = lambda event : resume()
		resumeId = self.window.bind("<KeyRelease-Escape>", fc)

		# Positionnement des boutons
		width, height = self.game.width, self.game.height
		resumeButton.place(x = (width - resumeButton.winfo_reqwidth()) / 2, y = height / 4)
		quitButton.place(x = (width - quitButton.winfo_reqwidth()) / 2, y = height / 2)

		# Ajout des enfants
		self.game.appendChild(resumeButton)
		self.game.appendChild(quitButton)

	def forward(self):
		"""
		Invoqué lorsque la touche pour avancer est pressée. Fait accélérer la voiture
		"""
		# Augmentation de la vitesse jusqu’à un plafond
		self.speed = min(self.speed + self.car.acceleration, float(self.car.max_speed))

		# Déclenchement du bruitage si la voiture va suffisamment vite
		if self.speed >= min(self.car.max_speed / 2, 10):
			AudioPlayer.playSound(AudioPlayer.DRIVING)

	def backward(self):
		"""
		Invoqué lorsque la touche pour freiner est pressée. Fait décélérer/reculer la voiture
		"""
		# Fait décroître la vitesse jusqu’à un plafond (négatif) dont sa valeur absolue est deux fois plus faible que celle en accélération
		self.speed = max(self.speed - self.car.acceleration, float(-self.car.max_speed / 2))

	def left(self):
		"""
		Invoqué lorsque la touche pour tourner à gauche est pressée. Provoque une rotation de la voiture vers la gauche
		"""
		# Rotation algébrique de la voiture
		self.angle -= math.pi / self.angle_division
		self.angle %= 2 * math.pi
		if self.angle > math.pi:
			self.angle -= 2 * math.pi
		# Calcul du nouveau vecteur vitesse de norme 1
		self.vector = self.angle_to_normalized_vector()
		# Actualisation et rotation de l’image de la voiture
		img_temp = Image.open("images/cars/" + self.car.img_file)
		img_temp = img_temp.convert("RGBA")
		img_temp = img_temp.resize((self.car.width, self.car.height), Image.ANTIALIAS)
		img_temp = img_temp.rotate(-self.angle * 180 / math.pi, expand = 1)
		self.img_img = ImageTk.PhotoImage(img_temp)
		self.canvas.delete(self.img)
		self.img = self.canvas.create_image(self.game.width / self.game.map.width * self.x, self.game.height / self.game.map.height * self.y, image = self.img_img)

	def right(self):
		"""
		Invoqué lorsque la touche pour tourner à droite est pressée. Provoque une rotation de la voiture vers la droite
		"""
		# Rotation algébrique de la voiture
		self.angle += math.pi / self.angle_division
		self.angle %= 2 * math.pi
		if self.angle > math.pi:
			self.angle -= 2 * math.pi
		# Calcul du nouveau vecteur vitesse de norme 1
		self.vector = self.angle_to_normalized_vector()
		# Actualisation et rotation de l’image de la voiture
		img_temp = Image.open("images/cars/" + self.car.img_file)
		img_temp = img_temp.convert("RGBA")
		img_temp = img_temp.resize((self.car.width, self.car.height), Image.ANTIALIAS)
		img_temp = img_temp.rotate(-self.angle * 180 / math.pi, expand = 1)
		self.img_img = ImageTk.PhotoImage(img_temp)
		self.canvas.delete(self.img)
		self.img = self.canvas.create_image(self.game.width / self.game.map.width * self.x, self.game.height / self.game.map.height * self.y, image = self.img_img)

class CarThread(Thread):
	def __init__(self, car : Car):
		"""
		Constructeur par défaut du processus principal faisant fonctionner la voiture.
		Prend l’objet voiture en argument
		"""
		Thread.__init__(self)
		self.car = car
		self.stopped = False
		self.last_passage = -1
		self.last_passage_dir = 1

	def run(self):
		"""
		Boucle principale du processus, actualisée 60 fois par seconde (en négligeant le temps d’actualisation)
		"""
		car = self.car
		import time
		while True:
			# Si le jeu est en pause, mise en pause du processus
			if car.paused:
				continue

			# Si l’ordre d’arrêt à été donné, le processus s’arrête
			if self.stopped:
				return

			# Si certaines touches sont pressées, déclenchement des actions correspondantes
			from utils import CONTROLS
			for key in set(car.keys_pressed):
				if key == CONTROLS["forward"]:
					car.forward()
				elif key == CONTROLS["backward"]:
					car.backward()
				elif key == CONTROLS["left"]:
					car.left()
				elif key == CONTROLS["right"]:
					car.right()
				else:
					continue

				# Si une touche utile a été pressée, déclenchement du chronomètre
				if car.game.time == -1:
					car.game.time = 0

			# Calcul des potentielles futures coordonnées (vitesse divisée par 60 en raison des 60 actualisations par seconde)
			newX = car.x + car.speed * car.vector[0] / 60.0
			newY = car.y + car.speed * car.vector[1] / 60.0

			# Détection de collision
			collision = False
			for wall in car.game.map.walls:
				# Pour chaque mur, compare la distance du centre de la voiture au projeté orthogonal de ce centre sur ce mur
				# Si cette distance est trop faible, une collsion est alors détectée
				dot_product = (wall.x_end - wall.x_start) * (newX - wall.x_start) + (wall.y_end - wall.y_start) * (newY - wall.y_start)
				line = (wall.x_end - wall.x_start, wall.y_end - wall.y_start)
				line_length = math.sqrt(line[0] ** 2 + line[1] ** 2)
				xH, yH = dot_product / (line_length ** 2) * line[0] + wall.x_start, dot_product / (line_length ** 2) * line[1] + wall.y_start

				if xH < min(wall.x_start, wall.x_end) or xH > max(wall.x_start, wall.x_end) or yH < min(wall.y_start, wall.y_end) or yH > max(wall.y_start, wall.y_end):
					continue

				diagonal = math.sqrt(car.car.width ** 2 + car.car.height ** 2) / 2
				if math.sqrt((xH - newX) ** 2 + (yH - newY) ** 2) < diagonal + 0.1:
					collision = True
					break

			# En cas de collision, le son de collision est déclenché, et la voiture est propulsée en arrière
			if collision:
				AudioPlayer.playSound(AudioPlayer.COLLISION, bypass = True)
				car.x = car.x - car.speed * car.vector[0] / 10.0
				car.y = car.y - car.speed * car.vector[1] / 10.0
				car.speed = -car.speed
				# Attente d’1/60 seconde et avancement du chronomètre
				time.sleep(1.0 / 60.0)
				car.game.time += 1.0 / 60.0
				car.game.time_label.config(text = formatTime(car.game.time))
				# Fin de boucle
				continue

			# Affectation des nouvelles coordonnées
			car.x = newX
			car.y = newY
			# Si la voiture n’accélère / ne décélère pas, les frottements avec le goudron font chuter la vitesse de 1 %
			if CONTROLS["forward"] not in car.keys_pressed and CONTROLS["backward"] not in car.keys_pressed:
				car.speed *= 0.99
			# Déplacement de la voiture sur l’interface
			car.canvas.coords(car.img, car.game.width / car.game.map.width * car.x, car.game.height / car.game.map.height * car.y)

			# Attente d’1/60 seconde
			time.sleep(1.0 / 60.0)
			# Si le chronomètre est lancé, mise à jour du chronomètre
			if car.game.time >= 0:
				car.game.time += 1.0 / 60.0
				car.game.time_label.config(text = formatTime(car.game.time))

			# Détection du passage de la voiture sur la ligne d’arrivée
			# Le procédé est le même que pour la détection de collision
			wall = car.game.map.start
			dot_product = (wall.x_end - wall.x_start) * (newX - wall.x_start) + (wall.y_end - wall.y_start) * (newY - wall.y_start)
			line = (wall.x_end - wall.x_start, wall.y_end - wall.y_start)
			line_length = math.sqrt(line[0] ** 2 + line[1] ** 2)
			xH, yH = dot_product / (line_length ** 2) * line[0] + wall.x_start, dot_product / (line_length ** 2) * line[1] + wall.y_start

			if xH < min(wall.x_start, wall.x_end) or xH > max(wall.x_start, wall.x_end) or yH < min(wall.y_start, wall.y_end) or yH > max(wall.y_start, wall.y_end):
				continue

			# Si la voiture est passée sur la ligne d’arrivée
			if math.sqrt((xH - newX) ** 2 + (yH - newY) ** 2) <= math.fabs(car.speed) / 60.0:
				# On calcule la direction de la voiture : elle vaut 1 si elle va dans le bon sens, -1 dans le sens contraire
				# Pour le savoir, on vérifie si l’angle se situe dans l’intervalle [t - pi/2; t + pi/2] où t est l’angle de départ, et on vérifie si la voiture avance ou recule
				# Cela permet d’éviter quelques tentatives de triche
				direction = (1 if math.fabs(car.start_angle - car.angle) <= math.pi / 2 else -1) * (1 if car.speed > 0 else -1)
				# Un délai d’une seconde est laissé à la voiture pour passer, si ce délai n’est pas passé et que la voiture va dans le même sens que précédemment, rien ne se passe
				# Il est improbable que la voiture arrive à s’arrêter exactement sur la ligne d’arrivée (cet événement est négligé)
				if direction == self.last_passage_dir and time.time() - self.last_passage < 1:
					continue
				# Enregistrement du dernier temps de passage ainsi que sa direction (pour le délai d’une seconde)
				self.last_passage = time.time()
				self.last_passage_dir = direction

				# Si la voiture a commencé un nouveau tour qu’elle n’avait encore jamais commencé, on calcule et on enregistre le temps passé pour le tour précédent
				if car.game.lap > len(car.lap_times):
					total_last_time = 0
					if car.game.lap >= 1:
						for lap in range(car.game.lap - 1):
							total_last_time += car.lap_times[lap]
					car.lap_times.append(car.game.time - total_last_time)

				# Si la voiture a effectué tous ses tours, la partie s’arrête et l’écran de fin s’affiche
				if car.game.lap == car.game.map.max_laps:
					self.stopped = True
					self.end()
					return

				# Le numéro du tour est ajouté de la direction préédemment introduite (passer la ligne d’arrivée dans le mauvais sens fait revenir au tour précédent)
				car.game.lap += direction
				car.game.lap_label.config(text = msgs.LAP_NUMBER.get().format(car.game.lap, car.game.map.max_laps))

	def end(self):
		"""
		Invoqué lorsque la partie se termine et que la voiture a terminé le parcours
		"""
		car = self.car #type: Car
		canvas = car.canvas #type: tk.Canvas

		# Sauvegarde du score
		laps_time_str = list()
		for lap_time in car.lap_times:
			laps_time_str.append(formatTime(lap_time))
		score = scores.Score(car.car, car.game.map, laps_time_str, formatTime(car.game.time), car.game.time)
		highScore = scores.getHighScore(car.game.map)

		# Affichage du même rectangle blanc que le menu pause
		canvas.create_rectangle(0, 0, car.game.width, car.game.height, fill = "#F0F0F0", stipple = "gray50")
		canvas.create_text(car.game.window.winfo_reqwidth() / 2, car.game.window.winfo_reqheight() / 5, text = msgs.YOU_WIN.get().format(formatTime(car.game.time)), font = ("Plantagenet Cherokee", 26))
		# Si le joueur a battu le record précédent, on lui indique, sinon on lui dit quel est le record à battre
		if score is highScore:
			canvas.create_text(car.game.window.winfo_reqwidth() / 2, car.game.window.winfo_reqheight() / 5 + 42, text = msgs.NEW_HIGH_SCORE.get(), font = ("Plantagenet Cherokee", 26))
		else:
			canvas.create_text(car.game.window.winfo_reqwidth() / 2, car.game.window.winfo_reqheight() / 5 + 42, text = msgs.HIGH_SCORE.get().format(highScore.total_time), font = ("Plantagenet Cherokee", 26))
		# Création du bouton de retour au menu principal
		quitButton = tk.Button(car.game.window, textvariable = msgs.MAIN_MENU, font = ("Plantagenet Cherokee", 26), bg = utils.BUTTON_BACKGROUND, command = lambda : mainMenu.MainMenu(car.game.window))
		# Création d’un cadre d’affichage des temps par tour
		lap_times = tk.Frame(car.game.window, borderwidth = 2, relief = tk.GROOVE)
		# Création et affichage des titres des colonnes du tableau
		lap_label = tk.Label(lap_times, textvariable = msgs.LAP, font = ("Plantagenet Cherokee", 22, "bold"), width = 5)
		time_label = tk.Label(lap_times, textvariable = msgs.TIME, font = ("Plantagenet Cherokee", 22, "bold"), width = 8)
		lap_label.grid(row = 0, column = 0)
		time_label.grid(row = 0, column = 1)
		for lap in range(car.game.map.max_laps):
			# Pour chaque tour, affichage du numéro du tour ainsi que le temps efectué dans le tableau
			lap_number = tk.Label(lap_times, text = str(lap + 1), font = ("Plantagenet Cherokee", 18))
			lap_time = tk.Label(lap_times, text = formatTime(car.lap_times[lap]), font = ("Plantagenet Cherokee", 18))
			lap_number.grid(row = lap + 1, column = 0)
			lap_time.grid(row = lap + 1, column = 1)

		# Positionnement du bouton pour quitter ainsi que les temps effectués
		quitButton.place(x = (car.game.window.winfo_reqwidth() - quitButton.winfo_reqwidth()) / 2, y = (car.game.window.winfo_reqheight() - quitButton.winfo_reqheight()) / 2)
		lap_times.place(x = car.game.window.winfo_reqwidth() - lap_times.winfo_reqwidth(), y = car.game.window.winfo_reqheight() / 5)

		# Ajout des enfants
		car.game.appendChild(quitButton)
		car.game.appendChild(lap_times)

def formatTime(t: float):
	"""
	Formatte une durée numérique en secondes en une chaîne de caractères de la forme HH:MM:SS.mmm
	HH : heures
	MM : minutes
	SS : secondes
	mmm : millisecondes
	"""
	hours = int(t // 3600)
	t %= 3600
	minutes = int(t // 60)
	t %= 60
	seconds = int(t)
	t %= 1
	millis = int(1000 * t)
	# str.zfill(n) remplit de zéros jusqu’à avoir n chiffres
	return str(hours).zfill(2) + ":" + str(minutes).zfill(2) + ":" + str(seconds).zfill(2) + "." + str(millis).zfill(3)

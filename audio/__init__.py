# Le module pygame est uniquement utilisé pour son sous-module de musique
from pygame import mixer
import pygame
from threading import Thread
import time

class AudioPlayer(Thread):
	# Initialisation du module pygame
	mixer.pre_init(44100, -16, 2, 2048)
	pygame.init()
	window = None
	# Musique de fond
	MUSIC = mixer.Sound("audio/Guazu.wav")
	# Liste des sons
	COLLISION = mixer.Sound("audio/Glass_break.wav")
	DRIVING = mixer.Sound("audio/driving.wav")
	CLICK = mixer.Sound("audio/click.wav")
	_channels = {COLLISION: None, DRIVING: None, CLICK: None}

	def __init__(self, window):
		"""
		Constructeur du lecteur audio
		"""
		Thread.__init__(self)
		self.window = window
		AudioPlayer.window = window
		self.music_state = False

	def run(self):
		"""
		Boucle de lecture
		"""
		while True:
			# Si la musique n’est pas lancée et que la musique est activée (équivalent à un appui du bouton du menu d’options délayé), lance la musique en boucle
			if not self.music_state and self.window.music_enabled:
				self.MUSIC.play(loops = -1)
				self.music_state = True
			# De même, si la musique est lancée et que la musique est désactivée, arrête la musique
			elif self.music_state and not self.window.music_enabled:
				self.MUSIC.stop()
				self.music_state = False

			# Attente de 50 ms pour ne pas tout surcharger
			time.sleep(0.05)

	@staticmethod
	def playSound(sound, loops = 0, bypass = False):
		"""
		Lecture d’un son
		Argument loops : Nombre de répétitions supplémentaires (-1 équivalent à l’infini)
		Argument bypass : Si le son est déjà lancé et que bypass vaut True, le son va s’interrompre et recommencer
		"""
		# Si les effets sonores sont activés et si le son n’est pas déjà en lecture (si on décide d’attendre que le précédent soit terminé), on lance le son
		if AudioPlayer.window.sounds_enabled and (bypass or AudioPlayer._channels[sound] is None or not AudioPlayer._channels[sound].get_busy()):
			AudioPlayer._channels[sound] = sound.play(loops)

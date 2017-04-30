from pygame import mixer
import pygame
from threading import Thread
import time

class AudioPlayer(Thread):
	mixer.pre_init(44100, -16, 2, 2048)
	pygame.init()
	window = None
	MUSIC = mixer.Sound("audio/Guazu.wav")
	COLLISION = mixer.Sound("audio/Glass_break.wav")
	DRIVING = mixer.Sound("audio/driving.wav")
	_channels = {COLLISION: None, DRIVING: None}

	def __init__(self, window):
		Thread.__init__(self)
		self.window = window
		AudioPlayer.window = window
		self.music_state = False

	def run(self):
		while True:
			if not self.music_state and self.window.music_enabled:
				self.MUSIC.play(loops = -1)
				self.music_state = True
			elif self.music_state and not self.window.music_enabled:
				self.MUSIC.stop()
				self.music_state = False

			time.sleep(0.05)

	@staticmethod
	def playSound(sound, loops = 0):
		if AudioPlayer.window.sounds_enabled and (AudioPlayer._channels[sound] is None or not AudioPlayer._channels[sound].get_busy()):
			AudioPlayer._channels[sound] = sound.play(loops)

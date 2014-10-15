# 
# a game by Adam Binks

import pygame, random

pygame.init()
	
SOUND = {}
for filename in ['explosion1', 'explosion2', 'explosion3', 'explosion4',
				 'explosion5', 'hit', 'plup', 'shoot1', 'shoot2', 'pip',
				 'swoosh', 'shoot down']: # .wav files only
	SOUND[filename] = pygame.mixer.Sound('assets/sounds/%s.wav' %(filename))

def play(sound, volume=0.8, varyVolume=True, loops=0):
	"""Plays the given sound"""
	if varyVolume:
		volume -= random.uniform(0.0, 0.2)
		if volume < 0.1: volume == 0.1
		SOUND[sound].set_volume(volume)
	SOUND[sound].play(loops)


def playMusic(filename):
	pygame.mixer.music.load(filename)
	pygame.mixer.music.play(-1)
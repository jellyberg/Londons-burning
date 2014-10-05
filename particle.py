# 
# a game by Adam Binks

import pygame, time, random

class Particle(pygame.sprite.Sprite):
	"""A simple particle"""
	gravity = 2
	def __init__(self, data, image, topleft, avgLifeSpan, velocity, obeysGravity):
		"""obeysGravity: 0 is no gravity, 1 is falling particle, -1 is upward floating particle"""
		pygame.sprite.Sprite.__init__(self)
		self.add(data.particles)

		self.image = image
		self.rect = image.get_rect()
		self.rect.topleft = topleft
		self.coords = list(topleft)

		self.velocity = list(velocity)
		self.gravity = obeysGravity

		self.birthTime = time.time()
		self.lifeTime = random.uniform(avgLifeSpan - 0.3, avgLifeSpan + 0.3)
		if self.lifeTime < 0: self.lifeTime = 0.05


	def update(self, data):
		if self.gravity != 0:
			self.velocity[1] = self.velocity[1] + Particle.gravity * self.gravity * data.dt # allow gravity to act upon the particle
		self.coords[0] += self.velocity[0] * data.dt
		self.coords[1] += self.velocity[1] * data.dt

		self.rect.topleft = self.coords

		data.screen.blit(self.image, self.rect)
		if time.time() - self.birthTime > self.lifeTime:
			self.kill()



class SmokeSpawner(pygame.sprite.Sprite):
	"""A particle spawner for smoke"""
	def __init__(self, data, topleft):
		pygame.sprite.Sprite.__init__(self)
		self.add(data.particleSpawners)

		self.sourceCoords = topleft
		self.image = data.loadImage('assets/particles/smoke.png')
		self.lifespan = 0.2


	def update(self, data):
		if random.randint(0, 10) == 0:
			Particle(data, self.image, self.sourceCoords, self.lifespan, (random.randint(-10, 10), random.randint(-10, 10)), -1)
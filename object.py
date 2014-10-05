# 
# a game by Adam Binks

import pygame, random, time
from particle import SmokeSpawner

class Building(pygame.sprite.Sprite):
	"""A static object that falls over then disappears when bombed"""
	def __init__(self, data, image, xCoord):
		pygame.sprite.Sprite.__init__(self)
		self.add(data.buildings)
		self.add(data.standingBuildings)
		self.add(data.destroyableEntities)

		self.baseImage = image
		self.image = image
		self.rect = image.get_rect()
		self.rect.x = xCoord
		self.rect.bottom = data.WINDOWHEIGHT

		self.state = 'stable'


	def update(self, data):
		if self.state == 'bombed':
			animIsDone = self.updateFallAnimation(data)
			if animIsDone:
				self.kill()
		data.screen.blit(self.image, self.rect)


	def updateFallAnimation(self, data):
		isDone = True
		return isDone


	def isBombed(self, data):
		self.state = 'bombed'
		self.remove(data.standingBuildings)



class Bomber(pygame.sprite.Sprite):
	"""An enemy plane that drops bombs on your buildings"""
	minTimeToDropBomb = 0.6
	maxTimeToDropBomb = 4
	speed = 15

	def __init__(self, data, startAtLeft, yPos):
		pygame.sprite.Sprite.__init__(self)
		self.add(data.bombers)

		self.imageL = data.loadImage('assets/enemies/bomber.png')
		self.imageR = pygame.transform.flip(self.imageL, 1, 0)

		self.droppedBomb = False
		self.timeTillBombPrimed = random.uniform(Bomber.minTimeToDropBomb, Bomber.maxTimeToDropBomb)
		self.lastBombDropTime = time.time()

		self.rect = self.imageR.get_rect()
		self.targetingRect = pygame.Rect((0, 0), (6, 10)) # BOMB SIZE

		if startAtLeft:
			self.direction = 'right'
			self.image = self.imageR
			self.rect.topleft = (0, yPos)
		else:
			self.direction = 'left'
			self.image = self.imageL
			self.rect.topright = (data.WINDOWWIDTH, yPos)
		self.coords = list(self.rect.topleft) # for more accurate positioning using floats


	def update(self, data):
		if self.direction == 'right': dirMultiplier = 1
		else: dirMultiplier =  -1

		if self.rect.left > data.WINDOWWIDTH + 1:
			self.direction = 'left'
			self.image = self.imageL
		elif self.rect.right < -1:
			self.direction = 'right'
			self.image = self.imageR

		self.coords[0] += Bomber.speed * data.dt * dirMultiplier
		self.coords[1] += random.uniform(-0.2, 0.2)
		self.rect.topleft = self.coords

		if time.time() - self.lastBombDropTime > self.timeTillBombPrimed:
			self.bomb(data)

		data.screen.blit(self.image, self.rect)


	def bomb(self, data):
		"""drops a bomb if there is a target beneath"""
		if not self.checkForTarget(data): return

		Bomb(data, self.rect.midbottom)
		self.timeTillBombPrimed = random.uniform(Bomber.minTimeToDropBomb, Bomber.maxTimeToDropBomb)
		self.lastBombDropTime = time.time()


	def checkForTarget(self, data):
		"""Checks if there is a building below the plane. CURRENTLY UNUSED"""
		self.targetingRect.bottom = data.WINDOWHEIGHT
		self.targetingRect.centerx = self.rect.centerx
		for building in data.standingBuildings:
			if self.targetingRect.colliderect(building.rect):
				return True



class Bomb(pygame.sprite.Sprite):
	"""A projectile that explodes on collision with other objects and detsroys them and itself in the process"""
	fallSpeed = 18
	def __init__(self, data, topleft):
		pygame.sprite.Sprite.__init__(self)
		self.add(data.bombs)

		self.baseImage = data.loadImage('assets/enemies/bomb.png')
		self.rotation = 0.0
		self.rect = self.baseImage.get_rect(topleft=topleft)
		self.yCoord = topleft[1] # float for accuracy

		self.smoke = SmokeSpawner(data, self.rect.midtop)


	def update(self, data):
		self.checkForCollisions(data)

		if self.rotation < 90.5:
			self.image = pygame.transform.rotate(self.baseImage, self.rotation)
			self.rotation += 20 * data.dt
			self.rect = self.image.get_rect(center=self.rect.center)
		else:
			self.image = pygame.transform.rotate(self.baseImage, self.rotation)
			self.rotation += random.uniform(-0.6, 0.5)
		
		self.yCoord += Bomb.fallSpeed * data.dt
		self.rect.y = self.yCoord

		self.smoke.sourceCoords = [self.rect.centerx - 2, self.rect.top - 2]

		data.screen.blit(self.image, self.rect)


	def checkForCollisions(self, data):
		collided = pygame.sprite.spritecollideany(self, data.destroyableEntities)
		if collided:
			collided.isBombed(data)
		if collided or self.rect.bottom > data.WINDOWHEIGHT:
			self.explode()


	def explode(self):
		# TODO
		self.kill()
		self.smoke.kill()
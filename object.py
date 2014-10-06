# 
# a game by Adam Binks

import pygame, random, time
from particle import SmokeSpawner, Explosion
from random import randint

class Building(pygame.sprite.Sprite):
	"""A static object that falls over then disappears when bombed"""
	rotateAccel = 3  # rotation acceleration when bombed
	fallAccel = 4 # falling acceleration when bombed
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
		self.rotation = 0.0 # current rotation amount
		self.rotationSpeed = 0 # rotation velocity
		self.rotationDirection = random.choice([1, -1]) # randomly fall left or right
		self.fallSpeed = 0 # current fall speed


	def update(self, data):
		if self.state == 'bombed':
			animIsDone = self.updateFallAnimation(data)
			if animIsDone:
				self.kill()
		data.screen.blit(self.image, self.rect)


	def updateFallAnimation(self, data):
		"""Fall over: rotate and move down"""
		if -80 < self.rotation < 80:
			self.rotationSpeed += Building.rotateAccel * data.dt
			self.rotation += self.rotationSpeed * data.dt
			self.image = pygame.transform.rotate(self.baseImage, self.rotation * self.rotationDirection)

			self.fallSpeed += Building.fallAccel * data.dt
			self.rect.y += self.fallSpeed * data.dt

			isDone = False
		else:
			isDone = True
		return isDone


	def isBombed(self, data):
		self.state = 'bombed'
		SmokeSpawner(data, (self.rect.midbottom), randint(5, 9), 3) # smoke for the wreckage
		if randint(0, 3) == 0:  # sometimes add another smoke spawner randomly
			SmokeSpawner(data, (self.rect.x + randint(5, self.rect.width - 6), self.rect.bottom), randint(3, 5), 2)
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

		self.smoke = SmokeSpawner(data, self.rect.topleft, 10)

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
		if self.direction == 'right':
			dirMultiplier = 1
			self.smoke.sourceCoords = self.rect.midleft
		else:
			dirMultiplier =  -1
			self.smoke.sourceCoords = self.rect.midright

		if self.rect.left > data.WINDOWWIDTH + 1:
			self.direction = 'left'
			self.image = self.imageL
		elif self.rect.right < -1:
			self.direction = 'right'
			self.image = self.imageR

		self.coords[0] += Bomber.speed * data.dt * dirMultiplier
		self.coords[1] += random.uniform(-0.2, 0.2)
		self.rect.topleft = self.coords

		self.smoke.update(data)

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

		self.smoke = SmokeSpawner(data, self.rect.midtop, 2)


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
			self.explode(data)


	def explode(self, data):
		# TODO
		self.kill()
		self.smoke.kill()
		Explosion(data, self.rect.center, 40)
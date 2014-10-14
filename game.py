#
# a game by Adam Binks

import random, time
from object import Building, Bomber, AAGun, Bomb, SuperBomb, Spotlight

class GameHandler:
	def __init__(self, data):
		Bomb.baseImage = data.loadImage('assets/enemies/bomb.png')
		SuperBomb.baseImage = data.loadImage('assets/enemies/superBomb.png')
		Spotlight.baseImage = data.loadImage('assets/defences/spotlight.png')

		self.newGame(data)
		self.timeTillNewBomber = random.randint(15, 20) # longer time till second bomber to get into the swing of things
		self.lastBomberTime = time.time()

		Bomber(data, random.randint(0, 1), random.randint(50, 300))


	def update(self, data, dt):
		data.gameSurf.fill((60, 60, 60))

		data.spotlights.update(data)
		data.buildings.update(data)
		
		data.particleSpawners.update(data)
		data.particles.update(data)

		data.AAguns.update(data)
		data.bullets.update(data)

		if time.time() - self.lastBomberTime > self.timeTillNewBomber or len(data.bombers) == 0:
			Bomber(data, random.randint(0, 1), random.randint(50, 250))
			self.timeTillNewBomber = random.randint(10, 14)
			self.lastBomberTime = time.time()

		data.bombers.update(data)
		data.bombs.update(data)

		data.screen.blit(data.gameSurf, (data.screenShakeOffset[0], data.screenShakeOffset[1]))
		data.updateScreenshake()




	def newGame(self, data):
		data.newGame()

		Spotlight(data, (200, data.WINDOWHEIGHT), 50)
		Spotlight(data, (400, data.WINDOWHEIGHT), 130)

		buildingImgs = []
		for buildingFileName in ['tall1', 'tall2', 'small1', 'small2', 'small3', 'factory1']:
			buildingImgs.append(data.loadImage('assets/buildings/%s.png' %(buildingFileName)))
		aaGunIsBuilt = False
		x = 4
		while x < data.WINDOWWIDTH:
			img = random.choice(buildingImgs)
			if x > int(data.WINDOWWIDTH / 2) - 32 and not aaGunIsBuilt:  # build a single AA Gun roughly halfway across the screen
				AAGun(data, x)
				x += 64
				aaGunIsBuilt = True

			elif x + img.get_width() < data.WINDOWWIDTH:
				Building(data, img, x)
				x += img.get_width()
			x += 4 # gap between buildings

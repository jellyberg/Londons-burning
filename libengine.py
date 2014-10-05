# 
# a game by Adam Binks

import pygame, input, game

def run():
	stateHandler = StateHandler()
	while True:
		stateHandler.update()


class StateHandler:
	"""handles menu and game state, runs boilerplate update code"""
	def __init__(self):
		self.data = Data()
		self.data.screen.fill((60, 60, 60))
		pygame.display.set_caption('Blitz Defence')

		self.gameHandler = game.GameHandler(self.data)


	def update(self):
		self.data.input.get()
		self.data.dt = self.data.FPSClock.tick(self.data.FPS) / 100.0
		pygame.display.set_caption('Blitz Defence  FPS: %s' %(int(self.data.FPSClock.get_fps())))

		# update game/menu objs
		self.gameHandler.update(self.data, self.data.dt)

		pygame.display.update()



class Data:
	"""stores variables to be accessed in many parts of the game"""
	def __init__(self):
		self.WINDOWWIDTH, self.WINDOWHEIGHT = (600, 800)
		self.screen = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))
		self.FPSClock = pygame.time.Clock()
		self.FPS = 1000
		self.input = input.Input()

		self.IMAGESCALEUP = 4


	def newGame(self):
		self.destroyableEntities = pygame.sprite.Group() # any objects destroyable by bombs

		self.particles = pygame.sprite.Group()
		self.particleSpawners = pygame.sprite.Group()

		self.buildings = pygame.sprite.Group()
		self.standingBuildings = pygame.sprite.Group()

		self.bombers = pygame.sprite.Group()
		self.bombs = pygame.sprite.Group()


	def loadImage(self, imagePath):
		"""Loads an image and scales it 4x so it's nice and pixellated"""
		img = pygame.image.load(imagePath)
		img = pygame.transform.scale(img, (img.get_width() * self.IMAGESCALEUP, img.get_height() * self.IMAGESCALEUP))
		img.convert_alpha()
		return img


	def saveGame(self):
		pass


if __name__ == '__main__':
	run()
from .config import *

class Platform(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		
		self.image = pygame.Surface(DIM_PLATFORM)
		self.image.fill(ROJO_CARAMELO)
		
		self.rect = self.image.get_rect()
		
		#La posicionamos.
		self.rect.x = 0
		self.rect.y = HEIGHT - ALT_PLATFORM
		
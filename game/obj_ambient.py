from .config import *

#clase de objetos del ambiente.
class ObjAmbient(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		#Establecemos un objeto rectangular.
		#Adimensional.
		self.rect = pygame.Rect(0, 0, 0, 0)
		self.vel_x = SPEED
		
	def update(self):
		self.rect.left -= self.vel_x
		
	def stop(self):
		self.vel_x = 0
		
class Wall(ObjAmbient):
	def __init__(self, left, bottom, ubic_src):
		super().__init__()
		
		self.image = pygame.image.load(ubic_src)
		
		self.rect = self.image.get_rect()
		self.rect.left = left
		self.rect.bottom = bottom
		
		#rectangulo minimo para controlar
		#las colisiones en la parte superior de la pared.
		
		#recordar que x, y, corresponden a la
		#coordenada de la esquina superior
		#izquierda.
		self.rect_top = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, 1)
		
	def update(self):
		super().update()
		#el rectangulo de colisiones.
		#sigue la posición de la pared.
		self.rect_top.x = self.rect.x
		
class Coin(ObjAmbient):
	def __init__(self, pos_x, pos_y, ubic_src):
		super().__init__()
		self.image = pygame.image.load(ubic_src)
		
		self.rect = self.image.get_rect()
		self.rect.x = pos_x
		self.rect.y = pos_y
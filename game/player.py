from .config import *

class Player(pygame.sprite.Sprite):
	def __init__(self, left, bottom, ubic_src):
		super().__init__()
		
		#Son varias imagenes para la animación
		#del personaje.
		self.images = (
			pygame.image.load(ubic_src['base']),
			pygame.image.load(ubic_src['walk']),
			pygame.image.load(ubic_src['jump']),
			pygame.image.load(ubic_src['fall'])
		)
		
		#Imagen que se muestra.
		#Por defecto es base.
		self.image = self.images[0]
		
		#Posicionamos.
		self.rect = self.image.get_rect()
		self.rect.left = left
		self.rect.bottom = bottom
		
		#Damos valores iniciales para
		#variables fisicas.
		self.pos_y = self.rect.bottom
		self.vel_y = 0
		
		#Limitación de salto.
		#Impide que salte en el aire.
		self.can_jump = False
		
		#Iniciar sin surfear paredes.
		self.surfing = False
		
		#Es True, mientras el personaje
		#Este activo.
		self.playing = True
		
	#Analisis de colisiones frontales.
	#sprites: otros objetos del ambiente.
	def collide_with(self, sprites):
		#spritecollide toma:
		#el objeto_base, los objetos.
		#sprites con los que choca,
		#False, impide que se ejecute Kill
		#en dokill, así no se borran.
		#los obstaculos al chocarlos.
		
		#retorna una lista de sprites
		#con el choque efectivo.
		#En caso de darse.
		obj_collide =  pygame.sprite.spritecollide(self, sprites, False)
		#Retorna el primer elemento de choque.
		if obj_collide:
			return obj_collide[0]
		
	#Analisis colisión rectangular.
	#Para que surfee la superficie.
	#de las paredes.
	def collide_bottom(self, wall):
		return self.rect.colliderect(wall.rect_top)
		
	#Función generica para mantener el personaje sobre una
	#Plataforma.
	def y_static(self, floor):
		#Evitan que se hunda en la pared.
		self.vel_y = 0
		self.pos_y = floor.top

		#Le permite saltar.
		self.can_jump = True
		
		#Alterna las imagenes para caminar.
		self.walked()
	
	#Función para surfear.
	#Establece las condiciones físicas para
	#'Surfear' encima de las paredes.
	#Y las condiciones booleanas para desactivar
	#La gravedad.
	def skid(self, wall):
		self.y_static(wall.rect_top)
		
		#Reporta que esta surfeando.
		self.surfing = True
		
	def validate_platform(self, platform):
		#Verifica por medio de los
		#atributos rect de ambos objetos.
		#Si chocan de forma rectangular.
		#retorna un valor booleano.
		if pygame.sprite.collide_rect(self, platform):
			self.y_static(platform.rect)
	
	def walked(self):
		index_walk = int(pygame.time.get_ticks()//PLAYER_WALK%2)
		self.image = self.images[index_walk]
		
	#Controla que no se de más de un salto por vez.
	#Además establece una velocidad negativa.
	#que hace al personaje ascender.
	#(y = 100, esta arriba de y = 200)
	def jump(self):
		if self.can_jump:
			self.vel_y = CAP_SALTO
			self.can_jump = False
			
			#Imagen de salto.
			self.image = self.images[2]

	#Mecanismo de gravedad.
	def mech_grav(self):
	#Si no esta surfeando la gravedad funciona.
		if not self.surfing:
			self.vel_y += PLAYER_GRAV
			self.pos_y += self.vel_y + 0.5 * PLAYER_GRAV

			#Cuando esta cayendo de un salto
			#baja los brazos.
			if self.vel_y > 0 and not self.can_jump:
				self.image = self.images[3] #Skin de caida.
				
	#Actualiza el estado del jugador.
	def update(self):
		if self.playing:
			#Gravedad.
			self.mech_grav()
			#Posición vertical.
			self.rect.bottom = self.pos_y
	
	#Detiene la actividad del jugador.
	def stop(self):
		self.playing = False
	
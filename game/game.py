import sys, random

#Elementos del juego.
from .config import *
from .platform import Platform
from .player import Player
from .obj_ambient import Wall, Coin

#Clase principal.
class Game:
	def __init__(self):
		pygame.init()
		
		self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption(TITLE)
		
		#El juego esta corriendo.
		self.running = True
		
		#Iniciamos una instancia para poder
		#controlar los Frames por segundo.
		self.clock = pygame.time.Clock()
		
		#Fuente del equipo. Con match_font
		self.font = pygame.font.match_font(FONT)
		
	def start(self):
		#Menu.
		self.menu()
		#Invocamos el constructor.
		self.built()
		
	#Termina los procesos.
	#Cierra pygame y cierra python.
	def finish_query(self, event):
		if event.type == pygame.QUIT:
			self.running = False
			pygame.quit()
			sys.exit()
		
	def built(self):
		#Valores cuantizables.
		self.score = 0
		self.level = 0
		
		#Elementos del ambiente.
		self.background = pygame.image.load(BACKGROUND)
		self.generate_elements()
		
		#Establecemos los sonidos base.
		self.sounds = self.generate_sounds(['stop', 'coin'], 
										   [LOSE_SRC, COIN_SOUND_SRC])
		
		#Ejecución:
		self.run()

	#Retorna un diccionario, y establece un volumen estandar.
	def generate_sounds(self, key_names, sounds_src):
		dict_sounds = {}
		for key_name, sound_src in zip(key_names, sounds_src):
			dict_sounds[key_name] = pygame.mixer.Sound(sound_src)
			dict_sounds[key_name].set_volume(VOL_SOUND)
		return dict_sounds
		
		
	def generate_elements(self):
		self.platform = Platform()
		self.player = Player(100, self.platform.rect.top - FLY_PLAYER, PLAYER_SRC)
		
		#Conjunto de sprites.
		self.walls = pygame.sprite.Group()
		self.coins = pygame.sprite.Group()
		self.sprites = pygame.sprite.Group()
		
		#Ponemos al jugador y la plataforma
		#En el mismo sprite.
		self.sprites.add(self.platform, self.player)
		
		self.generate_walls()
		
	def generate_ambient(self, last_position, MAX_, ESP_, cls, high, _SRC, sub_sprites):
		for o in range(0, MAX_):
			pos_x = random.randint(last_position+ESP_, last_position+ESP_*2)
			
			obj_ = cls(pos_x, high, _SRC)
			
			last_position = obj_.rect.right
			
			#Añadimos a sprites.
			#Y a paredes para metodos particulares.
			self.sprites.add(obj_)
			sub_sprites.add(obj_)		
		
	def generate_walls(self):
		#Si se han eliminado todas las paredes previas.
		if not len(self.walls):
			self.generate_ambient(INC_WALL, MAX_WALLS, ESP_WALL, Wall, self.platform.rect.top, WALL_SRC, self.walls)

			#Sube de nivel y genera monedas.
			self.level += 1
			self.generate_coins()
			
	def generate_coins(self):
		self.generate_ambient(INC_COIN, MAX_COINS, ESP_COIN, Coin, ALT_COIN, COIN_SRC, self.coins)
		
	#Ejecución del juego metodos principales.
	#Del juego.
	def run(self):
		while self.running:
			#Establecemos la velocidad.
			#De Frames por segundo.
			self.clock.tick(FPS)
			
			self.events()
			self.update()
			self.draw()
			
	def events(self):
		for event in pygame.event.get():
			self.finish_query(event)
				
		key = pygame.key.get_pressed()
		
		#Salto.
		if key[pygame.K_SPACE]:
			self.player.jump()
			
		#Recargar el juego si el jugador.
		#Perdio y se presiona r
		if key[pygame.K_r] and not self.player.playing:
			self.built()
			
	#Formatos para texto de puntaje y niveles.
	def score_format(self):
		return f'Score: {self.score}'

	def level_format(self):
		return f'Level: {self.level}'

		
	#Renderizar texto e imprimir.
	def display_text(self, text, size, color, pos_x, pos_y):
		font = pygame.font.Font(self.font, size)
	
		text = font.render(text, True, color)
		rect = text.get_rect()
		rect.midtop = (pos_x, pos_y)
		
		self.surface.blit(text, rect)

	#Estructurar textos.
	def draw_text(self):
		self.display_text(self.score_format(), T_SIZE, T_COLOR, WIDTH//2, TEXT_POSY)
		self.display_text(self.level_format(), T_SIZE, T_COLOR, 60, TEXT_POSY)
		
		if not self.player.playing:
			self.display_text('Perdiste', T_SIZE*2, T_COLOR, WIDTH//2, HEIGHT//2)
			self.display_text('Presina r para comenzar de nuevo', T_SIZE, T_COLOR, WIDTH//2, 50)
	
	#Dibujar:
	#Fondo, textos, actualizar pantalla.
	def draw(self):
		self.surface.blit(self.background, (0,0))
		self.sprites.draw(self.surface)
		self.draw_text()

		#flip es como update, pero para toda la pantalla.
		#con update, pueden actualizar zonas concretas de la pantalla.
		pygame.display.flip()
		
	def update(self):
		if self.player.playing:
		
			#choque con paredes.
			wall = self.player.collide_with(self.walls)
			if wall:
				#Choque por abajo con una pared (bottom).
				if self.player.collide_bottom(wall):
					self.player.skid(wall)
				else:
					self.stop()
			else:
				#Si no se cruza con una pared.
				#surfing es falso.
				self.player.surfing = False
				
			#Choque con monedas.
			coin = self.player.collide_with(self.coins)
			if coin:
				#Añade el score, y destruye
				#el sprite(objeto) moneda.
				self.score += 1
				coin.kill()
				
				self.sounds['coin'].play()
			
			#Ejecuta el metodo update.
			#A cada sprite.
			self.sprites.update()
			
			#Valida si esta sobre la plataforma.
			self.player.validate_platform(self.platform)
			
			#Eliminar elementos no usados.
			self.free_up([self.walls, self.coins])
			
			#Generamos nuevos elementos.
			self.generate_walls()
			
	#Borrado de elementos no usados.
	def free_up(self, lst_elements):
		for elements in lst_elements:
			for element in elements:
				#Si el elemento a salido de la
				#pantalla, lo destruye.
				if element.rect.right < 0:
					element.kill()
					
	def stop(self):
		self.sounds['stop'].play()
		
		#Detenemos al jugador.
		#self.player.playing pasa a ser falso.
		#y automaticamente se detienen las paredes y las monedas
		self.player.stop()
		
	def menu(self):
		#Mensaje de menu.
		self.surface.fill(GREEN_LIGHT)
		self.display_text('Presiona una tecla para comenzar...', T_SIZE, T_COLOR, WIDTH//2, 10)
		
		#Plasmar el fondo y el texto.
		pygame.display.flip()
		
		#Generar una espera antes de empezar.
		self.wait()
		
	def wait(self):
		wait = True
		
		while wait:
			for event in pygame.event.get():
				self.finish_query(event)
					
				if event.type == pygame.KEYUP:
					wait = False
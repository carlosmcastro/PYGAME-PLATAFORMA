#Importamos los modulos basicos.
import os, pygame

#Directorios y recursos.
djoin = os.path.join 
DIR_BASE = os.path.dirname(__file__)
DIR_IMGS = djoin(DIR_BASE, 'sources/sprites')
DIR_SOUNDS = djoin(DIR_BASE, 'sources/sounds')

#Imagenes.
BACKGROUND = djoin(DIR_IMGS, 'background.png')
PLAYER_SRC =  {
		'base': djoin(DIR_IMGS, 'player_base.png'),
		'jump' : djoin(DIR_IMGS, 'player_jump.png'),
		'fall' : djoin(DIR_IMGS, 'player_fall.png'),
		'walk' : djoin(DIR_IMGS, 'player_walk.png')
	}
WALL_SRC =  djoin(DIR_IMGS, 'wall.png')
COIN_SRC =  djoin(DIR_IMGS, 'coin.png')

#Sonidos.
LOSE_SRC = djoin(DIR_SOUNDS, 'lose.wav')
COIN_SOUND_SRC = djoin(DIR_SOUNDS, 'coin.wav')
VOL_SOUND = .1

#Archivo con las constantes del juego.

#DIMENSIONES Y ENTORNO
WIDTH = 800
HEIGHT = 400
ALT_PLATFORM = 40
DIM_PLATFORM = (WIDTH, ALT_PLATFORM)
FLY_PLAYER = 200 #CUANDO ES TIRADO AL INICIO.
TITLE = 'Primer Juego c:'

#Espaciado y generación de elementos.
INC_WALL = WIDTH+100 #Distanciamiento de la pared al inicio.
INC_COIN = WIDTH+80 #Distanciamiento de la moneda al inicio.
ESP_WALL = 200 #Espaciado entre paredes.
ESP_COIN = 120 #Espaciado entre paredes.
ALT_COIN = 100 #Altura de aparición de las monedas.

#FRAMES POR SEGUNDO
FPS = 60 #FRAMES POR SEGUNDO.
PLAYER_WALK = 100

#COLORES.
WHITE = (255, 255, 255)
BLACK = (0,0,0)
GRAY_A = (170, 170, 170)
ROJO_CARAMELO = (154, 65, 46)
GREEN = (69, 184, 61)
GREEN_LIGHT = (61, 174, 87)

#Textos.
FONT = 'Arial'
TEXT_POSY = 20
T_SIZE = 36
T_COLOR = WHITE

#FISICAS
PLAYER_GRAV = 1.2
SPEED = 5
CAP_SALTO = -23 #CAPACIDAD DE SALTO

#CANTIDAD ELEMENTOS
MAX_WALLS = 10
MAX_COINS = 10
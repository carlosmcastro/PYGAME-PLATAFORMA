# PYGAME-PLATAFORMA
Juego muy básico en pygame.

Inspirado en https://github.com/codigofacilito/pygame/tree/master/project
de Codigo Facilito.

Pero con algunas modificaciones:
  *Puede saltar sobre una pared, además de deslizar.
  *Animación de caminar.
  *Animación al caer de un salto.
  *Mayor uso de constantes, para directorios, imagenes y sonidos.
  *metodo general de Player para configurar superficies sin hundirse.
  *Volumen sonido al 10% (con una constante para modificarlo)
  *metodo general de Game para la generación de Coins y Walls.
  *Eliminación del atributo self.playing en Game, en su lugar se usa, self.player.playing.
  *Simplificación del del metodo stop en Game:
    --Eliminación de stop_elements (los elementos se detienen al ejecutar self.player.stop()
      por el uso de self.player.playing)
  *Clase general de la que heredan Coin y Wall, por metodos comunes.
  *Sonidos generados en un metodo, para mantener el orden.
  
El codigo esta completamente comentado y puede que lo adapte con el tiempo para probar alguna idea sencilla.    

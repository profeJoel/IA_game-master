import pygame, random
from pygame.locals import *

pygame.init()

ANCHO_VENTANA = 800
ALTO_VENTANA = 600
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("El juego mas inteligente del planeta!!!")
tiempo = pygame.time.Clock()

# colores RGB
NEGRO = (0,0,0)
GRIS = (200,200,200)
BLANCO = (255,255,255)
ROJO = (255,0,0)
AMARILLO = (255,255,0)
VERDE = (0,255,0)

#Atributos del auto
auto_imagen = pygame.image.load("racecar.png")
auto_velocidad = 10
auto_ancho = auto_imagen.get_width()
auto_alto = auto_imagen.get_height()
auto_x = (ANCHO_VENTANA - auto_ancho) // 2
auto_y = ALTO_VENTANA - auto_alto

#Atributos de la ventana
fondo = pygame.image.load("fondo.png")
sonido_choque = pygame.mixer.Sound("snd/choque.wav")
sonido_caida = pygame.mixer.Sound("snd/caida.wav")
musica_fondo = pygame.mixer.music.load("snd/clearday.mp3")
pygame.mixer.music.play(-1)

#textos de puntos
texto_puntos = pygame.font.SysFont("comicsans", 30, True)
puntaje = 0

# variables de bloques
bloque_velocidad = 10
bloque_alto = 100
bloque_ancho = 100
bloque_x = random.randint(0,ANCHO_VENTANA - bloque_ancho)
bloque_y = -bloque_alto
bloque_color = random.choice([ROJO,AMARILLO,VERDE])

# IA
IA_vigia = 200

esta_jugando = True
while esta_jugando:
    tiempo.tick(50)
    #Evento de cierre de ventana
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()

    # movimiento del auto
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and auto_x - auto_velocidad >= 0:
        auto_x -= auto_velocidad
    if teclas[pygame.K_RIGHT] and auto_x + auto_ancho + auto_velocidad < ANCHO_VENTANA:
        auto_x += auto_velocidad

    # Movimiento de bloques
    bloque_y += bloque_velocidad
    if bloque_y > ALTO_VENTANA:
        bloque_y = -bloque_alto
        bloque_x = random.randint(0,ANCHO_VENTANA - bloque_ancho)
        bloque_velocidad += 1
        bloque_ancho = random.randint(0,ANCHO_VENTANA//3)
        bloque_color = random.choice([ROJO,AMARILLO,VERDE])
        sonido_caida.play()

    #colisiones
    if bloque_y + bloque_alto > auto_y and auto_x + auto_ancho > bloque_x and auto_x < bloque_x + bloque_ancho:
        if bloque_color == ROJO:
            esta_jugando = False
            auto_imagen = pygame.image.load("explode.png")
            sonido_choque.play()
        elif bloque_color == AMARILLO:
            puntaje = 0
        elif bloque_color == VERDE:
            puntaje += 5

    # IA
    if bloque_y + bloque_alto > auto_y - IA_vigia and auto_x + auto_ancho > bloque_x and auto_x < bloque_x + bloque_ancho:
        if bloque_color == ROJO or bloque_color == AMARILLO:
            if auto_x - bloque_ancho > 0:
                auto_x -= bloque_ancho
            elif auto_x + auto_ancho + bloque_ancho < ANCHO_VENTANA:
                auto_x += bloque_ancho
    # Secci??n de caza de bloques verdes
    if bloque_y + bloque_alto > auto_y - IA_vigia:
        if bloque_color == VERDE:
            auto_x += bloque_x - auto_x

    #ventana.fill(VERDE)
    ventana.blit(fondo, (0,0))
    ventana.blit(auto_imagen, (auto_x,auto_y))
    pygame.draw.rect(ventana, bloque_color, (bloque_x, bloque_y, bloque_ancho, bloque_alto))
    puntos = texto_puntos.render("Puntaje: " + str(puntaje), 1, NEGRO)
    ventana.blit(puntos, (350,10))
    pygame.display.update()

#pantalla Final
pygame.time.delay(2000)
ventana.fill(NEGRO)
puntos = texto_puntos.render("Puntaje Total = " + str(puntaje), 1, BLANCO)
ventana.blit(puntos, (ANCHO_VENTANA//2 - puntos.get_width()//2, ALTO_VENTANA//2))
pygame.display.update()

pygame.time.delay(5000)
pygame.quit()
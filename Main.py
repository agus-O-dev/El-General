#!/usr/bin/env python
# coding: utf-8

# In[2]:


import math
import random
import pygame
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

background = pygame.image.load('villa.png').convert_alpha()


running=True
# Sound
mixer.music.load("Micky Vainilla - Basta de Amargura.wav")
mixer.music.set_volume(0.7)
mixer.music.play(-1)

pygame.display.set_caption("El General")
icon = pygame.image.load('El General Icon.png')
pygame.display.set_icon(icon)

#Videla
VidelaImg = pygame.image.load('Videla.png').convert_alpha()
VidelaX = 340
VidelaY = 520
VidelaX_change= 0
VidelaY_change= 0

# Subversivos
Negro_CabezaImg = []
Negro_CabezaX = []
Negro_CabezaY = []
Negro_CabezaX_change = []
Negro_CabezaY_change = []
num_of_Negros_Cabeza = 6

for i in range(num_of_Negros_Cabeza):
    Negro_CabezaImg.append(pygame.image.load('Negro_Cabeza.png').convert_alpha())
    Negro_CabezaX.append(random.randint(0, 736))
    Negro_CabezaY.append(random.randint(50, 150))
    Negro_CabezaX_change.append(0.1)
    Negro_CabezaY_change.append(40)

def Videla(x,y):
    screen.blit(VidelaImg,(x,y))
    
def Negr0_Cabeza(x, y, i):
    screen.blit(Negro_CabezaImg[i], (x, y))
    
# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)
    
def game_over_text():
    over_text = over_font.render("UNA COSA CAPO", True, (255, 0, 0))
    screen.blit(over_text, (110, 250))
    
# Falcon

# Ready - You can't see the Falcon on the screen
# Dissapear - The Falcon is currently moving

FalconImg = pygame.image.load('Falcon.png').convert_alpha()
FalconX = 0
FalconY = 350
FalconX_change = 0
FalconY_change = 2
Falcon_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

def show_score(x, y):
    score = font.render("Subversivos : " + str(score_value), True, (255, 0, 0))
    screen.blit(score, (x, y))

def Dissapear(x, y):
    global Falcon_state
    Falcon_state = "fire"
    screen.blit(FalconImg, (x + 16, y + 10))
    
def isCollision(SubversivoX, SubversivoY, FalconX, FalconY):
    distance = math.sqrt(math.pow(SubversivoX - FalconX, 2) + (math.pow(SubversivoY - FalconY, 2)))
    if distance < 27:
        return True
    else:
        return False

while running:
    
    screen.fill((0,0,0)) 
    
    screen.blit(background, (0,0))
    
    VidelaX += VidelaX_change
    if VidelaX <= 0:
        VidelaX = 0
    elif VidelaX >= 695:
        VidelaX = 695
        
    # Negro Movement
    for i in range(num_of_Negros_Cabeza):

        # Game Over
        if Negro_CabezaY[i] > 420:
            for j in range(num_of_Negros_Cabeza):
                Negro_CabezaY[j] = 2000
            game_over_text()
            pygame.mixer.stop()
            break

        Negro_CabezaX[i] += Negro_CabezaX_change[i]
        if Negro_CabezaX[i] <= 0:
            Negro_CabezaX_change[i] = 0.3
            Negro_CabezaY[i] += Negro_CabezaY_change[i]
        elif Negro_CabezaX[i] >= 720:
            Negro_CabezaX_change[i] = -0.3
            Negro_CabezaY[i] += Negro_CabezaY_change[i]

        # Desaparición
        collision = isCollision(Negro_CabezaX[i], Negro_CabezaY[i], FalconX, FalconY)
        if collision:
            DesaparecidoSound = mixer.Sound("Desaparecido.wav")
            DesaparecidoSound.play()
            FalconY = 480
            Falcon_state = "ready"
            score_value += 1
            Negro_CabezaX[i] = random.randint(0, 736)
            Negro_CabezaY[i] = random.randint(50, 150)

        Negr0_Cabeza(Negro_CabezaX[i], Negro_CabezaY[i], i)
        
    # Falcon Movement
    if FalconY <= 0:
        FalconY = 480
        Falcon_state = "ready"

    if Falcon_state is "fire":
        Dissapear(FalconX, FalconY)
        FalconY -= FalconY_change
    
    Videla(VidelaX,VidelaY)
    show_score(textX, testY)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
            pygame.quit() 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                VidelaX_change = -0.7
            if event.key == pygame.K_RIGHT:
                VidelaX_change = 0.7
            if event.key == pygame.K_SPACE:
                 if Falcon_state is "ready":
                    FalconSound = mixer.Sound("falcon.wav")
                    FalconSound.set_volume(0.3)
                    FalconSound.play()
                    # Get the current x coordinate of Videla
                    FalconX = VidelaX
                    Dissapear(FalconX, FalconY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                VidelaX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                VidelaY_change = 0


# In[ ]:





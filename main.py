import math
import pygame
import random

pygame.init()
scr = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Space Invader')
icon = pygame.image.load('ship.png')
pygame.display.set_icon(icon)

bg= pygame.image.load('bg.jpg')
bg= pygame.transform.scale(bg, (800,600))

shipimg = pygame.image.load('ship.png')
shipimg = pygame.transform.scale(shipimg, (40, 40))
shipx = 400
shipy = 450
shipx_change = 0

def ship(shipx, shipy):
    scr.blit(shipimg, (shipx, shipy))

enemyimg=[]
enemyx=[]
enemyy=[]
enemyx_change=[]
enemyy_change=[]
num_e=6

for x in range(num_e):
    temp_img= pygame.image.load('enemy.png')
    enemyimg.append(pygame.transform.scale(temp_img, (75, 75)))
    enemyx.append(random.randint(10, 750))
    enemyy.append(random.randint(50,150))
    enemyx_change.append(0.7)
    enemyy_change.append(0)

def enemy(enemyx, enemyy, i):
    scr.blit(enemyimg[i], (enemyx, enemyy))

missile= pygame.image.load('missile.png')
missile= pygame.transform.scale(missile, (40,40))
missilex= 0
missiley= 450
missiley_change=-3
missile_state='ready'

def fire(missilex, missiley):
    global missile_state
    missile_state='fire'
    scr.blit(missile, (missilex, missiley-20))

def isCollision(enemyx, enemyy, missilex, missiley):
    d= math.sqrt(math.pow(enemyx-missilex,2)+math.pow(enemyy-missiley,2))
    if d<27:
        return True
    else:
        return False

def game_over():
    font2= pygame.font.Font('freesansbold.ttf', 72)
    text= font2.render('Game Over', True, (255,255,255))
    scr.blit(text, (210,200))

score_val=0
font= pygame.font.Font('freesansbold.ttf', 32)
def show_score():
    score= font.render('Score: ' + str(score_val), True, (255,255,255))
    scr.blit(score, (600,40))
run = True
while run:
    scr.fill((0, 0, 0))
    scr.blit(bg, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                shipx_change = -2
            if event.key == pygame.K_RIGHT:
                shipx_change = 2
            if event.key == pygame.K_SPACE:
                if missile_state=='ready':
                    missilex = shipx
                    missile_state = 'fire' 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                shipx_change = 0
    
    if missile_state=='fire':
        if missiley>=0:
            missiley += missiley_change
            fire(missilex, missiley)
        else:
            missiley=shipy
            missile_state='ready'
    
    if shipx <= 10:
        shipx = 10
    elif shipx >= 750:
        shipx = 750
    shipx += shipx_change
    ship(shipx, shipy)
    for i in range(num_e):
        if enemyy[i]>= 400:
            for j in range(num_e):
                enemyy[j]=2000
            game_over()
            break
        if enemyx[i] <= 10:
            enemyx_change[i] = 0.7
            enemyy_change[i]=40
        elif enemyx[i] >= 750:
            enemyx_change[i] = -0.7
            enemyy_change[i]=40
        enemyx[i] += enemyx_change[i]
        enemyy[i] += enemyy_change[i]
        enemyy_change[i]=0
        if isCollision(enemyx[i], enemyy[i], missilex, missiley) and missile_state=='fire':
            missiley=450
            missile_state='ready'
            score_val+=1
            print(score_val)
            enemyx[i]=random.randint(10,750)
            enemyy[i]=random.randint(50,150)
        enemy(enemyx[i], enemyy[i], i)

    show_score()
    pygame.display.update()

pygame.quit()

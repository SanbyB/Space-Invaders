import pygame
import math
import random

# Initializes pygame
pygame.init()

# Creates the window for the pygame
(width, height) = (800, 600)
screen = pygame.display.set_mode((width, height))

# backgroud colour
background_colour = (20, 0, 50)

# Image of the player
playerIm = pygame.image.load('space invaders ship.png')

# Image of the bullet
bulletIM = pygame.image.load('bullet.png')

# sets the name of the window and the icon
pygame.display.set_caption('Space Invaders')
pygame.display.set_icon(playerIm)

# start x position of the player
playerx = width // 2

# height of the player (remains constant)
playery = height - 100

# starting movement of the player is 0
playerx_move = 0

# bullet
bullet_state = 'ready'
bullety = playery
bullety_move = 2
bulletx = playerx

number_of_enemies = 6

# Image of the enemy
enemyIM = []

# start x and y position of the enemy
enemyx = []  # needs to be 8 or greater and less than 'width-72' as that is the boundary set for the enemy
enemyy = []

# enemy movenent
enemyx_move = []
enemyy_move = []

for i in range(number_of_enemies):
    enemyIM.append(pygame.image.load('space invader.png'))
    enemyx.append(random.randint(9, width - 73))
    enemyy.append(random.randint(9, height // 3))
    enemyx_move.append(random.randint(1, 8) * 0.2)
    enemyy_move.append(32)


# definition to draw the enemy requires x and y position
def enemy(x, y, j):
    screen.blit(enemyIM[j], (x, y))


# definition to draw the player requires the x position of the player
def player(x):
    screen.blit(playerIm, (x, playery))


# definition to draw the bullet, when 'ready' the bullet is not drawn,
# when 'fire' the bullet is drawn moving up from the ship
def bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletIM, (x + 24, y - 14))


# definition of the collision between bullets and enemies
def collision(bulletx, bullety, enx, eny):
    dist = math.sqrt((bulletx - enx) ** 2 + (bullety - eny) ** 2)
    if dist < 45:
        return True
    else:
        return False


# Score
score_val = 0

font = pygame.font.Font('freesansbold.ttf', 32)


def score(score):
    scr = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(scr, (10, 10))


# GAMEOVER

font1 = pygame.font.Font('freesansbold.ttf', 72)


def gameover():
    GO = font1.render("GAMEOVER", True, (255, 255, 255))
    screen.blit(GO, (200, height // 2-50))


'''
Sets up the game so it remains open, any code we want to run 
while the game is running should be in this 'while running' loop.
'''

running = True
while running:

    # get the inputs from the keyboard, mouse, and other inputs from the window
    for event in pygame.event.get():

        '''
        Allows the window to remain open with the infinite while loop until the
        close button is pressed and the window is closed. 
        '''

        if event.type == pygame.QUIT:
            running = False

        '''
        Bullet movement, written here as it needs to be in the 'for event in...' section
        and the player movement follows on in the code, some of what is written
        will refer to later parts of the code, however it is just the position of the player
        '''

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bulletx = playerx
                    bullet(bulletx, bullety)

        '''
        Allows the player to move, when the left or right key is pressed
        the player will move in that direction respectively, also when the
        key is released the player will no longer move
        '''

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerx_move = 0
            if event.key == pygame.K_RIGHT:
                playerx_move = 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_move = -2
            if event.key == pygame.K_RIGHT:
                playerx_move = 2

    playerx += playerx_move

    '''
    Assigns a boundary that the player has to stay in
    so that it doesn't leave the screen
    '''

    if playerx <= 8:
        playerx = 8

    if playerx >= width - 72:
        playerx = width - 72

    '''
    Drawing the game
    '''

    # sets the screen background (must be drawn first otherwise it will draw over everything else)
    screen.fill(background_colour)

    # draws the player
    player(playerx)

    for j in range(number_of_enemies):

        # collision
        Hit = collision(bulletx, bullety, enemyx[j], enemyy[j])
        if Hit:
            bullet_state = 'ready'
            bullety = playery
            enemyx[j] = random.randint(9,
                                       width - 73)  # needs to be 8 or greater and less than 'width-72' as that is the boundary set for the enemy
            enemyy[j] = random.randint(9, height // 3)
            enemyx_move[j] = random.randint(1, 10) * 0.2
            score_val += 1

        '''
        Enemy movement
        '''

        enemyx[j] += enemyx_move[j]

        if enemyx[j] <= 8:
            enemyx_move[j] = -enemyx_move[j]
            enemyy[j] += enemyy_move[j]

        if enemyx[j] >= width - 72:
            enemyx_move[j] = -enemyx_move[j]
            enemyy[j] += enemyy_move[j]

        # GAMEOVER
        if enemyy[j] >= playery - 65:
            for i in range(number_of_enemies):
                enemyy[i] = height + 100
                enemyx_move[i] = 0
                gameover()

        # draws the enemy
        enemy(enemyx[j], enemyy[j], j)

    '''
    Bullet movement
    '''

    if bullet_state == 'fire':
        bullet(bulletx, bullety)
        bullety -= bullety_move

    # stops the drawing of the bullet once it has left the screen so as to save memory
    if bullety < 0:
        bullet_state = 'ready'
        bullety = playery

    # displays the score
    score(score_val)

    # updates the game
    pygame.display.update()

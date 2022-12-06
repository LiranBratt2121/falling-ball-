import random
import sys
import time

import pygame

# Global Variables
COLOR = (255, 100, 98)
SURFACE_COLOR = (167, 255, 100)
WIDTH = 500
HEIGHT = 500
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (0, 0, 0)

global game_start


# Object class
class Platform(pygame.sprite.Sprite):
    def __init__(self, color, height, width):
        super().__init__()
        # getting the values of the player
        self.image = pygame.Surface([width, height])
        self.image.fill(SURFACE_COLOR)
        self.image.set_colorkey(COLOR)
        # drawing the shape of the player
        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, width, height))
        # hitbox
        self.rect = self.image.get_rect()

    # movement methods
    def moveRight(self, pixels):
        self.rect.x += pixels

    def moveLeft(self, pixels):
        self.rect.x -= pixels


class Ball(pygame.sprite.Sprite):
    def __init__(self, color, height, width):
        super().__init__()
        # getting the values of the ball
        self.image = pygame.Surface([width, height])
        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, width, height))
        self.rect = self.image.get_rect()

    # movement methods
    def moveDown(self, pixels):
        self.rect.y += pixels

    def resetPos(self):
        self.rect.y = 50
        self.rect.x = random.randint(0, 500)


# 'main' method
def run():
    pygame.init()
    # global method variables
    global game_start, count
    game_start = False
    count = 0
    # setting up the screen
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("ball capture game")
    # creating the game sprites & text
    sprites = pygame.sprite.Group()
    playerCar = Platform(RED, 30, 150)
    ball = Ball(YELLOW, 30, 30)
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('start game - ENTER', True, WHITE)
    textRect = text.get_rect()
    # setting up the locations on the screen
    textRect.center = (240, 300)
    playerCar.rect.x = 160
    playerCar.rect.y = 450
    ball.rect.x = 220
    ball.rect.y = 450 - 30
    # creating a sprite group to hold the sprites
    sprites.add(playerCar, ball)
    exit_game = True
    # creating a clock to cap the fps
    clock = pygame.time.Clock()

    while exit_game:
        # ball movement
        if game_start:
            ball.moveDown(2 + count / 2)
        # collision detection for win & lose condition & updates
        if pygame.sprite.collide_mask(ball, playerCar):
            ball.resetPos()
            count += 1
            text = font.render('score: ' + str(count), True, WHITE)
        # lose condition
        if ball.rect.y > playerCar.rect.y:
            font = pygame.font.Font('freesansbold.ttf', 15)
            textRect.center = (200, 200)
            text = font.render('you lose, \'press enter\' to play again, \'other keys\' to leave', True, WHITE)
            # displaying the text
            pygame.event.clear()
            screen.fill(SURFACE_COLOR)
            screen.blit(text, textRect)
            sprites.draw(screen)
            pygame.display.flip()
            # replay condition
            time.sleep(1)
            event = pygame.event.wait()
            if event.key == pygame.K_RETURN:
                count = 0
                ball.resetPos()
                font = pygame.font.Font('freesansbold.ttf', 20)
                text = font.render('score: ' + str(count), True, WHITE)
                textRect.center = (160, 20)
            else:
                sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = False
            # key inputs
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    exit_game = False
                if not game_start:
                    if event.key == pygame.K_RETURN:
                        ball.resetPos()
                        font = pygame.font.Font('freesansbold.ttf', 20)
                        text = font.render('score: ' + str(count), True, WHITE)
                        textRect.center = (160, 20)

                        game_start = True
        # player movements
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            playerCar.moveLeft(10)
        if keys[pygame.K_RIGHT]:
            playerCar.moveRight(10)
        # updating the screen & sprites at every frame
        sprites.update()
        screen.fill(SURFACE_COLOR)
        screen.blit(text, textRect)
        sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

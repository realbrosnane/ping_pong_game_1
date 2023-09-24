from pygame import *
import random
import pygame.font

#parent class for other sprites
class GameSprite(sprite.Sprite):
    #class constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Call for the class (Sprite) constructor:
        super().__init__() #sprite.Sprite.__init__(self)
 
        #every sprite must store the image property
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        #every sprite must have the rect property – the rectangle it is fitted in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    #method drawing the character on the window
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#child class for player
class Paddle(GameSprite):
    #method to control the sprite with arrow keys
    def update_right(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 150:
            self.rect.y += self.speed
    def update_left(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 150:
            self.rect.y += self.speed

BLUE = (200, 255, 255)
win_width = 600
win_height = 500
window = display.set_mode((win_width, win_height))
window.fill(BLUE)
#we need the following images
img_paddle1 ="oo.jpg"
img_paddle2 = "pink.jpg"
img_ball = "ball.jpg"

background = Surface((win_width, win_height))
background.fill((0, 128, 0))  # Set green as background color

# Draw court boundaries
pygame.draw.rect(background, (255, 255, 255), (0, 0, win_width, 10))  # Top boundary
pygame.draw.rect(background, (255, 255, 255), (0, win_height - 10, win_width, 10))  # Bottom boundary

# Draw center line
pygame.draw.line(background, (255, 255, 255), (win_width // 2, 0), (win_width // 2, win_height), 2)


#window properties


#create sprites
paddle1 = Paddle(img_paddle1, 20, 200, 30, 150, 5)
paddle2 = Paddle(img_paddle2, 520, 200, 30, 150, 5)
ball = GameSprite(img_ball, 330, 200, 50, 50, 50)


#game loop
game = True #exit with "close window"
finish = False #end with win/lose
FPS = 60
clock = time.Clock()

pygame.font.init()
font = pygame.font.Font(None, 35)
lose1 = font.render('BLUE PLAYER LOSE!', True, (180, 0, 0))
lose2 = font.render('RED PLAYER LOSE!', True, (180, 0, 0))

BLUE_SCORE = 0
RED_SCORE = 0
font_score = pygame.font.Font(None,18)
blue_board = font_score.render('BLUE: ' + str(BLUE_SCORE), True, (0, 0, 0))
red_board = font_score.render('RED: ' + str(RED_SCORE), True, (0, 0, 0))

initial_direction = random.choice([-1, 1])
speed_x = 3
speed_y = 3

while game:
    #exit when "close window" is clicked
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    #end the game when win/lose
    if finish != True:
        window.fill(BLUE)
        paddle1.update_left()
        paddle2.update_right()
        ball.rect.x += speed_x
        ball.rect.y += speed_y
        window.blit(blue_board, (10, 10))
        window.blit(red_board, (win_width - 80, 10))

        
        if sprite.collide_rect(paddle1, ball) and speed_x < 0:
            BLUE_SCORE += 1
            blue_board = font_score.render("BLUE: " + str(BLUE_SCORE), True, (0,0,0))
            speed_x *= -1
            speed_y *= 1

        if sprite.collide_rect(paddle2, ball) and speed_x > 0:
            RED_SCORE += 1
            red_board = font_score.render("RED: " + str(RED_SCORE), True, (0,0,0))
            speed_x *= -1
            speed_y *= 1
        #ball bounces when hit the up or bottom wall
        if ball.rect.y <= 10 or ball.rect.y >= win_height - 100:
            speed_y *= -1

        #if ball flies behind this paddle, display loss condition for player left
        if ball.rect.x < 0:
            finish = False
            game_over = True
            window.blit(lose1, (200, 200))

        #if the ball flies behind this paddle, display loss condition for player right
        if ball.rect.x > win_width:
            finish = False
            game_over = True
            window.blit(lose2, (200, 200))

        paddle1.reset()
        paddle2.reset()
        ball.reset()

        

    display.update()
    clock.tick(FPS)

import sys
import pygame
import random
import math
import colorsys

pygame.init()
WIDTH, HEIGHT = 800, 600
dimensions = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(dimensions)
trail_screen = pygame.Surface(dimensions, pygame.SRCALPHA)

#Const
BLACK = (0, 0, 0)

N_BALLS = 20
RADIUS = 5
SPEED = 10

clock = pygame.time.Clock()

def random_color():
    h = random.random()
    s = 1.0
    v = 1.0
    r, g, b = colorsys.hsv_to_rgb(h, s, v)

    return(int(r * 255), int(g * 255), int(b * 255))

def random_angle():
    return random.uniform(0, 2 * math.pi)

def random_position():
    x = random.randint(RADIUS, WIDTH - RADIUS)
    y = random.randint(RADIUS, HEIGHT - RADIUS)
    return (x, y)

class Ball:
    def __init__(self):
        self.x, self.y = random_position()
        self.angle = random_angle()

        self.x_trail = self.x
        self.y_trail = self.y

        self.x_speed = math.cos(self.angle) * SPEED
        self.y_speed = math.sin(self.angle) * SPEED
        self.color = random_color()

    def get_coordinate(self):
        return (self.x, self.y)
    
    def update(self):
        self.x_trail = self.x
        self.y_trail = self.y

        self.x += self.x_speed
        self.y += self.y_speed

        if self.x + RADIUS >= WIDTH:
            self.x = WIDTH - RADIUS
            self.x_speed *= -1
        elif self.x - RADIUS <= 0:
            self.x = RADIUS
            self.x_speed *= -1
            
        if self.y + RADIUS >= HEIGHT:
            self.y = HEIGHT - RADIUS
            self.y_speed *= -1
        elif self.y - RADIUS <= 0:
            self.y = RADIUS
            self.y_speed *= -1
    
    def draw(self):
        pygame.draw.circle(screen, self.color, self.get_coordinate(), RADIUS)
        pygame.draw.line(trail_screen, self.color, (self.x_trail, self.y_trail),
                          self.get_coordinate(), RADIUS)
    

balls = [Ball() for _ in range(N_BALLS)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill(BLACK)
    screen.blit(trail_screen, (0, 0))

    for ball in balls:
        ball.update()
        ball.draw()

    pygame.display.flip()
    clock.tick(60)

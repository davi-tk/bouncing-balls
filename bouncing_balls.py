import sys
import pygame
import random
import math
import colorsys

pygame.init()
WIDTH, HEIGHT = 800, 600
dimensions = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(dimensions)
trail_surface = pygame.Surface(dimensions, pygame.SRCALPHA)

#Const
BLACK = (0, 0, 0)

N_BALLS = 20
RADIUS = 5
SPEED = 5

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
        pygame.draw.circle(screen, self.color, self.get_coordinate(), RADIUS, width=2)
        pygame.draw.line(trail_surface, self.color, (self.x_trail, self.y_trail),
                          self.get_coordinate(), RADIUS)

def is_colliding(ball1 : Ball, ball2 : Ball):
    dx = ball1.x - ball2.x
    dy = ball1.y - ball2.y
    distance = math.hypot(dx, dy)
    
    return distance <= RADIUS * 2

def resolve_collision(ball1: Ball, ball2: Ball):
    dx = ball1.x - ball2.x
    dy = ball1.y - ball2.y
    distance = math.hypot(dx, dy)

    if distance == 0 : 
        return

    nx = dx / distance
    ny = dy / distance
    overlap = 2 * RADIUS - distance
    if overlap > 0:


        ball1.x += nx * (overlap / 2)
        ball1.y += ny * (overlap / 2)
        ball2.x -= nx * (overlap / 2)
        ball2.y -= ny * (overlap / 2)

    dvx = ball1.x_speed - ball2.x_speed
    dvy = ball1.y_speed - ball2.y_speed

    dot = dvx * nx + dvy * ny

    if dot > 0:
        return

    ball1.x_speed -= dot * nx
    ball1.y_speed -= dot * ny
    ball2.x_speed += dot * nx
    ball2.y_speed += dot * ny
        


balls = [Ball() for _ in range(N_BALLS)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill(BLACK)
    trail_surface.fill((0, 0, 0, 5), special_flags=pygame.BLEND_RGBA_SUB)
    screen.blit(trail_surface, (0, 0))

    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            if is_colliding(balls[i], balls[j]):
                resolve_collision(balls[i], balls[j])

    for ball in balls:
        ball.update()
        ball.draw()
    

    pygame.display.flip()
    clock.tick(60)

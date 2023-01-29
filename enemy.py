import pygame
import random
import math
from player import Player


class Enemy():
    #image = pygame.image.load("img.png")

    def __init__(self, game, x, y, color):
        super().__init__()
        #self.image = Enemy.image
        #self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.color = color
        self.speed = 0.3
        self.game = game
        self.enemy_size = 10

    def wall_check(self, x, y):
        if (x, y, 1) not in self.game.map.world_map:
            return x, y

    def collision_check(self, dx, dy):
        scale = self.enemy_size / self.game.delta_time
        #print(int(self.x / 50 + dx * scale), int(self.y / 50))
        print(self.wall_check(int(self.x / 50 + dx * 0.2), int(self.y / 50)),
              self.wall_check(int(self.x / 50), int(self.y / 50 + dy * 0.2)), sep="|||")
        if self.wall_check(int(self.x / 50 + dx * 0.2), int(self.y / 50)):
            self.x += dx
        if self.wall_check(int(self.x / 50), int(self.y / 50 + dy * 0.2)):
            self.y += dy

    def move(self):
        next_x, next_y = self.game.kickguy.cords()
        self.x_cor = self.x
        self.y_cor = self.y
        next_x *= 50
        next_y *= 50
        if next_y > self.y_cor:
            if next_x == self.x_cor:
                self.angle = 1.570796325
            elif next_x < self.x_cor:
                self.angle = 3.14 + math.atan((next_y - self.y_cor) / (next_x - self.x_cor))
            else:
                self.angle = math.atan((next_y - self.y_cor) / (next_x - self.x_cor))
        else:
            if next_x == self.x_cor:
                self.angle = 4.712388975
            elif next_x < self.x_cor:
                self.angle = 3.14 + math.atan((next_y - self.y_cor) / (next_x - self.x_cor))
            else:
                self.angle = math.atan((next_y - self.y_cor) / (next_x - self.x_cor))

        self.angle %= math.tau
        dx = math.cos(self.angle) * self.speed
        dy = math.sin(self.angle) * self.speed
        self.collision_check(dx * 5, dy * 5)

    def update(self):
        self.move()

    def draw(self):
        pygame.draw.circle(self.game.screen, self.color, (self.x, self.y), 10)

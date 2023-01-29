import pygame
import random
import math
from player import Player


class Enemy(pygame.sprite.Sprite):
    image = pygame.image.load("img.png")

    def __init__(self, game):
        super().__init__()
        self.image = Enemy.image
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 300
        self.speed = 0.5
        self.game = game

    def wall_check(self, x, y):
        if (x, y, 1) not in self.game.map.world_map:
            return x, y

    def collision_check(self, dx, dy):
        if self.wall_check(int(self.rect.x + dx), int(self.rect.y)):
            self.rect.x += dx
        if self.wall_check(int(self.rect.x), int(self.rect.y + dy)):
            self.rect.y += dy

    def move(self):
        next_x, next_y = self.game.kickguy.cords()
        next_x *= 50
        next_y *= 50
        angle = math.atan2(next_y + 0.5 - self.rect.y, next_x + 0.5 - self.rect.x)
        if next_x <= self.rect.x and next_y <= self.rect.y:
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
        elif next_x >= self.rect.x and next_y >= self.rect.y:
            dx = math.cos(angle) * self.speed * -1
            dy = math.sin(angle) * self.speed * -1
        self.collision_check(dx, dy)

    def update(self):
        self.move()

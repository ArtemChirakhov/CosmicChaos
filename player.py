import math

import pygame

class player:
    def __init__(self, game):
        self.game = game
        self.x = 1.5
        self.y = 0
        self.angle = 0
        self.player_speed = 0.04
        self.angle_speed = 0.002

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx = 0
        dy = 0
        speed = self.player_speed * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            dy -= self.player_speed
        if keys[pygame.K_s]:
            dy += self.player_speed
        if keys[pygame.K_a]:
            dx -= self.player_speed
        if keys[pygame.K_d]:
            dx += self.player_speed
        self.x += dx
        self.y += dy

        if keys[pygame.K_LEFT]:
            self.angle -= self.angle_speed * self.game.delta_time
        if keys[pygame.K_RIGHT]:
            self.angle += self.angle_speed * self.game.delta_time
        self.angle %= math.tau

    def draw(self):
        pygame.draw.line(self.game.screen, 'blue', (self.x * 100, self.y * 100),
                         (self.x * 100 + 720 * math.cos(self.angle), self.y * 100 + 720 * math.sin(self.angle)), 2)
        pygame.draw.circle(self.game.screen, 'red', (self.x * 100, self.y * 100), 15)

    def update(self):
        self.movement()

    def cords(self):
        return self.x, self.y

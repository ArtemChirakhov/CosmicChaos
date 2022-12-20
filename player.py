import math

import pygame


class player:
    def __init__(self, game):
        self.game = game
        self.x = 1.5
        self.y = 1.5
        self.angle = 0
        self.player_speed = 0.004
        self.angle_speed = 0.002
        self.diagonal_speed = 0.004 * 0.70710678118

    def movement(self):
        counter = 0
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx = 0
        dy = 0
        keys = pygame.key.get_pressed()
        # исправление диагональной скорости
        if keys[pygame.K_w]:
            counter += 1
        if keys[pygame.K_s]:
            counter += 1
        if keys[pygame.K_a]:
            counter += 1
        if keys[pygame.K_d]:
            counter += 1
        if counter == 2:
            speed = self.diagonal_speed * self.game.delta_time
        else:
            speed = self.player_speed * self.game.delta_time
        # тут конец

        if keys[pygame.K_w]:
            dy -= speed
        if keys[pygame.K_s]:
            dy += speed
        if keys[pygame.K_a]:
            dx -= speed
        if keys[pygame.K_d]:
            dx += speed

        self.x += dx
        self.y += dy

        if keys[pygame.K_LEFT]:
            self.angle -= self.angle_speed * self.game.delta_time
        if keys[pygame.K_RIGHT]:
            self.angle += self.angle_speed * self.game.delta_time
        self.angle %= math.tau  # угол в модуле math считается в радианах

    def draw(self):
        pygame.draw.line(self.game.screen, 'blue', (self.x * 100, self.y * 100),
                         (self.x * 100 + 720 * math.cos(self.angle), self.y * 100 + 720 * math.sin(self.angle)), 2)
        pygame.draw.circle(self.game.screen, 'red', (self.x * 100, self.y * 100), 15)

    def update(self):
        self.movement()

    def cords(self):
        return self.x, self.y

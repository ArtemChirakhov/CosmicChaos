import math

import pygame


class player:
    def __init__(self, game):
        self.game = game
        self.x = 1.5
        self.y = 1.5
        self.kickguy_angle = 0
        self.player_speed = 0.004
        self.angle_speed = 0.002
        self.diagonal_speed = 0.004 * 0.70710678118

    def angle(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_y /= 100
        mouse_x /= 100
        if mouse_y > self.y:
            if mouse_x == self.x:
                self.kickguy_angle = 1.570796325
            elif mouse_x < self.x:
                self.kickguy_angle = 3.14 + math.atan(((mouse_y) - self.y) / ((mouse_x) - self.x))
            else:
                self.kickguy_angle = math.atan(((mouse_y) - self.y) / ((mouse_x) - self.x))
        else:
            if mouse_x == self.x:
                self.kickguy_angle = 4.712388975
            elif mouse_x < self.x:
                self.kickguy_angle = 3.14 + math.atan(((mouse_y) - self.y) / ((mouse_x) - self.x))
            else:
                self.kickguy_angle = math.atan(((mouse_y) - self.y) / ((mouse_x) - self.x))

        self.kickguy_angle %= math.tau  # угол в модуле math считается в радианах

    def movement(self):
        counter = 0
        sin_a = math.sin(self.kickguy_angle)
        cos_a = math.cos(self.kickguy_angle)
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


    def draw(self):
        pygame.draw.line(self.game.screen, 'red', (self.x * 100, self.y * 100),
                         (self.x * 100 + 720 * math.cos(self.kickguy_angle),
                          self.y * 100 + 720 * math.sin(self.kickguy_angle)), 2)
        pygame.draw.circle(self.game.screen, 'blue', (self.x * 100, self.y * 100), 15)

    def update(self):
        self.movement()
        self.angle()

    def cords(self):
        return self.x, self.y
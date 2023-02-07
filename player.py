import math

import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.og_image = pygame.image.load("Data/Kickguy.png")
        self.image = self.og_image
        self.game = game
        self.rect = self.og_image.get_rect()
        self.x = 1.5
        self.y = 1.5
        self.offset = 20
        self.rect.x = self.x * 50 - self.offset
        self.rect.y = self.y * 50 - self.offset
        self.kickguy_angle = 0
        self.player_speed = 0.004
        self.angle_speed = 0.002
        self.diagonal_speed = 0.004 * 0.70710678118
        self.player_size = 80
        self.HP = 100

    def angle(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_y /= 50
        mouse_x /= 50
        if mouse_y > self.y:
            if mouse_x == self.x:
                self.kickguy_angle = 1.570796325
            elif mouse_x < self.x:
                self.kickguy_angle = 3.14 + math.atan((mouse_y - self.y) / (mouse_x - self.x))
            else:
                self.kickguy_angle = math.atan((mouse_y - self.y) / (mouse_x - self.x))
        else:
            if mouse_x == self.x:
                self.kickguy_angle = 4.712388975
            elif mouse_x < self.x:
                self.kickguy_angle = 3.14 + math.atan((mouse_y - self.y) / (mouse_x - self.x))
            else:
                self.kickguy_angle = math.atan((mouse_y - self.y) / (mouse_x - self.x))

        self.kickguy_angle %= math.tau  # угол в модуле math считается в радианах

    def return_angle(self):
        return self.kickguy_angle

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

        self.collision_check(dx, dy)

    def wall_check(self, x, y):
        if (x, y, 1) not in self.game.map.world_map:
            return x, y

    def collision_check(self, dx, dy):
        scale = self.player_size / self.game.delta_time
        if self.wall_check(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.wall_check(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def draw(self):
        pygame.draw.line(self.game.screen, 'red', (self.x * 50, self.y * 50),
                         (self.x * 50 + 720 * math.cos(self.kickguy_angle),
                          self.y * 50 + 720 * math.sin(self.kickguy_angle)), 1)
        pygame.draw.circle(self.game.screen, 'cyan', (self.x * 50, self.y * 50), 10)

    def is_dead(self):
        if self.HP <= 0:
            return True
        return False

    def inflict_damage(self):
        self.HP -= 1

    def rot_center(self, image, rect, angle):
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image

    def update(self):
        self.is_dead()
        self.movement()
        self.rect.x = self.x * 50 - self.offset
        self.rect.y = self.y * 50 - self.offset
        self.angle()
        self.image = self.rot_center(self.og_image, self.rect, self.return_angle() * -57.2958)

    def cords(self):
        return self.x, self.y

    def tile(self):
        return int(self.x), int(self.y)

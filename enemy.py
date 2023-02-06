import pygame

from raycasting import *


class Enemy():

    def __init__(self, game, x, y, color):
        super().__init__()
        # координаты и тд.
        self.x = x
        self.y = y
        self.x_p = self.x / 50
        self.y_p = self.y / 50
        self.x_t = int(self.x_p)
        self.y_t = int(self.y_p)
        self.angle = 1
        # отображение и перемещение
        self.color = color
        self.speed = 0.4
        self.game = game
        self.enemy_size = 10
        self.in_sight = False
        # стрельба и урон
        self.DAMAGE = 50
        self.HP = 100
        self.is_dead = False

    def wall_check(self, x, y):
        if (x, y, 1) not in self.game.map.world_map:
            return x, y

    def collision_check(self, dx, dy):
        if self.wall_check(int(self.x / 50 + dx * 0.1), int(self.y / 50)):
            self.x += dx
        if self.wall_check(int(self.x / 50), int(self.y / 50 + dy * 0.1)):
            self.y += dy

    def move(self):
        next_x, next_y = self.game.player1.cords()
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

    def is_in_sight(self):  # находится ли в поле взгляда
        if self.game.player1.return_angle() - self.game.raycasting.return_half_fov() <= (
                self.angle + math.pi) % math.tau <= self.game.player1.return_angle() + \
                self.game.raycasting.return_half_fov():
            self.in_sight = True
        else:
            self.in_sight = False
        return self.in_sight

    def is_in_range(self):  # находится ли в поле взгляда
        if self.game.player1.return_angle() - self.game.weapon.return_half_fov() <= (
                self.angle + math.pi) % math.tau <= self.game.player1.return_angle() + \
                self.game.weapon.return_half_fov():
            return  True
        else:
            return False

    def ray_cast_player_npc(self):
        ############################################### Луч от врага к персонажу
        if self.game.player1.tile() == (int(self.x_t), int(self.y_t)):
            return True

        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0
        x, y = self.game.player1.cords()
        x_map, y_map = self.game.player1.tile()
        ray_angle = (self.angle + math.pi) % math.tau
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        if sin_a > 0:
            y_hor, dy = (y_map + 1, 1)
        else:
            y_hor, dy = (y_map - 0.000001, -1)

        depth_hor = (y_hor - y) / sin_a
        x_hor = x + depth_hor * cos_a
        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(MAX_DEPTH):
            tile_hor = (int(x_hor), int(y_hor), 1)
            if tile_hor == (self.x_t, self.y_t, 1):
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        if cos_a > 0:
            x_vert, dx = (x_map + 1, 1)
        else:
            x_vert, dx = (x_map - 0.000001, -1)

        depth_vert = (x_vert - x) / cos_a
        y_vert = y + depth_vert * sin_a
        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(MAX_DEPTH):
            tile_vert = (int(x_vert), int(y_vert), 1)
            if tile_vert == (self.x_t, self.y_t, 1):
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:
                wall_dist_v = depth_hor
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        # if depth_vert < depth_hor:
        #    depth = depth_vert
        # else:
        #    depth = depth_hor

        # pygame.draw.line(self.game.screen, 'white', (50 * x, 50 * y),
        #                 (50 * x + depth * 50 * cos_a, 50 * y + depth * 50 * sin_a), 3)
        # ^для дебага

        player_dist = max(player_dist_h, player_dist_v)
        npc_wall_dist = max(wall_dist_h, wall_dist_v)

        ############################################### Луч от персонажа к врагу
        if self.game.player1.tile() == (int(self.x_t), int(self.y_t)):
            return True

        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0
        x, y = self.x_p, self.y_p
        x_map, y_map = self.x_t, self.y_t
        ray_angle = self.angle
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        if sin_a > 0:
            y_hor, dy = (y_map + 1, 1)
        else:
            y_hor, dy = (y_map - 0.000001, -1)

        depth_hor = (y_hor - y) / sin_a
        x_hor = x + depth_hor * cos_a
        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(MAX_DEPTH):
            tile_hor = (int(x_hor), int(y_hor), 1)
            if tile_hor == (self.game.player1.tile()[0], self.game.player1.tile()[1], 1):
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        if cos_a > 0:
            x_vert, dx = (x_map + 1, 1)
        else:
            x_vert, dx = (x_map - 0.000001, -1)

        depth_vert = (x_vert - x) / cos_a
        y_vert = y + depth_vert * sin_a
        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(MAX_DEPTH):
            tile_vert = (int(x_vert), int(y_vert), 1)
            if tile_vert == (self.game.player1.tile()[0], self.game.player1.tile()[1], 1):
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:
                wall_dist_v = depth_hor
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        # if depth_vert < depth_hor:
        #    depth = depth_vert
        # else:
        #    depth = depth_hor

        # pygame.draw.line(self.game.screen, 'blue', (50 * x, 50 * y),
        #                 (50 * x + depth * 50 * cos_a, 50 * y + depth * 50 * sin_a), 3)
        # ^для дебага

        npc_dist = max(player_dist_h, player_dist_v)
        player_wall_dist = max(wall_dist_h, wall_dist_v)

        if (0 < player_dist <= npc_wall_dist or not npc_wall_dist) and (
                0 < npc_dist <= player_wall_dist or not player_wall_dist):
            return True
        return False
        ###############################################

    def update(self):
        if not self.is_dead:
            self.move()
            self.x_p = self.x / 50
            self.y_p = self.y / 50
            self.x_t = int(self.x_p)
            self.y_t = int(self.y_p)
            self.draw()

    def get_damage(self):
        if self.is_in_range():
            self.HP -= self.DAMAGE
            print('Hit')
        if self.HP <= 0:
            self.is_dead = True

    def draw(self):
        if self.ray_cast_player_npc() and self.is_in_sight():
            pygame.draw.circle(self.game.screen, self.color, (self.x, self.y), 10)

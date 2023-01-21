import math
import pygame

# В этом файле описана система Рейкаста
# От лица игрока пускают лучи и считают глубину до объекта при помощи математики и подсчёта пересечений с клетакми мира
# Depth измеряется в клетках

FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 2000 // 2  # 1600 - ШИРИНА ЭКРАНА
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 32


class RayCasting:
    def __init__(self, game):
        self.game = game

    def cast_ray(self):
        x, y = self.game.kickguy.cords()
        x_map, y_map = self.game.kickguy.tile()
        ray_angle = self.game.kickguy.return_angle() - HALF_FOV + 0.00001
        for ray in range(NUM_RAYS):

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
                tile_hor = int(x_hor), int(y_hor), 1
                if tile_hor in self.game.map.world_map:
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
                tile_vert = int(x_vert), int(y_vert), 1
                if tile_vert in self.game.map.world_map:
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            if depth_vert < depth_hor:
                depth = depth_vert
            else:
                depth = depth_hor

            pygame.draw.line(self.game.screen, 'white', (50 * x, 50 * y),
                             (50 * x + depth * 50 * cos_a, 50 * y + depth * 50 * sin_a), 3)

            ray_angle += DELTA_ANGLE


    def update(self):
        self.cast_ray()

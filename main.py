import sys

from blockmap import *
from enemy import Enemy
from player import *
from raycasting import *


class Game:
    FPS = 60
    RES = width, height = 1320, 720

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.RES)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.new_game()

    def new_game(self):
        self.player1 = Player(self)
        self.map = Map(self)
        self.raycasting = RayCasting(self)
        # self.enemy = Enemy(self, 300, 300, 'red')
        self.enemy1 = Enemy(self, 400, 400, 'orange')

    def update(self):
        self.player1.update()
        self.raycasting.update()
        self.enemy1.update()
        pygame.display.flip()
        self.delta_time = self.clock.tick(self.FPS)
        pygame.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.screen.fill('black')
        self.player1.draw()
        self.map.draw()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

    def run(self):
        while True:
            self.check_events()
            self.draw()
            self.update()


if __name__ == '__main__':
    game = Game()
    game.run()

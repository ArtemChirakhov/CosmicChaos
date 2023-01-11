import sys

from player import *
from blockmap import*


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
        self.kickguy = player(self)
        self.map = Map(self)

    def update(self):
        self.kickguy.update()
        pygame.display.flip()
        self.delta_time = self.clock.tick(self.FPS)
        pygame.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.screen.fill('black')
        self.kickguy.draw()
        self.map.draw()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()

import sys

from raycasting import *
from player import *
from blockmap import*
from enemy import Enemy


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
        self.kickguy = Player(self)
        self.map = Map(self)
        self.raycasting = RayCasting(self)
        self.enemy = Enemy(self)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.enemy)

    def update(self):
        self.all_sprites.update()
        self.kickguy.update()
        #self.raycasting.update()
        pygame.display.flip()
        self.delta_time = self.clock.tick(self.FPS)
        pygame.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.screen.fill('black')
        self.all_sprites.draw(self.screen)
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
            self.draw()
            self.update()


if __name__ == '__main__':
    game = Game()
    game.run()

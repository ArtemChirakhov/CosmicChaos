import sys
import pygame_menu
import pygame

from raycasting import *
from player import *
from blockmap import *


class Game:
    FPS = 60
    RES = width, height = 1320, 720

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(self.RES)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.new_game()
        f1 = pygame.font.Font(None, 36)
        self.text1 = f1.render('Hello Привет', True,
                               (180, 0, 0))

    def new_game(self):
        self.kickguy = Player(self)
        self.map = Map(self)
        self.raycasting = RayCasting(self)

    def update(self):
        self.kickguy.update()
        self.raycasting.update()
        pygame.display.flip()
        self.delta_time = self.clock.tick(self.FPS)
        pygame.display.set_caption(f'{self.clock.get_fps() :.1f}')
        self.screen.blit(self.text1, (10, 50))

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

    def load_game(self):
        pass

    def menu(self):
        font = pygame_menu.font.FONT_BEBAS
        myimage = pygame_menu.baseimage.BaseImage(image_path="Data/cosmos1.jpg",
                                                  drawing_mode=pygame_menu.baseimage.IMAGE_MODE_CENTER)
        mytheme = pygame_menu.Theme(background_color=myimage, title_background_color=(0, 0, 0), title_font=font,
                                    title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_SIMPLE, widget_font=font)
        menu = pygame_menu.Menu('Cosmic Chaos', 1320, 720, theme=mytheme)
        menu.add.button('New Game', self.run)
        menu.add.button('Load game', self.load_game)
        menu.add.button('Quit', pygame_menu.events.EXIT)
        menu.mainloop(self.screen)


if __name__ == '__main__':
    game = Game()
    game.menu()

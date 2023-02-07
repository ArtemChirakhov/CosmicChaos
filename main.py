import sys
import pygame_menu
import pygame

from blockmap import *
from enemy import Enemy
from player import *
from blockmap import *
from raycasting import *
from weapon import *


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


    def new_game(self):
        self.player1 = Player(self)
        self.map = Map(self)
        self.raycasting = RayCasting(self)
        self.weapon = Weapon(self)
        self.enemy_info = self.map.get_enemy_info()
        self.enemy_group = []
        for i in self.enemy_info:
            self.enemy_group.append(Enemy(self, i[0] * 50, i[1] * 50, 'orange'))
        # self.enemy = Enemy(self, 300, 300, 'red')
        #   self.enemy1 = Enemy(self, 400, 400, 'orange')

    def update(self):
        self.player1.update()
        self.raycasting.update()
        self.weapon.update()
        for i in range(len(self.enemy_group)):
            self.enemy_group[i].update()
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(self.enemy_group)):
                    self.enemy_group[i].get_damage()

    def run(self):
        while True:
            self.check_events()
            self.draw()
            self.update()

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

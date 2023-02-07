import sys
import pygame_menu

from blockmap import *
from enemy import Enemy
from player import *
from raycasting import *
from weapon import *


class Game:
    FPS = 60
    RES = width, height = 1320, 720

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.RES)
        self.clock = pygame.time.Clock()
        self.delta_time = 1


    def new_game(self):
        self.new_data = open("Data/Save.txt", mode="w")
        self.new_data.write("100;0;0")
        self.new_data.close()
        self.start_game()

    def start_game(self):
        self.load_data = open("Data/Save.txt", mode="r")
        print(list(map(int, self.load_data.readline().split(";"))), len(self.load_data.readline().split(";")))
        data = list(map(int, self.load_data.readline().split(";")))
        player_hp = data[0]
        self.kills = data[1]
        self.difficulty = data[2]
        self.lvl_kills = 0
        self.sptite_group = pygame.sprite.Group()
        self.player1 = Player(self, player_hp)
        self.sptite_group.add(self.player1)
        self.map = Map(self)
        self.raycasting = RayCasting(self)
        self.weapon = Weapon(self)
        self.enemy_info = self.map.get_enemy_info()
        self.enemy_group = []
        self.enemy_count = 0
        for i in self.enemy_info:
            self.enemy_group.append(Enemy(self, i[0] * 50, i[1] * 50, 'orange', self.difficulty))

    def update(self):
        self.raycasting.update()
        self.weapon.update()
        count = 0
        for i in range(len(self.enemy_group)):
            self.enemy_group[i].update()
            if self.enemy_group[i].return_dead():
                count += 1
        self.lvl_kills = count
        if count == len(self.enemy_group):
            self.load_data.write(f"{self.player1.return_hp()};{self.kills + self.lvl_kills};{self.difficulty}")
            self.start_game()
        self.sptite_group.draw(self.screen)
        self.sptite_group.update()
        pygame.display.flip()
        self.delta_time = self.clock.tick(self.FPS)
        pygame.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.screen.fill('black')
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
        self.start_game()
        while True:
            self.check_events()
            self.draw()
            self.update()

    def menu(self):  # меню
        font = pygame_menu.font.FONT_BEBAS
        myimage = pygame_menu.baseimage.BaseImage(image_path="Data/cosmos1.jpg",
                                                  drawing_mode=pygame_menu.baseimage.IMAGE_MODE_CENTER)
        mytheme = pygame_menu.Theme(background_color=myimage, title_background_color=(0, 0, 0), title_font=font,
                                    title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_SIMPLE, widget_font=font)
        menu = pygame_menu.Menu('Cosmic Chaos', 1320, 720, theme=mytheme)
        menu.add.button('New Game', self.new_game)
        menu.add.button('Load game', self.run)
        menu.add.button('Quit', pygame_menu.events.EXIT)
        menu.mainloop(self.screen)


if __name__ == '__main__':
    game = Game()
    game.menu()

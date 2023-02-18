import sys

import pygame.mixer_music
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
        self.font = pygame.font.Font(None, 36)
        self.shoot_sound = pygame.mixer.Sound("Data/Shoot.mp3")
        self.start_sound = pygame.mixer.Sound("Data/Cocking.mp3")
        self.hit_sound = pygame.mixer.Sound("Data/Hit.mp3")
        self.death_sound = pygame.mixer.Sound("Data/You_lost.mp3")
        self.heart = pygame.image.load("Data/heart.png")
        self.stage = 1
        
    def new_game(self):
        self.new_data = open("Data/Save.txt", mode="w")
        self.new_data.write("100;0;0")
        self.new_data.close()
        self.sprite_group = pygame.sprite.Group()
        self.run()

    def start_game(self):
        self.load_data = open("Data/Save.txt", mode="r", encoding="utf8")
        data = self.load_data.readline().split(";")
        print(data)
        for i in range(len(data)):
            data[i] = int(data[i])
        player_hp = data[0]
        self.kills = data[1]
        self.stage = data[2]
        self.lvl_kills = 0
        self.sprite_group = pygame.sprite.Group()
        self.player1 = Player(self, player_hp)
        self.sprite_group.add(self.player1)
        self.map = Map(self)
        self.raycasting = RayCasting(self)
        self.weapon = Weapon(self)
        self.enemy_info = self.map.get_enemy_info()
        self.enemy_group = []
        self.enemy_count = 0
        for i in self.enemy_info:
            self.enemy_group.append(Enemy(self, i[1] * 50 + 25, i[0] * 50 + 25, 'darkgreen', self.stage))
        self.hp_text = self.font.render(str(self.player1.return_hp()), True, (0, 0, 0))
        self.kill_text = self.font.render(f'Killcount: {self.kills}', True, (0, 0, 0))
        self.stage_text = self.font.render(f"Stage: {self.stage}", True, (0, 0, 0))
        self.start_sound.play()

    def update(self):
        self.raycasting.update()
        self.weapon.update()
        count = 0
        for i in range(len(self.enemy_group)):
            self.enemy_group[i].update()
            if self.enemy_group[i].return_dead():
                count += 1
        self.lvl_kills = count
        self.sprite_group.draw(self.screen)
        self.sprite_group.update()
        if count == len(self.enemy_group):
            self.stage += 1
            self.new_data = open("Data/Save.txt", mode="w")
            self.new_data.write(f"{self.player1.return_hp()};{self.kills + self.lvl_kills};{self.stage}")
            self.new_data.close()
            self.run()
        if self.player1.is_dead():
            self.kills += count
            self.death_screen()
        self.sprite_group.draw(self.screen)
        self.sprite_group.update()
        self.hp_text = self.font.render(str(self.player1.return_hp()), True, (0, 0, 0))
        self.kill_text = self.font.render(f'Killcount: {self.kills + count}', True, (0, 0, 0))
        self.stage_text = self.font.render(f"Stage: {self.stage}", True, (0, 0, 0))
        pygame.display.flip()
        self.delta_time = self.clock.tick(self.FPS)
        pygame.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.screen.fill('black')
        self.map.draw()
        self.screen.blit(self.hp_text, (40, 10))
        self.screen.blit(self.kill_text, (1000, 10))
        self.screen.blit(self.stage_text, (1200, 10))
        self.screen.blit(self.heart, (10, 5))

    def check_events(self):
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.shoot_sound.play()
                for i in range(len(self.enemy_group)):
                    self.enemy_group[i].get_damage()

    def run(self):
        self.start_game()
        self.start_sound.play()
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
        menu.add.button('Quit', sys.exit)
        menu.mainloop(self.screen)

    def death_screen(self):
        self.death_sound.play()
        font = pygame_menu.font.FONT_BEBAS
        myimage = pygame_menu.baseimage.BaseImage(image_path="Data/Skull1.PNG",
                                                  drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_Y)
        mytheme = pygame_menu.Theme(background_color=myimage, title_background_color=(0, 0, 0), title_font=font,
                                    widget_font=font)
        self.menu1 = pygame_menu.Menu(f'You died, your score is {self.kills}, Stage: {self.stage}', 1320, 720,
                                      theme=mytheme)
        self.menu1.enable()
        self.menu1.add.button('Quit', sys.exit)
        self.menu1.set_absolute_position(0, 0)
        self.menu1.mainloop(self.screen)


if __name__ == '__main__':
    game = Game()
    game.menu()

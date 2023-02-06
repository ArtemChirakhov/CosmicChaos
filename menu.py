import pygame
import pygame_menu
from main import Game

pygame.init()
surface = pygame.display.set_mode((400, 300))


def start_game():
    game = Game()
    game.run()


def load_game():
    pass


menu = pygame_menu.Menu('Welcome', 400, 300, theme=pygame_menu.themes.THEME_DARK)

menu.add.button('New Game', start_game)
menu.add.button('Load game', load_game())
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(surface)

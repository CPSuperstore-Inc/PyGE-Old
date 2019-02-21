import pygame
from pygame.locals import *

from PyGE.Platformer import Platformer
from PyGE.computer import *
from levels import a
from properties import props

pygame.init()

screen = pygame.display.set_mode((300, 600))

game = Platformer(screen, {"level1": a}, props)

game.set_level("level1")

clock = pygame.time.Clock()

world = game.get_objects_except_name("player")
player = game.get_object("player")

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()

    down = pygame.key.get_pressed()
    if down[K_a]:
        game.move_one_with_undo(player, -1, 0)

    if down[K_d]:
        game.move_one_with_undo(player, 1, 0)

    if down[K_w]:
        game.move_one_with_undo(player, 0, -1)

    if down[K_s]:
        game.move_one_with_undo(player, 0, 1)

    screen.fill((0, 0, 0))
    game.update_draw()
    pygame.display.update()

    clock.tick(USER_REFRESH_RATE)

import pygame
import random
import numpy as np

from enum import Enum


class GAME_STATE(Enum):
    MENU = 0
    GAME = 1
    GAME_OVER = 2


class Directions(Enum):
    NORTH = 0
    WEST = 1
    SOUTH = 2
    EAST = 3


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

milliseconds = 0
seconds = 0
first_tick = pygame.time.get_ticks()

# ENEMIES
Bunnie = 3
Chick = 5
Fredbear = 4
Vixen = 3

# ODDS OF MOVING OUT OF (DIFFICULTY/ THIS NUMBER)
# higher number = less chance of moving
Bunnie_odds = 20
Chick_odds = 20
Fredbear_odds = 30
Vixen_odds = 50

# MAP LAYOUT - simplified map
# | 1 |       | 2 |
# | 3 | | 4 | | 5 |
# | 6 |       | 7 |
# | 8 | | 9 | |10 |

# movement table
table = np.zeros((4, 10))


def insert_direction(current_cell, next_cell, direction):
    table[direction][current_cell] = next_cell


def populate_movement_table():
    # col 1
    insert_direction(1, 3, Directions.SOUTH)
    insert_direction(3, 1, Directions.NORTH)
    insert_direction(3, 4, Directions.WEST)
    insert_direction(3, 6, Directions.SOUTH)
    insert_direction(6, 3, Directions.NORTH)
    insert_direction(6, 8, Directions.EAST)
    insert_direction(8, 9, Directions.WEST)
    # col 2
    insert_direction(4, 3, Directions.EAST)
    insert_direction(4, 5, Directions.WEST)
    insert_direction(9, 8, Directions.EAST)
    insert_direction(9, 10, Directions.WEST)
    # col 3
    insert_direction(2, 5, Directions.SOUTH)
    insert_direction(5, 2, Directions.NORTH)
    insert_direction(5, 4, Directions.EAST)
    insert_direction(5, 7, Directions.SOUTH)
    insert_direction(7, 5, Directions.NORTH)
    insert_direction(7, 10, Directions.SOUTH)
    insert_direction(10, 9, Directions.EAST)


def is_valid_move(current_cell, direction):
    if table[direction][current_cell] == 0:
        return False
    return True


# TO DO - add later to specify entity
def move(current_cell, direction):
    return table[direction][current_cell]


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    # GAME LOGIC
    # count number off frames so to tell how many seconds have passed
    time_passed = clock.get_time()
    milliseconds += time_passed

    # converts to seconds so timings make sense to players
    if milliseconds > 1000:
        seconds = milliseconds / 1000
        milliseconds = milliseconds % 1000

    # BONNIE AI - PORT THIS TO ENEMY CLASS
    # if a second passed then check for movement opportunity

    # every second do a movement check
    if seconds >= 0:
        # 0 -> North
        # 1 -> West
        # 2 -> South
        # 3 -> East
        movement = random.randint(0, 3)

    # Render new frame
    pygame.display.flip()

    # 60 FPS
    clock.tick(60)

pygame.quit()

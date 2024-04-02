import pygame
import random
import numpy as np
from Bunnie import Bunnie_Class

from enum import Enum


class GAME_STATE(Enum):
    MENU = 0
    GAME = 1
    GAME_OVER = 2
    WIN = 3


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

milliseconds = 0
seconds = 0
prev_second = 0
first_tick = pygame.time.get_ticks()

# ENEMIES
Bunnie = Bunnie_Class
Chick = 5
Fredbear = 4
Vixen = 3

def draw_map(array_x, array_y):
    i = 0
    for x in array_x:
        pygame.draw.rect(screen, (0, 220, 0), (x, array_y[i], w, h), outline)
        i += 1


map_x = 30
map_y = 30
w = 50
h = 50
map_buff = 30
outline = 5
arr_x = [map_x, map_x + (map_buff * 4),
         map_x, map_x + (map_buff * 2), map_x + (map_buff * 4),
         map_x, map_x + (map_buff * 4),
         map_x, map_x + (map_buff * 2), map_x + (map_buff * 4), ]
arr_y = [map_y, map_y,
         map_y + (map_buff * 2), map_y + (map_buff * 2), map_y + (map_buff * 2),
         map_y + (map_buff * 4), map_y + (map_buff * 4),
         map_y + (map_buff * 6), map_y + (map_buff * 6), map_y + (map_buff * 6)]
radius = 10
thickness = 0

mouse_held = False

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_held = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    # GAME LOGIC
    # count number off frames so to tell how many seconds have passed
    time_passed = clock.get_time()
    milliseconds += time_passed

    # converts to seconds so timings make sense to players
    if milliseconds > 1000:
        seconds += milliseconds / 1000
        milliseconds = milliseconds % 1000

    # BONNIE AI - PORT THIS TO ENEMY CLASS
    # if a second passed then check for movement opportunity

    # every second do a movement check
    if seconds > prev_second:
        prev_second = seconds
        print(seconds)
        # check movement opportunity
        rand_num = random.randint(1, Bunnie)
        # begin movement if movement opportunity lands below
        if rand_num <= Bunnie_diff:
            print("Bunnie moved")
            Bunnie = int(move(Bunnie))
            print(Bunnie)
        # check movement opportunity
        rand_num = random.randint(1, Chick_odds)
        # begin movement if movement opportunity lands below
        if rand_num <= Chick_diff:
            print("Chick moved")
            Chick = int(move(Chick))
            print(Chick)
        if rand_num <= Fredbear_diff:
            print("Fredbear moved")
            Fredbear = int(move(Fredbear))
            print(Fredbear)
        if rand_num <= Vixen_diff:
            print("Vixen moved")
            Vixen = int(move(Vixen))
            print(Vixen)

    # DRAWING THE FRAME
    draw_map(arr_x, arr_y)
    Bunnie_x = arr_x[(Bunnie - 1)] + (w / 2)
    Bunnie_y = arr_y[(Bunnie - 1)] + (h / 2)

    Chick_x = arr_x[(Chick - 1)] + (w / 2)
    Chick_y = arr_y[(Chick - 1)] + (h / 2)

    Fredbear_x = arr_x[(Fredbear - 1)] + (w / 2)
    Fredbear_y = arr_y[(Fredbear - 1)] + (h / 2)

    Vixen_x = arr_x[(Vixen - 1)] + (w / 2)
    Vixen_y = arr_y[(Vixen - 1)] + (h / 2)

    # drawing enemy units
    pygame.draw.circle(screen, (0, 50, 200), (Bunnie_x, Bunnie_y), radius, thickness)
    pygame.draw.circle(screen, (225, 225, 0), (Chick_x, Chick_y), radius, thickness)
    pygame.draw.circle(screen, (150, 75, 0), (Fredbear_x, Fredbear_y), radius, thickness)

    btn_x = 200
    btn_y = 400
    btn2_x = 1000
    btn_size = 50
    # drawing the buttons used in game
    pygame.draw.rect(screen, (225, 0, 0), pygame.Rect(btn_x, btn_y, btn_size, btn_size))
    pygame.draw.rect(screen, (225, 0, 0), pygame.Rect(1000, 400, 50, 50))

    # if button is clicked
    mouse_presses = pygame.mouse.get_pressed()

    if mouse_presses[0] and not mouse_held:
        print("Left Mouse was pressed")
        mouse_held = True
        mousex, mousey = pygame.mouse.get_pos()
        # TO DO - FIX BUTTON PRESS TO BE MORE STREAMLINED
        if btn_y < mousey < btn_y + btn_size:
            if btn_x < mousex < btn_x + btn_size:
                print("press button 1")
            elif btn2_x < mousex < btn2_x + btn_size:
                print("press button 2")

    # Render new frame
    pygame.display.flip()

    # 60 FPS
    clock.tick(60)

pygame.quit()

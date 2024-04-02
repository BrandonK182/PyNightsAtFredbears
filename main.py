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

class CAM(Enum):
    CAM_1A = 0
    CAM_1B = 1
    CAM_1C = 2
    CAM_2A = 3
    CAM_2B = 4
    CAM_3 = 5
    CAM_4A = 6
    CAM_4B = 7
    CAM_5 = 8
    CAM_6 = 9
    CAM_7 = 10

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

grey = (100, 100, 100)
white = (200, 200, 200)
thick = 2
scale = 2
map_x = 225
map_y = 30
outline = 5
radius = 10
mouse_held = False
cam_x = np.zeros(11)
cam_y = np.zeros(11)
cam_w = 40*scale
cam_h = 25*scale

cam_x[CAM.CAM_1A.value] = map_x + 112.5*scale
cam_y[CAM.CAM_1A.value] = map_y + 12.5*scale

cam_x[CAM.CAM_1B.value] = map_x + 100*scale
cam_y[CAM.CAM_1B.value] = map_y + 50*scale

cam_x[CAM.CAM_1C.value] = map_x + 70*scale
cam_y[CAM.CAM_1C.value] = map_y + 130*scale

cam_x[CAM.CAM_2A.value] = map_x + 115*scale
cam_y[CAM.CAM_2A.value] = map_y + 235*scale

cam_x[CAM.CAM_2B.value] = map_x + 115*scale
cam_y[CAM.CAM_2B.value] = map_y + 265*scale

cam_x[CAM.CAM_3.value] = map_x + 55*scale
cam_y[CAM.CAM_3.value] = map_y + 235*scale

cam_x[CAM.CAM_4A.value] = map_x + 205*scale
cam_y[CAM.CAM_4A.value] = map_y + 235*scale

cam_x[CAM.CAM_4B.value] = map_x + 205*scale
cam_y[CAM.CAM_4B.value] = map_y + 265*scale

cam_x[CAM.CAM_5.value] = map_x + 5*scale
cam_y[CAM.CAM_5.value] = map_y + 75*scale

cam_x[CAM.CAM_6.value] = map_x + 295*scale
cam_y[CAM.CAM_6.value] = map_y + 225*scale

cam_x[CAM.CAM_7.value] = map_x + 295*scale
cam_y[CAM.CAM_7.value] = map_y + 80*scale

def draw_map():
    # MAP OUTLINE
    pygame.draw.rect(screen, grey, (map_x + 125*scale, map_y + 25*scale, 100*scale, 25*scale), thick)  # front stage
    pygame.draw.rect(screen, grey, (map_x + 25*scale, map_y + 40*scale, 35*scale, 75*scale), thick)  # maintenance room
    pygame.draw.rect(screen, grey, (map_x + 75*scale, map_y + 50*scale, 200*scale, 150*scale), thick)  # main room
    pygame.draw.rect(screen, grey, (map_x + 60*scale, map_y + 60*scale, 15*scale, 15*scale), thick)  # main - maintenance connector
    pygame.draw.rect(screen, grey, (map_x + 35*scale, map_y + 135*scale, 40*scale, 55*scale), thick)  # Vixen's room
    pygame.draw.rect(screen, grey, (map_x + 290*scale, map_y + 75*scale, 25*scale, 125*scale), thick)  # restrooms
    pygame.draw.rect(screen, grey, (map_x + 275*scale, map_y + 100*scale, 15*scale, 15*scale), thick)  # main - restroom connector
    pygame.draw.rect(screen, grey, (map_x + 115*scale, map_y + 215*scale, 30*scale, 100*scale), thick)  # left hallway
    pygame.draw.rect(screen, grey, (map_x + 200*scale, map_y + 215*scale, 30*scale, 100*scale), thick)  # right hallway
    pygame.draw.rect(screen, grey, (map_x + 122.5*scale, map_y + 200*scale, 15*scale, 15*scale), thick)    # main - left hall connector
    pygame.draw.rect(screen, grey, (map_x + 207.5*scale, map_y + 200*scale, 15*scale, 15*scale), thick)  # main - right hall connector
    pygame.draw.rect(screen, grey, (map_x + 75*scale, map_y + 225*scale, 30*scale, 50*scale), thick)  # janitor closet
    pygame.draw.rect(screen, grey, (map_x + 105*scale, map_y + 235*scale, 10*scale, 10*scale), thick)  # closet - right hall connector
    pygame.draw.rect(screen, grey, (map_x + 250*scale, map_y + 215*scale, 75*scale, 60*scale), thick)  # kitchen
    pygame.draw.rect(screen, grey, (map_x + 255*scale, map_y + 200*scale, 15*scale, 15*scale), thick)  # kitchen - main connector
    pygame.draw.rect(screen, grey, (map_x + 155*scale, map_y + 265*scale, 35*scale, 50*scale), thick)  # security room
    pygame.draw.rect(screen, grey, (map_x + 145*scale, map_y + 285*scale, 10*scale, 10*scale), thick)  # security - left connector
    pygame.draw.rect(screen, grey, (map_x + 190*scale, map_y + 285*scale, 10*scale, 10*scale), thick)  # security - right connector
    # CAM SQUARES
    pygame.draw.rect(screen, white, (cam_x[CAM.CAM_1A.value], cam_y[CAM.CAM_1A.value] , cam_w, cam_h), thick)           # Cam 1A
    pygame.draw.rect(screen, white, (cam_x[CAM.CAM_1B.value], cam_y[CAM.CAM_1B.value], cam_w, cam_h), thick)       # Cam 1B
    pygame.draw.rect(screen, white, (cam_x[CAM.CAM_5.value], cam_y[CAM.CAM_5.value], cam_w, cam_h), thick)         # Cam 5
    pygame.draw.rect(screen, white, (cam_x[CAM.CAM_1C.value], cam_y[CAM.CAM_1C.value], cam_w, cam_h), thick)       # Cam 1C
    pygame.draw.rect(screen, white, (cam_x[CAM.CAM_7.value], cam_y[CAM.CAM_7.value], cam_w, cam_h), thick)       # Cam 7
    pygame.draw.rect(screen, white, (cam_x[CAM.CAM_3.value], cam_y[CAM.CAM_3.value], cam_w, cam_h), thick)       # Cam 3
    pygame.draw.rect(screen, white, (cam_x[CAM.CAM_2A.value], cam_y[CAM.CAM_2A.value], cam_w, cam_h), thick)      # Cam 2A
    pygame.draw.rect(screen, white, (cam_x[CAM.CAM_2B.value], cam_y[CAM.CAM_2B.value], cam_w, cam_h), thick)      # Cam 2B
    pygame.draw.rect(screen, white, (cam_x[CAM.CAM_4A.value], cam_y[CAM.CAM_4A.value], cam_w, cam_h), thick)      # Cam 4A
    pygame.draw.rect(screen, white, (cam_x[CAM.CAM_4B.value], cam_y[CAM.CAM_4B.value], cam_w, cam_h), thick)      # Cam 4B
    pygame.draw.rect(screen, white, (cam_x[CAM.CAM_6.value], cam_y[CAM.CAM_6.value], cam_w, cam_h), thick)      # Cam 6


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
        rand_num = random.randint(1, 20)
        # begin movement if movement opportunity lands below
        '''
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
    '''

    draw_map()

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

import pygame
import random
import numpy as np
from Bunnie import Bunnie_Class
from map import Map
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
Bunnie = Bunnie_Class(15)
Chick = 5
Fredbear = 4
Vixen = 3

grey = (100, 100, 100)
white = (200, 200, 200)
off_white = (175, 175, 175)
thick = 2
scale = 2
map_x = 225
map_y = 30
outline = 5
radius = 10
mouse_held = False
cam_x = np.zeros(11)
cam_y = np.zeros(11)
cam_w = 40 * scale
cam_h = 25 * scale
left_door = False
right_door = False

game_map = Map(map_x, map_y, scale, thick)
current_cam = game_map.cameras[0]


def draw_map():
    i = 0
    # MAP OUTLINE
    for x in game_map.array_x:
        pygame.draw.rect(screen, grey, (x, game_map.array_y[i], game_map.width_arr[i],
                                        game_map.height_arr[i]), game_map.thick)
        i += 1
    # CAM SQUARES
    for cam in game_map.cameras:
        pygame.draw.rect(screen, white, (cam.x, cam.y, cam.w, cam.h), cam.thick)


def get_camera_clicked(x, y, current):
    for cam in game_map.cameras:
        if cam.y < y < cam.y + cam.h:
            if cam.x < x < cam.x + cam.w:
                print("pressed CAM " + cam.name)
                return cam
    return current


def match_camera(position):
    for cam in game_map.cameras:
        if cam.position == position:
            return cam
    return game_map.cameras[0]


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
        Bunnie.movement_opportunity()

    # DRAWING THE FRAME
    bunnie_cam = match_camera(Bunnie.position)
    Bunnie_x = bunnie_cam.x + 100

    # drawing enemy units
    pygame.draw.circle(screen, (0, 50, 200), (Bunnie_x, bunnie_cam.y), radius, 0)
    # pygame.draw.circle(screen, (225, 225, 0), (Chick_x, Chick_y), radius, 0)
    # pygame.draw.circle(screen, (150, 75, 0), (Fredbear_x, Fredbear_y), radius, 0)

    draw_map()

    btn_x = 200
    btn_y = 400
    btn2_x = 1000
    btn_size = 50
    # drawing the buttons used in game
    pygame.draw.rect(screen, (225, 0, 0), pygame.Rect(btn_x, btn_y, btn_size, btn_size))
    pygame.draw.rect(screen, (225, 0, 0), pygame.Rect(btn2_x, btn_y, btn_size, btn_size))

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
        # check if camera is clicked
        current_cam = get_camera_clicked(mousex, mousey, current_cam)

    pygame.draw.rect(screen, off_white, pygame.Rect(current_cam.x, current_cam.y, current_cam.w, current_cam.h))

    # Render new frame
    pygame.display.flip()

    # 60 FPS
    clock.tick(60)

pygame.quit()

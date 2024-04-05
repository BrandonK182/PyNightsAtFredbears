import pygame
import random
import numpy as np
from Bunnie import Bunnie
from Chick import Chick
from Fred import Fred
from Vixen import Vixen
from map import Map
from enum import Enum


class GAME_STATE(Enum):
    MENU = 0
    GAME = 1
    GAME_OVER = 2
    WIN = 3
    GAME_OVER_BUNNIE = 4
    GAME_OVER_CHICK = 5
    GAME_OVER_FRED = 6
    GAME_OVER_VIXEN = 7

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
state = GAME_STATE.GAME

debug = True

milliseconds = 0
seconds = 0
first_tick = pygame.time.get_ticks()

# ENEMIES
bunnieDifficulty = 15
chickDifficulty = 15
fredDifficulty = 15
vixenDifficulty = 15

vixenEZ = False

bunnie = Bunnie(bunnieDifficulty)
chick = Chick(chickDifficulty)
fred = Fred(fredDifficulty)
vixen = Vixen(vixenDifficulty, vixenEZ)

grey = (100, 100, 100)
white = (200, 200, 200)
off_white = (175, 175, 175)
red = (200, 0, 0)
green = (0, 200, 0)
thick = 3
scale = 1.5
map_x = 250
map_y = 30
outline = 5
radius = 10
mouse_held = False
cam_x = np.zeros(11)
cam_y = np.zeros(11)
cam_w = 40 * scale
cam_h = 25 * scale
left_door_closed = False
right_door_closed = False
left_color = red
right_color = green
cam_flip_x = 100
cam_flip_y = 600
cam_flip_w = 800
cam_flip_h = 100
cam_flipped_up = False
cam_flip_hover = False

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
    # count milliseconds between frames to tell how much time has passed
    time_passed = clock.get_time()
    milliseconds += time_passed

    # converts to seconds so timings make sense to players
    seconds = milliseconds / 1000

    # BONNIE AI - PORT THIS TO ENEMY CLASS
    # if a second passed then check for movement opportunity
    # check movement opportunity
    if bunnie.can_move(seconds):
        # if Bunnie next to the office, roll for kill
        if bunnie.can_attack():
            if bunnie.kill_opportunity():
                if left_door_closed:
                    # resets position if the player stopped Bunnie
                    bunnie.reset()
                else:
                    # kill player if door is open
                    state = GAME_STATE.GAME_OVER_BUNNIE
        # check if Bunnie can move to a different room
        else:
            bunnie.movement_opportunity()
    if chick.can_move(seconds):
        # if Chick next to the office, roll for kill
        if chick.can_attack():
            if chick.kill_opportunity():
                if right_door_closed:
                    # resets position if the player stopped Chick
                    chick.reset()
                else:
                    # kill player if door is open
                    state = GAME_STATE.GAME_OVER_CHICK
        # check if chick can move to a different room
        else:
            chick.movement_opportunity()
    if fred.can_move(seconds):
        # if Fred next to the office, roll for kill
        if fred.can_attack():
            if fred.kill_opportunity():
                if right_door_closed:
                    # resets position if the player stopped Fred
                    fred.reset()
                else:
                    # kill player if door is open
                    state = GAME_STATE.GAME_OVER_FRED
        # check if Fred can move to a different room
        else:
            fred.movement_opportunity()

    # Vixen's timer
    vixen.move(current_cam, cam_flipped_up, time_passed/1000)
    if vixen.can_kill():
        if left_door_closed:
            vixen.reset()
        else:
            state = GAME_STATE.GAME_OVER_VIXEN

    # CAMERA LOGIC
    # if button is clicked
    mouse_presses = pygame.mouse.get_pressed()
    mousex, mousey = pygame.mouse.get_pos()

    # check which door button or camera was clicked
    if mouse_presses[0] and not mouse_held:
        print("Left Mouse was pressed")
        mouse_held = True
        # let the user click cameras if cameras are up
        if cam_flipped_up:
            # check if camera is clicked
            current_cam = get_camera_clicked(mousex, mousey, current_cam)
        # if users are in the office, let them click the door buttons
        else:
            if btn_y < mousey < btn_y + btn_size:
                if btn_x < mousex < btn_x + btn_size:
                    print("press button 1")
                    left_door_closed = not left_door_closed
                elif btn2_x < mousex < btn2_x + btn_size:
                    print("press button 2")
                    right_door_closed = not right_door_closed

    # flips the camera if the user flicks their mouse down to the box
    if not cam_flip_hover:
        if cam_flip_x < mousex < cam_flip_x + cam_flip_w:
            if cam_flip_y < mousey < cam_flip_y + cam_flip_h:
                # toggles cameras
                cam_flip_hover = True
                cam_flipped_up = not cam_flipped_up
    # measure to prevent multiple toggles when user mouse hovers
    else:
        if cam_flip_y > mousey:
            cam_flip_hover = False

    # DRAWING THE FRAME
    # DEBUG ENEMY DOTS
    if debug:
        # bunnie blue dot position
        if bunnie.position == 11:
            bunnie_cam = match_camera(10)
            bunnie_x = bunnie_cam.x + (100 * game_map.scale)
            bunnie_y = bunnie_cam.y + (75 * game_map.scale)
        else:
            bunnie_cam = match_camera(bunnie.position)
            bunnie_x = bunnie_cam.x + (50 * game_map.scale)
            bunnie_y = bunnie_cam.y + (10 * game_map.scale)
        # chick yellow dot position
        if chick.position == 11:
            chick_cam = match_camera(10)
            chick_x = chick_cam.x + (120 * game_map.scale)
            chick_y = chick_cam.y + (75 * game_map.scale)
        else:
            chick_cam = match_camera(chick.position)
            chick_x = chick_cam.x + (70 * game_map.scale)
            chick_y = chick_cam.y + (10 * game_map.scale)
        # fred brown dot position
        if fred.position == 11:
            fred_cam = match_camera(10)
            fred_x = fred_cam.x + (140 * game_map.scale)
            fred_y = fred_cam.y + (75 * game_map.scale)
        else:
            fred_cam = match_camera(fred.position)
            fred_x = fred_cam.x + (90 * game_map.scale)
            fred_y = fred_cam.y + (10 * game_map.scale)
        if vixen.position == 7:
            vixen_cam = match_camera(7)
            vixen_x = vixen_cam.x + (70 * game_map.scale)
            vixen_y = vixen_cam.y + (10 * game_map.scale)
        else:
            vixen_cam = match_camera(vixen.position)
            vixen_x = vixen_cam.x + (50 * game_map.scale)
            vixen_y = vixen_cam.y + (10 * game_map.scale)

    # draw the boundaries for the camera flip marker
    pygame.draw.rect(screen, off_white, (cam_flip_x, cam_flip_y, cam_flip_w, cam_flip_h), thick)

    # draw camera scene
    if cam_flipped_up:
        draw_map()
        # highlight the camera selected
        pygame.draw.rect(screen, off_white, pygame.Rect(current_cam.x, current_cam.y, current_cam.w, current_cam.h))
        # drawing enemy units
        if debug:
            pygame.draw.circle(screen, (0, 50, 200), (bunnie_x, bunnie_y), radius, 0)
            pygame.draw.circle(screen, (225, 225, 0), (chick_x, chick_y), radius, 0)
            pygame.draw.circle(screen, (150, 75, 0), (fred_x, fred_y), radius, 0)
            pygame.draw.circle(screen, (225, 25, 25), (vixen_x, vixen_y), vixen.stage*scale, 0)
    # draw the office
    else:
        btn_x = 200
        btn_y = 400
        btn2_x = 1000
        btn_size = 50
        # drawing the buttons used in game
        if left_door_closed:
            left_color = green
        else:
            left_color = red
        if right_door_closed:
            right_color = green
        else:
            right_color = red
        pygame.draw.rect(screen, left_color, pygame.Rect(btn_x, btn_y, btn_size, btn_size))
        pygame.draw.rect(screen, right_color, pygame.Rect(btn2_x, btn_y, btn_size, btn_size))

    if state == GAME_STATE.GAME_OVER_BUNNIE:
        screen.fill("purple")

    if state == GAME_STATE.GAME_OVER_CHICK:
        screen.fill("yellow")

    if state == GAME_STATE.GAME_OVER_FRED:
        screen.fill("brown")

    if state == GAME_STATE.GAME_OVER_VIXEN:
        screen.fill("red")

    # Render new frame
    pygame.display.flip()

    # 60 FPS
    clock.tick(60)

pygame.quit()

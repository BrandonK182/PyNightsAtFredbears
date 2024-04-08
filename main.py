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
    NO_POWER = 8
    INTRO = 9


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
state = GAME_STATE.MENU

debug = True

milliseconds = 0
seconds = 0
first_tick = pygame.time.get_ticks()

# ENEMIES
bunnieDifficulty = 1
chickDifficulty = 1
fredDifficulty = 0
vixenDifficulty = 0

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
yellow = (225, 225, 0)
thick = 3
scale = 1.25
map_x = 800
map_y = 300
outline = 5
radius = 10
mouse_held = False
cam_x = np.zeros(11)
cam_y = np.zeros(11)
cam_w = 40 * scale
cam_h = 25 * scale
left_door_closed = False
right_door_closed = False
left_light_on = False
right_light_on = False
left_color = red
right_color = red
left_light_clr = grey
right_light_clr = grey
cam_flip_x = 250
cam_flip_y = 650
cam_flip_w = 600
cam_flip_h = 50
cam_flipped_up = False
cam_flip_hover = False

btn_xL = 50
btn_y = 400
btn_xR = 1150
btn_size = 50

light_y = 500

window_xL = 400
window_xR = 750
window_y = 50
window_w = 100
window_h = 300

door_xL = 150
door_xR = 900
door_y = 50
door_w = 200
door_h = 500

energy = 100.0
power_consumption = 1
drain_tick = 0.002
win_timer = 600
power_out = False

game_map = Map(map_x, map_y, scale, thick)
current_cam = game_map.cameras[0]
level = 1


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


def reset_all():
    bunnie.full_reset()
    chick.full_reset()
    fred.full_reset()
    vixen.reset()


pygame.font.init()  # you have to call this at the start,
# if you want to use this module.
my_font = pygame.font.SysFont('Comic Sans MS', 30)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_held = False
            if left_light_on or right_light_on:
                left_light_on = False
                right_light_on = False
                power_consumption -= 1

    # if mouse button is clicked
    mouse_presses = pygame.mouse.get_pressed()
    mousex, mousey = pygame.mouse.get_pos()

    # GAME LOGIC
    # count milliseconds between frames to tell how much time has passed
    time_passed = clock.get_time()
    milliseconds += time_passed

    # converts to seconds so timings make sense to players
    seconds = milliseconds / 1000

    if state == GAME_STATE.MENU:
        screen.fill("black")
        start_text = my_font.render("click anywhere to start", False, white)
        screen.blit(start_text, (450, 350))

        if mouse_presses[0]:
            level = 1
            state = GAME_STATE.INTRO

    if state == GAME_STATE.INTRO:
        screen.fill("black")

        # level determines enemy difficulty
        if level == 1:
            bunnieDifficulty = 1
            chickDifficulty = 1
            fredDifficulty = 0
            vixenDifficulty = 0

        if level == 2:
            bunnieDifficulty = 4
            chickDifficulty = 3
            fredDifficulty = 0
            vixenDifficulty = 1

        if level == 3:
            bunnieDifficulty = 7
            chickDifficulty = 5
            fredDifficulty = 1
            vixenDifficulty = 3

        if level == 4:
            bunnieDifficulty = 10
            chickDifficulty = 7
            fredDifficulty = 3
            vixenDifficulty = 5

        if level == 5:
            bunnieDifficulty = 12
            chickDifficulty = 10
            fredDifficulty = 5
            vixenDifficulty = 7

        bunnie.difficulty = bunnieDifficulty
        chick.difficulty = chickDifficulty
        fred.difficulty = fredDifficulty
        vixen.difficulty = vixenDifficulty

        reset_all()

        start_text = my_font.render("Night " + str(level), False, white)
        screen.blit(start_text, (600, 350))
        pygame.display.flip()
        pygame.time.delay(5000)
        game_start_time = seconds
        state = GAME_STATE.GAME

    if state == GAME_STATE.GAME:

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        # RENDER YOUR GAME HERE
        # check win condition
        seconds_remaining = seconds - game_start_time
        if seconds_remaining >= win_timer:
            state = GAME_STATE.WIN

        if seconds_remaining >= 100:
            game_clock = round((seconds_remaining - (seconds_remaining % 100)) / 100)
        else:
            game_clock = 12

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
        vixen.move(current_cam, cam_flipped_up, time_passed / 1000)
        if vixen.can_kill():
            if left_door_closed:
                vixen.reset()
                energy -= 10
            else:
                pygame.draw.circle(screen, (225, 25, 25), (175, 300), 100, 0)
                pygame.display.flip()
                pygame.time.delay(1000)
                state = GAME_STATE.GAME_OVER_VIXEN

        # CAMERA LOGIC

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
                    if btn_xL < mousex < btn_xL + btn_size:
                        print("press door left")
                        left_door_closed = not left_door_closed
                        if left_door_closed:
                            power_consumption += 1
                        else:
                            power_consumption -= 1
                    elif btn_xR < mousex < btn_xR + btn_size:
                        print("press door right")
                        right_door_closed = not right_door_closed
                        if right_door_closed:
                            power_consumption += 1
                        else:
                            power_consumption -= 1
                # check if the door lights are turned on
                elif light_y < mousey < light_y + btn_size:
                    if btn_xL < mousex < btn_xL + btn_size:
                        print("press light left")
                        left_light_on = True
                        if left_light_on:
                            power_consumption += 1
                    elif btn_xR < mousex < btn_xR + btn_size:
                        print("press light right")
                        right_light_on = True
                        if right_light_on:
                            power_consumption += 1

        # flips the camera if the user flicks their mouse down to the box
        if not cam_flip_hover:
            if cam_flip_x < mousex < cam_flip_x + cam_flip_w:
                if cam_flip_y < mousey < cam_flip_y + cam_flip_h:
                    # toggles cameras
                    cam_flip_hover = True
                    cam_flipped_up = not cam_flipped_up
                    if cam_flipped_up:
                        power_consumption += 1
                    else:
                        power_consumption -= 1
        # measure to prevent multiple toggles when user mouse hovers
        else:
            if cam_flip_y > mousey:
                cam_flip_hover = False

        # Calculate the power consumption
        energy -= power_consumption * drain_tick

        if energy <= 0 and not power_out:
            state = GAME_STATE.NO_POWER
            power_loss_time = seconds
            time_left = random.randint(10, 30)
            power_out = True

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
                pygame.draw.circle(screen, (225, 25, 25), (vixen_x, vixen_y), vixen.stage * scale, 0)
                if vixen.difficulty > 0:
                    vixen_timer = my_font.render(str(round(vixen.timer)), False, (225, 25, 25))
                    screen.blit(vixen_timer, (vixen_x + 25, vixen_y - 25))
        # draw the office
        else:
            # drawing the buttons used in game
            if left_door_closed:
                left_color = green
                # draw the door if closed
                pygame.draw.rect(screen, grey, pygame.Rect(door_xL, door_y, door_w, door_h))
            else:
                left_color = red
            if right_door_closed:
                right_color = green
                # draw the door if closed
                pygame.draw.rect(screen, grey, pygame.Rect(door_xR, door_y, door_w, door_h))
            else:
                right_color = red
            if left_light_on:
                left_light_clr = white
                rand = random.randint(1, 10)
                # create a flicker effect
                if rand <= 9:
                    pygame.draw.rect(screen, off_white, pygame.Rect(window_xL, window_y, window_w, window_h))
                    # draw the enemy at the window if they are at the office
                    if bunnie.position == 11:
                        pygame.draw.circle(screen, (0, 50, 200), (window_xL + window_w / 2, window_y + window_h / 2),
                                           50, 0)

            else:
                left_light_clr = grey
            if right_light_on:
                right_light_clr = white
                rand = random.randint(1, 10)
                # create a flicker effect
                if rand <= 9:
                    pygame.draw.rect(screen, off_white, pygame.Rect(window_xR, window_y, window_w, window_h))
                    # draw the enemy at the window if they are at the office
                    if chick.position == 11:
                        pygame.draw.circle(screen, (225, 225, 0), (window_xR + window_w / 2, window_y + window_h / 2),
                                           50, 0)
            else:
                right_light_clr = grey
            pygame.draw.rect(screen, left_color, pygame.Rect(btn_xL, btn_y, btn_size, btn_size))
            pygame.draw.rect(screen, right_color, pygame.Rect(btn_xR, btn_y, btn_size, btn_size))
            pygame.draw.rect(screen, left_light_clr, pygame.Rect(btn_xL, light_y, btn_size, btn_size))
            pygame.draw.rect(screen, right_light_clr, pygame.Rect(btn_xR, light_y, btn_size, btn_size))

        power_left = my_font.render("power left: " + str(round(energy)), False, white)
        screen.blit(power_left, (25, 600))

        # draw additional rectangles for each tick of power usage
        usage = my_font.render("Usage:", False, white)
        screen.blit(usage, (25, 650))
        pygame.draw.rect(screen, green, pygame.Rect(125, 650, 20, 50))
        if power_consumption >= 2:
            pygame.draw.rect(screen, green, pygame.Rect(150, 650, 20, 50))
        if power_consumption >= 3:
            pygame.draw.rect(screen, yellow, pygame.Rect(175, 650, 20, 50))
        if power_consumption >= 4:
            pygame.draw.rect(screen, red, pygame.Rect(200, 650, 20, 50))

        clock_text = my_font.render(str(game_clock) + " AM", False, white)
        screen.blit(clock_text, (0, 0))

    if state == GAME_STATE.GAME_OVER_BUNNIE:
        screen.fill("purple")
        game_over = my_font.render("you died to Bunnie", False, (0, 0, 0))
        screen.blit(game_over, (600, 400))
        pygame.display.flip()
        # pause game and send user back to menu
        pygame.time.delay(5000)
        state = GAME_STATE.MENU

    if state == GAME_STATE.GAME_OVER_CHICK:
        screen.fill("yellow")
        game_over = my_font.render("you died to Chick", False, (0, 0, 0))
        screen.blit(game_over, (600, 400))
        pygame.display.flip()
        # pause game and send user back to menu
        pygame.time.delay(5000)
        state = GAME_STATE.MENU

    if state == GAME_STATE.GAME_OVER_FRED:
        screen.fill("brown")
        game_over = my_font.render("you died to Fred", False, (0, 0, 0))
        screen.blit(game_over, (600, 400))
        pygame.display.flip()
        # pause game and send user back to menu
        pygame.time.delay(5000)
        state = GAME_STATE.MENU

    if state == GAME_STATE.GAME_OVER_VIXEN:
        screen.fill("red")
        game_over = my_font.render("you died to Vixen", False, (0, 0, 0))
        screen.blit(game_over, (600, 400))
        pygame.display.flip()
        # pause game and send user back to menu
        pygame.time.delay(5000)
        state = GAME_STATE.MENU

    if state == GAME_STATE.NO_POWER:
        screen.fill("black")
        # allow win condition in power out mode
        if seconds - game_start_time >= win_timer:
            state = GAME_STATE.WIN

        # random amount of seconds before fred kills player
        if seconds - power_loss_time > time_left:
            state = GAME_STATE.GAME_OVER_FRED

        # generate Fred's eye flicker
        if seconds - power_loss_time > 5:
            rand = random.randint(1, 10)
            # create a flicker effect
            if rand <= 9:
                pygame.draw.circle(screen, white, (100, 200), 25, 15)
                pygame.draw.circle(screen, white, (175, 200), 25, 15)

    if state == GAME_STATE.WIN:
        screen.fill("black")
        win_text = my_font.render("5 AM", False, (0, 0, 0))
        screen.blit(win_text, (600, 400))
        pygame.display.flip()
        pygame.time.delay(1000)
        win_text = my_font.render("6 AM", False, (0, 0, 0))
        screen.blit(win_text, (600, 400))
        pygame.display.flip()
        pygame.time.delay(5000)
        if level < 5:
            level += 1
            state = GAME_STATE.INTRO
        else:
            state = GAME_STATE.MENU

    # Render new frame
    pygame.display.flip()

    # 60 FPS
    clock.tick(60)

pygame.quit()

import random

import numpy as np
from Enemy import Enemy

'''
Vixen is a special enemy in that her mechanics are
completely different from that of the average enemy
'''
default_timer = 20.0
class Vixen(Enemy):
    def __init__(self, difficulty, ez_mode):
        self.name = "Vixen"
        self.stage = 1
        self.position = 4
        self.difficulty = difficulty
        self.timer = default_timer
        self.viewing_vixen = False
        self.checked_hall_already = False
        self.is_ez = ez_mode
        self.progress_bar = 0.0

    def inc_stage(self):
        self.stage += 1
        self.reset_timer()

    def dec_stage(self):
        if self.stage > 1:
            self.stage -= 1
        self.timer = 5.0

    def inc_timer(self,time):
        self.timer += time
    def dec_timer(self,time):
        self.timer -= time

    def reset_timer(self):
        self.timer = default_timer

    def checked_vixen_cam(self):
        if self.timer < 2.0:
            self.timer = 2.0

    def checked_hall_cam(self):
        if self.position == 7 and not self.checked_hall_already:
            self.timer = 1.2
            self.checked_hall_already = True

    def can_attack(self):
        if self.stage >= 5:
            return True
        return False

    def attack(self):
        self.position = 7
        self.timer = 10.0

    def can_kill(self):
        if self.position == 7 and self.timer <= 0:
            return True
        return False

    def move(self, cam_watching, cam_up, time_passed):
        # decrease time regardless of cam watched if in
        # the attack phase
        if self.position == 7:
            self.dec_timer(time_passed)
            # special mechanic where if player checks the hallway cam
            # Vixen will attack after a set amount of time regardless
            # of prior timer
            if cam_watching.position == 7 and cam_up:
                self.checked_hall_cam()
        # if vixen is not in attack phase
        else:
            # increment timer if the player is not monitoring Vixen
            if cam_watching.position != 4 or not cam_up:
                self.dec_timer(time_passed)
            # if ez_mode is turned on, then watching vixen will increase
            # her timer and can even revert aggression stage
            if cam_watching.position == 4 and cam_up:
                self.checked_vixen_cam()
                if self.is_ez:
                    self.inc_timer(time_passed*0.5)
                    # set cap of how high timer can go
                    if self.stage == 1:
                        self.reset_timer()
                    # revert stage if timer cap is reached
                    if self.timer > default_timer:
                        self.dec_stage()
            # if the timer reaches 0, then roll for attack stage
            if self.timer <= 0:
                num = random.randint(1,20)
                # landed move chance
                if num < self.difficulty:
                    if self.can_attack():
                        self.attack()
                    else:
                        self.inc_stage()

    def reset(self):
        self.checked_hall_already = False
        self.stage = 1
        self.reset_timer()
        self.position = 4

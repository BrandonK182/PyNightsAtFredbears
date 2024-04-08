'''
Template class for the general structure of an Enemy type storing
- current location
- movement options based off their current location
- checking if they can kill the player
'''
from enum import Enum
import random
import numpy as np


class Enemy:
    def __init__(self, difficulty):
        self.name = "placeholder"
        self.movement_table = np.zeros((4, 13))
        self.position = 1
        self.difficulty = difficulty
        self.last_move_time = 0
        self.cooldown = 10

    class Directions(Enum):
        UP = 0
        DOWN = 1
        LEFT = 2
        RIGHT = 3

    def insert_direction(self, current_cell, next_cell, direction):
        self.movement_table[direction][current_cell] = next_cell

    def is_valid_move(self, current_cell, direction):
        if self.movement_table[direction][current_cell] == 0:
            return False
        return True

    def move(self, enemy_location):
        valid = False
        while not valid:
            movement = random.randint(0, 3)
            if self.is_valid_move(enemy_location, movement):
                return self.movement_table[movement][enemy_location]
        return enemy_location

    def reset(self):
        self.position = 3

    def full_reset(self):
        self.position = 1

    def movement_opportunity(self):
        rand_num = random.randint(1, 20)
        if rand_num <= self.difficulty:
            self.position = int(self.move(self.position))
            print(self.name + " moved to " + str(self.position))

    def kill_opportunity(self):
        rand_num = random.randint(1, 20)
        if rand_num <= self.difficulty:
            return True
        return False

    def raise_difficulty(self):
        self.difficulty += 1

    def can_attack(self):
        if self.position == 11:
            return True
        return False

    def can_move(self, current_time):
        if current_time - self.last_move_time > self.cooldown:
            self.last_move_time = current_time
            return True
        return False

    def room_occupied(self, room, other):
        if room == other.position:
            return True
        return False

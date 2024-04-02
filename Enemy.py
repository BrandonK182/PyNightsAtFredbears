'''
Template class for the general structure of an Enemy type storing
- location
- movement options
'''
from enum import Enum
import random
import numpy as np


class Directions(Enum):
    NORTH = 0
    WEST = 1
    SOUTH = 2
    EAST = 3


class Enemy:
    def __init__(self):
        self.name = "placeholder"
        self.movement_table = np.zeros((4, 13))

    def insert_direction(self, current_cell, next_cell, direction):
        self.movement_table[direction][current_cell] = next_cell

    '''
                | 1 |
    | 2 |   | 3 |   | 4 |     | 5 |
    | 6 |   | 7 |   | 8 |     | 9 |
            |10 ||11||12 |
    '''
    def populate_movement_table(self):
        # col 1
        self.insert_direction(1, 3, Directions.SOUTH.value)
        self.insert_direction(3, 1, Directions.NORTH.value)
        self.insert_direction(3, 4, Directions.WEST.value)
        self.insert_direction(3, 6, Directions.SOUTH.value)
        self.insert_direction(6, 3, Directions.NORTH.value)
        self.insert_direction(6, 8, Directions.EAST.value)
        self.insert_direction(8, 9, Directions.WEST.value)
        # col 2
        self.insert_direction(4, 3, Directions.EAST.value)
        self.insert_direction(4, 5, Directions.WEST.value)
        self.insert_direction(9, 8, Directions.EAST.value)
        self.insert_direction(9, 10, Directions.WEST.value)
        # col 3
        self.insert_direction(2, 5, Directions.SOUTH.value)
        self.insert_direction(5, 2, Directions.NORTH.value)
        self.insert_direction(5, 4, Directions.EAST.value)
        self.insert_direction(5, 7, Directions.SOUTH.value)
        self.insert_direction(7, 5, Directions.NORTH.value)
        self.insert_direction(7, 10, Directions.SOUTH.value)
        self.insert_direction(10, 9, Directions.EAST.value)

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

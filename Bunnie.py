from enum import Enum
import random
import numpy as np

from Enemy import Enemy


class Bunnie_Class(Enemy):
    def __init__(self, difficulty):
        self.name = "Bunnie"
        self.movement_table = np.zeros((4, 13))
        self.position = 1
        self.difficulty = difficulty
        self.populate_movement_table()

    '''
                        Stage
                        | 1 |
    Maintenance  <-->   Main Room    <-->  Restrooms
    | 2 |------------| 3 |------------------| 5 |
                    VIXEN CAM
                  |  | 4 |            |         
    Closet      <-->  Left   |  Right          Kitchen     
    | 6 |-------| 7 |               | 8 |       | 9 |
                  |         YOU       |
                |10 |------|11|-----|12 |
    '''

    def populate_movement_table(self):
        # row 1
        self.insert_direction(1, 3, self.Directions.DOWN.value)
        # row 2
        self.insert_direction(2, 3, self.Directions.RIGHT.value)
        self.insert_direction(3, 5, self.Directions.RIGHT.value)
        self.insert_direction(3, 2, self.Directions.LEFT.value)
        self.insert_direction(3, 7, self.Directions.DOWN.value)
        self.insert_direction(5, 3, self.Directions.LEFT.value)
        # row 3
        self.insert_direction(6, 7, self.Directions.RIGHT.value)
        self.insert_direction(7, 6, self.Directions.LEFT.value)
        self.insert_direction(7, 3, self.Directions.UP.value)
        self.insert_direction(7, 10, self.Directions.DOWN.value)
        # row 4
        self.insert_direction(10, 7, self.Directions.UP.value)
        self.insert_direction(10, 11, self.Directions.RIGHT.value)

    def can_attack(self):
        if self.position == 11:
            return True
        return False

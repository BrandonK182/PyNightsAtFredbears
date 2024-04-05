'''
class Chick extending Enemy class
*********************************************
This is a specific enemy that has access to the
right hallway and the kitchen.
Chick has a longer cooldown than Bunnie.
**********************************************
variables
- name - name of the enemy type
- movement_table - table dictating where this enemy can move
- position - current room entity is occupying
- difficulty - how likely the entity is to switch position
- last_move_time - last time the entity had a movement check
- cooldown - how long the entity has to wait till they can move again
*********************************************
functions
- populate_movement_table() - fills the movement_table with the
                              room options that this specific enemy
                              can move towards
*********************************************
'''

import numpy as np
from Enemy import Enemy

class Chick(Enemy):
    def __init__(self, difficulty):
        self.name = "Chick"
        self.movement_table = np.zeros((4, 13))
        self.position = 1
        self.difficulty = difficulty
        self.populate_movement_table()
        self.last_move_time = 0
        self.cooldown = 5

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
        self.insert_direction(3, 8, self.Directions.DOWN.value)
        # command below leads main room to kitchen but down is already used for moving to hallway
        # so instead using unoccupied direction which is functionally the same
        self.insert_direction(3, 9, self.Directions.UP.value)
        self.insert_direction(5, 3, self.Directions.LEFT.value)
        # row 3
        self.insert_direction(8, 3, self.Directions.UP.value)
        self.insert_direction(8, 12, self.Directions.DOWN.value)
        self.insert_direction(9, 3, self.Directions.UP.value)
        # row 4
        self.insert_direction(12, 8, self.Directions.UP.value)
        self.insert_direction(12, 11, self.Directions.LEFT.value)

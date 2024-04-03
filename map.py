from camera import Camera

grey = (100, 100, 100)
white = (200, 200, 200)

class Map():
    def __init__(self, x, y, scale, thickness):
        self.map_x = x
        self.map_y = y
        self.cameras = list()
        self.array_x = list()
        self.array_y = list()
        self.width_arr = list()
        self.height_arr = list()
        self.scale = scale
        self.thick = thickness

    def insert_rect(self, x, y, w, h):
        self.array_x.append(x)
        self.array_y.append(y)
        self.width_arr.append(w)
        self.height_arr.append(h)

    def populate_map(self):
        # front stage
        self.insert_rect(self.map_x + 125 * self.scale, self.map_y + 25 * self.scale, 100 * self.scale, 25 * self.scale)
        # maintenance
        self.insert_rect(self.map_x + 25 * self.scale, self.map_y + 40 * self.scale, 35 * self.scale, 75 * self.scale)
        # main room
        self.insert_rect(self.map_x + 75 * self.scale, self.map_y + 50 * self.scale, 200 * self.scale, 150 * self.scale)
        # main - maintenance connector
        self.insert_rect(self.map_x + 60 * self.scale, self.map_y + 60 * self.scale, 15 * self.scale, 15 * self.scale)
        # Vixen's room
        self.insert_rect(self.map_x + 35 * self.scale, self.map_y + 135 * self.scale, 40 * self.scale, 55 * self.scale)
        # restrooms
        self.insert_rect(self.map_x + 290 * self.scale, self.map_y + 75 * self.scale, 25 * self.scale, 125 * self.scale)
        # main - restroom connector
        self.insert_rect(self.map_x + 275 * self.scale, self.map_y + 100 * self.scale, 15 * self.scale, 15 * self.scale)
        # left hallway
        self.insert_rect(self.map_x + 115 * self.scale, self.map_y + 215 * self.scale, 30 * self.scale, 100 * self.scale)
        # right hallway
        self.insert_rect(self.map_x + 200 * self.scale, self.map_y + 215 * self.scale, 30 * self.scale, 100 * self.scale)
        # main - left hall connector
        self.insert_rect(self.map_x + 122.5 * self.scale, self.map_y + 200 * self.scale, 15 * self.scale, 15 * self.scale)
        # main - right hall connector
        self.insert_rect(self.map_x + 207.5 * self.scale, self.map_y + 200 * self.scale, 15 * self.scale, 15 * self.scale)
        # janitor closet
        self.insert_rect(self.map_x + 75 * self.scale, self.map_y + 225 * self.scale, 30 * self.scale, 50 * self.scale)
        # closet - right hall connector
        self.insert_rect(self.map_x + 105 * self.scale, self.map_y + 235 * self.scale, 10 * self.scale, 10 * self.scale)
        # kitchen
        self.insert_rect(self.map_x + 250 * self.scale, self.map_y + 215 * self.scale, 75 * self.scale, 60 * self.scale)
        # kitchen - main connector
        self.insert_rect(self.map_x + 255 * self.scale, self.map_y + 200 * self.scale, 15 * self.scale, 15 * self.scale)
        # security room
        self.insert_rect(self.map_x + 155 * self.scale, self.map_y + 265 * self.scale, 35 * self.scale, 50 * self.scale)
        # security room
        self.insert_rect(self.map_x + 145 * self.scale, self.map_y + 285 * self.scale, 10 * self.scale, 10 * self.scale)
        # security - left connector
        self.insert_rect(self.map_x + 145 * self.scale, self.map_y + 285 * self.scale, 10 * self.scale, 10 * self.scale)
        # security - right connector
        self.insert_rect(self.map_x + 190 * self.scale, self.map_y + 285 * self.scale, 10 * self.scale, 10 * self.scale)

    def insert_camera(self, camera):
        self.cameras.append(camera)

    def populate_cameras(self):
        self.insert_camera(Camera("1A", self.map_x + 112.5*self.scale, self.map_y + 12.5*self.scale, self.scale))
        self.insert_camera(Camera("1B", self.map_x + 100*self.scale, self.map_y + 50*self.scale, self.scale))
        self.insert_camera(Camera("1C", self.map_x + 70*self.scale, self.map_y + 130*self.scale, self.scale))
        self.insert_camera(Camera("2A", self.map_x + 115*self.scale, self.map_y + 235*self.scale, self.scale))
        self.insert_camera(Camera("2B", self.map_x + 115*self.scale,  self.map_y + 265*self.scale, self.scale))
        self.insert_camera(Camera("C", self.map_x + 55*self.scale, self.map_y + 235*self.scale, self.scale))

        self.insert_camera(Camera("4A", self.map_x + 205*self.scale, self.map_y + 235*self.scale, self.scale))
        self.insert_camera(Camera("4B", self.map_x + 205*self.scale, self.map_y + 265*self.scale, self.scale))
        self.insert_camera(Camera("5", self.map_x + 5*self.scale, self.map_y + 75*self.scale, self.scale))
        self.insert_camera(Camera("6", self.map_x + 295*self.scale, self.map_y + 225*self.scale, self.scale))
        self.insert_camera(Camera("7", self.map_x + 295*self.scale, self.map_y + 80*self.scale, self.scale))

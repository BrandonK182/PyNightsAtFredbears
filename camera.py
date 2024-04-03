class Camera:
    def __init__(self, name, x, y, scale):
        self.name = name
        self.x = x
        self.y = y
        self.w = 40*scale
        self.h = 25*scale
        self.thick = 2

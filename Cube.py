#from gameobjects.vector2 import Vector2
import math
class Cube():
    def __init__(self, position, image):
        self.cube_image = image
        self.position = position
        self.rotation = 0
        self.state = 0
        self.points = [position + (-20, -20), position + (20, -20), position + (20, 20), position + (-20, 20)]

    def updatepoints(self):
        rotation = -self.rotation % 90 / 180 * math.pi
        sin = 20 * math.sin(rotation)
        cos = 20 * math.cos(rotation)
        self.points[0] = self.position + (sin, -cos) + (-cos, -sin)
        self.points[1] = self.position + (sin, -cos) + (cos, sin)
        self.points[2] = self.position + (-sin, cos) + (cos, sin)
        self.points[3] = self.position + (-sin, cos) + (-cos, -sin)

    def update(self, c, x):
        if self.state == 0:
            self.position.y = c
            self.rotation = 0
        if self.state == 1:
            self.position.y = 0.01 * x * x - 2 * x + c
            self.rotation = -0.9 * x
            self.updatepoints()
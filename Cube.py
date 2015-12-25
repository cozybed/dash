from gameobjects.vector2 import Vector2
import math
class Cube():
    def __init__(self, position, image):
        self.cube_image = image
        self.position = position
        self.rotation = 0
        self.state = 0
        self.points = [position + (-20, -20), position + (20, -20), position + (20, 20), position + (-20, 20)]
        self.role = 0
        self.up = 0

    def initposition(self):
        position = Vector2(320, 367.9)
        self.position = position
        self.rotation = 0
        self.state = 0
        self.points = [position + (-20, -20), position + (20, -20), position + (20, 20), position + (-20, 20)]

    def initall(self):
        self.initposition()
        self.state = 0
        self.role = 0
        self.up = 0

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
           # self.position.y = 0.01 * x * x - 2 * x + c
            if self.role == 0:
                self.position.y = 0.01 * x * x - 2 * x + c
                self.rotation = -0.9 * x
            if self.role == 1:
                if x < 100:
                    self.position.y = 0.01 * x * x - 2 * x + c
                    self.rotation = math.atan(-0.01 * x + 2) / math.pi * 180
                else:
                    self.position.y = 0.004 * x * x - 0.8 * x + c - 60
                    self.rotation = math.atan(-0.004 * x + 0.8) / math.pi * 180
            if self.role == 2:
                if self.up == 0:
                    self.position.y = x + c
                    self.rotation = 45
                else:
                    self.position.y = -x + c
                    self.rotation = -45
            self.updatepoints()
        if self.state == 2:
            if self.role == 0:
                self.position.y = 0.01 * x * x + c
                self.rotation = -0.9 * x
            if self.role == 1:
                self.position.y = 0.004 * x * x + c
                self.rotation = math.atan(-0.004 * x) / math.pi * 180
            self.updatepoints()
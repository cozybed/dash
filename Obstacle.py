from gameobjects.vector2 import Vector2
class Obstacle():
    def __init__(self, position, image, style):
        self.position = position
        self.style = style
        self.image = image
        self.width, self.height = self.image.get_size()
        self.points = [Vector2(position.x, position.y), position + (self.width, 0), position + (self.width, self.height), position + (0, self.height)]

    def Move(self, direction, distance):
        self.position += direction * distance
        for x in self.points:
            x += direction * distance

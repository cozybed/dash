class Cube(object):
    def __init__(self, position, image):
        self.position = position
        self.state = 0
        self.speed = 470
        self.rotation = 0
        self.ori_inc = 0
        self.rotation_speed = 400
        self.cube_image = image

    def update_position(self, increment, rotation_increment):
        if self.state == 0:
            self.rotation = 0
            return
        if self.state == 1:
            self.position.y -= increment
            self.rotation -= rotation_increment
            self.ori_inc -= increment

            if self.rotation < -90:
                self.state = -1
                self.rotation = -90
        if self.state == -1:
            self.position.y += increment
            self.ori_inc+=increment
            self.rotation -= rotation_increment
        return

    def move(self):
        self.state = 1

    def stop(self):
        self.state = 0

    def GetLines(self):
        lines = []


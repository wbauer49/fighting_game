
class Color:

    def __init__(self, r, g, b, a=255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def as_tuple(self):
        return self.r, self.g, self.b


class Object:
    x = 0
    y = 0
    r = 40
    color = Color(1, 1, 1, a=150)
    is_facing_right = True

    sub_objects = []

    def calculate_update(self):
        for obj in self.sub_objects:
            obj.calculate_update()

    def update_sub_objects(self):
        for sub_obj in self.sub_objects:
            sub_obj.calculate_update()
            sub_obj.update_sub_objects()

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_color(self):
        return self.color

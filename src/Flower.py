import random
from numpy import cos, sin

colors = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255),
          (128, 0, 255), (255, 0, 128)]

max_radio = 50


class Flower:
    def __init__(self):
        self.color = ""
        self.angle = 0
        self.radio = 0
        self.x = 0
        self.y = 0
        self.other_flower_pollen = []
        self.position_id = 0

    def __str__(self):
        return "color:{}, angle:{}, radio:{}".format(self.color, self.angle, self.radio)

    def add_pollen(self, other_flowers):
        self.other_flower_pollen += other_flowers
        # print("pollen: ", self.other_flower_pollen)

    def generate_parent(self):
        self.color = random.choice(colors)
        self.angle = random.uniform(0, 360)
        self.radio = random.uniform(0, max_radio)
        self.x = self.radio * cos(self.angle)
        self.y = self.radio * sin(self.angle)

        tem_x = 50 + int(round(self.x, 0))
        tem_y = 50 - int(round(self.y, 0))
        self.position_id = tem_x + 100 * tem_y

        # print(self.position_id)
        # print("AQUIIIIIIII", int(round(self.x, 0)), int(round(self.y, 0)), self.color)

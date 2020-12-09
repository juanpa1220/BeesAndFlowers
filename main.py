import random

directions = ["N", "S", "E", "O", "NE", "NO", "SE", "SO"]
colors = [(10, 100, 200), (10, 100, 200), (10, 100, 200), (10, 100, 200), (10, 100, 200), (10, 100, 200),
          (10, 100, 200), (10, 100, 200)]
num_bees = 100
num_flowers = 400
num_nectar = 0
global_traveled_distance = 10000


class Bee:
    def __init__(self):
        self.favorite_color = ""
        self.favorite_direction = ""
        self.deflection_angle = 0
        self.max_distance = 0

        self.traveled_distance = 0
        self.found_flowers = 0

        self.genes = self.favorite_color + self.favorite_direction



class Flower:
    def __init__(self):
        self.color = random.choice(colors)
        self.angle = 0
        self.radio = 0
        self.x = 0
        self.y = 0
        self.bee_pollen = []


def init():
    while (True):
        pass
        # iteración acá


if __name__ == '__main__':
    init()

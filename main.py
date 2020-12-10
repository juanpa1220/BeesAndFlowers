import random
from numpy import cos, sin, sqrt

# directions = ["N_", "S_", "E_", "O_", "NE", "NO", "SE", "SO"]
directions = [270, 90, 0, 180, 315, 225, 45, 135]
colors = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255),
          (128, 0, 255), (255, 0, 128)]

num_bees = 10
num_flowers = 300
num_nectar = 0
global_traveled_distance = 10000
max_radio = 100


class Bee:
    def __init__(self):
        self.favorite_color = ""
        self.favorite_direction = 0
        self.deflection_angle = 0
        self.max_distance = 0
        self.genes = ""
        self.x = 0
        self.y = 0

        self.traveled_distance = 0
        self.max_traveled_distance = 2 * max_radio
        self.found_flowers = 0

    def __str__(self):
        return self.favorite_color, self.favorite_direction, self.deflection_angle, self.max_distance

    def generate_parent(self):
        self.favorite_color = random.choice(colors)
        self.favorite_direction = random.choice(directions)
        self.deflection_angle = round(random.uniform(10, 45), 2)
        self.max_distance = round(random.uniform(max_radio / 2, max_radio), 2)

        # self.genes = self.favorite_color + self.favorite_direction + self.deflection_angle + self.max_distance

    def route(self, flowers):
        flowers_in_area = []
        route = []

        for flower in flowers:
            if self.favorite_direction - self.deflection_angle < flower.angle < self.favorite_direction + self.deflection_angle:
                flowers_in_area.append(flower)

        for flower in flowers_in_area:
            if flower.color == self.favorite_color:
                route.append(flower)

        route.sort(key=lambda f: f.radio)

        print("\n\n\nfavs")
        for i in route:
            print(i)

        print("\n\n")

        # flag = True
        while self.traveled_distance <= self.max_traveled_distance:
            if len(route) > 0:
                distance = sqrt((route[0].x - self.x) ** 2 + (route[0].y - self.y) ** 2)
                if self.traveled_distance + distance > self.max_traveled_distance:
                    print("se salio", self.traveled_distance + distance)
                    # flag = False
                    break
                else:
                    self.found_flowers += 1
                    self.x = route[0].x
                    self.y = route[0].y
                    self.traveled_distance += distance
                    print("recorrida: ", self.traveled_distance)
                    route.remove(route[0])

            else:
                print("aqui")
                closest = max_radio * 4
                closest_flower = None
                if len(flowers_in_area) > 0:
                    for flower in flowers_in_area:
                        distance = sqrt((flower.x - self.x) ** 2 + (flower.y - self.y) ** 2)
                        if distance < closest:
                            closest = distance
                            closest_flower = flower

                    if self.traveled_distance + closest > self.max_traveled_distance:
                        print("se salio2", self.traveled_distance + closest)
                        # flag = False
                        break
                    else:
                        self.found_flowers += 1
                        self.x = closest_flower.x
                        self.y = closest_flower.y
                        self.traveled_distance += closest
                        print("recorrida2: ", self.traveled_distance)
                        flowers_in_area.remove(closest_flower)
                else:
                    # flag = False
                    break

    def mutate(self, parent):
        print()


class Flower:
    def __init__(self):
        self.color = ""
        self.angle = 0
        self.radio = 0
        self.x = 0
        self.y = 0
        self.bee_pollen = []

    def __str__(self):
        return "color:{}, angle:{}, radio:{}".format(self.color, self.angle, self.radio)

    def generate_parent(self):
        self.color = random.choice(colors)
        self.angle = random.uniform(0, 360)
        self.radio = random.uniform(0, max_radio)
        self.x = self.radio * cos(self.angle)
        self.y = self.radio * sin(self.angle)


def init():
    num_bees_aux = 0
    num_flowers_aux = 0

    Bee().generate_parent()
    bees = []
    flowers = []

    while num_bees_aux < num_bees:
        bee = Bee()
        bee.generate_parent()
        bees.append(bee)
        num_bees_aux += 1

    while num_flowers_aux < num_flowers:
        flower = Flower()
        flower.generate_parent()
        flowers.append(flower)
        num_flowers_aux += 1

    # for bee in bees:
    #     bee.route(flowers)

    bees[0].route(flowers)

    # print(bees)
    # for i in bees:
    #     print(i)

    # for i in flowers:
    #     print(i)

    # while True:
    #     break


if __name__ == '__main__':
    init()

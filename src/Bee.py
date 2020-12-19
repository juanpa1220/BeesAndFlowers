import random
from numpy import sqrt, cos, sin

colors = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255),
          (128, 0, 255), (255, 0, 128)]
colors_bin = ['000', '001', '010', '011', '100', '101', '110', '111']
directions = [270, 90, 0, 180, 315, 225, 45, 135]
directions_bin = ['000', '001', '010', '011', '100', '101', '110', '111']
max_radio = 50


class Bee:
    def __init__(self, origin=True, favorite_color="", favorite_direction=0, deflection_angle=0, max_distance=0,
                 parents=None, name=""):

        if parents is None:
            parents = []

        self.origin = origin  # true si sale del panal, flase si no
        self.favorite_color = favorite_color
        self.favorite_direction = favorite_direction
        self.deflection_angle = deflection_angle
        self.max_distance = max_distance

        self.parents = parents
        self.name = name

        self.genes = []
        self.genes_bin = ""
        self.x = 0
        self.y = 0

        self.traveled_distance = 0
        self.max_traveled_distance = 2 * max_radio
        self.visited_flowers = []
        self.adaptability_percentage = 0
        self.max_route_recursions = 10

    def __str__(self):
        return "name: {} \t\t found flowers: {} \t\t adaptability: {} \t\t color: {} \t\t direction: {}" \
               " \t\t angle: {} \t\t max distance: {} \t\t origin: {}".format(self.name,
                                                                              len(self.visited_flowers),
                                                                              round(self.adaptability_percentage, 2),
                                                                              self.favorite_color,
                                                                              self.favorite_direction,
                                                                              self.deflection_angle,
                                                                              self.max_distance,
                                                                              self.origin)

    def set_up_genes(self):
        self.genes += [self.origin, self.favorite_color, self.favorite_direction, self.deflection_angle,
                       self.max_distance]

        self.genes_bin += str(self.origin) + \
                          colors_bin[colors.index(self.favorite_color)] + \
                          directions_bin[directions.index(self.favorite_direction)] + \
                          '{:05b}'.format(int(self.deflection_angle)) + \
                          '{:06b}'.format(int(self.max_distance))

    def set_up_origin(self):
        if self.origin:
            self.x = 0
            self.y = 0
        else:
            self.x = self.max_distance * cos(self.favorite_direction)
            self.y = self.max_distance * sin(self.favorite_direction)

    def generate_parent(self):
        self.favorite_color = random.choice(colors)
        self.favorite_direction = random.choice(directions)

        self.deflection_angle = random.randint(0, 31)
        self.max_distance = random.randint(0, max_radio)

        self.origin = random.choice([0, 1])

        self.set_up_origin()
        self.set_up_genes()

    def route(self, flowers):
        flowers_in_area = []
        favorite_flowers = []  # flowers in area with bee's fav color

        for flower in flowers:
            if (
                    self.favorite_direction - self.deflection_angle < flower.angle < self.favorite_direction + self.deflection_angle) and (
                    flower.radio <= self.max_distance):
                flowers_in_area.append(flower)

        for flower in flowers_in_area:
            if flower.color == self.favorite_color:
                favorite_flowers.append(flower)
        favorite_flowers.sort(key=lambda f: f.radio)

        while self.traveled_distance <= self.max_traveled_distance:
            if len(favorite_flowers) > 0:
                distance = sqrt((favorite_flowers[0].x - self.x) ** 2 + (favorite_flowers[0].y - self.y) ** 2)
                if self.traveled_distance + distance > self.max_traveled_distance:
                    break
                else:
                    if favorite_flowers[0] not in self.visited_flowers:
                        favorite_flowers[0].add_pollen(self.visited_flowers)
                        self.visited_flowers.append(favorite_flowers[0])

                        self.x = favorite_flowers[0].x
                        self.y = favorite_flowers[0].y
                        self.traveled_distance += distance

                        flowers_in_area.remove(favorite_flowers[0])
                        favorite_flowers.remove(favorite_flowers[0])
                    else:
                        self.x = favorite_flowers[0].x
                        self.y = favorite_flowers[0].y
                        self.traveled_distance += distance
                        flowers_in_area.remove(favorite_flowers[0])
                        favorite_flowers.remove(favorite_flowers[0])

            else:
                closest = max_radio * 4
                closest_flower = None
                if len(flowers_in_area) > 0:
                    for flower in flowers_in_area:
                        distance = sqrt((flower.x - self.x) ** 2 + (flower.y - self.y) ** 2)
                        if distance < closest:
                            closest = distance
                            closest_flower = flower

                    if self.traveled_distance + closest > self.max_traveled_distance:
                        break
                    else:
                        if closest_flower not in self.visited_flowers:
                            closest_flower.add_pollen(self.visited_flowers)
                            self.visited_flowers.append(closest_flower)

                            self.x = closest_flower.x
                            self.y = closest_flower.y
                            self.traveled_distance += closest
                            flowers_in_area.remove(closest_flower)
                        else:
                            self.x = closest_flower.x
                            self.y = closest_flower.y
                            self.traveled_distance += closest
                            flowers_in_area.remove(closest_flower)

                else:
                    if self.max_route_recursions > 0:
                        self.max_route_recursions -= 1
                        self.favorite_direction = random.choice(directions)
                        self.route(flowers)
                        break

                    else:
                        break

import random
from numpy import sqrt

colors = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255),
          (128, 0, 255), (255, 0, 128)]
directions = [270, 90, 0, 180, 315, 225, 45, 135]
max_radio = 100


class Bee:
    def __init__(self):
        self.favorite_color = ""
        self.favorite_direction = 0
        self.deflection_angle = 0
        self.max_distance = 0
        self.genes = []
        self.x = 0
        self.y = 0

        self.traveled_distance = 0
        self.max_traveled_distance = 2 * max_radio
        self.visited_flowers = []
        self.adaptability_percentage = 0

    def __str__(self):
        return "found flowers: {} \t adaptability: {} \t\t color: {} \t\t direction: {}" \
               " \t\t angle: {} \t\t max distance: {}".format(len(self.visited_flowers),
                                                              round(self.adaptability_percentage, 2),
                                                              self.favorite_color,
                                                              self.favorite_direction,
                                                              self.deflection_angle,
                                                              self.max_distance)

    def generate_parent(self):
        self.favorite_color = random.choice(colors)
        self.favorite_direction = random.choice(directions)
        self.deflection_angle = round(random.uniform(10, 45), 2)
        self.max_distance = round(random.uniform(max_radio / 2, max_radio), 2)

        self.genes += [self.favorite_color, self.favorite_direction, self.deflection_angle, self.max_distance]

    def route(self, flowers):
        flowers_in_area = []
        favorite_flowers = []  # flowers in area with bee's fav color

        for flower in flowers:
            if self.favorite_direction - self.deflection_angle < flower.angle \
                    < self.favorite_direction + self.deflection_angle and flower.radio <= self.max_distance:
                flowers_in_area.append(flower)
        for flower in flowers_in_area:
            if flower.color == self.favorite_color:
                favorite_flowers.append(flower)
        favorite_flowers.sort(key=lambda f: f.radio)

        print("\n\nin area: ", len(flowers_in_area))
        print("favs")
        for i in favorite_flowers:
            print(i)

        while self.traveled_distance <= self.max_traveled_distance:
            if len(favorite_flowers) > 0:
                distance = sqrt((favorite_flowers[0].x - self.x) ** 2 + (favorite_flowers[0].y - self.y) ** 2)
                if self.traveled_distance + distance > self.max_traveled_distance:
                    print("se salio", self.traveled_distance + distance)
                    break
                else:
                    favorite_flowers[0].add_pollen(self.visited_flowers)
                    self.visited_flowers.append(favorite_flowers[0])

                    self.x = favorite_flowers[0].x
                    self.y = favorite_flowers[0].y
                    self.traveled_distance += distance
                    print("recorrida: ", self.traveled_distance)

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
                        print("se salio2", self.traveled_distance + closest)
                        break
                    else:
                        closest_flower.add_pollen(self.visited_flowers)
                        self.visited_flowers.append(closest_flower)

                        self.x = closest_flower.x
                        self.y = closest_flower.y
                        self.traveled_distance += closest
                        print("recorrida2: ", self.traveled_distance)
                        flowers_in_area.remove(closest_flower)

                else:
                    print("\t\tCAMBIO DE DIRECCION")
                    self.favorite_direction = self.favorite_direction = random.choice(directions)
                    self.route(flowers)

                    break

    def mutate(self, parent):
        print()

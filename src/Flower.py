import random
from numpy import cos, sin

colors = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255),
          (128, 0, 255), (255, 0, 128)]
colors_bin = ['000', '001', '010', '011', '100', '101', '110', '111']
max_radio = 50


class Flower:
    def __init__(self, color="", angle=0, radio=0):
        self.color = color
        self.angle = angle
        self.radio = radio
        self.genes = ""

        self.x = 0
        self.y = 0
        self.other_flower_pollen = []
        self.position_id = 0

    def __str__(self):
        return "color:{}, angle:{}, radio:{}, x: {}, y: {}".format(self.color, self.angle, self.radio, self.x, self.y)

    def set_up_genes(self):
        self.genes += colors_bin[colors.index(self.color)] + '{:012b}'.format(int(self.angle)) + '{:06b}'.format(
            int(self.radio))

    def set_up_position(self):
        self.x = self.radio * cos(self.angle)
        self.y = self.radio * sin(self.angle)
        tem_x = 50 + int(round(self.x, 0))
        tem_y = 50 - int(round(self.y, 0))
        self.position_id = tem_x + 100 * tem_y

    def mutate(self):
        if len(self.other_flower_pollen) == 0:
            new_flower = Flower()
            new_flower.generate_parent()
            return new_flower
        else:
            parent2 = random.choice(self.other_flower_pollen)
            genes_parent2 = parent2.genes

            num = random.randint(0, len(genes_parent2))
            side = random.choice([0, 1])
            if side:
                child_gen1 = self.genes[num:]
                child_gen2 = genes_parent2[:num]
                child = child_gen2 + child_gen1
            else:
                child_gen1 = self.genes[:num]
                child_gen2 = genes_parent2[num:]
                child = child_gen1 + child_gen2

            tem_color = colors[int("0b" + child[1:4], 2)]
            tem_angle = int("0b" + child[4:16], 2)
            tem_radio = int("0b" + child[16:], 2)

            if tem_angle >= 360:
                tem_angle = 359
            if tem_radio > max_radio:
                tem_radio = max_radio

            new_flower = Flower(tem_color, tem_angle, tem_radio)
            new_flower.set_up_position()
            new_flower.set_up_genes()

            return new_flower

    def add_pollen(self, other_flowers):
        self.other_flower_pollen += other_flowers

    def generate_parent(self):
        self.color = random.choice(colors)
        self.angle = random.randint(0, 360)
        self.radio = random.randint(0, max_radio)
        self.set_up_position()
        self.set_up_genes()

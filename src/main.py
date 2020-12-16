from src.Bee import *
from src.Flower import *
from src.window import *
import numpy

num_bees = 10
num_flowers = 100

num_nectar = 0
global_traveled_distance = 10000
current_generation = 1
last_generation = 1
num_generations = 1
generations = {}
genes_generation = []

total_num_bees = 1
total_num_flowers = 0


def init():
    global total_num_bees
    genes_generation1 = ""
    num_bees_aux = 0
    num_flowers_aux = 0
    bees = []
    flowers = []

    while num_bees_aux < num_bees:
        bee = Bee()
        bee.generate_parent()
        bee.name = "bee {}".format(total_num_bees)
        bees.append(bee)
        num_bees_aux += 1
        total_num_bees += 1

    while num_flowers_aux < num_flowers:
        flower = Flower()
        flower.generate_parent()
        flowers.append(flower)
        num_flowers_aux += 1

    total_visited_flowers = 0
    percentage_list = []
    for bee in bees:
        bee.route(flowers)
        total_visited_flowers += len(bee.visited_flowers)

    for bee in bees:
        percentage = len(bee.visited_flowers) / total_visited_flowers
        bee.adaptability_percentage = percentage
        percentage_list.append(percentage)

    generations[last_generation] = {"bees": bees, "flowers": flowers}
    print("\n\nRESULT\n")
    for bee in bees:
        print(bee)

    print("\n\nEscogidas:")
    selected_bees = []
    tem_selected_bees = numpy.random.choice(range(0, len(bees)), size=len(bees), p=percentage_list)
    for i in tem_selected_bees:
        selected_bees.append(bees[i])

    for i in selected_bees:
        print(i)

    for i in range(0, len(selected_bees), 2):
        parent1 = selected_bees[i].genes_bin
        parent2 = selected_bees[i + 1].genes_bin

        num = random.randint(0, len(parent1))

        parent1_1 = parent1[:num]
        parent1_2 = parent1[num:]

        parent2_1 = parent2[:num]
        parent2_2 = parent2[num:]

        children1 = parent2_1 + parent1_2
        children2 = parent1_1 + parent2_2

        genes_generation1 += children1
        genes_generation1 += children2

        print("Padres1", parent1, "Padres2", parent2, "hijos", children1, " ", children2)

    # Aqui se hace la mutacion

    genes_mutated = list(genes_generation1)

    for i in range(mutation):
        muta = random.randint(0, len(genes_generation1) - 1)
        if genes_mutated[muta] == '0':
            genes_mutated[muta] = '1'
        else:
            genes_mutated[muta] = '0'

    genes_generation1 = str(genes_mutated)
    genes_mutated_final = ""

    # Aqui se transforma de lista a string denuevo
    for i in range(len(genes_generation1)):
        if genes_generation1[i] == '1' or genes_generation1[i] == '0':
            genes_mutated_final += genes_generation1[i]

    # Aqui se guarda la nueva generacion
    left = 0
    right = 18
    for i in range(num_bees):
        tem_genes_bee = genes_mutated_final[left:right]
        genes_generation.append(tem_genes_bee)
        left += 18
        right += 18
        # print(genes_generation)

    for i in range(len(genes_generation)):
        tem_genes_bee = genes_generation[i]
        print(tem_genes_bee)
        tem_origin = tem_genes_bee[0]
        tem_color = colors[(int("0b" + tem_genes_bee[1:4], 2))]
        tem_direction = directions[(int("0b" + tem_genes_bee[4:7], 2))]
        tem_deflection_angle = int("0b" + tem_genes_bee[7:12], 2)
        tem_max_distance = int("0b" + tem_genes_bee[12:], 2)
        if tem_max_distance > 50:
            tem_max_distance = 50

        print(tem_origin, "  ", tem_color, "  ", tem_direction, " ", tem_deflection_angle, " ", tem_max_distance)

    # GUI
    root = Tk()
    window = Window(root)
    window.pack(fill=BOTH, expand=1)
    window.fill_board(flowers, str(current_generation))

    root.wm_title("Bees and Flowers")
    root.geometry("1200x800")

    root.mainloop()


def cross_bees(parent1, parent2):
    print()


def click_next():
    print("next")


def click_previous():
    print("previous")


if __name__ == '__main__':
    init()

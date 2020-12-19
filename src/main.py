from src.Bee import *
from src.Flower import *
from src.window import *
import numpy
import matplotlib.pyplot as plt

values_to_plot = []
num_bees = 10
num_flowers = 100

num_nectar = 0
global_traveled_distance = 10000
last_generation = 1
num_generations = 20
generations = {}

total_num_bees = 1
total_num_flowers = 0
num_mutations = num_bees // 2


def init():
    global total_num_bees
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

    make_new_generation(bees, flowers)

    # GUI
    x = range(1, len(values_to_plot) + 1)
    y = values_to_plot
    plt.plot(x, y)
    z = numpy.polyfit(x, y, 1)
    p = numpy.poly1d(z)
    plt.plot(x, p(x), "r--")
    plt.legend(('Adaptability Distribution', 'Trend Line'), prop={'size': 10}, loc='upper left')

    plt.xlabel('num Generation')
    plt.ylabel('num Collected Flowers')
    plt.title("Generations vs Flowers Collected")
    plt.show()

    root = Tk()
    window = Window(generations, root)
    window.pack(fill=BOTH, expand=1)
    root.wm_title("Bees and Flowers")
    root.geometry("1200x800")
    root.mainloop()


def make_new_generation(bees, flowers):
    global num_generations, last_generation

    total_visited_flowers = 0
    percentage_list = []

    print("\t\t\t\t---- GENERATION", last_generation, "-----")
    for bee in bees:
        bee.route(flowers)
        total_visited_flowers += len(bee.visited_flowers)

    for bee in bees:
        percentage = len(bee.visited_flowers) / total_visited_flowers
        bee.adaptability_percentage = percentage
        percentage_list.append(percentage)

    generations[last_generation] = {"bees": bees, "flowers": flowers}
    last_generation += 1
    values_to_plot.append(total_visited_flowers)

    print("\n\nWITHOUT SELECTION\n")
    for bee in bees:
        print(bee)

    print("\n\nTOTAL VISITED FLOWERS: ", total_visited_flowers)

    print("\n\nSELECTION:")
    selected_bees = []
    tem_selected_bees = numpy.random.choice(range(0, len(bees)), size=len(bees), p=percentage_list)
    for i in tem_selected_bees:
        selected_bees.append(bees[i])

    for i in selected_bees:
        print(i)

    print("\n\n\n\n")

    genes_generation1 = ""
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

    # Aqui se hace la mutacion
    new_flower_generation = []
    for flower in flowers:
        new_flower_generation.append(flower.mutate())

    bees_new_generation = mutate_bees(genes_generation1, selected_bees)

    if num_generations > 1:
        num_generations -= 1
        make_new_generation(bees_new_generation, new_flower_generation)


def mutate_bees(genes_generation, parents):
    global total_num_bees
    genes_mutated = list(genes_generation)

    for i in range(num_mutations):
        mutation = random.randint(0, len(genes_generation) - 1)
        if genes_mutated[mutation] == '0':
            genes_mutated[mutation] = '1'
        else:
            genes_mutated[mutation] = '0'

    genes_generation = str(genes_mutated)
    genes_mutated_final = ""

    # Aqui se transforma de lista a string denuevo
    for i in range(len(genes_generation)):
        if genes_generation[i] == '1' or genes_generation[i] == '0':
            genes_mutated_final += genes_generation[i]

    # Aqui se guarda la nueva generacion
    genes_generation = []
    left = 0
    right = 18
    for i in range(num_bees):
        tem_genes_bee = genes_mutated_final[left:right]
        genes_generation.append(tem_genes_bee)
        left += 18
        right += 18

    next_generation = []
    for i in range(len(genes_generation)):
        tem_genes_bee = genes_generation[i]
        tem_origin = tem_genes_bee[0]
        tem_color = colors[(int("0b" + tem_genes_bee[1:4], 2))]
        tem_direction = directions[(int("0b" + tem_genes_bee[4:7], 2))]
        tem_deflection_angle = int("0b" + tem_genes_bee[7:12], 2)
        tem_max_distance = int("0b" + tem_genes_bee[12:], 2)

        if tem_max_distance > max_radio:
            tem_max_distance = max_radio

        next_generation.append(
            Bee(tem_origin, tem_color, tem_direction, tem_deflection_angle, tem_max_distance, None,
                "bee {}".format(total_num_bees)))
        total_num_bees += 1

    for i in range(0, len(parents), 2):
        next_generation[i].parents += [parents[i], parents[i + 1]]
        next_generation[i + 1].parents += [parents[i], parents[i + 1]]

    for bee in next_generation:
        bee.set_up_origin()
        bee.set_up_genes()

    return next_generation


if __name__ == '__main__':
    init()

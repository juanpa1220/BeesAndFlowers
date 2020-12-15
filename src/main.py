from src.Bee import *
from src.Flower import *
from src.main_window import *

num_bees = 10
num_flowers = 100

num_nectar = 0
global_traveled_distance = 10000


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

    total_visited_flowers = 0
    percentage_list = []
    for bee in bees:
        bee.route(flowers)
        total_visited_flowers += len(bee.visited_flowers)

    for bee in bees:
        percentage = len(bee.visited_flowers) / total_visited_flowers
        bee.adaptability_percentage = percentage
        percentage_list.append(percentage)

    print("\n\nRESULT\n")
    for bee in bees:
        print(bee)

    print("\n\nEscogidas:")
    selected_bees = random.choices(bees, weights=percentage_list, k=len(bees))
    for i in selected_bees:
        print(i)

    for i in range(len(selected_bees) // 2):
        parent1 = random.choice(selected_bees)
        selected_bees.remove(parent1)
        parent2 = random.choice(selected_bees)
        selected_bees.remove(parent2)

    # GUI
    main_window = MainWindow()
    while not main_window.game_done:
        main_window.show_window()


def cross_bees(parent1, parent2):
    print()


if __name__ == '__main__':
    init()

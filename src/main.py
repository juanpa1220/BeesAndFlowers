from src.Bee import *
from src.Flower import *
from src.window import *

num_bees = 10
num_flowers = 100

num_nectar = 0
global_traveled_distance = 10000
current_generation = 1
last_generation = 1
num_generations = 1
generations = {}

total_num_bees = 1
total_num_flowers = 0


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
    selected_bees = random.choices(bees, weights=percentage_list, k=len(bees))
    for i in selected_bees:
        print(i)

    for i in range(len(selected_bees) // 2):
        parent1 = random.choice(selected_bees)
        selected_bees.remove(parent1)
        parent2 = random.choice(selected_bees)
        selected_bees.remove(parent2)

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

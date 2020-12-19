from tkinter import *
from src.main import num_generations
from math import sqrt

board_dimensions = [800, 800]
window_dimensions = [1200, 800]
num_quadrants = 100


class Window(Frame):
    def __init__(self, generations, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.generations = generations
        self.current_generation = 1

        self.rows = num_quadrants
        self.columns = num_quadrants
        self.quadrants_dimension = board_dimensions[0] / num_quadrants
        self.quadrants_color = "white"
        self.flag = True
        self.selected_bee = None

        self.board = Canvas(
            width=board_dimensions[0],
            height=board_dimensions[1],
        )
        self.board.pack(side=LEFT, fill=BOTH, expand=True)

        self.details = Canvas(
            width=window_dimensions[0] - board_dimensions[0],
            height=window_dimensions[1],
        )
        self.details.pack(side=RIGHT, fill=BOTH, expand=True)

        Label(self.details, text="Generation: ", font=("Helvetica", 18)).place(x=140, y=20)
        self.lbl_generation = StringVar()
        Label(self.details, textvariable=self.lbl_generation, font=("Helvetica", 18)).place(x=240, y=20)

        Label(self.details, text="Details", font=("Helvetica", 18)).place(x=150, y=360)
        Label(self.details, text="Name:", font=("Helvetica", 14)).place(x=50, y=400)
        Label(self.details, text="Origin:", font=("Helvetica", 14)).place(x=50, y=430)
        Label(self.details, text="Fav Color:", font=("Helvetica", 14)).place(x=50, y=460)
        Label(self.details, text="Fav Direction:", font=("Helvetica", 14)).place(x=50, y=490)
        Label(self.details, text="Angle:", font=("Helvetica", 14)).place(x=50, y=520)
        Label(self.details, text="Max Distance:", font=("Helvetica", 14)).place(x=50, y=550)
        Label(self.details, text="Binary Genes:", font=("Helvetica", 14)).place(x=50, y=580)
        Label(self.details, text="Found Flowers:", font=("Helvetica", 14)).place(x=50, y=610)
        Label(self.details, text="Adaptability:", font=("Helvetica", 14)).place(x=50, y=640)
        Label(self.details, text="Parents:", font=("Helvetica", 14)).place(x=50, y=670)

        self.lbl_name = StringVar()
        Label(self.details, textvariable=self.lbl_name, font=("Helvetica", 14)).place(x=160, y=400)
        self.lbl_origin = StringVar()
        Label(self.details, textvariable=self.lbl_origin, font=("Helvetica", 14)).place(x=160, y=430)
        self.lbl_color = StringVar()
        Label(self.details, textvariable=self.lbl_color, font=("Helvetica", 14)).place(x=160, y=460)
        self.lbl_dir = StringVar()
        Label(self.details, textvariable=self.lbl_dir, font=("Helvetica", 14)).place(x=160, y=490)
        self.lbl_angle = StringVar()
        Label(self.details, textvariable=self.lbl_angle, font=("Helvetica", 14)).place(x=160, y=520)
        self.lbl_max_dis = StringVar()
        Label(self.details, textvariable=self.lbl_max_dis, font=("Helvetica", 14)).place(x=160, y=550)
        self.lbl_genes = StringVar()
        Label(self.details, textvariable=self.lbl_genes, font=("Helvetica", 14)).place(x=160, y=580)
        self.lbl_found = StringVar()
        Label(self.details, textvariable=self.lbl_found, font=("Helvetica", 14)).place(x=160, y=610)
        self.lbl_adap = StringVar()
        Label(self.details, textvariable=self.lbl_adap, font=("Helvetica", 14)).place(x=160, y=640)
        self.lbl_parent1 = StringVar()
        Label(self.details, textvariable=self.lbl_parent1, font=("Helvetica", 14)).place(x=160, y=670)
        self.lbl_parent2 = StringVar()
        Label(self.details, textvariable=self.lbl_parent2, font=("Helvetica", 14)).place(x=160, y=700)

        self.btn_previous = Button(self.details, text="Previous", command=self.click_previous,
                                   highlightbackground='#3E4149')
        self.btn_previous.place(x=50, y=70)
        self.btn_previous["state"] = DISABLED

        self.btn_next = Button(self.details, text="Next", command=self.click_next, highlightbackground='#3E4149')
        self.btn_next.place(x=250, y=70)
        if num_generations > 1:
            self.btn_next["state"] = NORMAL
        else:
            self.btn_next["state"] = DISABLED

        flowers = self.generations[self.current_generation]['flowers']
        self.fill_board(flowers, str(self.current_generation))

        self.listbox = Listbox(self.details)
        self.listbox.place(x=110, y=120)
        for i in range(len(self.generations[self.current_generation]['bees'])):
            self.listbox.insert('end', self.generations[self.current_generation]['bees'][i].name)
        self.btn_show_details = Button(self.details, text="Show Details", command=self.show_details,
                                       highlightbackground='#3E4149')
        self.btn_show_details.place(x=130, y=310)

        self.show_details()

    def show_details(self):
        tem = self.listbox.get(ACTIVE)

        for i in range(len(self.generations[self.current_generation]['bees'])):
            tem2 = self.generations[self.current_generation]['bees'][i]
            if tem2.name == tem:
                self.selected_bee = tem2

        if self.selected_bee is not None:
            self.lbl_name.set(self.selected_bee.name)
            if self.selected_bee.origin:
                self.lbl_origin.set("inside")
            else:
                self.lbl_origin.set("outside")
            self.lbl_color.set(self.selected_bee.favorite_color)
            self.lbl_dir.set(self.selected_bee.favorite_direction)
            self.lbl_angle.set(self.selected_bee.deflection_angle)
            self.lbl_max_dis.set(self.selected_bee.max_distance)
            self.lbl_genes.set(self.selected_bee.genes_bin)
            self.lbl_found.set(len(self.selected_bee.visited_flowers))
            self.lbl_adap.set(round(self.selected_bee.adaptability_percentage, 2))
            if self.current_generation > 1:
                self.lbl_parent1.set(
                    "generation: {}, {}".format(self.current_generation - 1, self.selected_bee.parents[0].name))
                self.lbl_parent2.set(
                    "generation: {}, {}".format(self.current_generation - 1, self.selected_bee.parents[1].name))
            else:
                self.lbl_parent1.set("-")
                self.lbl_parent2.set("")

    def click_previous(self):
        self.current_generation -= 1
        flowers = self.generations[self.current_generation]['flowers']
        self.fill_board(flowers, str(self.current_generation))
        self.btn_next["state"] = NORMAL
        self.update_listbox()
        if self.current_generation <= 1:
            self.btn_previous["state"] = DISABLED
        else:
            self.btn_previous["state"] = NORMAL

    def click_next(self):
        self.current_generation += 1
        flowers = self.generations[self.current_generation]['flowers']
        self.fill_board(flowers, str(self.current_generation))
        self.btn_previous["state"] = NORMAL
        self.update_listbox()
        if self.current_generation >= num_generations:
            self.btn_next["state"] = DISABLED
        else:
            self.btn_next["state"] = NORMAL

    def update_listbox(self):
        self.listbox.delete(0, END)
        for i in range(len(self.generations[self.current_generation]['bees'])):
            self.listbox.insert('end', self.generations[self.current_generation]['bees'][i].name)
        self.show_details()

    def pointCircle(self, radius, p1, p2):
        return sqrt(pow(p2[0] - p1[0], 2) + pow(p2[1] - p1[1], 2)) < radius

    def fill_board(self, flowers, generation):
        self.lbl_generation.set(generation)

        if self.flag:
            for r in range(self.rows):
                for c in range(self.columns):
                    id_quadrant = str(r * 100 + c)
                    x1, y1 = c * self.quadrants_dimension, r * self.quadrants_dimension
                    x2, y2 = x1 + self.quadrants_dimension, y1 + self.quadrants_dimension
                    self.board.create_rectangle(
                        x1, y1, x2, y2,
                        fill=_from_rgb((0, 0, 0)),
                        tags=id_quadrant)

            self.flag = False

        for i in range(0, self.rows):
            for j in range(0, self.columns):
                if not self.pointCircle(51, [50, 50], [j, i]):
                    self.board.itemconfig(i * 100 + j, fill=_from_rgb((0, 0, 0)))
                else:
                    self.board.itemconfig(i * 100 + j, fill=_from_rgb((255, 255, 255)))

        for flower in flowers:
            self.board.itemconfig(flower.position_id, fill=_from_rgb(flower.color))
        self.board.itemconfig(50 * 100 + 50, fill=_from_rgb((0, 0, 0)))


def switch(button):
    if button["state"] == NORMAL:
        button["state"] = DISABLED
    else:
        button["state"] = NORMAL


def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'

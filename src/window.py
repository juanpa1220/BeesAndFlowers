from tkinter import *
from src.main import click_previous, click_next, current_generation, num_generations

board_dimensions = [800, 800]
window_dimensions = [1200, 800]
num_quadrants = 100


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        self.rows = num_quadrants
        self.columns = num_quadrants
        self.quadrants_dimension = board_dimensions[0] / num_quadrants
        self.quadrants_color = "white"

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

        Label(self.details, text="Generation: ", font=("Helvetica", 18)).place(x=140, y=50)
        self.lbl_generation = StringVar()
        Label(self.details, textvariable=self.lbl_generation, font=("Helvetica", 18)).place(x=240, y=50)

        self.btn_previous = Button(self.details, text="Previous", command=self.click_previous,
                                   highlightbackground='#3E4149')
        self.btn_previous.place(x=50, y=100)
        self.btn_previous["state"] = DISABLED

        self.btn_next = Button(self.details, text="Next", command=self.click_next, highlightbackground='#3E4149')
        self.btn_next.place(x=250, y=100)
        self.btn_next["state"] = DISABLED

    def click_previous(self):
        if current_generation <= 1:
            self.btn_previous["state"] = DISABLED
        else:
            self.btn_previous["state"] = NORMAL

    def click_next(self):
        if current_generation == num_generations:
            self.btn_next["state"] = DISABLED
        else:
            self.btn_next["state"] = NORMAL

    def fill_board(self, flowers, generation):
        self.lbl_generation.set(generation)
        for r in range(self.rows):
            for c in range(self.columns):
                id_quadrant = str(r + 100 * c)
                x1, y1 = c * self.quadrants_dimension, r * self.quadrants_dimension
                x2, y2 = x1 + self.quadrants_dimension, y1 + self.quadrants_dimension
                self.board.create_rectangle(
                    x1, y1, x2, y2,
                    fill=self.quadrants_color,
                    tags=id_quadrant)

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

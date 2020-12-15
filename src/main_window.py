import pygame

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
dimensions = [500, 400]


class MainWindow:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Bees and Flowers")
        self.window = pygame.display.set_mode(dimensions)
        self.game_done = False
        self.width = int(dimensions[0] / 8)  # ancho
        self.height = int(dimensions[1] / 8)  # alto
        self.clock = pygame.time.Clock()

    def show_window(self):
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_done = True

            self.window.fill(BLANCO)
            color = 0
            for i in range(0, dimensions[0], self.width):
                for j in range(0, dimensions[1], self.height):
                    if color % 2 == 0:
                        pygame.draw.rect(self.window, NEGRO, [i, j, self.width, self.height], 0)
                    else:
                        pygame.draw.rect(self.window, BLANCO, [i, j, self.width, self.height], 0)
                    color += 1
                color += 1
            pygame.display.flip()
            self.clock.tick(5)

            if self.game_done:
                pygame.quit()

        except KeyboardInterrupt:
            self.game_done = True


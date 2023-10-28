import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Object:
    def __init__(self, x, y, color, width=50, height=30):  # Changing size to width and height
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))  # Using width and height

    def move(self, x, y):
        self.x += x
        self.y += y

def main():
    # Initializing Pygame
    pygame.init()

    # Setting up display
    win_size = (500, 500)
    win = pygame.display.set_mode(win_size)
    pygame.display.set_caption("Room Environment")

    # Creating objects
    static_objects = [
        Object(100, 100, BLACK, 400, 20),  # Specifying width and height
        Object(300, 200, BLACK, 20, 300),
    ]

    dynamic_objects = [
        Object(200, 200, RED, 30, 80),
        Object(400, 100, GREEN, 70, 40),
    ]

    run = True
    while run:
        pygame.time.delay(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Moving dynamic objects randomly
        for obj in dynamic_objects:
            obj.move(random.randint(-10, 10), random.randint(-10, 10))

        # Drawingobjects
        win.fill(WHITE)
        for obj in static_objects:
            obj.draw(win)
        for obj in dynamic_objects:
            obj.draw(win)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()

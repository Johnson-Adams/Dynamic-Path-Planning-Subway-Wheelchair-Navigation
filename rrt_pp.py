import pygame
import random
import math

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

win_size = (500, 500)
pygame.init()
win = pygame.display.set_mode(win_size)
pygame.display.set_caption("RRT-Simple")
scale_factor = 5

def draw_tree(tree):
    for p1, p2 in tree:
        pygame.draw.line(win, GREEN, p1, p2, 1)

def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

# def is_path_clear(p1, p2):
#     return True

def rrt(start, goal):
    tree = []
    nodes = [start]

    while True:
        rand_point = (random.randint(0, win_size[0]), random.randint(0, win_size[1]))

        closest_point = nodes[0]
        for p in nodes:
            if distance(p, rand_point) < distance(closest_point, rand_point):
                closest_point = p

        angle = math.atan2(rand_point[1]-closest_point[1], rand_point[0]-closest_point[0])
        new_point = (closest_point[0]+int(math.cos(angle)*scale_factor), closest_point[1]+int(math.sin(angle)*scale_factor))

        if True:
            nodes.append(new_point)
            tree.append((closest_point, new_point))

            win.fill(WHITE)
            pygame.draw.circle(win, RED, start, 5)
            pygame.draw.circle(win, BLUE, goal, 5)
            draw_tree(tree)
            pygame.display.update()

            if distance(new_point, goal) < 20:
                return tree

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.time.delay(10)

def main():
    start = (50, 50)
    goal = (450, 450)

    rrt(start, goal)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.time.delay(50)

if __name__ == "__main__":
    main()

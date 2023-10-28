import pygame
import random
import math
import time

# Initializing pygame and the screen
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("RRT with Obstacles")

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Obstacles
obstacles = [
    # Benches on the platform
    (120, 430, 50, 15),
    (190, 430, 50, 15),
    (260, 430, 50, 15),
    (330, 430, 50, 15),
    (400, 430, 50, 15),
    (470, 430, 50, 15),
    (540, 430, 50, 15),
    (610, 430, 50, 15),

    # Pillars/supports 
    (200, 50, 15, 350),
    (300, 50, 15, 350),
    (400, 50, 15, 350),
    (500, 50, 15, 350),
    (600, 50, 15, 350),
]

# obstacles = [(100, 0, 30, 450), (100, 500, 30, 100), (200, 0, 30, 100), (400, 300, 100, 50)]  # Each obstacle is a tuple (x, y, width, height)

def draw_obstacles(screen, obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(screen, black, pygame.Rect(obstacle[0], obstacle[1], obstacle[2], obstacle[3]))

# RRT Algorithm
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None

def distance(a, b):
    return math.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)

def step_from_to(node1, node2, stepSize):
    if distance(node1, node2) < stepSize:
        return node2
    else:
        theta = math.atan2(node2.y - node1.y, node2.x - node1.x)
        return Node(node1.x + stepSize * math.cos(theta), node1.y + stepSize * math.sin(theta))

def is_path_clear(start, end, obstacles):
    """
    Checking if the path between start and end points is clear of obstacles.
    :param start: tuple (x, y), start point
    :param end: tuple (x, y), end point
    :param obstacles: list of tuples (x, y, width, height), representing obstacles
    :return: boolean, True if path is clear, False otherwise
    """
    for obstacle in obstacles:
        # Calculating the rectangle's (obstacle's) vertices
        top_left = (obstacle[0], obstacle[1])
        top_right = (obstacle[0] + obstacle[2], obstacle[1])
        bottom_left = (obstacle[0], obstacle[1] + obstacle[3])
        bottom_right = (obstacle[0] + obstacle[2], obstacle[1] + obstacle[3])

        # Checking for all sides of the rectangle
        if do_intersect(start, end, top_left, top_right):
            return False
        if do_intersect(start, end, top_right, bottom_right):
            return False
        if do_intersect(start, end, bottom_right, bottom_left):
            return False
        if do_intersect(start, end, bottom_left, top_left):
            return False

    # If we've not returned False yet, path is clear
    return True

def do_intersect(p1, q1, p2, q2):
    """
    Checkingif two line segments intersect.
    :param p1: tuple (x, y), start point of line segment 1
    :param q1: tuple (x, y), end point of line segment 1
    :param p2: tuple (x, y), start point of line segment 2
    :param q2: tuple (x, y), end point of line segment 2
    :return: boolean, True if lines intersect, False otherwise
    """
    # Helper functions
    def orientation(p, q, r):
        """
        Finding orientation of ordered triplet (p, q, r).
        :param p: tuple (x, y), first point
        :param q: tuple (x, y), second point
        :param r: tuple (x, y), third point
        :return: int, 0 --> p, q and r are colinear, 1 --> Clockwise, 2 --> Counterclockwise
        """
        val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1]))
        if val == 0: return 0  # colinear
        elif val > 0: return 1  # clockwise
        else: return 2  # counterclockwise

    def on_segment(p, q, r):
        """
        Checking if point q lies on line segment 'pr'
        :param p: tuple (x, y), first point
        :param q: tuple (x, y), second point
        :param r: tuple (x, y), third point
        :return: boolean, True if q lies on segment pr, False otherwise
        """
        if q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]):
            return True
        return False

    # Finding the four orientations needed for the general and special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case
    if o1 != o2 and o3 != o4:
        return True

    # Theres some pecial cases: when any three points are colinear
    if o1 == 0 and on_segment(p1, p2, q1): return True
    if o2 == 0 and on_segment(p1, q2, q1): return True
    if o3 == 0 and on_segment(p2, p1, q2): return True
    if o4 == 0 and on_segment(p2, q1, q2): return True

    return False  # Doesn't fall

def main():
    average_time = 0
    rrt_loops = 5
    for i in range(rrt_loops):

        running = True
        nodes = []
        stepSize = 20
        FinalProx = 20
        start = Node(50, 50)  # Starting position
        nodes.append(start)
        goal = Node(550, 550)  # Goal position

        start_time = time.time()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill(white)
            draw_obstacles(screen, obstacles)

            # Drawing existing nodes and edges
            for n in nodes:
                pygame.draw.circle(screen, black, (int(n.x), int(n.y)), 3)
                if n.parent:
                    pygame.draw.line(screen, green, (n.x, n.y), (n.parent.x, n.parent.y))

            # Drawing goal
            pygame.draw.circle(screen, blue, (int(goal.x), int(goal.y)), 5)

            # RRT Algorithm
            rand = Node(random.random()*width, random.random()*height)
            nn = nodes[0]
            for p in nodes:
                if distance(p, rand) < distance(nn, rand):
                    nn = p

            newnode = step_from_to(nn, rand, stepSize)

            # Checking if the path between the nearest node and the new node is clear
            if is_path_clear((nn.x, nn.y), (newnode.x, newnode.y), obstacles):
                newnode.parent = nn
                nodes.append(newnode)

            # Checking for completion
            if distance(newnode, goal) < FinalProx:
                # Draw final path
                while newnode.parent:
                    pygame.draw.line(screen, blue, (newnode.x, newnode.y), (newnode.parent.x, newnode.parent.y), 3)
                    newnode = newnode.parent
                running = False

            pygame.display.flip()
            # pygame.time.wait(50)

        finish_time = time.time()

        print("Time taken for loop ", i+1, "/", rrt_loops, " : ", finish_time-start_time)
        average_time += finish_time-start_time 
        pygame.time.wait(2000)
    print("Average time : ", average_time/rrt_loops)
    pygame.quit()

if __name__ == "__main__":
    main()

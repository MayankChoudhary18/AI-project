import pygame
import random
import numpy as np
import tkinter as tk
from tkinter import messagebox

pygame.init()

sx = 500
sy = 500
screen = pygame.display.set_mode((sx, sy))
done = False
x = 0
y = 0
ev = 'r'
clock = pygame.time.Clock()
color = (51, 204, 51)
sp = {0: (x, y)}
size = 1
points = 0

class Node():

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
  
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    open_list = []
    closed_list = []

    open_list.append(start_node)

    count = 0

    while len(open_list) > 0:
        pygame.event.get()
        count += 1
        if count > 1000:
            return -1

        current_node = open_list[0]
        current_index = 0
    
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] 

        children = []

        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  

            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            a1, b1 = node_position

            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue
                    
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            new_node = Node(current_node, node_position)

            children.append(new_node)

        for child in children:
            
            for closed_child in closed_list:
                if child == closed_child:
                    break
            else:
                
                child.g = current_node.g + 1
                
                child.h = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1])
                child.f = child.g + child.h
                
                for open_node in open_list:
                    if child == open_node and child.g >= open_node.g:
                        break
                else:
                    open_list.append(child)

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 15)


def drawbox(x, y, col=color):
    pygame.draw.rect(screen, col, pygame.Rect(x, y, 20, 20))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x, y, 20, 20), 2)


def randomSnack():
    rx1 = random.randrange((sx - 20) / 20)
    ry1 = random.randrange((sy - 20) / 20)
    rx2, ry2 = rx1 * 20, ry1 * 20
    for i in range(0, size):
        a, b = sp[i]
        if a == rx2 and b == ry2:
            return randomSnack()

    return rx1 * 20, ry1 * 20


rx, ry = randomSnack()


def genMatrix(sp):
    mat = np.zeros(shape=(2 + sx // 20, 2 + sy // 20))
    for i in range(0, 2 + sx // 20):
        mat[0, i] = 1
        mat[i, 0] = 1
        mat[1 + sx // 20, i] = 1
        mat[i, 1 + sx // 20] = 1

    for i in sp:
        a, b = sp[i]
        mat[1 + a // 20, 1 + b // 20] = 1
    a, b = sp[0]
    mat[1 + a // 20, 1 + b // 20] = 0
    start = (1 + a // 20, 1 + b // 20)
    end = (1 + rx // 20, 1 + ry // 20)
    path = astar(mat, start, end)
    print(path)
    return path

def message_box(subject, content):
        root = tk.Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        messagebox.showinfo(subject, content)

screen.fill((0, 0, 0))

while not done:

    path = genMatrix(sp)

    if path is None:
        
        message_box('You Lost!', 'Play again...')
        size = 1
        points = 0
        x, y = 0, 0
        sp = {0: (x, y)}
        exit(0)
    
    for j in path:
        
        screen.fill((0, 0, 0))
    
        screen.blit(pygame.image.load('files/apple.png'), (rx - 2, ry - 2))
        textsurface = myfont.render("Current Score : " + str(points), False, (255, 255, 0))
        screen.blit(textsurface, (sx - 160, 30))
        
        nx, ny = sp[0]
        nx1, ny1 = j
        sp[0] = ((nx1 - 1) * 20, (ny1 - 1) * 20)
        nx1, ny1 = ((nx1 - 1) * 20, (ny1 - 1) * 20)
        sp[1] = (nx, ny)
        for i in range(size - 1, 0, -1):
            nx, ny = sp[i]
            drawbox(nx, ny, color)
            tx, ty = sp[i - 1]
            sp[i] = (tx, ty)
        drawbox(nx1, ny1, (0, 102, 0))
        pygame.display.flip()
        clock.tick(30)
        x, y = sp[0]
        if x == rx and y == ry:
            sp[size] = (rx + 1, ry + 1)
            rx, ry = randomSnack()
            if size < 5000:
                size += 1
            points += 10
            pygame.mixer.Channel(1).set_volume(100)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('files/hit.wav'))
        #print(sp)
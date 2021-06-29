import numpy
import numpy as np
import pygame
from PIL import Image


class Group:

    def __init__(self):self.all_entities = {}

    def remove(self, entity):del self.all_entities[entity]

    def add(self, entity):self.all_entities[entity] = ""

    def draw(self, surface):
        for entity in self.all_entities:
            entity.draw(surface)

    def get(self):
        res = []
        for entity in self.all_entities:
            res.append(entity)
        return res

    def getByClass(self, target_class):
        all_entities = self.get()
        output = []
        for entity in all_entities:
            if entity.__class__ == target_class:
                output.append(entity)
        return output

    def __add__(self, entity):self.all_entities[entity] = 0

    def __len__(self):
        return len(self.all_entities)

    def __repr__(self):return f'Group({self.get()})'

    def __delattr__(self, entity):del self.all_entities[entity]

    def __delitem__(self, entity):del self.all_entities[entity]




def collisionRect(rectA, rectB):
    if rectB.right < rectA.left:
        # rectB est à gauche
        return False
    if rectB.bottom < rectA.top:
        # rectB est au-dessus
        return False
    if rectB.left > rectA.right:
        # rectB est à droite
        return False
    if rectB.top > rectA.bottom:
        # rectB est en-dessous
        return False
    # Dans tous les autres cas il y a collision
    return True


def delQueue(dict, list):
    print(f"dict : {dict}")
    print(f"list : {list}")
    i = 0
    for item in list:
        del dict[item]
        del list[i]
        i += 1

def calcVector(v1, v2, sign):
    v1 = list(v1)
    v2 = list(v2)
    output = []
    for i in range(len(v1)):
        if sign == "+": dat = v1[i] + v2[i]
        if sign == "-": dat = v1[i] - v2[i]
        if sign == "*": dat = v1[i] * v2[i]
        if sign == "/": dat = v1[i] / v2[i]

        output.append(dat)
    return output

def grayscale(img):
    arr = pygame.surfarray.array3d(img)
    #luminosity filter
    avgs = [[(r*0.298 + g*0.587 + b*0.114) for (r,g,b) in col] for col in arr]
    arr = numpy.array([[[avg,avg,avg] for avg in col] for col in avgs])
    return pygame.surfarray.make_surface(arr)

def fill(surface, color):
    """Fill all pixels of the surface with color, preserve transparency."""
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))

def split_animated_gif(gif_file_path):
    ret = []
    gif = Image.open(gif_file_path)
    for frame_index in range(gif.n_frames):
        gif.seek(frame_index)
        frame_rgba = gif.convert("RGBA")
        pygame_image = pygame.image.fromstring(
            frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode
        )
        ret.append(pygame_image)
    return ret
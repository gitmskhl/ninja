import pygame
from os import listdir

BASE_DIR_PATH = 'data/images/'

def load_image(path):
    img = pygame.image.load(BASE_DIR_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img


def load_images(path):
    images = []
    for img_name in sorted(listdir(BASE_DIR_PATH + path)):
        images.append(load_image(path + "/" + img_name))
    return images


class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.done = False
        self.frame = 0

        self.img_duration = img_dur
        self.timer = img_dur


    def reset(self):
        self.timer = self.img_duration
        self.frame = 0


    def img(self):
        return self.images[self.frame]


    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)


    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.timer = self.img_duration
            if self.loop:
                self.frame = (self.frame + 1) % len(self.images)
            else:
                self.frame += 1
                if self.frame == len(self.images):
                    self.frame -= 1
                    self.done = True


class AnimationStates:
    def __init__(self, animations, states, firstState=None):
        self.animations = {
            state: animation
            for state, animation in zip(states, animations)
        }
        self.current_state = firstState if firstState is not None else states[0]
    
    def img(self):
        return self.animations[self.current_state].img()
    
    def set_state(self, newstate):
        if self.current_state != newstate:
            self.current_state = newstate
            self.animations[newstate].reset()
        
    def update(self):
        self.animations[self.current_state].update()
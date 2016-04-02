import pygame
import sys
from pygame.locals import *

class Map:
    def __init__(self, IMAGE_PATH):

        self.image = pygame.image.load(IMAGE_PATH).convert()

        #self.img.set_colorkey(TRANS_COLOR)

    def get_image(self):
        return self.image

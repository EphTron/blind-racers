import pygame
import sys
from pygame.locals import *

class Map:
    def __init__(self, IMAGE_PATH):

        self.visible = True
        self.image = pygame.image.load(IMAGE_PATH).convert()
        self.start_line = [(350,305),(400,305)]
    #185,122,87,255

        #self.img.set_colorkey(TRANS_COLOR)

    def get_image(self):
        return self.image

    def get_start_line(self):
        return self.start_line

    def get_off_color(self):
        return (185,122,87,255)
        
    def get_road_color(self):
        return (255,127,39,255)


    def is_visible(self):
        return self.visible

    def set_map_visibility(self, BOOL):
        self.visible = BOOL

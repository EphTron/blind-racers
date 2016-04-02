import pygame
import sys
import math
from pygame.locals import *

from Utility import Vec2

import math

class Player:

    number_of_instances = 0

    #def __init__(self, IMAGE_PATH = "images/players/default.png", START_POSITION = Vec2(0,0)):
    def __init__(self, IMAGE_PATH = "images/players/ship_1.png", START_POSITION = Vec2(0,0)):
        self.id = Player.number_of_instances
        Player.number_of_instances += 1

        _img = pygame.image.load(IMAGE_PATH)
        self.image = _img.convert()
        self.image.set_colorkey(pygame.Color(255,255,255))
        self.image_position = START_POSITION
        self.image_size = Vec2(self.image.get_width(), self.image.get_height())

        self.player_position = Vec2(self.image_position.x + self.image_size.x / 2,
                                    self.image_position.y + self.image_size.y / 2)
        self.direction = math.pi #0.0#90.0
        self.image_direction = 0
        self.path = [(self.player_position.x,self.player_position.y)]

        #ship values
        self.steer_speed = 0.05

    def rotate(self, LEFT = False, RIGHT = False):
        if LEFT == True and RIGHT == False:
            self.direction += self.steer_speed
            self.image_direction += self.steer_speed * (180/math.pi)
        if RIGHT == True and LEFT == False:
            self.direction -= self.steer_speed
            self.image_direction -= self.steer_speed * (180/math.pi)

    def create_path(self, POSITION):
        _new_pos = (POSITION.x,POSITION.y)
        _last_pos = self.path[-1]
        if _last_pos[0] != _new_pos[0] or _last_pos[1] != _new_pos[1]:
            self.path.append((POSITION.x,POSITION.y))

    def get_path(self):
        return self.path

    def get_position(self):
        return self.player_position

    def update_position(self):
        self.player_position = Vec2(self.image_position.x + self.image_size.x / 2,
                                    self.image_position.y + self.image_size.y / 2)

    def set_position(self, VEC2 = None, X = None, Y = None):
        if VEC2 is not None:
            self.player_position = VEC2
            self.update_image_position() 
        elif X is not None and Y is not None:
            self.player_position = Vec2(X,Y)
            self.update_image_position() 
        elif X is not None:
            self.player_position.x = X
            self.update_image_position() 
        elif Y is not None:
            self.player_position.y = Y
            self.update_image_position() 
        else:
            pass


    def get_image(self):
        return self.image

    def get_image_position(self):
        return self.image_position

    def update_image_position(self):
        self.image_position = Vec2(self.player_position.x - self.image_size.x / 2,
                                   self.player_position.y - self.image_size.y / 2)


    def set_image_position(self, VEC2 = None, X = None, Y = None):
        if VEC2 is not None:
            self.image_position = VEC2
            self.update_position() 
        elif X is not None and Y is not None:
            self.image_position = Vec2(X,Y)
            self.update_position() 
        elif X is not None:
            self.image_position.x = X
            self.update_position() 
        elif Y is not None:
            self.image_position.y = Y
            self.update_position() 
        else:
            pass

    def get_image_size(self):
        return (self.image.get_width(), self.image.get_height())

    def get_direction(self):
        return self.direction

    def set_direction(self, VALUE):
        self.direction += VALUE

    def get_image_direction(self):
        return self.image_direction

    def set_image_direction(self, VALUE):
        self.image_direction += VALUE

    

       
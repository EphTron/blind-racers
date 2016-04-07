import pygame
import sys
import math
from pygame.locals import *

from Utility import Vec2

import math

class Player:

    number_of_instances = 0

    def __init__(self, IMAGE_PATH = "images/players/ship_1.png", START_POSITION = (0,0)):
        self.id = Player.number_of_instances
        Player.number_of_instances += 1

        _img = pygame.image.load(IMAGE_PATH)
        self.image = _img.convert()
        self.image.set_colorkey(pygame.Color(255,255,255))
        self.image_position = START_POSITION
        self.image_size = (self.image.get_width(), self.image.get_height())

        self.player_position = (self.image_position[0] + self.image_size[0] / 2,
                                self.image_position[1] + self.image_size[1] / 2)
        self.image_direction = 0
        self.direction = math.pi #0.0#90.0

        self.current_path = [(self.player_position[0], self.player_position[1])]
        self.good_paths = []
        self.bad_paths = []

        self.crash_flag = False
        self.last_start_position = (self.player_position)
        self.trys = 0
        self.fails = 0

        #ship values
        self.steer_speed = 0.05

    def rotate(self, LEFT = False, RIGHT = False):
        if LEFT == True and RIGHT == False:
            self.direction += self.steer_speed
            self.image_direction += self.steer_speed * (180/math.pi)
        if RIGHT == True and LEFT == False:
            self.direction -= self.steer_speed
            self.image_direction -= self.steer_speed * (180/math.pi)

    def set_crash_flag(self, BOOL):
        self.crash_flag = BOOL

    def has_crashed(self):
        return self.crash_flag

    def create_path(self, POSITION):
        _new_pos = POSITION
        _last_pos = self.current_path[-1]
        if _last_pos[0] != _new_pos[0] or _last_pos[1] != _new_pos[1]:
            self.current_path.append(_new_pos)

    def get_current_path(self):
        return self.current_path

    def reset_current_path(self):
        self.current_path = [(self.player_position[0], self.player_position[1])]

    def get_last_start_position(self):
        return self.last_start_position
        
    def get_good_paths(self):
        return self.good_paths

    def set_good_paths(self, PATH):
        self.good_paths = PATH
        self.trys += 1

    def get_bad_paths(self):
        return self.bad_paths

    def set_bad_paths(self, PATH):
        self.bad_paths.append(PATH)
        self.fails += 1

    def get_trys(self):
        return self.trys

    def get_fails(self):
        return self.fails

    def set_last_start_position(self, POSITION):
        self.last_start_position = POSITION

    def get_position(self):
        return self.player_position

    def update_position(self):
        self.player_position = (self.image_position[0] + self.image_size[0] / 2,
                                self.image_position[1] + self.image_size[1] / 2)

    def set_position(self, VEC2 = None, X = None, Y = None):
        if VEC2 is not None:
            self.player_position = VEC2
            self.update_image_position() 
        elif X is not None and Y is not None:
            self.player_position = (X,Y)
            self.update_image_position() 
        elif X is not None:
            self.player_position[0] = X
            self.update_image_position() 
        elif Y is not None:
            self.player_position[1] = Y
            self.update_image_position() 
        else:
            pass


    def get_image(self):
        return self.image

    def get_image_position(self):
        return self.image_position

    def update_image_position(self):
        self.image_position = (self.player_position[0] - self.image_size[0] / 2,
                               self.player_position[1] - self.image_size[1] / 2)


    def set_image_position(self, VEC2 = None, X = None, Y = None):
        if VEC2 is not None:
            self.image_position = VEC2
            self.update_position() 
        elif X is not None and Y is not None:
            self.image_position = (X,Y)
            self.update_position() 
        elif X is not None:
            self.image_position[0] = X
            self.update_position() 
        elif Y is not None:
            self.image_position[1] = Y
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

    

       
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

        self.position = START_POSITION
        self.direction = math.pi #0.0#90.0
        self.image_direction = 0


        #ship values
        self.steer_speed = 0.05

        _img = pygame.image.load(IMAGE_PATH)
        self.image = _img.convert()
        self.image.set_colorkey(pygame.Color(255,255,255))
        """
        #draw line PARAM screen, color, start pos, end pos, width
        self.player_ray = pygame.draw.line(self.screen,
            (200,200,0),      
            (_player_position.x,_player_position.y), 
            (_player_position.x + 15 * (math.sin(_player_direction)),     
            _player_position.y + 15 * (math.cos(_player_direction))), 
            3) 
        """

    def rotate(self, LEFT = False, RIGHT = False):
        if LEFT == True and RIGHT == False:
            self.direction += self.steer_speed
            self.image_direction += self.steer_speed * (180/math.pi)
        if RIGHT == True and LEFT == False:
            self.direction -= self.steer_speed
            self.image_direction -= self.steer_speed * (180/math.pi)


    def get_position(self):
        return self.position

    def set_position(self, VEC2 = None, X = None, Y = None):
        if VEC2 is not None:
            self.position = VEC2
        elif X is not None and Y is not None:
            self.position = Vec2(X,Y)
        elif X is not None:
            self.position.x = X
        elif Y is not None:
            self.position.y = Y
        else:
            pass

    def get_image(self):
        return self.image

    def get_direction(self):
        #if self.direction > 180:
            #self.direction = self.direction - 180
        #elif self.direction < -180:
            #self.direction = self.direction % 180
        return self.direction

    def set_direction(self, VALUE):
        self.direction += VALUE

    def get_image_direction(self):
        return self.image_direction

    def set_image_direction(self, VALUE):
        self.image_direction += VALUE

    

       
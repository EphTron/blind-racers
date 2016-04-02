import pygame
import sys
from pygame.locals import *

#include own libs
from Model import *
from Controller import *
from Utility import Vec2
import Utility as util

class View:
    def __init__(self, MODEL = None, SCREEN_SIZE = Vec2(800,600)):

        self.model = MODEL
        self.screen_size = SCREEN_SIZE
        self.screen = pygame.display.set_mode((self.screen_size.x, self.screen_size.y))
        pygame.display.set_caption("blind-racers")

        self.background = pygame.Color(0,0,0)

    def set_model(self, MODEL):
        self.model = MODEL

    def draw(self):
        self.screen.fill(self.background)
        if self.model is not None:
            self.draw_map(self.model.get_map())
            self.draw_player(self.model.get_player())

    def draw_map(self, MAP):
        _map_image = MAP.get_image()
        self.screen.blit(_map_image, (0,0))
        
    def draw_player(self, PLAYER):
        _player_position = PLAYER.get_position()
        _player_direction = PLAYER.get_direction()
        _image_direction = PLAYER.get_image_direction()
        
        #draw line PARAM screen, color, start pos, end pos, width
        self.player_ray = pygame.draw.line(self.screen,
                                           (200,200,0),      
                                           (_player_position.x,_player_position.y), 
                                           (_player_position.x + 15 * (math.sin(_player_direction)),     
                                            _player_position.y + 15 * (math.cos(_player_direction))), 
                                           3) 
    
        _player_image = PLAYER.get_image()
        _player_image = util.rot_center(_player_image, _image_direction)
        self.screen.blit(_player_image, (_player_position.x, _player_position.y))

 
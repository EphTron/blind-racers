import pygame
import sys
from pygame.locals import *

#include own libs
from Model import *
from Controller import *
from Utility import Vec2
import Utility as util

class View:
    def __init__(self, MODEL = None, SCREEN_SIZE = (800,600)):

        self.model = MODEL
        self.screen_size = SCREEN_SIZE
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("blind-racers")

        self.background = pygame.Color(0,0,0)

    def set_model(self, MODEL):
        self.model = MODEL

    def draw(self):
        self.screen.fill(self.background)
        if self.model is not None:
            self.draw_map(self.model.get_map(), self.model.get_player())
            self.draw_player(self.model.get_player())

    def draw_map(self, MAP, PLAYER):
        _map_image = MAP.get_image()
        if MAP.is_visible():
            self.screen.blit(_map_image, (0,0))
            pygame.draw.lines(self.screen, (100,250,100), False, MAP.get_start_line(), 1)

            if len(PLAYER.get_good_paths()) > 1:
                pygame.draw.lines(self.screen, (150,50,0), False, PLAYER.get_good_paths(), 1)

            for _bad_path in PLAYER.get_bad_paths():
                if len(_bad_path) > 1:
                    pygame.draw.lines(self.screen, (50,50,150), False, _bad_path, 1)

        
    def draw_player(self, PLAYER):
        _player_position = PLAYER.get_position()
        _player_direction = PLAYER.get_direction()
        _image_direction = PLAYER.get_image_direction()
        _player_size = PLAYER.get_image_size()
        
        #draw line PARAM screen, color, start pos, end pos, width
        self.player_ray = pygame.draw.line(self.screen,
                                           (200,200,0),
                                           _player_position, 
                                           (_player_position[0] + 30 * (math.sin(_player_direction)),     
                                            _player_position[1] + 30 * (math.cos(_player_direction))), 
                                           3)

        _player_path = PLAYER.get_current_path()
        _temp_pos = _player_position
        _temp_path = list(_player_path)
        _temp_path.append(_temp_pos)
        
        pygame.draw.lines(self.screen, (200,50,0), False, _temp_path, 1)

        _player_image = PLAYER.get_image()
        _player_image = util.rot_center(_player_image, _image_direction)
        _image_position = PLAYER.get_image_position()
        self.screen.blit(_player_image, (_image_position[0], _image_position[1]))

 
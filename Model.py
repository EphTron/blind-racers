import pygame
import sys
from pygame.locals import *

from Map import *
from Player import *

class Model:
    def __init__(self, PLAYER_COUNT = 2):
        
        #game settings
        self.fps = 60
        self.trans_color = pygame.Color(255,255,255)

        #init map
        self.map = Map("images/maps/test-map.png")



        #init player
        self.player = Player(START_POSITION = (350,300))

    def get_map(self):
        return self.map

    def get_player(self):
        return self.player
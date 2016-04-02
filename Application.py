import pygame
import sys
from pygame.locals import *

from Model import *
from View import *
from Controller import *
from Utility import *

class Application:

    def __init__(self):
        # setup pygame
        pygame.init()

        self.running_flag = False
        self.player_count = 1

        self.model = Model(PLAYER_COUNT = self.player_count)
        self.view = View(MODEL = self.model, SCREEN_SIZE = Vec2(500,500))
        self.controller = Controller(self.model, self.view)
        self.fpsTime = pygame.time.Clock()


    def run(self):
        self.running_flag = True
        while self.running_flag:
            self.controller.run(self.fpsTime)
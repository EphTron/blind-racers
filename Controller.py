import pygame
import sys
import math
from pygame.locals import *


class Controller:
    def __init__(self, MODEL, VIEW):
        self.model = MODEL
        self.view = VIEW
        self.wasd = [0,0,0,0]

        self.map = self.model.get_map()

    def run(self, time):
        self.get_input()
        self.check_collision(self.model.get_player())
        self.view.draw() 

        pygame.display.update()
        time.tick(self.model.fps)
     
    def get_input(self):
        _keys = pygame.key.get_pressed()  #checking pressed keys
        if _keys[pygame.K_w]:
            self.wasd[0] = 1
            self.map.set_map_visibility(False)
        else:
            self.wasd[0] = 0
            

        if _keys[pygame.K_a]:
            self.wasd[1] = 1
        else:
            self.wasd[1] = 0

        if _keys[pygame.K_s]:
            self.wasd[2] = 1
        else:
            self.wasd[2] = 0

        if _keys[pygame.K_d]:
            self.wasd[3] = 1
        else:
            self.wasd[3] = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif (event.type == KEYDOWN):
                if event.key == K_w:
                    self.map.set_map_visibility(False)
                if event.key == K_x:
                    pygame.quit()
                    sys.exit()
            elif event.type == KEYUP:
                if event.key == K_w:
                    self.map.set_map_visibility(True)
            #   if event.key == K_a:
            #       self.MODEL.player.stop()


        self.move_player(self.model.get_player())



    def move_player(self, PLAYER):
        _player_position = PLAYER.get_position()
        _player_direction =  PLAYER.get_direction()

        if self.wasd[0] == 1: # forward
            if not PLAYER.has_crashed():
                _player_position.x = _player_position.x + math.sin(_player_direction)
                _player_position.y = _player_position.y + math.cos(_player_direction)
                PLAYER.set_position(VEC2 = _player_position)
            elif PLAYER.has_crashed():
                self.map.set_map_visibility(True)

        if self.wasd[1] == 1: # left

            PLAYER.rotate(LEFT = True)
            PLAYER.create_path(_player_position)
    
        if self.wasd[2] == 1: # back

            print len(PLAYER.get_path())

        if self.wasd[3] == 1: # right
            
            PLAYER.rotate(RIGHT = True)
            PLAYER.create_path(_player_position)

    def check_collision(self, PLAYER):

        _player_position = PLAYER.get_position()
        _pixel_color = self.map.get_image().get_at((int(_player_position.x),int(_player_position.y)))
        if _pixel_color == self.map.get_off_color():
            PLAYER.set_crash_flag(True)
        elif _pixel_color == self.map.get_road_color():
            PLAYER.set_crash_flag(False)

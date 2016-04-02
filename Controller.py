import pygame
import sys
import math
from pygame.locals import *


class Controller:
    def __init__(self, MODEL, VIEW):
        self.model = MODEL
        self.view = VIEW
        self.wasd = [0,0,0,0]

    def run(self, time):
        self.get_input()
        self.view.draw() 

        pygame.display.update()
        time.tick(self.model.fps)
     
    def get_input(self):
        _keys = pygame.key.get_pressed()  #checking pressed keys
        if _keys[pygame.K_w]:
            self.wasd[0] = 1
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
                if event.key == K_x:
                    pygame.quit()
                    sys.exit()
            elif event.type == KEYUP:
                if event.key == K_w:
                    pass
          #  if event.key == K_a:
          #    self.MODEL.player.stop()

        self.move_player(self.model.get_player())


    def move_player(self,PLAYER):
        if self.wasd[0] == 1: # forward
            _player_position = PLAYER.get_position()
            _player_direction =  PLAYER.get_direction()
            #print ("direction",(_player_direction))
            #print ("direction cos",math.cos(_player_direction))
            _player_position.x = _player_position.x + math.sin(_player_direction)
            _player_position.y = _player_position.y + math.cos(_player_direction)
            PLAYER.set_position(VEC2 = _player_position)
        if self.wasd[1] == 1: # left
            PLAYER.rotate(LEFT = True)
            print PLAYER.get_direction()
            print PLAYER.get_image_direction()
            #print "left"
    
        if self.wasd[2] == 1: # back
            pass
        if self.wasd[3] == 1: # right
            #print "right"
            PLAYER.rotate(RIGHT = True)
            #print PLAYER.get_direction()
            #print "pos", PLAYER.get_position().x, PLAYER.get_position().y


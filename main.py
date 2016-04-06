#from Application import *

#app = Application()
#app.run()

import pygame
import sys
from pygame.locals import *

from Model import *
from View import *
from Controller import *


# setup pygame 
pygame.init()
#
#detector = CollisionDetection()

view = View()
model = Model()
view.set_model(model)
controller = Controller(model, view)
fpsTime = pygame.time.Clock()

while 1:
	controller.run(fpsTime)


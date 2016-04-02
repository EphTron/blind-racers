import pygame

class Vec2:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Vec3:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z 

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

#def rot_center(image, angle):
    """rotate a Surface, maintaining position."""

#    loc = image.get_rect().center  #rot_image is not defined 
#    rot_sprite = pygame.transform.rotate(image, angle)
#    rot_sprite.get_rect().center = loc
#    return rot_sprite
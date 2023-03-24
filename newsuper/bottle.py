import arcade
from constants import *

class BottleSprite(arcade.Sprite):
    """ Player Sprite """
    def __init__(self, texture, scale, angle=0):
        super().__init__()
        self.texture = texture
        self.scale = scale
        self.angle = angle

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        """ Handle when the sprite is moved by the physics engine. """
        # If the bullet falls below the screen, remove it
        if self.center_y < -100:
            self.remove_from_sprite_lists()
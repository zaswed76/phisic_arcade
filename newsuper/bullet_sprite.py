
import arcade
from constants import *

class BulletSprite(arcade.SpriteSolidColor):
    """ Bullet Sprite """
    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        """ Handle when the sprite is moved by the physics engine. """
        # If the bullet falls below the screen, remove it
        if self.center_y < -100:
            self.remove_from_sprite_lists()

class BoxSprite(arcade.Sprite):
    """ Player Sprite """
    def __init__(self, scr, scale):
        super().__init__()

        self.texture = arcade.load_texture(scr)
        self.scale = scale
    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        """ Handle when the sprite is moved by the physics engine. """
        # If the bullet falls below the screen, remove it
        if self.center_y < -100:
            self.remove_from_sprite_lists()

class Bullet(arcade.Sprite):

    def __init__(self, scr, scale=1.0, collisions_lists=None, damage=0):
        super().__init__()
        self.damage = damage
        if collisions_lists is not None:
            self.collisions_lists = collisions_lists
        else:
            self.collisions_lists = []
        self.texture = arcade.load_texture(scr)
        self.scale = scale

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        """ Handle when the sprite is moved by the physics engine. """
        # If the bullet falls below the screen, remove it
        # if self.center_y < -100:
        #     self.remove_from_sprite_lists()
        ccc = self.collides_with_list(self.sprite_lists[0])
        # if ccc:
        #     ccc[0].kill
        #     self.kill()

        for list_sprite in self.collisions_lists:
            coll = self.collides_with_list(list_sprite)

            if coll:

                if list_sprite.collision_type == "player":
                    coll[0].live.current -= self.damage
                    self.kill()

                elif list_sprite.collision_type == "wall":
                    pass
                    # self.kill()

                    # coll[0].kill()






"""
Platformer Game

python -m arcade.examples.platform_tutorial.11_animate_character
"""
import math
import os

import arcade
from paths import  *

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
TILE_SCALING = 0.5
CHARACTER_SCALING = TILE_SCALING * 2
COIN_SCALING = TILE_SCALING
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 7
GRAVITY = 1.5
PLAYER_JUMP_SPEED = 30

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 200
RIGHT_VIEWPORT_MARGIN = 200
BOTTOM_VIEWPORT_MARGIN = 150
TOP_VIEWPORT_MARGIN = 100

PLAYER_START_X = 2
PLAYER_START_Y = 1

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1




def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]


class Entity(arcade.Sprite):
    def __init__(self, name_folder):
        super().__init__()

        # Default to facing right
        self.facing_direction = RIGHT_FACING

        # Used for image sequences
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING
        self.root = ENEMIES
        main_path = self.root / name_folder
        # main_path = f":resources:images/animated_characters/{name_folder}/{name_file}"

        self.idle_texture_pair = load_texture_pair(main_path /"idle.png")
        self.jump_texture_pair = load_texture_pair(main_path /"jump.png")
        self.fall_texture_pair = load_texture_pair(main_path /"fall.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(main_path / f"walk{i}.png")
            self.walk_textures.append(texture)

        # Load textures for climbing
        self.climbing_textures = []
        texture = arcade.load_texture(main_path /"climb0.png")
        self.climbing_textures.append(texture)
        texture = arcade.load_texture(main_path /"climb1.png")
        self.climbing_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # self.set_hit_box([[-22, -64], [22, -64], [22, 28], [-22, 28]])
        self.set_hit_box(self.texture.hit_box_points)


class Enemy(Entity):
    POS_BULLET_BLOCK_CENTER = "center"
    POS_BULLET_BLOCK_RIGHT = "right"
    POS_BULLET_BLOCK_LEFT = "left"
    POS_BULLET_BLOCK_TOP = "top"
    POS_BULLET_BLOCK_BOTTOM = "bottom"
    def __init__(self, name_folder, bullet_block=None, live=1000):

        # Setup parent class
        super().__init__(name_folder)
        self.block_positions = {
            Enemy.POS_BULLET_BLOCK_CENTER: (self.center_x, self.center_y),
            Enemy.POS_BULLET_BLOCK_LEFT: (self.center_x-self.width/1.5, self.center_y),
            Enemy.POS_BULLET_BLOCK_RIGHT: (self.center_x+self.width/1.5, self.center_y),
            Enemy.POS_BULLET_BLOCK_TOP: (self.center_x, self.center_y+self.height/1.5),
            Enemy.POS_BULLET_BLOCK_BOTTOM: (self.center_x, self.center_y-self.center_y+self.height/1.5),
                                }
        self.live = live
        self.live = None
        self.bullet_block = bullet_block
        self.bullet_block_list = list()

        self.should_update_walk = 0

    def set_bullet_block(self, block, pos=None):
        self.pos = pos if pos is not None else Enemy.POS_BULLET_BLOCK_CENTER
        self.bullet_block_list.append(block)

    def set_damage(self, damage):

        self.live -= damage

    def get_block_pos(self, pos):
        if pos == Enemy.POS_BULLET_BLOCK_CENTER:
            p = self.center_x, self.center_y
        elif pos == Enemy.POS_BULLET_BLOCK_LEFT:
            p = (self.center_x-self.width/3, self.center_y)
        elif pos == Enemy.POS_BULLET_BLOCK_RIGHT:
            p= (self.center_x+self.width/3, self.center_y)
        elif pos == Enemy.POS_BULLET_BLOCK_TOP:
            p= (self.center_x, self.center_y+self.height/3)
        elif pos == Enemy.POS_BULLET_BLOCK_BOTTOM:
            p= (self.center_x, self.center_y-self.height/3)

        return p

    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return

        # Walking animation
        if self.should_update_walk == 3:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.facing_direction]
            self.should_update_walk = 0
            return

        self.should_update_walk += 1

    def on_update(self, delta_time: float = 1 / 60):
            if self.live < 0:
                self.game.create_explosion((self.center_x, self.center_y),
                                           texture_list=self.emplosion_texture, scale=self.emplosion_scale)
                for b in self.bullet_block_list:
                    arcade.unschedule(b.get_bullet)
                self.kill()

            if (
                self.boundary_right
                and self.right > self.boundary_right
                and self.change_x > 0
            ):
                self.change_x *= -1


            if (
                self.boundary_left
                and self.left < self.boundary_left
                and self.change_x < 0
            ):

                self.change_x *= -1



class RobotEnemy(Enemy):
    def __init__(self, bullet_block=None):

        # Set up parent class
        super().__init__("robot", bullet_block=None)
        self.bullet_block = bullet_block


    def on_update(self, delta_time: float = 1 / 60):
        super().on_update()

class NLoEnemy(Enemy):
    def __init__(self, bullet_block=None):

        # Set up parent class
        super().__init__("nlo", bullet_block=None)
        self.bullet_block = bullet_block

    def on_update(self, delta_time: float = 1 / 60):

        super().on_update()









import arcade


from paths import *
import os
import random


class Entity(arcade.Sprite):
    def __init__(self, name_folder, pos,  **kwargs):
        super().__init__()
        self.flipH = kwargs.get('flipH', False)
        self.flipV = kwargs.get('flipV', False)
        self.scale = 1
        self.name_folder = name_folder
        self.pos = pos
        self.cur_texture = 0
        main_path = ANIMATION_OBJECTS / name_folder
        self.leng = len(os.listdir(main_path))
        # print(self.leng)



        self.anim_textures = []
        for i in range(1, self.leng+1):
            p = f"{main_path}/{i}.png"
            # print(self.flipH)
            texture = arcade.load_texture(p, flipped_horizontally=self.flipH, flipped_vertically=self.flipV)
            self.anim_textures.append(texture)




class AnimateObject(arcade.Sprite):
    def __init__(self, game, tile_object):

        super().__init__()
        self.game = game
        self.tile_object = tile_object
        self.properties = self.tile_object.properties
        self.center_x = tile_object.coordinates.x+tile_object.size.width/2
        self.center_y = ((self.game.tile_map.tile_height*self.game.tile_map.height) -  tile_object.coordinates.y)+tile_object.size.height/2
        self.scale = tile_object.size.height/self.properties.get('h', tile_object.size.height)
        # print(self.scale)
        self.flipH = self.properties.get('flipH', False)
        self.flipV = self.properties.get('flipV', False)
        main_path = ANIMATION_OBJECTS / tile_object.name
        self.speed_anim = self.properties.get('speed', 5)
        images = [os.path.join(main_path, x) for x in sorted(os.listdir(main_path))]
        if self.properties.get('random_frame', False):
            random.shuffle(images)


        self.cur_texture = 0

        self.leng = len(os.listdir(main_path))-1




        self.anim_textures = []
        for p in images:
            texture = arcade.load_texture(p, flipped_horizontally=self.flipH, flipped_vertically=self.flipV)
            self.anim_textures.append(texture)

        self.texture = self.anim_textures[0]
        self.alpha = self.properties.get('alpha', 255)

    def update_animation(self, delta_time: float = 1 / 60):
        self.cur_texture += 1
        # print(self.cur_texture, 444)
        if self.cur_texture > (self.leng) * self.speed_anim:
            self.cur_texture = 0
        frame = self.cur_texture // self.speed_anim

        self.texture = self.anim_textures[frame]













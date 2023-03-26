
import os
import math
import arcade
from base_game_parent import BaseGame
from tilemap import TileMap
from camera import Camera

from const import *

file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)



LAYER_OPTIONS = {
    LAYER_NAME_PLATFORMS: {"use_spatial_hash": True},
}


class GameView(BaseGame):
    def __init__(self, size):
        super().__init__()
        self.size = size
        self.width = size[0]
        self.height = size[1]
        self.next_view = None
        self.level = 1

    def __getattr__(self, item):
        if item in self.__dict__:
            return item

    def setup(self):
        map_name = f"levels/map_{self.level}.json"
        self.tile_map = TileMap(map_name, SPRITE_SCALING_TILES, LAYER_OPTIONS)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.scene.add_sprite_list(LAYER_NAME_PLAYER)
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=DEFAULT_DAMPING,
                                                         gravity=(0, -GRAVITY))
        cam_w = self.tile_map.width*SPRITE_IMAGE_SIZE*SPRITE_SCALING_TILES
        cam_h = self.tile_map.height*SPRITE_IMAGE_SIZE*SPRITE_SCALING_TILES

        self.view_left = 0
        self.view_bottom = 0
        self.camera = Camera(0, 0, cam_w/2, cam_h/2)
        self.gui_camera = Camera(0, 0, cam_w/2, cam_h/2)

        self._init_player_sprite()
        self._init_phisics_items()
        self.camera.pan_camera_to_user(self.player_sprite, panning_fraction=0.1)
        self.list_for_button = arcade.SpriteList()
        self.box_down_button = False
        self.box_up_button = False
        self.curr_y = 2

        self.list_for_button.extend(self.scene[LAYER_NAME_DINAMIC])
        self.list_for_button.extend(self.scene[LAYER_NAME_PLAYER])

    def on_update(self, delta_time):
        self.camera.pan_camera_to_user(self.player_sprite, panning_fraction=0.1)
        self.player_sprite.update()
        self.update_mooving_platform(delta_time)
        self.update_mooving_platform_on_item(delta_time)
        self.update_buttons(delta_time)
        self.physics_engine.step()

    def on_draw(self):
        arcade.start_render()
        self.clear()
        self.camera.use()

        self.scene.draw()

    def on_resize(self, width, height):
        self.camera.resize(width, height)

    def on_show(self):
        color = self.tile_map.background_color
        if color:
            arcade.set_background_color(self.tile_map.background_color)

    def set_player_jump_impuls(self):
        if self.physics_engine.is_on_ground(self.player_sprite) \
                and not self.player_sprite.is_on_ladder:
            # She is! Go ahead and jump
            impulse = (0, PLAYER_JUMP_IMPULSE)
            self.physics_engine.apply_impulse(self.player_sprite, impulse)

    def update_buttons(self, delta_time):
        self._collision_box_button(delta_time)
        self._collision_player_button(delta_time)

    def _collision_box_button(self, delta_time):
        for pl in self.scene[LAYER_NAME_BUTTON]:
            for d in self.list_for_button:
                l = pl.left - 26
                r = pl.right + 26
                diff_y = d.center_y - pl.center_y
                if (d.center_x > l and d.center_x< r) and diff_y < 25.0:
                    pl.change_y = -1
                    self.check_sprite(LAYER_NAME_MOOVING, 'mooving1', True)
                    self.box_on_button = True
                elif pl.center_y < 210:
                    pl.change_y = 1
                else:
                    self.box_on_button = False
                    self.check_sprite(LAYER_NAME_MOOVING, 'mooving1', False)
                    pl.change_y = 0
                velocity = (pl.change_x * 1 / delta_time, pl.change_y * 1 / delta_time)
                self.physics_engine.set_velocity(pl, velocity)

    def _collision_player_button(self, delta_time):
        if not self.box_on_button:
            for pl2 in self.scene[LAYER_NAME_BUTTON]:
                l = pl2.left - 28
                r = pl2.right + 28
                diff_y2 = self.player_sprite.center_y - pl2.center_y
                # print(arcade.get_cpl2.center_y)
                if (self.player_sprite.center_x > l and self.player_sprite.center_x< r) and diff_y2 < 60:
                    pl2.change_y = -2

                    self.check_sprite(LAYER_NAME_MOOVING, 'mooving1', True)
                elif pl2.center_y < 210:
                    pl2.change_y = 2

                else:
                    pl2.change_y = 0
                    self.check_sprite(LAYER_NAME_MOOVING, 'mooving1', False)


                velocity2 = (pl2.change_x * 1 / delta_time, pl2.change_y * 1 / delta_time)
                self.physics_engine.set_velocity(pl2, velocity2)

    def check_sprite(self, list_name, sprite_name, check):
        for pl in self.scene[list_name]:
            if pl.properties['name'] == sprite_name:
                pl.properties['active'] = check

    def update_mooving_platform_on_item(self, delta_time):
        """
        работает когда стоиш на ней
        :param delta_time:
        """
        for moving_sprite in self.scene[LAYER_NAME_MOOVING_ON_ITEM]:

            coll = moving_sprite.collides_with_list(self.scene[LAYER_NAME_DINAMIC])
            if coll:
                diff = coll[0].bottom - moving_sprite.top
                if -3 < diff < 3:
                    moving_sprite.properties['active'] = True
                    self.box_down_button = True
                else:
                    moving_sprite.properties['active'] = False
                    self.box_down_button = False
                if moving_sprite.properties['active']:
                    self._mooving_platform(moving_sprite)
                    velocity = (moving_sprite.change_x * 1 / delta_time, moving_sprite.change_y * 1 / delta_time)
                    self.physics_engine.set_velocity(moving_sprite, velocity)
                else:
                    self.physics_engine.set_velocity(moving_sprite, (0, 0))


            if not self.box_down_button:
                for item in self.scene[LAYER_NAME_PLAYER]:
                    l = moving_sprite.left - 26
                    r = moving_sprite.right + 26
                    if (moving_sprite.properties['type'] == 'on_press'
                             and (item.center_x > l and item.center_x< r)
                             and -2 < moving_sprite.top - item.bottom < 2):
                            moving_sprite.properties['active'] = True
                    else:
                        moving_sprite.properties['active'] = False



                    if moving_sprite.properties['active']:
                        self._mooving_platform(moving_sprite)
                        velocity = (moving_sprite.change_x * 1 / delta_time, moving_sprite.change_y * 1 / delta_time)
                        self.physics_engine.set_velocity(moving_sprite, velocity)
                    else:
                        self.physics_engine.set_velocity(moving_sprite, (0, 0))

    def _mooving_platform(self, moving_sprite):
        if moving_sprite.boundary_right and \
                moving_sprite.change_x > 0 and \
                moving_sprite.right > moving_sprite.boundary_right:
            moving_sprite.change_x *= -1
        elif moving_sprite.boundary_left and \
                moving_sprite.change_x < 0 and \
                moving_sprite.left < moving_sprite.boundary_left:
            moving_sprite.change_x *= -1
        if moving_sprite.boundary_top and \
                moving_sprite.change_y > 0 and \
                moving_sprite.top > moving_sprite.boundary_top:
            moving_sprite.change_y *= -1
        elif moving_sprite.boundary_bottom and \
                moving_sprite.change_y < 0 and \
                moving_sprite.bottom < moving_sprite.boundary_bottom:
                moving_sprite.change_y *= -1

    def update_mooving_platform(self, delta_time):
        for moving_sprite in self.scene[LAYER_NAME_MOOVING]:
            if moving_sprite.properties['active']:
                if moving_sprite.boundary_right and \
                        moving_sprite.right > moving_sprite.boundary_right:
                    moving_sprite.change_x *= -1
                elif moving_sprite.boundary_left and \
                        moving_sprite.change_x < 0 and \
                        moving_sprite.left < moving_sprite.boundary_left:
                    moving_sprite.change_x *= -1
                if moving_sprite.boundary_top and \
                        moving_sprite.change_y > 0 and \
                        moving_sprite.top > moving_sprite.boundary_top:
                    moving_sprite.change_y *= -1
                elif moving_sprite.boundary_bottom and \
                        moving_sprite.change_y < 0 and \
                        moving_sprite.bottom < moving_sprite.boundary_bottom:
                    moving_sprite.change_y *= -1
                velocity = (moving_sprite.change_x * 1 / delta_time, moving_sprite.change_y * 1 / delta_time)
                self.physics_engine.set_velocity(moving_sprite, velocity)
            else:
                self.physics_engine.set_velocity(moving_sprite, (0, 0))

    def set_next_view(self, next_view):
        self.next_view = next_view




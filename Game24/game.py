import math
import operator
import time
import yaml
import arcade
from base_game_parent import BaseGame
from gui.interface import Interface
from sprites import mooving_platform
from tilemap import TileMap
from camera import Camera
from paths import *

from const import *
from sprites.bullet_sprite import Bullet
from sprites.animation_objects import AnimateObject
from sprites.nps import Nps
from text_interface import TextInterface
from text_interface2 import TextInterface2

file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)


from arcade import load_texture
from arcade.gui import UIManager
from arcade.gui.widgets import UITextArea, UIInputText, UITexturePane




list_for_scene = (LAYER_NAME_PLATFORMS,
LAYER_NAME_PLAYER,
LAYER_NAME_DINAMIC,
LAYER_NAME_BUTTON,
LAYER_NAME_MOOVING,
LAYER_NAME_GATE,
LAYER_NAME_MOOVING_ON_ITEM,
LAYER_NAME_LADDERS,
LAYER_NAME_OBJECTPLATFORM,
LAYER_NAME_DONT_TOUCH,
LAYER_NAME_INVERTORY,
LAYER_NAME_ANIMATION,
LAYER_NAME_BULLET)




LAYER_OPTIONS = {
    LAYER_NAME_PLATFORMS: {"use_spatial_hash": True},
}

def load_settings(file):
    with open(file) as f:
        templates = yaml.safe_load(f)
    return templates

def save_settings(file, data):
    with open(file, 'w') as f:
        yaml.dump(data, f)

class GameView(BaseGame):
    def __init__(self, size):
        super().__init__()
        self.game_pause = False
        self.size = size
        self.width = size[0]
        self.height = size[1]
        self.next_view = None
        self.level = 1
        self.map_name = f"levels/map_{self.level}.json"
        self.scene = arcade.Scene()
        self.tile_map = TileMap(self.map_name, SPRITE_SCALING_TILES, LAYER_OPTIONS)

        # for name, obj in self.tile_map.sprite_lists.items():
        #     if name in list_for_scene:
        #         self.scene.add_sprite_list(name, sprite_list=obj)

        # self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.check_points_list = [(round(x.shape[0]), round(x.shape[1])) for x in self.tile_map.get_obgect_by_name("check_point", "Mark")][::-1]
        self.current_check_point = load_settings('saves/save.yaml')["player"]["pos"]
        print(load_settings('saves/save.yaml'))
        arcade.exit()

        self.save_player_pos()
        self.tic = -1



    def set_pause(self, v: bool):
        self.game_pause = v
        if not v:
            self.text_interface.set_visible(False)
            self.curreent_nps.state = "wait"
        else:
            if self.player_sprite.center_x - self.curreent_nps.center_x < 0:
                k = -5
                self.left_pressed = True
            else:
                k = 5
                self.right_pressed = True
            self._xn = (self.player_sprite.center_x +k, k)





    def __getattr__(self, item):
        if item in self.__dict__:
            return item



    def save_player_pos(self):
        sett = load_settings('saves/save.yaml')
        sett['player']['pos'] = list(self.current_check_point)
        save_settings('saves/save.yaml', sett)

    def create_bullet(self,x, y):
               if self.on_bullet:
                    self.collision_lists = [self.player_list,
                                self.wall_list,
                                self.box_list
                                ]
                    if len(self.scene[LAYER_NAME_BULLET].sprite_list) > 10:
                        k = self.scene[LAYER_NAME_BULLET].pop(0)
                        k.kill()

                    bullet = Bullet(":resources:images/space_shooter/laserBlue01.png", collisions_lists=self.collision_lists, damage=50)
                    self.scene.add_sprite(LAYER_NAME_BULLET, bullet)
                    start_x = self.player_sprite.center_x
                    start_y = self.player_sprite.center_y
                    bullet.position = self.player_sprite.position
                    dest_x = x + self.view_left
                    dest_y = y + self.view_bottom
                    x_diff = dest_x - start_x
                    y_diff = dest_y - start_y
                    angle = math.atan2(y_diff, x_diff)

                    size = max(self.player_sprite.width, self.player_sprite.height) / 2
                    bullet.center_x += size * math.cos(angle)
                    bullet.center_y += size * math.sin(angle)
                    bullet.angle = math.degrees(angle)

                    bullet_gravity = (0, -100)


                    self.physics_engine.add_sprite(bullet,
                                                   mass=2,
                                                   damping=1,
                                                   friction=0.9,
                                                   collision_type="bullet",
                                                   gravity=bullet_gravity,
                                                   elasticity=0.5)

                    force = (BULLET_MOVE_FORCE, 1)
                    self.physics_engine.apply_force(bullet, force)

    def up(self):
        self.change_x  = 2
        velocity = (self.change_x * 1 / 60, self.change_y * 1 / 60)
        self.physics_engine.set_velocity(self, velocity)

    def set_curreent_nps(self, nps):
        print('22222')
        self.curreent_nps = nps

    def setup(self):



        self.curreent_nps = None
        self.on_bullet = True
        self.tile_map = TileMap(self.map_name, SPRITE_SCALING_TILES, LAYER_OPTIONS)
        self.height_game = self.tile_map.height*self.tile_map.tile_height*SPRITE_SCALING_TILES
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.scene.add_sprite_list(LAYER_NAME_PLAYER)

        self.contact_text = arcade.SpriteList()

        self.text_interface = TextInterface()
        self.text_interface.set_pos(self.width/2,self.text_interface.rect[1]/2)

        self.text_interface2 = TextInterface2()
        self.text_interface2.set_pos(self.width/2,self.text_interface2.height/2)








        self.physics_engine = arcade.PymunkPhysicsEngine(damping=DEFAULT_DAMPING,
                                                         gravity=(0, -GRAVITY))
        cam_w = self.tile_map.width*SPRITE_IMAGE_SIZE*SPRITE_SCALING_TILES
        cam_h = self.tile_map.height*SPRITE_IMAGE_SIZE*SPRITE_SCALING_TILES

        self.view_left = 0
        self.view_bottom = 0
        self.camera = Camera(0, 0, cam_w/2, cam_h/2)
        self.gui_camera = Camera(0, 0, cam_w/2, cam_h/2)

        self.scene.add_sprite_list(LAYER_NAME_NPS)
        for name, layer in self.tile_map.object_lists.items():
            if name == LAYER_NAME_NPS:
                for obj in layer:
                    nps = Nps(self, obj, self.physics_engine)
                    self.scene.add_sprite(LAYER_NAME_NPS, nps)

        self._init_player_sprite()



        self.scene.add_sprite_list(LAYER_NAME_BULLET)

        # self.current_check_point = load_settings('saves/save.yaml')['player']['pos']
        self._init_phisics_items()
        self.camera.pan_camera_to_user(self, self.player_sprite, panning_fraction=0.1)
        self.list_for_button = arcade.SpriteList()
        self.box_down_button = False
        self.box_up_button = False
        self.curr_y = 2
        self.list_for_button.extend(self.scene[LAYER_NAME_DINAMIC])
        self.save_ckick = False
        P  ='myresources/icons/Untitled.png'
        self.interface = Interface(P, 64, self.height-64)
        self.interface.append_cell()

        self.animation_list = arcade.SpriteList()
        for o in self.tile_map.tiled_map.layers:
            if o.name == 'animation':

                for x in o.tiled_objects:

                    obj = AnimateObject(self, x)
                    self.animation_list.append(obj)
                self.scene.add_sprite_list_before(LAYER_NAME_ANIMATION, LAYER_NAME_PLATFORMS, sprite_list=self.animation_list)

        # for objx in self.scene[LAYER_NAME_ANIMATION]:
        #     object_name = objx.properties
        #     print(objx.scale)
        #     print('iiiiiiiiiiiiiiiiiiiiiiiiiiiii')
        #     flip = objx.properties.get('flipH', False)
        #     path_dir = ANIMATION_OBJECTS / object_name
        #     obj = AnimateObject(path_dir, objx.position, flipH=flip)
        #
        #
        #
        #     self.animation_list.append(obj)
        # def player_hit_handler(player_sprite, Dont_touch, _arbiter, _space, _data):
        #     self.setup()
        # self.physics_engine.add_collision_handler("player", "Dont_touch", post_handler=player_hit_handler)
    def save_game(self):
            self.current_check_point = self.player_sprite.center_x+10, self.player_sprite.center_y + 192
            self.save_ckick = True
            self.tic = int(time.perf_counter())


    def on_update(self, delta_time):

        self.camera.pan_camera_to_user(self, self.player_sprite, panning_fraction=0.1)

        self.scene.update(names=[LAYER_NAME_PLAYER,LAYER_NAME_BULLET, LAYER_NAME_NPS])
        mooving_platform.update_mooving_platform(self.scene[LAYER_NAME_MOOVING], self.physics_engine, delta_time)
        self.update_mooving_platform_on_item(delta_time)
        self.update_buttons(delta_time)
        self.update_gate(delta_time)
        if self.player_sprite.collides_with_list(self.scene[LAYER_NAME_DONT_TOUCH]):
            self.setup()
        inv = self.player_sprite.collides_with_list(self.scene[LAYER_NAME_INVERTORY])
        if inv:
            for i in inv:
                self.interface.append_item(i)
                i.kill()


        if self.tic >= 0:
            if int(time.perf_counter())-self.tic > 1:
                self.tic = -1
                self.save_ckick = False

        if self._xn is not None:
            print('@@@@@@@@@@@@@@@@@@@@@@@')
            if self._xn[1] < 0:
                if self.player_sprite.center_x < self._xn[0]:
                    self.left_pressed = False
                    self.player_sprite.turn_texture_right()
                    self._xn = None
            else:
                 if self.player_sprite.center_x > self._xn[0]:
                    self.right_pressed = False
                    self.player_sprite.turn_texture_left()
                    self._xn = None

        for obj in self.scene[LAYER_NAME_DINAMIC_KEY]:
            if obj.properties['active']:
                yn = self.height_game - obj.properties['yy']
                xn = obj.properties['xx']
                diff_x = abs(obj.center_x - xn)
                diff_y = abs(obj.center_y - yn)
                if diff_x > 44 or diff_y > 44:
                    self.check_sprite(LAYER_NAME_GATE, obj.properties['link'], True)
                    obj.properties['active'] = False



        self.interface.update()
        self.physics_engine.step()




    def update_gate(self, delta_time):
        for moving_sprite in self.scene[LAYER_NAME_GATE]:
            open_x = round(moving_sprite.properties.get('open_x', None))
            close_x = round(moving_sprite.properties.get('close_x', None))
            open_y = moving_sprite.properties.get('open_y', None)
            if open_x:
                if open_x - close_x > 0:
                    speedf = 1
                    oper_open = operator.lt
                    oper_close = operator.gt
                else:
                    oper_open = operator.gt
                    oper_close = operator.lt
                    speedf = -1

                if moving_sprite.properties['active']:
                    if open_x and oper_open(round(moving_sprite.center_x), open_x):
                        moving_sprite.change_x  = 2 * speedf
                        velocity = (moving_sprite.change_x * 1 / delta_time, moving_sprite.change_y * 1 / delta_time)
                        self.physics_engine.set_velocity(moving_sprite, velocity)
                    else:
                        moving_sprite.change_x  = 0
                        velocity = (0, 0)
                        self.physics_engine.set_velocity(moving_sprite, velocity)
                else:
                    if oper_close(moving_sprite.center_x, close_x):
                        moving_sprite.change_x  = -2 * speedf
                        velocity = (moving_sprite.change_x * 1 / delta_time, moving_sprite.change_y * 1 / delta_time)
                        self.physics_engine.set_velocity(moving_sprite, velocity)
                    else:
                        moving_sprite.change_x  = 0
                        velocity = (0, 0)
                        self.physics_engine.set_velocity(moving_sprite, velocity)


    def save_text(self):
        arcade.draw_text(
            'Save',
            self.width-100,
            self.height-50,
            arcade.csscolor.WHITE,
            18,
        )

    def on_draw(self):
        arcade.start_render()
        self.clear()
        self.camera.use()



        self.scene.draw()
        self.scene.update_animation(1/60)


        self.gui_camera.use()
        # self.manager.draw()
        self.interface.draw()
        # self.text_interface.draw()
        self.text_interface2.draw()
        if self.save_ckick:
            self.save_text()


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
                diff_y3 = d.bottom - pl.top
                if -12 < diff_y3 < 12:
                        if (d.center_x > l and d.center_x< r):



                            pl.change_y = -1
                            # print(diff_y3, "#######")

                            self.check_sprite(LAYER_NAME_MOOVING, pl.properties["link"], True)
                            self.box_on_button = True
                        elif pl.center_y < pl.properties['check_y']:
                            pl.change_y = 1
                        else:
                            self.box_on_button = False
                            self.check_sprite(LAYER_NAME_MOOVING, pl.properties["link"], False)
                            pl.change_y = 0
                velocity = (pl.change_x * 1 / delta_time, pl.change_y * 1 / delta_time)
                self.physics_engine.set_velocity(pl, velocity)

    def _collision_player_button(self, delta_time):

        if not self.box_on_button:
            for pl2 in self.scene[LAYER_NAME_BUTTON]:
                l = pl2.left - 28
                r = pl2.right + 28
                diff_y2 = self.player_sprite.center_y - pl2.center_y
                diff_y3 = self.player_sprite.bottom - pl2.top

                if (self.player_sprite.center_x > l and self.player_sprite.center_x< r) and -1 <diff_y3 < 4:
                    pl2.change_y = -2
                    # print(diff_y3, '!!!!!')

                    self.check_sprite(LAYER_NAME_MOOVING, pl2.properties["link"], True)
                elif pl2.center_y < pl2.properties['check_y']:
                    pl2.change_y = 2

                else:

                    pl2.change_y = 0
                    self.check_sprite(LAYER_NAME_MOOVING, pl2.properties["link"], False)


                velocity2 = (pl2.change_x * 1 / delta_time, pl2.change_y * 1 / delta_time)
                self.physics_engine.set_velocity(pl2, velocity2)

    def check_sprite(self, list_name, sprite_name, check):
        for pl in self.scene[list_name]:

            if pl.properties['name'] == sprite_name:

                if pl.properties['name'] == 'p2':
                    pass
                    # print(pl.properties['name'], "!!!!")
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

    def y_calc(self, y):
        return (self.tile_map.height * (self.tile_map.tile_height * TILE_SCALING)) - y

    def set_next_view(self, next_view):
        self.next_view = next_view




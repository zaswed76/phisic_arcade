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
from sprites.bullet_sprite import Bullet, BulletSingleBlock
from sprites.animation_objects import AnimateObject
from sprites.nps import Nps
from text_interface2 import TextInterface2
from sprites.explosion import Explosion, get_explosian_texture
from sprites.enemy import RobotEnemy, NLoEnemy, Enemy
file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)
from pathlib import Path






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

columns = 5
count = 20
sprite_width = 96
sprite_height = 96
file_name =  EXPLOSION / "EXP96.png"


def load_settings(file):
    with open(file) as f:
        templates = yaml.safe_load(f)
    return templates



EXPLOSION_TEXTURE_LIST_96 = get_explosian_texture(EXPLOSION, 'EXP96')
EXPLOSION_TEXTURE_LIST_ice = get_explosian_texture(EXPLOSION, 'ice_exp')
EXPLOSION_TEXTURE_LIST_fiolet_1_exp = get_explosian_texture(EXPLOSION, 'fiolet_1_exp')
EXPLOSION_TEXTURE_LIST_exp111 = get_explosian_texture(EXPLOSION, 'exp111')

BULLET_BLOCK_TYPES = {'BulletSingleBlock': BulletSingleBlock}



EXPLOSIANS_TEXTURES = {'EXPLOSION_TEXTURE_LIST_96': EXPLOSION_TEXTURE_LIST_96,
                       'EXPLOSION_TEXTURE_LIST_ice': EXPLOSION_TEXTURE_LIST_ice,
                       'EXPLOSION_TEXTURE_LIST_fiolet_1_exp': EXPLOSION_TEXTURE_LIST_fiolet_1_exp,
                       'EXPLOSION_TEXTURE_LIST_exp111': EXPLOSION_TEXTURE_LIST_exp111
                       }



def save_settings(file, data):
    with open(file, 'w') as f:
        yaml.dump(data, f)

class Scene(arcade.Scene):
    def __init__(self):
        super().__init__()



    def get_layer_by_name(self, layer_name):
        for i in self.sprite_lists:
            print(i.name)

class GameView(BaseGame):
    def __init__(self, size):
        super().__init__()
        self.blocks_all = {}

        self.permanent_items = arcade.SpriteList()
        self.enemies_type = {"robot": RobotEnemy, 'nlo': NLoEnemy}
        self._xn = None
        self.jupm_impulse_k = 0
        self.box_on_button = False
        self.game_pause = False
        self.size = size
        self.width = size[0]
        self.height = size[1]
        self.next_view = None
        self.level = 1
        self.load_flag  = None
        self._bullet_list_for_portal = []
        self.current_person = 0

        self.explosions_list = None

        self.check_btn_texture = arcade.load_texture(CHECK_BTN_TEXTURE)
        self.uncheck_btn_texture = arcade.load_texture(UNCHECK_BTN_TEXTURE)
        self.enemies_collision_lists = []
        self.settings = load_settings('saves/save.yaml')
        self.portal_stoun_flag = self.settings["player"]["portal_stoun_flag"]
        if self.portal_stoun_flag:
            self.set_permanent_item("PORTAL_STOUN")

    def create_bullet(self, name_bullet, x, y, force=BULLET_MOVE_FORCE, cfg_bullet=STANDART_BULLET, scale=1, type=Bullet.BULLET_TYPE, alpha=255, damage=10):
               img = BULLETS / f"{name_bullet}.png"
               if self.on_bullet:

                    if type == Bullet.BULLET_TYPE and len(self.scene[LAYER_NAME_BULLET].sprite_list) > 10:
                        k = self.scene[LAYER_NAME_BULLET].pop(0)
                        k.kill()
                    if type == Bullet.BOX_TYPE and  len(self.scene[LAYER_NAME_BOX].sprite_list) > 0:
                        k = self.scene[LAYER_NAME_BOX].pop(0)
                        k.kill()
                    bullet = Bullet(self, self.player_sprite, img, cl=self.collision_lists,
                                    damage=damage, type=type, alpha=alpha, cfg_bullet=cfg_bullet)

                    bullet.set_explosion(EXPLOSION_TEXTURE_LIST_96, explosion_scale=1)
                    bullet.scale = scale
                    if type == Bullet.BULLET_TYPE:
                        self.scene.add_sprite(LAYER_NAME_BULLET, bullet)
                    elif type == Bullet.BOX_TYPE:
                        self.scene.add_sprite(LAYER_NAME_BOX, bullet)
                        self.list_for_button.append(bullet)
                        self.coll_list_for_on_item_platform.append(bullet)
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
                    self.physics_engine.add_sprite(bullet,
                                                   **cfg_bullet)
                    force = (force, 1)
                    self.physics_engine.apply_force(bullet, force)

    def init_enemys(self):
        self.blocks_all.clear()
        config = load_settings(LEVELS / f'enemy_cfg_{self.level}_level.yaml')
        if config is None:
            return
        self.enemies_collision_lists.clear()
        self.enemies_collision_lists.extend(self.collision_lists)
        self.enemies_collision_lists.append(self.scene[LAYER_NAME_PLAYER])
        enemies_layer = self.tile_map.object_lists[LAYER_NAME_ENEMIES]
        for my_object in enemies_layer:
            cfg = config.get(my_object.name)
            if cfg is None:
                continue
            cartesian = self.tile_map.get_cartesian(
                my_object.shape[0], my_object.shape[1]
            )
            enemy_type = my_object.properties["type"]


            enemy = self.enemies_type[enemy_type]()
            enemy.name = my_object.name
            enemy.game = self
            enemy.emplosion_texture = EXPLOSION_TEXTURE_LIST_ice
            enemy.emplosion_scale = 3
            blocks = cfg['bullet_blocks']
            live = cfg.get('live', 1000)
            if blocks is not None:
                for blocks_dict in blocks:
                    for n, k in enumerate(blocks_dict.items()):
                        name, bl = k



                        self.blocks_all[(n, name)] = BULLET_BLOCK_TYPES[bl['type']](self,enemy, bl['bullet_name'],
                                          EXPLOSIANS_TEXTURES.get(bl.get('explosion')), bl['direct'],
                                          delay=bl['delay'], bullet_scale=bl['bullet_scale'],
                                          collision_lists=self.enemies_collision_lists,
                                          physics_engine=self.physics_engine, force=bl['force'],
                                          explosion_scale=bl['explosion_scale'], pos=bl['pos'],
                                          cfg_bullet=BULLETS_CFG.get(bl['config_bullet']),
                                          kill_distance=bl.get('kill_distance', 2000)
                                                                                    )
                        arcade.schedule(self.blocks_all[(n, name)].get_bullet, bl['delay'])
                        enemy.set_bullet_block(self.blocks_all[(n, name)], bl['pos'])

            enemy.scale = my_object.properties.get('scale', 1)
            enemy.live = live


            enemy.center_x = math.floor(
                cartesian[0] * TILE_SCALING * self.tile_map.tile_width
            )
            enemy.center_y = math.floor(
                (cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SCALING)
            )
            if "boundary_left" in my_object.properties:
                enemy.boundary_left = my_object.properties["boundary_left"]
            if "boundary_right" in my_object.properties:
                enemy.boundary_right = my_object.properties["boundary_right"]
            if "change_x" in my_object.properties:
                enemy.change_x = my_object.properties["change_x"]
            self.scene.add_sprite(LAYER_NAME_ENEMIES, enemy)

    def init_mooving_bg(self):
        for obj in self.scene[LAYER_NAME_MOOV_BACKGROUND]:
            obj.alpha = obj.properties.get('alpha', 255)

    def setup(self):
        for b in self.blocks_all.values():
            arcade.unschedule(b.get_bullet)
            del(b)
        self.blocks_all.clear()

        self.background = arcade.load_texture(BG_TEX)
        self.explosions_list = arcade.SpriteList()
        self.bullet_enemys_list = arcade.SpriteList()


        self.curreent_nps = None
        self.on_bullet = True
        self.level = self.settings['level']
        self.map_name = f"levels/map_{self.level}.json"
        self.tile_map = TileMap(self.map_name, SPRITE_SCALING_TILES, LAYER_OPTIONS)
        self.check_points_list = [(round(x.shape[0]), round(x.shape[1])) for x in self.tile_map.get_obgect_by_name("check_point", "Mark")][::-1]
        if self.load_flag == "check_point":
            self.current_check_point = self.check_points_list[-1]
        else:

            self.current_check_point = self.settings["player"]["pos"]
        self.load_flag  = None
        self.tic = -1
        self.height_game = self.tile_map.height*self.tile_map.tile_height*SPRITE_SCALING_TILES
        self.scene = Scene.from_tilemap(self.tile_map)
        self.scene.add_sprite_list(LAYER_NAME_PLAYER)
        self.scene.add_sprite_list(LAYER_NAME_BOX)
        self.contact_text = arcade.SpriteList()
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
        self.collision_lists = [
                                self.scene[LAYER_NAME_PLATFORMS],
                                self.scene[LAYER_NAME_INVERTORY],
                                self.scene[LAYER_NAME_DINAMIC],
                                self.scene[LAYER_NAME_BUTTON],
                                self.scene[LAYER_NAME_GATE],
                                self.scene[LAYER_NAME_DINAMIC_KEY],
                                self.scene[LAYER_NAME_DONT_TOUCH],
                                self.scene[LAYER_NAME_MOOVING],
                                self.scene[LAYER_NAME_MOOVING_ON_ITEM],
                                self.scene[LAYER_NAME_OBJECTPLATFORM],
                                ]
        self.coll_list_for_on_item_platform = arcade.SpriteList()
        self.coll_list_for_on_item_platform.extend(self.scene[LAYER_NAME_DINAMIC])

        self._init_player_sprite()
        self.init_enemys()
        self.init_mooving_bg()


        self.scene.move_sprite_list_before(LAYER_NAME_PORTAL, LAYER_NAME_PLAYER)

        self.scene.add_sprite_list(LAYER_NAME_BULLET)
        self.scene.add_sprite_list(LAYER_NAME_BOX)


        for b in self._bullet_list_for_portal:
            pass
            # obj, pos = b

            # self.create_bullet(obj.name, pos[0]-50, pos[1]-20,  force=0, cfg_bullet=obj.cfg_bullet, type=obj.type, scale=obj.scale)
        self._bullet_list_for_portal.clear()
        # self.current_check_point = load_settings('saves/save.yaml')['player']['pos']
        self._init_phisics_items()
        self.camera.pan_camera_to_user(self, self.player_sprite, panning_fraction=0.1)
        self.list_for_button = arcade.SpriteList()
        self.box_down_button = False
        self.box_up_button = False
        self.curr_y = 2
        try:
            self.list_for_button.extend(self.scene[LAYER_NAME_DINAMIC])
            pass

        except KeyError:
            pass
        self.save_ckick = False
        P  ='myresources/icons/Untitled.png'
        self.interface = Interface(P, 64, self.height-64)
        self.interface.append_cell()
        self.interface.append_cell()
        self.interface.append_cell()
        self.interface.append_cell()
        self.interface.append_cell()

        self.animation_list = arcade.SpriteList()
        for o in self.tile_map.tiled_map.layers:
            if o.name == 'animation':

                for x in o.tiled_objects:

                    obj = AnimateObject(self, x)
                    self.animation_list.append(obj)
                self.scene.add_sprite_list_before(LAYER_NAME_ANIMATION, LAYER_NAME_PLATFORMS, sprite_list=self.animation_list)

    def set_pause(self, v: bool):
        self.game_pause = v
        if not v:
            self.text_interface2.set_visible(False)
            self.curreent_nps.state = "wait"
        else:
            if self.player_sprite.center_x - self.curreent_nps.center_x < 0:
                k = -5
                self.left_pressed = True
            else:
                k = 5
                self.right_pressed = True
            self._xn = (self.player_sprite.center_x +k, k)

    def save_player_pos(self):
        sett = load_settings('saves/save.yaml')
        sett['player']['pos'] = list(self.current_check_point)
        save_settings('saves/save.yaml', sett)

    def save_lavel(self):
        sett = load_settings('saves/save.yaml')
        sett['player']['pos'] = list(self.current_check_point)
        sett['level'] = self.level
        save_settings('saves/save.yaml', sett)


    def up(self):
        self.change_x  = 2
        velocity = (self.change_x * 1 / 60, self.change_y * 1 / 60)
        self.physics_engine.set_velocity(self, velocity)

    def set_curreent_nps(self, nps):

        self.curreent_nps = nps

    def save_game(self):
            self.current_check_point = self.player_sprite.center_x+10, self.player_sprite.center_y + 64
            self.save_ckick = True
            self.tic = int(time.perf_counter())

    def create_explosion(self, pos, texture_list = None, scale=1):
        if texture_list is None:
            texture_list = EXPLOSION_TEXTURE_LIST_96
        explosion = Explosion(texture_list)
        explosion.scale = scale
        explosion.center_x = pos[0]
        explosion.center_y = pos[1]
        explosion.update()
        self.explosions_list.append(explosion)

    def on_update(self, delta_time):

        self.camera.pan_camera_to_user(self, self.player_sprite, panning_fraction=0.1)

        self.scene.update(names=[LAYER_NAME_PLAYER,LAYER_NAME_BULLET, LAYER_NAME_NPS, LAYER_NAME_ENEMIES])
        self.explosions_list.on_update(1/10)
        for obj in self.scene[LAYER_NAME_MOOV_BACKGROUND]:
            r = obj.properties.get('rotation', 0)
            sx = obj.properties.get('change_x', 0)
            sy = obj.properties.get('change_y', 0)
            alpha = obj.properties.get('alpha', 255)

            obj.center_x += sx
            obj.center_y += sy
            obj.angle +=r


        self.scene[LAYER_NAME_ENEMIES].on_update()
        # self.bullet_enemys_list.update()



        for p in self.scene[LAYER_NAME_PORTAL]:
            c = p.collides_with_sprite(self.player_sprite)
            if c:
                self.level = p.properties['level']
                self.save_lavel()

                self.load_flag = "check_point"
                self.setup()

        for p in self.scene[LAYER_NAME_PORTAL]:
            c = p.collides_with_list(self.scene[LAYER_NAME_BOX])
            c2 = p.collides_with_list(self.scene[LAYER_NAME_BULLET])
            if c:
                for o in c:
                    # self._bullet_list_for_portal.append((o, p.position))
                    o.kill()
            if c2:
                for o in c2:
                    # self._bullet_list_for_portal.append((o, p.position))
                    o.kill()



        mooving_platform.update_mooving_platform(self.scene[LAYER_NAME_MOOVING], self.physics_engine, delta_time)
        self.update_mooving_platform_on_item(delta_time)
        self.update_buttons(delta_time)
        self.update_gate(delta_time)
        if self.player_sprite.collides_with_list(self.scene[LAYER_NAME_DONT_TOUCH]):
            self.setup()
        inv = self.player_sprite.collides_with_list(self.scene[LAYER_NAME_INVERTORY])
        if inv:
            for i in inv:
                if not self.portal_stoun_flag and i.properties.get("name") == "PORTAL_STOUN":
                    self.set_permanent_item("PORTAL_STOUN")
                    self.settings["player"]["portal_stoun_flag"] = True
                    save_settings('saves/save.yaml', self.settings)
                    self.portal_stoun_flag = True
                else:
                    self.interface.append_item(i)
                i.kill()


        if self.tic >= 0:
            if int(time.perf_counter())-self.tic > 1:
                self.tic = -1
                self.save_ckick = False

        if self._xn is not None:
            # print('@@@@@@@@@@@@@@@@@@@@@@@')
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

    def set_permanent_item(self, item_name):
        self.portal_stoun = arcade.Sprite(PERMANENT_DIR / f'{item_name}.png')
        self.portal_stoun.scale = 0.8
        self.portal_stoun.set_position(64, self.height-128)
        # self.portal_stoun.scale = 0,8
        self.permanent_items.append(self.portal_stoun)

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
        self.gui_camera.use()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.width, self.height,
                                            self.background, alpha=46)
        self.camera.use()
        # print(self.width)

        self.scene.draw()
        # self.scene[LAYER_NAME_BOX].draw_hit_boxes(arcade.color.RED)
        self.bullet_enemys_list.draw()

        self.scene.update_animation(1/60)
        self.explosions_list.draw()
        self.gui_camera.use()

        self.permanent_items.draw()
        self.interface.draw()

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
            impulse = (0, PLAYER_JUMP_IMPULSE+self.jupm_impulse_k)
            self.physics_engine.apply_impulse(self.player_sprite, impulse)

    def update_buttons(self, delta_time):
        for btn in self.scene[LAYER_NAME_BUTTON]:
            if btn.collides_with_list(self.list_for_button) or btn.collides_with_sprite(self.player_sprite):
                btn.texture = self.check_btn_texture
                self.check_sprite(LAYER_NAME_MOOVING, btn.properties["link"], True)
                self.check_sprite(LAYER_NAME_GATE, btn.properties["link"], True)
            else:
                btn.texture = self.uncheck_btn_texture
                self.check_sprite(LAYER_NAME_MOOVING, btn.properties["link"], False)

    def _collision_player_button(self, delta_time):

                for btn in self.scene[LAYER_NAME_BUTTON]:
                    if btn.collides_with_sprite(self.player_sprite):
                        self.box_on_button = False

                        btn.texture = self.check_btn_texture
                        print(btn.properties["link"])
                        self.check_sprite(LAYER_NAME_MOOVING, btn.properties["link"], True)
                    else:
                        btn.texture = self.uncheck_btn_texture
                        self.check_sprite(LAYER_NAME_MOOVING, btn.properties["link"], False)

    def check_sprite(self, list_name, sprite_name, check):
        for pl in self.scene[list_name]:
            if pl.properties['name'] == sprite_name:
                if pl.properties['name'] == 'p2':
                    pass
                    # print(pl.properties['name'], "!!!!")
                nps = pl.properties.get('condition', None)
                if nps is not None:
                    self.add_item_to_nps(LAYER_NAME_NPS, nps, pl.properties['name'])
                pl.properties['active'] = check

    def add_item_to_nps(self, list_name, nps_name, item):
        for nps in self.scene[list_name]:
            if nps.obgect.name == nps_name:
                nps.invertory.append(item)

    def update_mooving_platform_on_item(self, delta_time):
        """
        работает когда стоиш на ней
        :param delta_time:
        """

        for moving_sprite in self.scene[LAYER_NAME_MOOVING_ON_ITEM]:

            coll = moving_sprite.collides_with_list(self.coll_list_for_on_item_platform)
            # coll = moving_sprite.collides_with_list(self.scene[LAYER_NAME_BOX])
            if coll:
                print(coll, 222222)
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




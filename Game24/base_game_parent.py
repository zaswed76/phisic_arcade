import arcade
from const import *
from sprites.player_sprite import PlayerSprite, PlayerError
from sprites.bullet_sprite import Bullet
from live import Live
import math
import const



class BaseReg(arcade.View):
    def __init__(self):
        super().__init__()

    def _init_phisics_items(self):
        self.physics_engine.add_sprite_list(self.scene[LAYER_NAME_PLATFORMS],
                                            friction=PLATFORMS_FRICTION,
                                            collision_type="wall",
                                            elasticity=0.1,
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)



        self.physics_engine.add_sprite_list(self.scene[LAYER_NAME_OBJECTPLATFORM],
                                            friction=PLATFORMS_FRICTION,
                                            collision_type="wall",
                                            elasticity=0.1,
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)

        self.physics_engine.add_sprite(self.player_sprite,
                                       damping=0.1,
                                       friction=PLAYER_FRICTION,
                                       mass=PLAYER_MASS,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="player",
                                       max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
                                       max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED)

        # self.physics_engine.add_sprite_list(self.scene[LAYER_NAME_DINAMIC],
        #                                     friction=PLATFORMS_FRICTION,
        #                                     elasticity=0.2,
        #                                     collision_type="wall",
        #                                     mass=4,
        #                                     body_type=arcade.PymunkPhysicsEngine.DYNAMIC)
        try:
            layer = self.scene[LAYER_NAME_DINAMIC]
        except KeyError as er:
            print(f"нет слоя {LAYER_NAME_DINAMIC} або нема жодного об'єкта на ньму")
            pass
        else:
            for obj in layer:
                _mass = obj.properties.get('mass', DYNAMIC_MASS)
                _friction = obj.properties.get('friction', DYNAMIC_ITEM_FRICTION)
                _elasticity = obj.properties.get('elasticity', DYNAMIC_ELASTICITY)
                _damping = obj.properties.get('damping', DYNAMIC_DAMPING)
                _gravity = 0, -obj.properties.get('gravity', GRAVITY)
                self.physics_engine.add_sprite(obj, mass=_mass,
                                               friction=_friction,
                                               elasticity=_elasticity,
                                               body_type=arcade.PymunkPhysicsEngine.DYNAMIC,
                                               damping=_damping,
                                               gravity=_gravity,
                                               )

        self.physics_engine.add_sprite_list(self.scene[LAYER_NAME_BUTTON],
                                            friction=PLATFORMS_FRICTION,
                                            collision_type="wall",
                                            body_type=arcade.PymunkPhysicsEngine.KINEMATIC)

        self.physics_engine.add_sprite_list(self.scene[LAYER_NAME_DINAMIC_KEY],
                                            friction=1,
                                            mass=6,
                                            collision_type="wall",
                                            body_type=arcade.PymunkPhysicsEngine.DYNAMIC)

        self.physics_engine.add_sprite_list(self.scene[LAYER_NAME_MOOVING],
                                            friction=1.0,
                                            collision_type="wall",
                                            body_type=arcade.PymunkPhysicsEngine.KINEMATIC)

        self.physics_engine.add_sprite_list(self.scene[LAYER_NAME_NPS],
                                            collision_type="nps",
                                            body_type=arcade.PymunkPhysicsEngine.KINEMATIC)

        self.physics_engine.add_sprite_list(self.scene[LAYER_NAME_GATE],
                                            friction=PLATFORMS_FRICTION,
                                            collision_type="wall",
                                            body_type=arcade.PymunkPhysicsEngine.KINEMATIC)

        self.physics_engine.add_sprite_list(self.scene[LAYER_NAME_MOOVING_ON_ITEM],
                                            friction=PLATFORMS_FRICTION,
                                            collision_type="wall",
                                            body_type=arcade.PymunkPhysicsEngine.KINEMATIC)
    def _init_player_sprite(self):
        # player_object = self.tile_map.get_obgect_by_name("player", "Mark")[0]
        # if player_object is None:
        #     raise PlayerError()
        live = Live()
        self.player_sprite = PlayerSprite(self.scene[LAYER_NAME_LADDERS],
                                          hit_box_algorithm="Detailed",
                                          physics_engine=self.physics_engine,
                                          live=live, type='player', game=self)
        self.player_sprite.properties = {}
        self.player_sprite.properties['name'] = "Player"
        self.player_sprite.name = "Player"


        cartesian = self.tile_map.get_cartesian(self.current_check_point[0], self.current_check_point[1])
        xn = math.floor(cartesian[0] * SPRITE_SCALING_TILES * self.tile_map.tile_width)
        yn = math.floor((cartesian[1] + 1) * (self.tile_map.tile_height * SPRITE_SCALING_TILES))
        self.player_sprite.center_x = xn
        self.player_sprite.center_y = yn
        # self.scene.add_sprite_list_after("Player", LAYER_NAME_BUTTON)
        # self.scene.add_sprite("Player", self.player_sprite)
        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)

class BaseGame(BaseReg):
    def __init__(self):
        super().__init__()
        self.left_pressed: bool = False
        self.right_pressed: bool = False
        self.up_pressed: bool = False
        self.down_pressed: bool = False
        self.text_int_coll_list = arcade.SpriteList()

    # def __getattr__(self, item):
    #     if item in self.__dict__:
    #         return item

    def on_key_press(self, key, modifiers):

        if modifiers & arcade.key.MOD_CAPSLOCK:
            self.player_sprite.set_fast(True)
            self.jupm_impulse_k = -2000
        else:

            self.player_sprite.set_fast(False)
            self.jupm_impulse_k = 0


        if self.game_pause:
            return
        if key == arcade.key.ESCAPE:
            arcade.exit()
        if key == arcade.key.F5:
            self.save_game()
            self.save_lavel()
        if key == arcade.key.KEY_1:
            self.player_sprite.set_person(PlayerSprite.SHOOTER)
            self.player_sprite.setup_person()

        if key == arcade.key.KEY_2:
            self.player_sprite.set_person(PlayerSprite.CREATOR)
            self.player_sprite.setup_person()

        if key == arcade.key.R:
            self.setup()

        # if key == arcade.key.F:
        #     self.check_sprite(LAYER_NAME_GATE, 'gate1', True)
        # if key == arcade.key.G:
        #     self.check_sprite(LAYER_NAME_GATE, 'gate1', False)

        if key == arcade.key.MINUS:
            self.player_sprite.pymunk.gravity = (0, 200)
        if key == arcade.key.EQUAL:
            print(5555)
            self.player_sprite.pymunk.gravity = (0, -1300)
        if modifiers == arcade.key.MOD_SHIFT and key == arcade.key.R:

            self.load_flag = "check_point"

            self.setup()


        if key == arcade.key.A:
            self.left_pressed = True

            # else:
            #     self.player_sprite.set_fast(False)



        elif key == arcade.key.D:
            self.right_pressed = True
            if modifiers & arcade.key.MOD_SHIFT:
                self.player_sprite.set_fast(True)
            # else:
            #     self.player_sprite.set_fast(False)

        elif key == arcade.key.SPACE or key == arcade.key.W:
            self.up_pressed = True
            # find out if player is standing on ground, and not on a ladder
            self.set_player_jump_impuls()
        elif key == arcade.key.S:
            self.down_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if modifiers & arcade.key.MOD_CAPSLOCK:
            self.player_sprite.set_fast(True)
        else:

            self.player_sprite.set_fast(False)
        if key == arcade.key.A:
            self.left_pressed = False

        elif key == arcade.key.D:
            self.right_pressed = False

        elif key == arcade.key.W or key == arcade.key.SPACE:
            self.up_pressed = False
        elif key == arcade.key.S:
            self.down_pressed = False



    def on_mouse_motion(self, x, y, dx, dy):

        for obj in self.text_interface2.nps_message_list:
            coll = obj.collides_with_point((x, y))
            if coll:
                self.text_interface2.hover(obj, 255)
            else:
                self.text_interface2.hover(obj, 90)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.player_sprite.current_person == PlayerSprite.SHOOTER:
            if self.game_pause:
                for obj in self.text_interface2.nps_message_list:
                    coll = obj.collides_with_point((x, y))
                    if coll:
                        try:
                            transition = obj.name

                            self.curreent_nps.set_message(transition)
                        except AttributeError as er:
                            print(er)
                            arcade.exit()

            else:

                if button == 1:
                    print(self.player_sprite.current_person)
                    if self.player_sprite.current_person == PlayerSprite.SHOOTER:

                        self.create_bullet(f"{BULLET_NAME}", x, y, scale=0.4, cfg_bullet=STANDART_BULLET)
                        self.player_sprite.texture = self.player_sprite.jump_texture_pair[0]

        elif self.player_sprite.current_person == PlayerSprite.CREATOR:

            if self.game_pause:
                for obj in self.text_interface2.nps_message_list:
                    coll = obj.collides_with_point((x, y))
                    if coll:
                        try:
                            transition = obj.name

                            self.curreent_nps.set_message(transition)
                        except AttributeError as er:
                            print(er)
                            arcade.exit()
            else:
                if button == 1:
                    self.create_bullet(f"{BOX_NAME}", x, y, scale=1,
                                           type=Bullet.BOX_TYPE,
                                           cfg_bullet=STANDART_BOX,
                                           force=BOX_MOVE_FORCE,
                                           alpha=255)
                elif button == 4 and self.portal_stoun_flag:
                    self.create_bullet(f"{BOX_NAME2}", x, y, scale=1,
                                           type=Bullet.BOX_TYPE,
                                           cfg_bullet=PORTAL_BOX,
                                           force=BOX_MOVE_FORCE,
                                           alpha=255)
                        # self.player_sprite.texture = self.player_sprite.jump_texture_pair[0]
        # else:
        #     for btn in self.text_interface.bg_list:
        #         if btn.collides_with_point((x, y)):
        #             if btn.name == "close":
        #                 self.set_pause(False)
        #             elif btn.name == "forward":
        #                 self.text_interface.forward_text()
        #             elif btn.name == "back":
        #                 self.text_interface.back_text()
        # if x < 300:
        #     self.check_sprite('Mooving platform',  'mooving1', True)
        # else:
        #     self.check_sprite('Mooving platform',  'mooving1', False)

    # def on_mouse_scroll (self, x, y, sx, sy):
    #     #     print(sx, sy)
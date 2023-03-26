import arcade
from const import *
from sprites.player_sprite import PlayerSprite, PlayerError
from live import Live
import math


class BaseReg(arcade.View):
    def __init__(self):
        super().__init__()

    def _init_phisics_items(self):
        self.physics_engine.add_sprite_list(self.scene[LAYER_NAME_PLATFORMS],
                                            friction=PLATFORMS_FRICTION,
                                            collision_type="wall",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)


        self.physics_engine.add_sprite(self.player_sprite,
                                       damping=0.1,
                                       friction=PLAYER_FRICTION,
                                       mass=PLAYER_MASS,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="player",
                                       max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
                                       max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED)

        self.physics_engine.add_sprite_list(self.scene[LAYER_NAME_DINAMIC],
                                            friction=PLATFORMS_FRICTION,
                                            collision_type="wall",
                                            body_type=arcade.PymunkPhysicsEngine.DYNAMIC)

        self.physics_engine.add_sprite_list(self.scene[LAYER_NAME_BUTTON],
                                            friction=PLATFORMS_FRICTION,
                                            collision_type="wall",
                                            body_type=arcade.PymunkPhysicsEngine.KINEMATIC)

        self.physics_engine.add_sprite_list(self.scene[LAYER_NAME_MOOVING],
                                            friction=PLATFORMS_FRICTION,
                                            collision_type="wall",
                                            body_type=arcade.PymunkPhysicsEngine.KINEMATIC)
        self.physics_engine.add_sprite_list(self.scene[LAYER_NAME_MOOVING_ON_ITEM],
                                            friction=PLATFORMS_FRICTION,
                                            collision_type="wall",
                                            body_type=arcade.PymunkPhysicsEngine.KINEMATIC)
    def _init_player_sprite(self):
        player_object = self.tile_map.get_obgect_by_name("player", "Mark")
        if player_object is None:
            raise PlayerError()
        live = Live()
        self.player_sprite = PlayerSprite(self.scene[LAYER_NAME_LADDERS],
                                          hit_box_algorithm="Detailed",
                                          physics_engine=self.physics_engine, live=live, type='player', game=self)
        cartesian = self.tile_map.get_cartesian(player_object.shape[0], player_object.shape[1])
        xn = math.floor(cartesian[0] * SPRITE_SCALING_TILES * self.tile_map.tile_width)
        yn = math.floor((cartesian[1] + 1) * (self.tile_map.tile_height * SPRITE_SCALING_TILES))
        self.player_sprite.center_x = xn
        self.player_sprite.center_y = yn
        self.scene.add_sprite_list_after("Player", LAYER_NAME_PLATFORMS)
        self.scene.add_sprite("Player", self.player_sprite)

class BaseGame(BaseReg):
    def __init__(self):
        super().__init__()
        self.left_pressed: bool = False
        self.right_pressed: bool = False
        self.up_pressed: bool = False
        self.down_pressed: bool = False

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.ESCAPE:
            arcade.exit()
        if modifiers == arcade.key.MOD_SHIFT and key == arcade.key.R:
            self.level = 3
            self.setup()
        if key == arcade.key.R:
            self.setup()

        if key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.SPACE or key == arcade.key.W:
            self.up_pressed = True
            # find out if player is standing on ground, and not on a ladder
            self.set_player_jump_impuls()
        elif key == arcade.key.S:
            self.down_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.D:
            self.right_pressed = False
        elif key == arcade.key.W or key == arcade.key.SPACE:
            self.up_pressed = False
        elif key == arcade.key.S:
            self.down_pressed = False

    def on_mouse_press(self, x, y, button, modifiers):
        print(button)
        # if x < 300:
        #     self.check_sprite('Mooving platform',  'mooving1', True)
        # else:
        #     self.check_sprite('Mooving platform',  'mooving1', False)

    def on_mouse_scroll (self, x, y, sx, sy):
        print(sx, sy)
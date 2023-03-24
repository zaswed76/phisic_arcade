
import os
import math
import arcade
from controller import Controller
from gui.start_menu import MenuView
from sprites.player_sprite import PlayerSprite, PlayerError
from live import Live
from constants import *

file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)

LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_PLAYER = "Player"
LAYER_NAME_LADDERS = "Ladders"

LAYER_OPTIONS = {
    LAYER_NAME_PLATFORMS: {"use_spatial_hash": True},
}



class TileMap(arcade.TileMap):
    def __init__(self, *args):
        super().__init__(*args)

    def get_obgect_by_name(self, name, layer_name):
        for obj in self.object_lists.get(layer_name, list()):
            if obj.name == name:
                return obj



class GameView(Controller):
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
        self.tile_map = TileMap(map_name, ConstGame.SPRITE_SCALING_TILES, LAYER_OPTIONS)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.scene.add_sprite_list(LAYER_NAME_PLAYER)
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=ConstGame.DEFAULT_DAMPING,
                                                         gravity=(0, -ConstGame.GRAVITY))



        self._init_player_sprite()
        self._init_phisics_items()


    def on_show(self):
        color = self.tile_map.background_color
        if color:
            arcade.set_background_color(self.tile_map.background_color)

    def on_draw(self):
        arcade.start_render()
        self.scene.draw()


    def on_update(self, delta_time):
        is_on_ground = self.physics_engine.is_on_ground(self.player_sprite)
        # Update player forces based on keys pressed
        # if not is_on_ground and not self.player_sprite.is_on_ladder:
        #     self.aaa.append(self.player_sprite.position)
        # elif self.aaa:
        #     k = self.aaa[0][1]-self.player_sprite.center_y
        #
        #     if k > 420.0:
        #         self.player_sprite.live.current -= k/14
        #     self.aaa.clear()




        #
        # if self.left_pressed and not self.right_pressed:
        #     # Create a force to the left. Apply it.
        #     if is_on_ground or self.player_sprite.is_on_ladder:
        #         force = (-PLAYER_MOVE_FORCE_ON_GROUND, 0)
        #
        #     else:
        #
        #         force = (-PLAYER_MOVE_FORCE_IN_AIR, 0)
        #     self.physics_engine.apply_force(self.player_sprite, force)
        #     # Set friction to zero for the player while moving
        #     self.physics_engine.set_friction(self.player_sprite, 0)
        # elif self.right_pressed and not self.left_pressed:
        #     # Create a force to the right. Apply it.
        #     if is_on_ground or self.player_sprite.is_on_ladder:
        #         force = (PLAYER_MOVE_FORCE_ON_GROUND, 0)
        #     else:
        #         force = (PLAYER_MOVE_FORCE_IN_AIR, 0)
        #     self.physics_engine.apply_force(self.player_sprite, force)
        #     # Set friction to zero for the player while moving
        #     self.physics_engine.set_friction(self.player_sprite, 0)
        # elif self.up_pressed and not self.down_pressed:
        #     # Create a force to the right. Apply it.
        #     if self.player_sprite.is_on_ladder:
        #         force = (0, PLAYER_MOVE_FORCE_ON_GROUND)
        #         self.physics_engine.apply_force(self.player_sprite, force)
        #         # Set friction to zero for the player while moving
        #         self.physics_engine.set_friction(self.player_sprite, 0)
        # elif self.down_pressed and not self.up_pressed:
        #     # Create a force to the right. Apply it.
        #     if self.player_sprite.is_on_ladder:
        #         force = (0, -PLAYER_MOVE_FORCE_ON_GROUND)
        #         self.physics_engine.apply_force(self.player_sprite, force)
        #         # Set friction to zero for the player while moving
        #         self.physics_engine.set_friction(self.player_sprite, 0)
        # else:
        #     # Player's feet are not moving. Therefore up the friction so we stop.
        #     self.physics_engine.set_friction(self.player_sprite, 1.0)
        #
        # # Move items in the physics engine
        self.physics_engine.step()

    def set_next_view(self, next_view):
        self.next_view = next_view

    def _init_phisics_items(self):
        self.physics_engine.add_sprite_list(self.scene[LAYER_NAME_PLATFORMS],
                                            friction=ConstGame.PLATFORMS_FRICTION,
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

    def _init_player_sprite(self):
        player_object = self.tile_map.get_obgect_by_name("player", "Mark")
        if player_object is None:
            raise PlayerError()
        live = Live()
        self.player_sprite = PlayerSprite(self.scene[LAYER_NAME_LADDERS], hit_box_algorithm="Detailed", live=live, type='player')
        cartesian = self.tile_map.get_cartesian(player_object.shape[0], player_object.shape[1])
        xn = math.floor(cartesian[0] * ConstGame.TILE_SCALING * self.tile_map.tile_width)
        yn = math.floor((cartesian[1] + 1) * (self.tile_map.tile_height * ConstGame.TILE_SCALING))
        self.player_sprite.center_x = xn
        self.player_sprite.center_y = yn
        self.scene.add_sprite_list_after("Player", LAYER_NAME_PLATFORMS)
        self.scene.add_sprite("Player", self.player_sprite)
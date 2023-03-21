"""
Example of Pymunk Physics Engine Platformer
"""
import math
from typing import Optional
import arcade
from constants import *
from player_sprite import PlayerSprite

from interface import CellSprite, Interface
from enemy import RobotEnemy, ZombieEnemy
from live import Live
from controller import Controller

LAYER_NAME_PLATFORMS ="Platforms"
LAYER_NAME_DYNAMIC = "Dynamic Items"
LAYER_NAME_LADDERS = "Ladders"
LAYER_NAME_MOVING_PLATFORMS = "Moving Platforms"
LAYER_NAME_COINS = "Coins"
LAYER_NAME_BOTTLE = "bottle"
LAYER_NAME_BACKGROUND = "Background"
LAYER_NAME_PLAYER = "Player"
LAYER_NAME_ENEMIES = "Enemies"







class GameWindow(Controller):
    """ Main Window """

    def __init__(self, width, height, title):
        """ Create the variables """

        # Init the parent class
        super().__init__(width, height, title)
        self.set_fullscreen()
        self.level = 1 # с какого начинаем
        self.max_level = 2 # сколько уровней

        self.player_sprite: Optional[PlayerSprite] = None
        self.player_list: Optional[arcade.SpriteList] = None
        self.wall_list: Optional[arcade.SpriteList] = None
        self.box_list: Optional[arcade.SpriteList] = None
        self.bullet_list: Optional[arcade.SpriteList] = None
        self.item_list: Optional[arcade.SpriteList] = None
        self.moving_sprites_list: Optional[arcade.SpriteList] = None
        self.ladder_list: Optional[arcade.SpriteList] = None
        self.enemy_: Optional[arcade.SpriteList] = None



        self.physics_engine: Optional[arcade.PymunkPhysicsEngine] = None


        self.camera = None
        self.gui_camera = None
        self.count_box = 0
        self.on_bullet = False





    def setup(self):

        layer_options = {
            LAYER_NAME_PLATFORMS: {"Platforms": True},
            LAYER_NAME_DYNAMIC: {"Dynamic Items": False},
            LAYER_NAME_LADDERS: {"Ladders": True},
            LAYER_NAME_BOTTLE: {"bottle": True},
            LAYER_NAME_MOVING_PLATFORMS: {"Moving Platforms": False}
        }

        self.player_list = arcade.SpriteList()
        self.box_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()


        map_name = f"resources/my_maps/pymunk_test_map_{self.level}.json"
        self.tile_map = arcade.load_tilemap(map_name, SPRITE_SCALING_TILES,
                                            layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        arcade.set_background_color(self.tile_map.background_color)
        self.end_of_map = END_OF_MAP[0]*SPRITE_SIZE, (self.tile_map.height - END_OF_MAP[1] - 1)*SPRITE_SIZE


        # Pull the sprite layers out of the tile map
        self.wall_list = self.tile_map.sprite_lists["Platforms"]
        self.item_list = self.tile_map.sprite_lists["Dynamic Items"]
        self.ladder_list = self.tile_map.sprite_lists["Ladders"]
        self.bottle_list = self.tile_map.sprite_lists["bottle"]
        self.moving_sprites_list = self.tile_map.sprite_lists['Moving Platforms']
        self.foreground = self.tile_map.sprite_lists['foreground']
        self.background= self.tile_map.sprite_lists['background']
        self.invertory_list = self.tile_map.sprite_lists['invertory']
        self.invertory_list.rescale(0.5)

        self.interface = Interface('resources/icons/Untitled.png')
        self.interface.append_cell()
        self.interface.append_cell()
        self.interface.append_cell()
        self.interface.append_cell()
        self.interface.append_cell()
        # self.interface.append_item('resources/icons/boxCrate_double.png')


        cam_w = self.tile_map.width*SPRITE_IMAGE_SIZE*SPRITE_SCALING_TILES
        cam_h = self.tile_map.height*SPRITE_IMAGE_SIZE*SPRITE_SCALING_TILES
        self.view_left = 0
        self.view_bottom = 0
        self.camera = arcade.Camera(cam_w/2, cam_h/2)
        self.gui_camera = arcade.Camera(cam_w/2, cam_h/2)


        self._init_player_sprite()
        self.enemies_layer = self.tile_map.object_lists[LAYER_NAME_ENEMIES]
        for my_object in self.enemies_layer:
            cartesian = self.tile_map.get_cartesian(
                my_object.shape[0], my_object.shape[1]
            )
            enemy_type = my_object.properties["type"]
            if enemy_type == "robot":
                enemy = RobotEnemy(self.ladder_list, my_object.properties)
            elif enemy_type == "zombie":
                enemy = ZombieEnemy(self.ladder_list, my_object.properties)
            enemy.center_x = math.floor(
                cartesian[0] * SPRITE_SCALING_TILES * self.tile_map.tile_width
            )
            enemy.center_y = math.floor(
                (cartesian[1] + 1) * (self.tile_map.tile_height * SPRITE_SCALING_TILES)
            )
            if "boundary_left" in my_object.properties:
                enemy.boundary_left = my_object.properties["boundary_left"] * SPRITE_SCALING_TILES
                # print(enemy.boundary_left,  "enemy.boundary_left")
            if "boundary_right" in my_object.properties:
                enemy.boundary_right = int(my_object.properties["boundary_right"]) * SPRITE_SCALING_TILES
                # print(enemy.boundary_right, "enemy.boundary_right")
            if "change_x" in my_object.properties:
                enemy.change_x = my_object.properties["change_x"]
            self.scene.add_sprite(LAYER_NAME_ENEMIES, enemy)

        self.pan_camera_to_user()

        # --- Pymunk Physics Engine Setup ---

        # The default damping for every object controls the percent of velocity
        # the object will keep each second. A value of 1.0 is no speed loss,
        # 0.9 is 10% per second, 0.1 is 90% per second.
        # For top-down games, this is basically the friction for moving objects.
        # For platformers with gravity, this should probably be set to 1.0.
        # Default value is 1.0 if not specified.
        damping = DEFAULT_DAMPING

        # Set the gravity. (0, 0) is good for outer space and top-down.
        gravity = (0, -GRAVITY)

        # Create the physics engine
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=damping,
                                                         gravity=gravity)


        def wall_hit_handler(bullet_sprite, _wall_sprite, _arbiter, _space, _data):
            """ Called for bullet/wall collision """
            bullet_sprite.remove_from_sprite_lists()

        self.physics_engine.add_collision_handler("bullet", "wall", post_handler=wall_hit_handler)

        def item_hit_handler(bullet_sprite, item_sprite, _arbiter, _space, _data):
            """ Called for bullet/wall collision """
            bullet_sprite.remove_from_sprite_lists()
            item_sprite.remove_from_sprite_lists()

        self.physics_engine.add_collision_handler("bullet", "item", post_handler=item_hit_handler)

        def enemy_hit_handler(bullet_sprite, enemy_sprite, _arbiter, _space, _data):
            """ Called for bullet/wall collision """
            bullet_sprite.remove_from_sprite_lists()
            enemy_sprite.remove_from_sprite_lists()

        self.physics_engine.add_collision_handler("bullet", "enemy", post_handler=enemy_hit_handler)



        def player_hit_handler(player_sprite, enemy_sprite, _arbiter, _space, _data):
            self.player_sprite.live.minus(enemy_sprite.properties["damage"])
        self.physics_engine.add_collision_handler("player", "enemy", post_handler=player_hit_handler)

        def player2_hit_handler(invertory, player_sprite,  _arbiter, _space, _data):
            self.interface.append_item(invertory.texture)
            self.count_box += invertory.properties["count"]
            invertory.remove_from_sprite_lists()
            print(invertory.properties)

        self.physics_engine.add_collision_handler("invertory", "player",  post_handler=player2_hit_handler)

        self.physics_engine.add_sprite(self.player_sprite,
                                       damping=0.1,
                                       friction=PLAYER_FRICTION,
                                       mass=PLAYER_MASS,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="player",
                                       max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
                                       max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED)

        # Create the walls.
        # By setting the body type to PymunkPhysicsEngine.STATIC the walls can't
        # move.
        # Movable objects that respond to forces are PymunkPhysicsEngine.DYNAMIC
        # PymunkPhysicsEngine.KINEMATIC objects will move, but are assumed to be
        # repositioned by code and don't respond to physics forces.
        # Dynamic is default.
        self.physics_engine.add_sprite_list(self.wall_list,
                                            friction=WALL_FRICTION,
                                            collision_type="wall",

                                            body_type=arcade.PymunkPhysicsEngine.STATIC)

        self.physics_engine.add_sprite_list(self.invertory_list,
                                            friction=WALL_FRICTION,
                                            collision_type="invertory",
                                            body_type=arcade.PymunkPhysicsEngine.DYNAMIC)




        # Create the items
        self.physics_engine.add_sprite_list(self.item_list,
                                            friction=DYNAMIC_ITEM_FRICTION,

                                            collision_type="item")

        # Add kinematic sprites
        self.physics_engine.add_sprite_list(self.moving_sprites_list,
                                            body_type=arcade.PymunkPhysicsEngine.KINEMATIC,

                                            collision_type="wall")
        for sp in self.scene[LAYER_NAME_ENEMIES].sprite_list:
            self.physics_engine.add_sprite(sp,
                                            collision_type="enemy",
                                            body_type=arcade.PymunkPhysicsEngine.DYNAMIC,
                                            friction=0.1,
                                            mass=1,
                                            damping=0.1,
                                            elasticity=0.5,
                                            moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                           #
                                           max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
                                           max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED)

        self.level_restsrt_options = [lambda: not self.player_list.sprite_list,
                                      lambda: self.player_sprite.center_y < -512,
                                      lambda: self.player_sprite.live.current <= 0]


    def _init_player_sprite(self):
        live = Live()
        self.player_sprite = PlayerSprite(self.ladder_list, hit_box_algorithm="Detailed", live=live)


        self.player_sprite.center_x = SPRITE_SIZE * PLAYER_START_GRID[0] + SPRITE_SIZE / 2
        self.player_sprite.center_y = SPRITE_SIZE * PLAYER_START_GRID[1] + SPRITE_SIZE / 2
        self.player_list.append(self.player_sprite)


    def on_update(self, delta_time):
        """ Movement and game logic """

        if any([x() for x in self.level_restsrt_options]):
            self.setup()

        is_on_ground = self.physics_engine.is_on_ground(self.player_sprite)
        # Update player forces based on keys pressed
        if self.left_pressed and not self.right_pressed:
            # Create a force to the left. Apply it.
            if is_on_ground or self.player_sprite.is_on_ladder:
                force = (-PLAYER_MOVE_FORCE_ON_GROUND, 0)
            else:
                force = (-PLAYER_MOVE_FORCE_IN_AIR, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            # Set friction to zero for the player while moving
            self.physics_engine.set_friction(self.player_sprite, 0)
        elif self.right_pressed and not self.left_pressed:
            # Create a force to the right. Apply it.
            if is_on_ground or self.player_sprite.is_on_ladder:
                force = (PLAYER_MOVE_FORCE_ON_GROUND, 0)
            else:
                force = (PLAYER_MOVE_FORCE_IN_AIR, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            # Set friction to zero for the player while moving
            self.physics_engine.set_friction(self.player_sprite, 0)
        elif self.up_pressed and not self.down_pressed:
            # Create a force to the right. Apply it.
            if self.player_sprite.is_on_ladder:
                force = (0, PLAYER_MOVE_FORCE_ON_GROUND)
                self.physics_engine.apply_force(self.player_sprite, force)
                # Set friction to zero for the player while moving
                self.physics_engine.set_friction(self.player_sprite, 0)
        elif self.down_pressed and not self.up_pressed:
            # Create a force to the right. Apply it.
            if self.player_sprite.is_on_ladder:
                force = (0, -PLAYER_MOVE_FORCE_ON_GROUND)
                self.physics_engine.apply_force(self.player_sprite, force)
                # Set friction to zero for the player while moving
                self.physics_engine.set_friction(self.player_sprite, 0)

        else:
            # Player's feet are not moving. Therefore up the friction so we stop.
            self.physics_engine.set_friction(self.player_sprite, 1.0)

        # Move items in the physics engine
        self.physics_engine.step()

        # For each moving sprite, see if we've reached a boundary and need to
        # reverse course.
        for moving_sprite in self.moving_sprites_list:
            if moving_sprite.boundary_right and \
                    moving_sprite.change_x > 0 and \
                    moving_sprite.right > moving_sprite.boundary_right:
                moving_sprite.change_x *= -1
            elif moving_sprite.boundary_left and \
                    moving_sprite.change_x < 0 and \
                    moving_sprite.left > moving_sprite.boundary_left:
                moving_sprite.change_x *= -1
            if moving_sprite.boundary_top and \
                    moving_sprite.change_y > 0 and \
                    moving_sprite.top > moving_sprite.boundary_top:
                moving_sprite.change_y *= -1
            elif moving_sprite.boundary_bottom and \
                    moving_sprite.change_y < 0 and \
                    moving_sprite.bottom < moving_sprite.boundary_bottom:
                moving_sprite.change_y *= -1

            # Figure out and set our moving platform velocity.
            # Pymunk uses velocity is in pixels per second. If we instead have
            # pixels per frame, we need to convert.
            velocity = (moving_sprite.change_x * 1 / delta_time, moving_sprite.change_y * 1 / delta_time)
            self.physics_engine.set_velocity(moving_sprite, velocity)
            self.pan_camera_to_user(panning_fraction=0.12)
            self.setup_next_level()
        # Update moving platforms and enemies
        self.scene.update_animation(delta_time,[LAYER_NAME_ENEMIES])
        self.scene.update([LAYER_NAME_ENEMIES])

        # See if the enemy hit a boundary and needs to reverse direction.
        for enemy in self.scene[LAYER_NAME_ENEMIES]:
            self.enspeed = enemy.center_y
            is_on_ground = self.physics_engine.is_on_ground(enemy)
            if not is_on_ground:
                # enemy.change_x = 0
                enemy.change_y = -0.4
                if enemy.center_y < 226:
                    enemy.change_x = 0
                    enemy.change_y = -4
                if enemy.center_y < -64:
                    enemy.remove_from_sprite_lists()
                    return



            if (
                enemy.boundary_right
                and enemy.right > enemy.boundary_right
                and enemy.change_x > 0
            ):
                enemy.change_x *= -1

            if (
                enemy.boundary_left
                and enemy.left < enemy.boundary_left
                and enemy.change_x < 0
            ):
                enemy.change_x *= -1
            velocity = (enemy.change_x * 1 / delta_time, enemy.change_y * 1 / delta_time)
            self.physics_engine.set_velocity(enemy, velocity)

        btl_list = arcade.check_for_collision_with_list(self.player_sprite, self.bottle_list)
        for botl in btl_list:
            # print('!!!!!!!!!AAAAAAAAAAAAAAAAAAAAAAAAA')
            botl.remove_from_sprite_lists()
            self.player_sprite.live.add(botl.properties['live'])

        self.interface.update()



    def setup_next_level(self):
        if self.player_sprite.left >= self.end_of_map[0] and self.player_sprite.center_y >= self.end_of_map[1]:
            self.level += 1
            if self.level <= self.max_level:
                self.setup()

    def on_draw(self):
        """ Draw everything """

        self.clear()
        # arcade.draw_lrwh_rectangle_textured(0, 0,
        #                                     3400, 2048,
        #                                     self.background)
        self.camera.use()
        self.scene[LAYER_NAME_ENEMIES].draw()
        self.background.draw()
        self.wall_list.draw()
        self.ladder_list.draw()
        self.moving_sprites_list.draw()
        self.bottle_list.draw()
        self.invertory_list.draw()
        self.box_list.draw()
        self.bullet_list.draw()
        self.item_list.draw()
        self.player_list.draw()
        self.foreground.draw()
        self.gui_camera.use()


        arcade.draw_lrtb_rectangle_filled(
            0, 1368, 54, 0, (0, 66, 66)
        )

        self.player_sprite.live.update()
        arcade.draw_lrtb_rectangle_filled(
            264, 414, 25, 15, arcade.csscolor.WHITE
        )

        arcade.draw_lrtb_rectangle_filled(
            264, 325, 25, 15, arcade.csscolor.DODGER_BLUE
        )

        score_text = f"{len(self.box_list.sprite_list)}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )

        self.interface.draw()



    def pan_camera_to_user(self, panning_fraction: float = 0.5):
        """
        Manage Scrolling

        :param panning_fraction: Number from 0 to 1. Higher the number, faster we
                                 pan the camera to the user.
        """

        # This spot would center on the user
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )

        if screen_center_x > 0:
            self.view_left = screen_center_x
        if screen_center_y > 0:
            self.view_bottom = screen_center_y


        if screen_center_x < 0:

            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        user_centered = screen_center_x, screen_center_y


        self.camera.move_to(user_centered, panning_fraction)

    def on_resize(self, width, height):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        self.camera.resize(width, height)


def main():
    """ Main function """
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()

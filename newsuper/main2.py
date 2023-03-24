"""
Example of Pymunk Physics Engine Platformer
"""
import math
import pprint
from typing import Optional
import arcade
from constants import *
from player_sprite import PlayerSprite
from bullet_sprite import BulletSprite, BoxSprite, Bullet
from interface import CellSprite, Interface
from enemy import RobotEnemy, ZombieEnemy
from live import Live
from bottle import BottleSprite
from controller import Controller

LAYER_NAME_PLATFORMS ="Platforms"
LAYER_NAME_BGPLATFORMS ="BgPlatforms"
LAYER_NAME_DYNAMIC = "Dynamic Items"
LAYER_NAME_LADDERS = "Ladders"
LAYER_NAME_MOVING_PLATFORMS = "Moving Platforms"
LAYER_NAME_BOTTLE = "bottle"
LAYER_NAME_DINAMIC_BOTTLE = "dinamic_bottle"
LAYER_NAME_BACKGROUND = "background"
LAYER_NAME_PLAYER = "Player"
LAYER_NAME_ENEMIES = "Enemies"
LAYER_NAME_INVERTORY = "invertory"
LAYER_NAME_FOREGROUND = "foreground"

class GameWindow(Controller):
    def __init__(self, width, height, title):
        """ Create the variables """

        # Init the parent class
        super().__init__(width, height, title)
        self.aaa = []
        self.current_AAAAAAA = 0
        self.set_fullscreen()
        self.set_vsync(True)
        self.level = 3 # с какого начинаем
        self.max_level = 2 # сколько уровней
        self.background_image = None

        self.player_sprite: Optional[PlayerSprite] = None
        self.player_list: Optional[arcade.SpriteList] = None
        self.wall_list: Optional[arcade.SpriteList] = None
        self.box_list: Optional[arcade.SpriteList] = None
        self.bullet_list: Optional[arcade.SpriteList] = None
        self.dinamic_list: Optional[arcade.SpriteList] = None
        self.moving_list: Optional[arcade.SpriteList] = None
        self.ladder_list: Optional[arcade.SpriteList] = None
        self.enemy_: Optional[arcade.SpriteList] = None
        self.physics_engine: Optional[arcade.PymunkPhysicsEngine] = None
        self.camera = None
        self.gui_camera = None
        self.count_box = 1
        self.on_bullet = True

    def setup(self):
        layer_options = {
            LAYER_NAME_PLATFORMS: {"use_spatial_hash": True},
            LAYER_NAME_BGPLATFORMS: {"use_spatial_hash": True},
            LAYER_NAME_DYNAMIC: {"use_spatial_hash": True},
            LAYER_NAME_LADDERS: {"use_spatial_hash": True},
            LAYER_NAME_BOTTLE: {"use_spatial_hash": True},
            LAYER_NAME_MOVING_PLATFORMS: {"use_spatial_hash": False},
            LAYER_NAME_INVERTORY: {"use_spatial_hash": True}
        }

        self.player_list = arcade.SpriteList()
        self.player_list.collision_type = 'player'

        self.box_list = arcade.SpriteList()
        self.box_list.collision_type = 'wall'
        self.bullet_list = arcade.SpriteList()
        self.bullet_list_enemy = arcade.SpriteList()
        self.enemies_list = arcade.SpriteList()
        self.dinamic_bottle_list = arcade.SpriteList()


        map_name = f"resources/my_maps/pymunk_test_map_{self.level}.json"
        self.tile_map = arcade.load_tilemap(map_name, SPRITE_SCALING_TILES,
                                            layer_options)

        # print(self.tile_map.tiled_map.layers)
        # arcade.set_background_color(self.tile_map.background_color)
        self.background_image = arcade.load_texture("myresource/images/Untitled.png")
        self.fbackground_image = arcade.load_texture("myresource/images/fgUntitled.png")

        self.end_of_map = END_OF_MAP[0]*SPRITE_SIZE, (self.tile_map.height - END_OF_MAP[1] - 1)*SPRITE_SIZE


        # Pull the sprite layers out of the tile map
        self.wall_list = self.tile_map.sprite_lists[LAYER_NAME_PLATFORMS]
        self.wall_list.collision_type = 'wall'





        self.wall_bg_list = self.tile_map.sprite_lists[LAYER_NAME_BGPLATFORMS]
        self.dinamic_list = self.tile_map.sprite_lists[LAYER_NAME_DYNAMIC]
        self.ladder_list = self.tile_map.sprite_lists[LAYER_NAME_LADDERS]
        self.bottle_list = self.tile_map.sprite_lists[LAYER_NAME_BOTTLE]
        self.moving_list = self.tile_map.sprite_lists.get(
            LAYER_NAME_MOVING_PLATFORMS, arcade.SpriteList())
        self.foreground = self.tile_map.sprite_lists[LAYER_NAME_FOREGROUND]
        self.background= self.tile_map.sprite_lists[LAYER_NAME_BACKGROUND]
        self.invertory_list = self.tile_map.sprite_lists[LAYER_NAME_INVERTORY]
        self.invertory_layer = self.tile_map.object_lists

        self.invertory_list.rescale(1)

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


        damping = DEFAULT_DAMPING
        gravity = (0, -GRAVITY)
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=damping,
                                                         gravity=gravity)

        self._init_player_sprite()
        self._init_enemies()
        self.pan_camera_to_user()

        def wall_hit_handler(bullet_sprite, _wall_sprite, _arbiter, _space, _data):
            """ Called for bullet/wall collision """
            bullet_sprite.remove_from_sprite_lists()
        self.physics_engine.add_collision_handler("bullet", "wall", post_handler=wall_hit_handler)
        def item_hit_handler(bullet_sprite, item_sprite, _arbiter, _space, _data):
            """ Called for bullet/wall collision """
            print("bullet_sprite, item_sprite")
            bullet_sprite.remove_from_sprite_lists()
            item_sprite.remove_from_sprite_lists()
        self.physics_engine.add_collision_handler("bullet", "box", post_handler=item_hit_handler)

        def enemy_hit_handler(bullet_sprite, enemy_sprite, _arbiter, _space, _data):
            """ Called for bullet/wall collision """

            enemy_sprite.turn_right()
        self.physics_engine.add_collision_handler("bullet", "enemy", post_handler=enemy_hit_handler)




        def bottle_hit_handler(box, bottle, _arbiter, _space, _data):
            """ Called for bullet/wall collision """

            texture = bottle.texture
            pos = bottle.center_x, bottle.center_y
            prop = bottle.properties

            bottle.remove_from_sprite_lists()
            bt = BottleSprite(texture, 1, 0)
            bt.set_position(*pos)
            bt.properties = prop
            self.physics_engine.add_sprite(bt, body_type=arcade.PymunkPhysicsEngine.DYNAMIC)
            self.dinamic_bottle_list.append(bt)

        self.physics_engine.add_collision_handler("box", "bottle", post_handler=bottle_hit_handler)

        def bottle__player_hit_handler(player, bottle, _arbiter, _space, _data):
            """ Called for bullet/wall collision """

            bottle.remove_from_sprite_lists()
        self.physics_engine.add_collision_handler("player", "bottle", post_handler=bottle__player_hit_handler)




        def player_hit_handler(player_sprite, enemy_sprite, _arbiter, _space, _data):
            self.player_sprite.live.minus(enemy_sprite.properties.get("damage", 0))
        self.physics_engine.add_collision_handler("player", "enemy", post_handler=player_hit_handler)

        def player2_hit_handler(invertory, player_sprite,  _arbiter, _space, _data):
            self.interface.append_item(invertory.texture)
            self.count_box += invertory.properties["count"]
            invertory.remove_from_sprite_lists()
        self.physics_engine.add_collision_handler("invertory", "player",  post_handler=player2_hit_handler)

        self.physics_engine.add_sprite(self.player_sprite,
                                       damping=0.1,
                                       friction=PLAYER_FRICTION,
                                       mass=PLAYER_MASS,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="player",
                                       max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
                                       max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED)


        self.physics_engine.add_sprite_list(self.wall_list,
                                            friction=WALL_FRICTION,
                                            collision_type="wall",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)



        self.physics_engine.add_sprite_list(self.bottle_list,
                                            friction=WALL_FRICTION,
                                            collision_type="bottle",
                                            body_type=arcade.PymunkPhysicsEngine.KINEMATIC)


        self.physics_engine.add_sprite_list(self.dinamic_bottle_list,
                                            friction=WALL_FRICTION,
                                            collision_type="bottle",
                                            body_type=arcade.PymunkPhysicsEngine.DYNAMIC)

        self.physics_engine.add_sprite_list(self.wall_bg_list,
                                            friction=WALL_FRICTION,
                                            collision_type="wall",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)

        self.physics_engine.add_sprite_list(self.invertory_list,
                                            friction=WALL_FRICTION,
                                            collision_type="invertory",
                                            body_type=arcade.PymunkPhysicsEngine.DYNAMIC)




        # Create the items
        self.physics_engine.add_sprite_list(self.dinamic_list,
                                            friction=DYNAMIC_ITEM_FRICTION,
                                            body_type=arcade.PymunkPhysicsEngine.DYNAMIC,
                                            collision_type="item")

        # Add kinematic sprites
        self.physics_engine.add_sprite_list(self.moving_list,
                                            body_type=arcade.PymunkPhysicsEngine.KINEMATIC,

                                            collision_type="wall")
        for sp in self.enemies_list.sprite_list:
            self.physics_engine.add_sprite(sp,
                                            collision_type="enemy",
                                            body_type=arcade.PymunkPhysicsEngine.DYNAMIC,
                                            friction=0.1,
                                            mass=0.5,
                                            damping=0.1,
                                            elasticity=0.5,
                                            moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                           #
                                           max_horizontal_velocity=100,
                                           max_vertical_velocity=100)

        self.level_restsrt_options = [lambda: not self.player_list.sprite_list,
                                      lambda: self.player_sprite.center_y < -512,
                                      lambda: self.player_sprite.live.current <= 0]

    def create_bullet(self,x, y):
               if self.on_bullet:
                    self.collision_lists = [self.player_list,
                                self.wall_list,
                                self.box_list
                                ]
                    bullet = Bullet(":resources:images/space_shooter/laserBlue01.png", collisions_lists=self.collision_lists, damage=50)
                    self.bullet_list.append(bullet)

                    start_x = self.player_sprite.center_x
                    start_y = self.player_sprite.center_y
                    bullet.position = self.player_sprite.position

                    # Get from the mouse the destination location for the bullet
                    # IMPORTANT! If you have a scrolling screen, you will also need
                    # to add in self.view_bottom and self.view_left.
                    dest_x = x + self.view_left
                    dest_y = y + self.view_bottom
                    # self.view_bottom = self.view_bottom
                    # self.view_left = self.view_left

                    # Do math to calculate how to get the bullet to the destination.
                    # Calculation the angle in radians between the start points
                    # and end points. This is the angle the bullet will travel.
                    x_diff = dest_x - start_x
                    y_diff = dest_y - start_y
                    angle = math.atan2(y_diff, x_diff)

                    # What is the 1/2 size of this sprite, so we can figure out how far
                    # away to spawn the bullet
                    size = max(self.player_sprite.width, self.player_sprite.height) / 2

                    # Use angle to to spawn bullet away from player in proper direction
                    bullet.center_x += size * math.cos(angle)
                    bullet.center_y += size * math.sin(angle)

                    # Set angle of bullet
                    bullet.angle = math.degrees(angle)

                    # Gravity to use for the bullet
                    # If we don't use custom gravity, bullet drops too fast, or we have
                    # to make it go too fast.
                    # Force is in relation to bullet's angle.

                    bullet_gravity = (0, -100)

                    # Add the sprite. This needs to be done AFTER setting the fields above.
                    self.physics_engine.add_sprite(bullet,
                                                   mass=2,
                                                   damping=1,
                                                   friction=0.9,
                                                   collision_type="bullet",
                                                   gravity=bullet_gravity,
                                                   elasticity=0.5)
                    # Add force to bullet
                    force = (BULLET_MOVE_FORCE, 1)
                    self.physics_engine.apply_force(bullet, force)

    def create_box(self, x, y):
               scr = 'myresource/tiles64/green_box.png'
               bullet = BoxSprite(scr, 1)
               self.box_list.append(bullet)
               if len(self.box_list.sprite_list) > self.count_box:
                   self.box_list.pop(0).remove_from_sprite_lists()

               # Position the bullet at the player's current location
               start_x = self.player_sprite.center_x
               start_y = self.player_sprite.center_y
               bullet.position = self.player_sprite.position

               # Get from the mouse the destination location for the bullet
               # IMPORTANT! If you have a scrolling screen, you will also need
               # to add in self.view_bottom and self.view_left.
               dest_x = x + self.view_left
               dest_y = y + self.view_bottom
               self.view_bottom = self.view_bottom
               # self.view_left = self.view_left

               # Do math to calculate how to get the bullet to the destination.
               # Calculation the angle in radians between the start points
               # and end points. This is the angle the bullet will travel.
               x_diff = dest_x - start_x
               y_diff = dest_y - start_y
               angle = math.atan2(y_diff, x_diff)

               # What is the 1/2 size of this sprite, so we can figure out how far
               # away to spawn the bullet
               size = max(self.player_sprite.width, self.player_sprite.height) / 2

               # Use angle to to spawn bullet away from player in proper direction
               bullet.center_x += size * math.cos(angle)
               bullet.center_y += size * math.sin(angle)

               # Set angle of bullet
               bullet.angle = math.degrees(angle)

               # Gravity to use for the bullet
               # If we don't use custom gravity, bullet drops too fast, or we have
               # to make it go too fast.
               # Force is in relation to bullet's angle.

               bullet_gravity = (0, -BULLET_GRAVITY)
               box_gravity = (0, -BOX_GRAVITY)

               # Add the sprite. This needs to be done AFTER setting the fields above.
               self.physics_engine.add_sprite(bullet,
                                              mass=MY_BOX_MASS,
                                              damping=0.9,
                                              friction=0.9,
                                              collision_type="box",
                                              gravity=box_gravity,
                                              elasticity=0.9)
               # Add force to bullet

               force_box = (BOX_MOVE_FORCE, 1)
               self.physics_engine.apply_force(bullet, force_box)

    def _init_enemies(self):

        enemies_layer = self.tile_map.object_lists[LAYER_NAME_ENEMIES]
        # print(self.enemies_list, 333)
        for my_object in enemies_layer:
            # print('555555')
            cartesian = self.tile_map.get_cartesian(
                my_object.shape[0], my_object.shape[1]
            )
            # cartesian = (32, 23)
            enemy_type = my_object.properties["type"]
            if enemy_type == "robot":
                enemy = RobotEnemy(self.ladder_list, my_object.properties, self.physics_engine, self.bullet_list, 3.0, self)
                enemy.scale = 1.3
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
            self.enemies_list.append(enemy)

    def _init_player_sprite(self):
        live = Live()
        self.player_sprite = PlayerSprite(self.ladder_list, hit_box_algorithm="Detailed", live=live, type='player')


        self.player_sprite.center_x = SPRITE_SIZE * PLAYER_START_GRID[0] + SPRITE_SIZE / 2
        self.player_sprite.center_y = SPRITE_SIZE * (SCREEN_GRID_HEIGHT-PLAYER_START_GRID[1]) + SPRITE_SIZE / 2
        self.player_list.append(self.player_sprite)

    def on_update(self, delta_time):
        """ Movement and game logic """

        if any([x() for x in self.level_restsrt_options]):
            self.setup()

        is_on_ground = self.physics_engine.is_on_ground(self.player_sprite)
        # Update player forces based on keys pressed
        if not is_on_ground and not self.player_sprite.is_on_ladder:
            self.aaa.append(self.player_sprite.position)
        elif self.aaa:
            k = self.aaa[0][1]-self.player_sprite.center_y

            if k > 420.0:
                self.player_sprite.live.current -= k/14
            self.aaa.clear()





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

        for moving_sprite in self.moving_list:
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
            # print(delta_time)
            velocity = (moving_sprite.change_x * 1 / delta_time, moving_sprite.change_y * 1 / delta_time)
            self.physics_engine.set_velocity(moving_sprite, velocity)
            self.bullet_list.update()
            self.pan_camera_to_user(panning_fraction=0.12)
            self.setup_next_level()

        # Update moving platforms and enemies
        if self.enemies_list.sprite_list:
            self.enemies_list.update_animation(delta_time)
            self.enemies_list.update()

        # See if the enemy hit a boundary and needs to reverse direction.
        for enemy in self.enemies_list.sprite_list:
            self.enspeed = enemy.center_y
            is_on_ground = self.physics_engine.is_on_ground(enemy)
            if not is_on_ground:
                # enemy.change_x = 0
                border_no_movement = SCREEN_HEIGHT- enemy.properties['border_no_movement']
                enemy.change_y = -0.4
                if enemy.center_y < border_no_movement:
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


        btl_list = arcade.check_for_collision_with_list(self.player_sprite, self.dinamic_bottle_list)
        for botl in btl_list:
            # print('!!!!!!!!!AAAAAAAAAAAAAAAAAAAAAAAAA')
            botl.remove_from_sprite_lists()
            self.player_sprite.live.add(botl.properties.get('live', 0))




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
        self.wall_bg_list.draw()
        # if self.background_image:
        #     arcade.draw_lrwh_rectangle_textured(2, 0,
        #                                     4480,2560,
        #                                     self.background_image)

        self.ladder_list.draw()
        self.player_list.draw()
        # if self.fbackground_image:
        #     arcade.draw_lrwh_rectangle_textured(0, 0,
        #                                     4480,2560,
        #                                     self.fbackground_image)
        self.wall_list.draw()
        self.enemies_list.draw()
        self.background.draw()
        self.moving_list.draw()
        self.bottle_list.draw()
        self.dinamic_bottle_list.draw()
        self.invertory_list.draw()
        self.box_list.draw()
        self.bullet_list.draw()
        self.dinamic_list.draw()

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


        score_text = f"{round(self.player_sprite.center_y, 1)}"

        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )

        self.interface.draw()

    def pan_camera_to_user(self, panning_fraction: float = 0.1):
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

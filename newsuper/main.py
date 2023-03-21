"""
Example of Pymunk Physics Engine Platformer
"""
import math
from typing import Optional
import arcade
from constants import *
from player_sprite import PlayerSprite
from bullet_sprite import BulletSprite


class GameWindow(arcade.Window):
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
        self.bullet_list: Optional[arcade.SpriteList] = None
        self.item_list: Optional[arcade.SpriteList] = None
        self.moving_sprites_list: Optional[arcade.SpriteList] = None
        self.ladder_list: Optional[arcade.SpriteList] = None

        self.left_pressed: bool = False
        self.right_pressed: bool = False
        self.up_pressed: bool = False
        self.down_pressed: bool = False

        self.physics_engine: Optional[arcade.PymunkPhysicsEngine] = None


        self.camera_sprites = arcade.Camera(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)

    def _init_player_sprite(self):
        self.player_sprite = PlayerSprite(self.ladder_list, hit_box_algorithm="Detailed")
        grid_x = 4
        grid_y = 4
        self.player_sprite.center_x = SPRITE_SIZE * grid_x + SPRITE_SIZE / 2
        self.player_sprite.center_y = SPRITE_SIZE * grid_y + SPRITE_SIZE / 2
        self.player_list.append(self.player_sprite)

    def setup(self):
        # self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        map_name = f"resources/my_maps/pymunk_test_map_{self.level}.json"
        self.tile_map = arcade.load_tilemap(map_name, SPRITE_SCALING_TILES)
        arcade.set_background_color(self.tile_map.background_color)
        self.end_of_map = END_OF_MAP[0]*SPRITE_SIZE, (self.tile_map.height - END_OF_MAP[1] - 1)*SPRITE_SIZE


        # Pull the sprite layers out of the tile map
        self.wall_list = self.tile_map.sprite_lists["Platforms"]
        self.item_list = self.tile_map.sprite_lists["Dynamic Items"]
        self.ladder_list = self.tile_map.sprite_lists["Ladders"]
        self.moving_sprites_list = self.tile_map.sprite_lists['Moving Platforms']
        self.foreground = self.tile_map.sprite_lists['foreground']
        self.background= self.tile_map.sprite_lists['background']

        cam_w = self.tile_map.width*SPRITE_IMAGE_SIZE*SPRITE_SCALING_TILES
        cam_h = self.tile_map.height*SPRITE_IMAGE_SIZE*SPRITE_SCALING_TILES
        self.view_left = 0
        self.view_bottom = 0
        self.camera = arcade.Camera(cam_w/2, cam_h/2)


        self._init_player_sprite()
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

        # Add the player.
        # For the player, we set the damping to a lower value, which increases
        # the damping rate. This prevents the character from traveling too far
        # after the player lets off the movement keys.
        # Setting the moment to PymunkPhysicsEngine.MOMENT_INF prevents it from
        # rotating.
        # Friction normally goes between 0 (no friction) and 1.0 (high friction)
        # Friction is between two objects in contact. It is important to remember
        # in top-down games that friction moving along the 'floor' is controlled
        # by damping.
        self.physics_engine.add_sprite(self.player_sprite,
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

        # Create the items
        self.physics_engine.add_sprite_list(self.item_list,
                                            friction=DYNAMIC_ITEM_FRICTION,
                                            collision_type="item")

        # Add kinematic sprites
        self.physics_engine.add_sprite_list(self.moving_sprites_list,
                                            body_type=arcade.PymunkPhysicsEngine.KINEMATIC)


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.ESCAPE:
            arcade.exit()
        if modifiers == arcade.key.MOD_SHIFT and key == arcade.key.R:
            self.level = 1
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
            if self.physics_engine.is_on_ground(self.player_sprite) \
                    and not self.player_sprite.is_on_ladder:
                # She is! Go ahead and jump
                impulse = (0, PLAYER_JUMP_IMPULSE)
                self.physics_engine.apply_impulse(self.player_sprite, impulse)
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
        """ Called whenever the mouse button is clicked. """

        bullet = BulletSprite(32, 32, arcade.color.DARK_YELLOW)
        self.bullet_list.append(bullet)

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
        print(dest_x, start_x, self.view_left)
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

        # Add the sprite. This needs to be done AFTER setting the fields above.
        self.physics_engine.add_sprite(bullet,
                                       mass=BULLET_MASS,
                                       damping=1.0,
                                       friction=0.6,
                                       collision_type="bullet",
                                       gravity=bullet_gravity,
                                       elasticity=0.9)

        # Add force to bullet
        force = (BULLET_MOVE_FORCE, 0)
        self.physics_engine.apply_force(bullet, force)

    def on_update(self, delta_time):
        """ Movement and game logic """
        # print(self.player_sprite.bottom)
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
        self.background.draw()
        self.wall_list.draw()
        self.ladder_list.draw()
        self.moving_sprites_list.draw()
        self.bullet_list.draw()
        self.item_list.draw()
        self.player_list.draw()
        self.foreground.draw()

        self.gui_camera.use()
        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )

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

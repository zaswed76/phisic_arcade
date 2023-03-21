import math

from constants import *
import arcade
from bullet_sprite import BulletSprite, BoxSprite

class Controller(arcade.Window):
    def __init__(self, width, height, title):
        """ Create the variables """

        # Init the parent class
        super().__init__(width, height, title)
        self.left_pressed: bool = False
        self.right_pressed: bool = False
        self.up_pressed: bool = False
        self.down_pressed: bool = False
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
           if y < 54:
               for cell in self.interface.cell_list:
                   if cell.collides_with_point((x, y)):
                       print(cell.toggle())

               return
           if button == 4 and self.count_box:
               print(self.count_box, 'ttt')
               scr = 'resources/images/tiles/boxCrate_double.png'
               bullet = BoxSprite(scr, 0.25)
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
                                              friction=0.5,
                                              collision_type="item",
                                              gravity=box_gravity,
                                              elasticity=0.9)
               # Add force to bullet

               force_box = (BOX_MOVE_FORCE, 1)
               self.physics_engine.apply_force(bullet, force_box)
           elif button == 1:
               if self.on_bullet:
                    bullet = BulletSprite(32, 8, arcade.color.DARK_YELLOW)
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
                                                   mass=0.1,
                                                   damping=1,
                                                   friction=0.9,
                                                   collision_type="bullet",
                                                   gravity=bullet_gravity,
                                                   elasticity=0.5)
                    # Add force to bullet
                    force = (BULLET_MOVE_FORCE, 1)
                    self.physics_engine.apply_force(bullet, force)


import math

from constants import *
import arcade
from bullet_sprite import BulletSprite, BoxSprite

class Controller(arcade.Window):
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
               self.create_box(x, y)

           elif button == 1:
               self.create_bullet(x, y)




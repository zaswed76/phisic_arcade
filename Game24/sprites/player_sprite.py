import math
from typing import Optional
import arcade
from const import *
from paths import *

class PlayerError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        print('calling str')
        if self.message:
            return 'MyCustomError, {0} '.format(self.message)
        else:
            return 'в tilemap в слое объектов Mark должен быть создана точка с именем player'


class PlayerSprite(arcade.Sprite):
    SHOOTER = 'shooter'
    CREATOR = 'creator'
    def __init__(self,
                 ladder_list: arcade.SpriteList,
                 hit_box_algorithm, physics_engine=None, live=None, type='player', game=None):
        """ Init """
        # Let parent initialize
        super().__init__()
        self.hit_box_algorithm = hit_box_algorithm
        self.game = game
        self.physics_engine = physics_engine
        self.type = type
        self.fast_run_k = 0
        self.horizontal_speed_k = 0
        self.fast_run = False

        # Set our scale
        self.live = live
        self.scale = SPRITE_SCALING_PLAYER

        self.character_face_direction = RIGHT_FACING

        # Index of our current texture
        self.cur_texture = 0

        # How far have we traveled horizontally since changing the texture
        self.x_odometer = 0
        self.y_odometer = 0

        self.ladder_list = ladder_list
        self.is_on_ladder = False
        self.current_person = 'shooter'
        self.setup_person()

    def setup_person(self):

        main_path = CHARACTERS / f"{self.current_person}"
        self.idle_texture_pair = arcade.load_texture_pair(main_path / "idle.png",
                                                          hit_box_algorithm=self.hit_box_algorithm)
        self.jump_texture_pair = arcade.load_texture_pair(main_path / "jump.png")
        self.fall_texture_pair = arcade.load_texture_pair(main_path / "fall.png")
        self.walk_textures = []
        for i in range(8):
            texture = arcade.load_texture_pair(main_path / f"walk{i}.png")
            self.walk_textures.append(texture)
        self.climbing_textures = []
        texture = arcade.load_texture(main_path / "climb0.png")
        self.climbing_textures.append(texture)
        texture = arcade.load_texture(main_path / "climb1.png")
        self.climbing_textures.append(texture)
        self.texture = self.idle_texture_pair[0]
        self.hit_box = self.texture.hit_box_points


    def set_person(self, n):
        self.current_person = n

    def turn_texture_right(self):
        self.character_face_direction = RIGHT_FACING
        self.texture = self.idle_texture_pair[self.character_face_direction]

    def turn_texture_left(self):
        self.character_face_direction = LEFT_FACING
        self.texture = self.idle_texture_pair[self.character_face_direction]

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        """ Handle being moved by the pymunk engine """
        # Figure out if we need to face left or right
        if dx < -DEAD_ZONE and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif dx > DEAD_ZONE and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Are we on the ground?
        is_on_ground = physics_engine.is_on_ground(self)

        # Are we on a ladder?
        if len(arcade.check_for_collision_with_list(self, self.ladder_list)) > 0:
            if not self.is_on_ladder:
                self.is_on_ladder = True
                self.pymunk.gravity = (0, 0)
                self.pymunk.damping = 0.0001
                self.pymunk.max_vertical_velocity = PLAYER_MAX_HORIZONTAL_SPEED
        else:
            if self.is_on_ladder:
                self.pymunk.damping = 1.0
                self.pymunk.max_vertical_velocity = PLAYER_MAX_VERTICAL_SPEED
                self.is_on_ladder = False
                self.pymunk.gravity = None

        # Add to the odometer how far we've moved
        self.x_odometer += dx
        self.y_odometer += dy

        if self.is_on_ladder and not is_on_ground:
            # Have we moved far enough to change the texture?
            if abs(self.y_odometer) > DISTANCE_TO_CHANGE_TEXTURE:

                # Reset the odometer
                self.y_odometer = 0

                # Advance the walking animation
                self.cur_texture += 1

            if self.cur_texture > 1:
                self.cur_texture = 0
            self.texture = self.climbing_textures[self.cur_texture]
            return

        # Jumping animation
        if not is_on_ground:
            if dy > DEAD_ZONE:
                self.texture = self.jump_texture_pair[self.character_face_direction]
                return
            elif dy < -DEAD_ZONE:
                self.texture = self.fall_texture_pair[self.character_face_direction]
                return

        # Idle animation
        if abs(dx) <= DEAD_ZONE:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Have we moved far enough to change the texture?
        if abs(self.x_odometer) > DISTANCE_TO_CHANGE_TEXTURE:

            # Reset the odometer
            self.x_odometer = 0

            # Advance the walking animation
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]
    def set_fast(self, b):
        if b:
            self.fast_run_k = 5000
            self.horizontal_speed_k = 1000
        else:
            self.fast_run_k = 0
            self.horizontal_speed_k = 0


    def update(self):
        # Update player forces based on keys pressed
        # if not is_on_ground and not self.player_sprite.is_on_ladder:
        #     self.aaa.append(self.player_sprite.position)
        # elif self.aaa:
        #     k = self.aaa[0][1]-self.player_sprite.center_y
        #
        #     if k > 420.0:
        #         self.player_sprite.live.current -= k/14
        #     self.aaa.clear()
        is_on_ground = self.physics_engine.is_on_ground(self)
        if self.game.left_pressed and not self.game.right_pressed:
            # Create a force to the left. Apply it.
            if is_on_ground or self.is_on_ladder:
                f = -PLAYER_MOVE_FORCE_ON_GROUND-self.fast_run_k
                # print(self.fast_run_k, '<<<<')
                # print(f, '<<<<')
                force = (f, 0)

            else:

                force = (-PLAYER_MOVE_FORCE_IN_AIR, 0)
            self.physics_engine.apply_force(self, force)
            # Set friction to zero for the player while moving
            self.physics_engine.set_friction(self, 0)
        elif self.game.right_pressed and not self.game.left_pressed:
            # Create a force to the right. Apply it.
            if is_on_ground or self.is_on_ladder:
                f2 = PLAYER_MOVE_FORCE_ON_GROUND + self.fast_run_k
                force = (f2, 0)
                # print(f2, '>>>>')
            else:
                force = (PLAYER_MOVE_FORCE_IN_AIR, 0)
            self.physics_engine.apply_force(self, force)
            # Set friction to zero for the player while moving
            self.physics_engine.set_friction(self, 0)
        elif self.game.up_pressed and not self.game.down_pressed:
            # Create a force to the right. Apply it.
            if self.is_on_ladder:
                force = (0, PLAYER_MOVE_FORCE_ON_GROUND)
                self.physics_engine.apply_force(self, force)
                # Set friction to zero for the player while moving
                self.physics_engine.set_friction(self, 0)
        elif self.game.down_pressed and not self.game.up_pressed:
            # Create a force to the right. Apply it.
            if self.is_on_ladder:
                force = (0, -PLAYER_MOVE_FORCE_ON_GROUND)
                self.physics_engine.apply_force(self, force)
                # Set friction to zero for the player while moving
                self.physics_engine.set_friction(self, 0)
        else:
            # Player's feet are not moving. Therefore up the friction so we stop.
            self.physics_engine.set_friction(self, 1.0)

        # Move items in the physics engine

    def on_update(self, delta_time: float = 1 / 60):
        self.update()
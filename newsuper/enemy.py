import arcade
from constants import *
from functions import *
from bullet_sprite import Bullet

class Entity(arcade.Sprite):
    def __init__(self, name_folder, name_file):
        super().__init__()

        # Default to facing right
        self.facing_direction = RIGHT_FACING

        # Used for image sequences
        self.cur_texture = 0
        # self.scale = CHARACTER_SCALING
        self.character_face_direction = RIGHT_FACING

        main_path = f":resources:images/animated_characters/{name_folder}/{name_file}"

        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")
        self.jump_texture_pair = load_texture_pair(f"{main_path}_jump.png")
        self.fall_texture_pair = load_texture_pair(f"{main_path}_fall.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

        # Load textures for climbing
        self.climbing_textures = []
        texture = arcade.load_texture(f"{main_path}_climb0.png")
        self.climbing_textures.append(texture)
        texture = arcade.load_texture(f"{main_path}_climb1.png")
        self.climbing_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # set_hit_box = [[-22, -64], [22, -64], [22, 28], [-22, 28]]
        self.hit_box = self.texture.hit_box_points


class Enemy(Entity):
    def __init__(self, name_folder, name_file):

        # Setup parent class
        super().__init__(name_folder, name_file)

        self.should_update_walk = 0

    def update_animation(self, delta_time: float = 1 / 60):
        # is_on_ground = self.physics_engine.is_on_ground(self)
        # if not is_on_ground:
        #     self.kill()
        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return

        # Walking animation
        if self.should_update_walk == 3:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.facing_direction]
            self.should_update_walk = 0
            return

        self.should_update_walk += 1



class RobotEnemy(Enemy):
    def __init__(self, ladder_list, properties, physics_engine, bullet_list, time_between_firing, main):

        # Set up parent class
        super().__init__("robot", "robot")
        self.main = main
        self.properties = properties
        self.physics_engine = physics_engine
        self.x_odometer = 0
        self.y_odometer = 0
        self.ladder_list = ladder_list
        self.is_on_ladder = False
        self.time_since_last_firing = 0.0

        # How often do we fire?
        self.time_between_firing = time_between_firing

        # When we fire, what list tracks the bullets?
        self.bullet_list = bullet_list
        self.bullet_gravity = (0, -30)
        self.collision_lists = [self.main.player_list,
                                self.main.wall_list,
                                self.main.wall_list,
                                self.main.box_list
                                ]

    def update(self, delta_time: float = 1/60):
        self.time_since_last_firing += delta_time

        # If we are past the firing time, then fire
        if self.time_since_last_firing >= self.time_between_firing:

            # Reset timer
            self.time_since_last_firing = 0

            # Fire the bullet
            bullet = Bullet(":resources:images/space_shooter/laserBlue01.png", collisions_lists=self.collision_lists, damage=50)
            bullet.center_x = self.left
            bullet.angle = 180
            bullet.top = self.center_y - self.height/4
            self.bullet_list.append(bullet)
            self.physics_engine.add_sprite(bullet,
                                                   mass=ENEMY_BULLET_MASS,
                                                   damping=1,
                                                   friction=0.9,
                                                   collision_type="bullet2",
                                                   gravity=self.bullet_gravity,
                                                   elasticity=0.5,)
            force = (ENEMY_BULLET_FORCE, 1)
            self.physics_engine.apply_force(bullet, force)

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        if dx < -DEAD_ZONE and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif dx > DEAD_ZONE and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        is_on_ground = physics_engine.is_on_ground(self)
        if not is_on_ground:
            self.change_y *= 4

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

class ZombieEnemy(Enemy):
    def __init__(self):

        # Set up parent class
        super().__init__("zombie", "zombie")
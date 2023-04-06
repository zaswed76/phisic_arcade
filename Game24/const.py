LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_PLAYER = "Player"
LAYER_NAME_DINAMIC= "Dinamic"
LAYER_NAME_DINAMIC_KEY= "Dinamic_key"
LAYER_NAME_BUTTON= "Buttons"
LAYER_NAME_MOOVING = "Mooving platform"
LAYER_NAME_GATE = "gate"
LAYER_NAME_MOOVING_ON_ITEM = "Mooving platform on item"
LAYER_NAME_LADDERS = "Ladders"
LAYER_NAME_OBJECTPLATFORM = "objectplatform"
LAYER_NAME_DONT_TOUCH = "Dont_touch"
LAYER_NAME_INVERTORY = "invertory"
LAYER_NAME_ANIMATION = "animation"
LAYER_NAME_BULLET = "bullet"
LAYER_NAME_NPS = "nps"




# ###################################################################
# ###############     Game   #####################################

SPRITE_SCALING_TILES = 1
_GRAVITY = 1300
GRAVITY = 1300
DEFAULT_DAMPING = 1
PLATFORMS_FRICTION = 1
TILE_SCALING = 1
DISTANCE_TO_CHANGE_TEXTURE = 20
SPRITE_IMAGE_SIZE = 64


# ###################################################################
# ###############     PLAYER    #####################################
# ###################################################################

SPRITE_SCALING_PLAYER = 0.8
PLAYER_DAMPING = 1
PLAYER_MASS = 4.0

PLAYER_START_GRID = 6, 23
# Friction between objects
PLAYER_FRICTION = 1
WALL_FRICTION = 1

DYNAMIC_ITEM_FRICTION = 0.9
DYNAMIC_MASS = 2
DYNAMIC_ELASTICITY = 0.2 # 0 нет отскока
DYNAMIC_DAMPING = 1 # 0 количество скорости, которое сохраняется до следующего тика.
# значение 1,0 означает отсутствие потери скорости,
# а значение 0,9 означает потерю скорости на 10% и т. д.


# Mass (defaults to 1)


# Keep player from going too fast
PLAYER_MAX_HORIZONTAL_SPEED = 500
PLAYER_MAX_VERTICAL_SPEED = 800

# Force applied while on the ground
PLAYER_MOVE_FORCE_ON_GROUND = 5900

# Force applied when moving left/right in the air
PLAYER_MOVE_FORCE_IN_AIR = 4000

# Strength of a jump
PLAYER_JUMP_IMPULSE = 6700

# Close enough to not-moving to have the animation go to idle.
DEAD_ZONE = 0.1

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1


BULLET_MOVE_FORCE = 150000



# END_OF_MAP = (48, 28)
# DEFAULT_SCREEN_WIDTH = 800
# DEFAULT_SCREEN_HEIGHT = 400
# VIEWPORT_MARGIN_LEFT = 128
# VIEWPORT_MARGIN_RIGHT = 360
# VIEWPORT_MARGIN_TOP = 260
# VIEWPORT_MARGIN_BOTTOM = 64
# CAMERA_SPEED = 0.3
# SCREEN_TITLE = "PyMunk Platformer"
#
# # How big are our image tiles?
# SPRITE_IMAGE_SIZE = 64
#
# # Scale sprites up or down
#
# SPRITE_SCALING_TILES = 1
#
# # Scaled sprite size for tiles
# SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING_TILES)
#
# # Size of grid to show on screen, in number of tiles
# SCREEN_GRID_WIDTH = 70
# SCREEN_GRID_HEIGHT = 40
#
# # Size of screen to show, in pixels
# SCREEN_WIDTH = SPRITE_SIZE   * SCREEN_GRID_WIDTH
# SCREEN_HEIGHT = SPRITE_SIZE * SCREEN_GRID_HEIGHT
#
# # --- Physics forces. Higher number, faster accelerating.
#

#
#
# # How many pixels to move before we change the texture in the walking animation

#
# # How much force to put on the bullet
# BULLET_MOVE_FORCE = 100000
#
#
# # Mass of the bullet
# BULLET_MASS = 2
#
# # Make bullet less affected by gravity
# BOX_MOVE_FORCE = 131800
# BULLET_GRAVITY = 1100
# BOX_GRAVITY = 500
#
# MY_BOX_MASS = 4
# MY_BOX_MAX_COUNT = 3
#

# ###################################################################
# ###############     ENEMY     #####################################
# ###################################################################
#
#
# ENEMY_BULLET_SPEED = 6
# ENEMY_BULLET_MASS = 2
# ENEMY_BULLET_DAMAGE = 10
# ENEMY_BULLET_TIME_FIRING = 3
# ENEMY_BULLET_FORCE = 100000
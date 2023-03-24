END_OF_MAP = (48, 28)
DEFAULT_SCREEN_WIDTH = 800
DEFAULT_SCREEN_HEIGHT = 400
VIEWPORT_MARGIN_LEFT = 128
VIEWPORT_MARGIN_RIGHT = 360
VIEWPORT_MARGIN_TOP = 260
VIEWPORT_MARGIN_BOTTOM = 64
CAMERA_SPEED = 0.3
SCREEN_TITLE = "PyMunk Platformer"

# How big are our image tiles?
SPRITE_IMAGE_SIZE = 64

# Scale sprites up or down
SPRITE_SCALING_PLAYER = 1
SPRITE_SCALING_TILES = 1

# Scaled sprite size for tiles
SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING_TILES)

# Size of grid to show on screen, in number of tiles
SCREEN_GRID_WIDTH = 70
SCREEN_GRID_HEIGHT = 40

# Size of screen to show, in pixels
SCREEN_WIDTH = SPRITE_SIZE   * SCREEN_GRID_WIDTH
SCREEN_HEIGHT = SPRITE_SIZE * SCREEN_GRID_HEIGHT

# --- Physics forces. Higher number, faster accelerating.

# Gravity
GRAVITY = 1300

# Damping - Amount of speed lost per second
DEFAULT_DAMPING = 1


# How many pixels to move before we change the texture in the walking animation
DISTANCE_TO_CHANGE_TEXTURE = 20

# How much force to put on the bullet
BULLET_MOVE_FORCE = 100000


# Mass of the bullet
BULLET_MASS = 2

# Make bullet less affected by gravity
BOX_MOVE_FORCE = 131800
BULLET_GRAVITY = 1100
BOX_GRAVITY = 500

MY_BOX_MASS = 4
MY_BOX_MAX_COUNT = 3

###################################################################
###############     PLAYER    #####################################
###################################################################

PLAYER_DAMPING = 1


PLAYER_START_GRID = 6, 23
# Friction between objects
PLAYER_FRICTION = 1
WALL_FRICTION = 1
DYNAMIC_ITEM_FRICTION = 0.7

# Mass (defaults to 1)
PLAYER_MASS = 3.0

# Keep player from going too fast
PLAYER_MAX_HORIZONTAL_SPEED = 500
PLAYER_MAX_VERTICAL_SPEED = 800

# Force applied while on the ground
PLAYER_MOVE_FORCE_ON_GROUND = 5500

# Force applied when moving left/right in the air
PLAYER_MOVE_FORCE_IN_AIR = 3000

# Strength of a jump
PLAYER_JUMP_IMPULSE = 1400

# Close enough to not-moving to have the animation go to idle.
DEAD_ZONE = 0.1

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

###################################################################
###############     ENEMY     #####################################
###################################################################


ENEMY_BULLET_SPEED = 6
ENEMY_BULLET_MASS = 2
ENEMY_BULLET_DAMAGE = 10
ENEMY_BULLET_TIME_FIRING = 3
ENEMY_BULLET_FORCE = 100000
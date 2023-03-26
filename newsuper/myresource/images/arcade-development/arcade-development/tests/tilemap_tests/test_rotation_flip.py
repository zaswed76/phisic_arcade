import arcade


def test_rotation_mirror(window):
    # Read in the tiled map
    my_map = arcade.load_tilemap("../tiled_maps/rotation.json")

    assert my_map.tile_width == 128
    assert my_map.tile_height == 128
    assert my_map.width == 11
    assert my_map.height == 10

    # --- Platforms ---
    assert "Blocking Sprites" in my_map.sprite_lists
    wall_list = my_map.sprite_lists["Blocking Sprites"]

    wall = wall_list[0]
    assert wall.position == (64, 64)
    pos = 0, 0
    assert wall.texture.image.getpixel(pos) == (255, 0, 0, 255)
    pos = 127, 0
    assert wall.texture.image.getpixel(pos) == (0, 255, 0, 255)
    pos = 127, 127
    assert wall.texture.image.getpixel(pos) == (255, 0, 255, 255)

    wall = wall_list[1]
    assert wall.position == (192, 64)
    pos = 0, 0
    assert wall.texture.image.getpixel(pos) == (0, 255, 0, 255)
    pos = 127, 0
    assert wall.texture.image.getpixel(pos) == (255, 0, 0, 255)
    pos = 127, 127
    assert wall.texture.image.getpixel(pos) == (0, 0, 255, 255)

    wall = wall_list[2]
    assert wall.position == (448, 64)
    pos = 0, 0
    assert wall.texture.image.getpixel(pos) == (0, 0, 255, 255)
    pos = 127, 0
    assert wall.texture.image.getpixel(pos) == (255, 0, 0, 255)
    pos = 127, 127
    assert wall.texture.image.getpixel(pos) == (0, 255, 0, 255)

    wall = wall_list[3]
    assert wall.position == (576, 64)
    pos = 0, 0
    assert wall.texture.image.getpixel(pos) == (255, 0, 255, 255)
    pos = 127, 0
    assert wall.texture.image.getpixel(pos) == (0, 255, 0, 255)
    pos = 127, 127
    assert wall.texture.image.getpixel(pos) == (255, 0, 0, 255)

    wall = wall_list[4]
    assert wall.position == (832, 64)
    pos = 0, 0
    assert wall.texture.image.getpixel(pos) == (255, 0, 255, 255)
    pos = 127, 0
    assert wall.texture.image.getpixel(pos) == (0, 0, 255, 255)
    pos = 127, 127
    assert wall.texture.image.getpixel(pos) == (255, 0, 0, 255)

    wall = wall_list[5]
    assert wall.position == (960, 64)
    pos = 0, 0
    assert wall.texture.image.getpixel(pos) == (0, 0, 255, 255)
    pos = 127, 0
    assert wall.texture.image.getpixel(pos) == (255, 0, 255, 255)
    pos = 127, 127
    assert wall.texture.image.getpixel(pos) == (0, 255, 0, 255)

    wall = wall_list[6]
    assert wall.position == (1216, 64)
    pos = 0, 0
    assert wall.texture.image.getpixel(pos) == (0, 255, 0, 255)
    pos = 127, 0
    assert wall.texture.image.getpixel(pos) == (255, 0, 255, 255)
    pos = 127, 127
    assert wall.texture.image.getpixel(pos) == (0, 0, 255, 255)

    wall = wall_list[7]
    assert wall.position == (1344, 64)
    pos = 0, 0
    assert wall.texture.image.getpixel(pos) == (255, 0, 0, 255)
    pos = 127, 0
    assert wall.texture.image.getpixel(pos) == (0, 0, 255, 255)
    pos = 127, 127
    assert wall.texture.image.getpixel(pos) == (255, 0, 255, 255)

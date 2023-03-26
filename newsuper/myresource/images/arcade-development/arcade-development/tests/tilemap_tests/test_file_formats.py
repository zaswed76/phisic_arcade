import arcade

TILE_SCALING = 1.0


def test_csv_left_up():
    # Read in the tiled map
    my_map = arcade.load_tilemap("../tiled_maps/csv_left_up_embedded.json")

    assert my_map.tile_width == 128
    assert my_map.tile_height == 128
    assert my_map.width == 10
    assert my_map.height == 10

    # --- Platforms ---
    assert "Blocking Sprites" in my_map.sprite_lists
    wall_list = my_map.sprite_lists["Blocking Sprites"]

    assert wall_list[0].position == (64, 1216)
    assert "dirtCenter" in wall_list[0].texture.name

    assert wall_list[1].position == (1216, 1216)
    assert "grassCenter" in wall_list[1].texture.name

    assert wall_list[2].position == (64, 64)
    assert "boxCrate" in wall_list[2].texture.name


def test_csv_right_down():
    # Read in the tiled map
    my_map = arcade.load_tilemap("../tiled_maps/csv_right_down_external.json")

    assert my_map.tile_width == 128
    assert my_map.tile_height == 128
    assert my_map.width == 10
    assert my_map.height == 10

    # --- Platforms ---
    assert "Blocking Sprites" in my_map.sprite_lists
    wall_list = my_map.sprite_lists["Blocking Sprites"]

    assert wall_list[0].position == (64, 1216)
    assert "dirtCenter" in wall_list[0].texture.name

    assert wall_list[1].position == (1216, 1216)
    assert "grassCenter" in wall_list[1].texture.name

    assert wall_list[2].position == (64, 64)
    assert "boxCrate" in wall_list[2].texture.name


def test_base_64_zlib():
    # Read in the tiled map
    my_map = arcade.load_tilemap("../tiled_maps/base_64_zlib.json")

    assert my_map.tile_width == 128
    assert my_map.tile_height == 128
    assert my_map.width == 10
    assert my_map.height == 10

    # --- Platforms ---
    assert "Blocking Sprites" in my_map.sprite_lists
    wall_list = my_map.sprite_lists["Blocking Sprites"]

    assert wall_list[0].position == (64, 1216)
    assert "dirtCenter" in wall_list[0].texture.name

    assert wall_list[1].position == (1216, 1216)
    assert "grassCenter" in wall_list[1].texture.name

    assert wall_list[2].position == (64, 64)
    assert "boxCrate" in wall_list[2].texture.name


def test_base_64_gzip():
    # Read in the tiled map
    my_map = arcade.load_tilemap("../tiled_maps/base_64_gzip.json")

    assert my_map.tile_width == 128
    assert my_map.tile_height == 128
    assert my_map.width == 10
    assert my_map.height == 10

    # --- Platforms ---
    assert "Blocking Sprites" in my_map.sprite_lists
    wall_list = my_map.sprite_lists["Blocking Sprites"]

    assert wall_list[0].position == (64, 1216)
    assert "dirtCenter" in wall_list[0].texture.name

    assert wall_list[1].position == (1216, 1216)
    assert "grassCenter" in wall_list[1].texture.name

    assert wall_list[2].position == (64, 64)
    assert "boxCrate" in wall_list[2].texture.name

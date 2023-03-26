import arcade

# noinspection PyCompatibility
class TileMap(arcade.TileMap):
    def __init__(self, *args):
        super().__init__(*args)

    def get_obgect_by_name(self, name, layer_name):
        for obj in self.object_lists.get(layer_name, list()):
            if obj.name == name:
                return obj
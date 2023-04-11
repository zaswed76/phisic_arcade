import arcade
from pathlib import Path
import yaml

def load_settings(file):
    with open(file) as f:
        templates = yaml.safe_load(f)
    return templates

def get_explosian_texture(dir_name: Path, name, ext=".png"):
    file = dir_name / f'{name}{ext}'
    cfg = load_settings(dir_name / 'config.yaml')[name]
    return arcade.load_spritesheet(file, **cfg)


class Explosion(arcade.Sprite):
    """ This class creates an explosion animation """
    def __init__(self, texture_list, scale=1):
        super().__init__()
        self.current_texture = 0
        self.textures = texture_list
        self.scale = scale


    def on_update(self, delta_time: float = 1 / 60):


            self.current_texture += 1


            if self.current_texture < len(self.textures):
                self.set_texture(self.current_texture)
            else:

                self.remove_from_sprite_lists()
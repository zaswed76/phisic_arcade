import arcade
from arcade import load_texture
import textwrap
from arcade.gui.widgets import UITextArea, UIInputText, UITexturePane
from paths import *

class ContentList(arcade.SpriteList):
    def __init__(self):
        super().__init__()

    def append(self, obj):
        self.append(obj.sprite)

    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        for obj in self.sprite_list:
            obj.sprite.draw()


class Controll(arcade.Sprite):
    def __init__(self, img, name):
        super().__init__()
        self.texture = load_texture(img)
        self.name = name




class TextInterface:
    def __init__(self):
        self.bg_list = arcade.SpriteList()
        self.content_list = arcade.SpriteList()
        self.icon_list = arcade.SpriteList()
        self.row_height_table = {5: 70, 2: 140, 1: 160, 3: 120, 4: 80, 6: 50}

        self.bg = Controll(TEXT_INTERFACE_BG, 'bg')
        self.bg.scale = 1.2

        self.close = Controll(CLOSE_TEXT_INTERFACE, 'close')

        self.forward = Controll(RIGHT_ARROW, 'forward')

        self.back = Controll(LEFT_ARROW, 'back')

        self.bg_list.append(self.bg)
        self.bg_list.append(self.close)
        # self.bg_list.append(self.forward)
        # self.bg_list.append(self.back)

        self.rect = self.bg.width, self.bg.height
        self.show = False


    def set_visible(self, b):
        self.show = b
        if not b:
            self.icon_list.clear()

    def set_pos(self, x, y):
        self.bg.set_position(x, y)
        self.close.set_position(x, y)
        self.close.scale = 0.8
        self.close.set_position(self.bg.right-self.close.width/1.2, self.bg.top-self.close.height/1.2)
        self.forward.set_position(self.bg.right-self.forward.width/1.2, self.bg.bottom+self.forward.height/1.2)
        self.back.set_position(self.bg.center_x-self.back.width, self.bg.bottom+self.back.height/1.5)

    def set_icon(self, texture):
        self.icon = arcade.Sprite()

        self.icon.texture = texture
        self.icon.center_x = self.bg.center_x - self.bg.width/3.1
        self.icon.center_y = self.bg.center_y
        self.icon_list.append(self.icon)

    def forward_text(self):
        print('forward_text')

    def back_text(self):
        print('back_text')

    def set_text(self, text: str):
        tw = textwrap.wrap(text, 32)
        rows = len(tw)
        text = "\n".join(tw)

        self.content_list.clear()
        sprite = arcade.create_text_sprite(text, self.bg.center_x - self.bg.width/10, self.row_height_table[rows], color=arcade.color.BLACK, font_size=22)
        self.content_list.append(sprite)


    def update(self):
        pass


    def draw(self):
        # self.manager.draw()
        if self.show:
            self.bg_list.draw()
            self.icon_list.draw()
            self.content_list.draw()

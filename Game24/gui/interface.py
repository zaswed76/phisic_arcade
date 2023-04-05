import arcade
from paths import *



class ItemSprite(arcade.Sprite):
    def __init__(self, object):
        super().__init__()
        self.texture = object.texture
        self.name = object.properties.get("name")





class CellSprite(arcade.Sprite):
    def __init__(self):
        super().__init__()
        print(ICON_iNTERFACE)
        self.activ = arcade.load_texture(ICON_iNTERFACE/'activ.png')
        self.notactive = arcade.load_texture(ICON_iNTERFACE/'notactiv.png')
        self.check = False

    def toggle(self):
        self.check = not self.check
        self.set_active(self.check)

    def set_active(self, v):
        if v: self.texture = self.activ
        else: self.texture = self.notactive




class Interface:
    def __init__(self, img, left=64, top=28, scale=0.4, border=8, item_scale=0.5):
        self.item_scale = item_scale
        self.border = border
        self.scale = scale
        self.img = img
        self.cell_list = arcade.SpriteList()
        self.top = top
        self.left = left
        self.right_border = left
        self.invertory = arcade.SpriteList()

    def append_cell(self):
        cell = CellSprite()
        cell.scale = self.scale
        cell.set_active(False)

        cell.set_position(self.right_border, self.top)
        self.right_border += cell.width + self.border
        self.cell_list.append(cell)

    def append_item(self, item):
        x, y = self.cell_list.sprite_list[0].position
        item = ItemSprite(item)
        item.scale = self.item_scale
        item.set_position(x, y)
        self.invertory.append(item)
        if len(self.invertory.sprite_list) < 2:
            self.cell_list.sprite_list[0].toggle()

    def pop_item(self, item_name):
        for i in self.invertory:
            if i.name == item_name:
                _i = i
                i.kill()
                return _i


    def get_item(self, item_name):
        for i in self.invertory:
            if i.name == item_name:
                return True
        else:
            return False

    def update(self):
        self.cell_list.update()
        self.invertory.update()

    def draw(self):
        self.cell_list.draw()
        self.invertory.draw()
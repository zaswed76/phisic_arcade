import arcade

class ItemSprite(arcade.Sprite):
    def __init__(self, texture):
        super().__init__()
        self.texture = texture




class CellSprite(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.activ = arcade.load_texture('resources/icons/activ.png')
        self.notactive = arcade.load_texture('resources/icons/notactiv.png')
        self.check = False

    def toggle(self):
        self.check = not self.check
        self.set_active(self.check)

    def set_active(self, v):
        if v: self.texture = self.activ
        else: self.texture = self.notactive




class Interface:
    def __init__(self, img, left=464, top=28, scale=0.4, border=8, item_scale=0.25):
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



    def update(self):
        self.cell_list.update()
        self.invertory.update()

    def draw(self):
        self.cell_list.draw()
        self.invertory.draw()
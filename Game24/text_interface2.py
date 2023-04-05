import random

import arcade
import textwrap
from paths import *

FONT_SIZE = 20

def text_wrap(text, width):
    tw = textwrap.wrap(text, width/(FONT_SIZE-4))
    return "\n".join(tw)

class Controll(arcade.Sprite):
    def __init__(self, img, name):
        super().__init__()
        self.texture = arcade.load_texture(img)
        self.name = name


class Icon(arcade.Sprite):
    def __init__(self, img, name):
        super().__init__()
        self.name = name
        self.texture = arcade.load_texture(img)


class Message:
    def __init__(self, nps_name, content, bg: arcade.Sprite):
        self.name = nps_name
        print(content, 1111111)
        r_list = content['вопрос']
        random.shuffle(r_list)
        nps_repl = text_wrap(r_list[0], bg.width)
        rlist = content['ответ']

        self.reply_list = [x[0] for x in rlist]
        self.transition_list = [x[1] for x in rlist]
        self.reply_list = [text_wrap(t, bg.width-60) for t in self.reply_list]
        mx = bg.left + 145
        ix = mx - 80
        iy = bg.top - 70
        my = bg.top - 70
        self.content = arcade.SpriteList()
        self.nps_content = arcade.SpriteList()

        mess = arcade.create_text_sprite(nps_repl, 0, 0, color=(24, 106, 59), font_size=FONT_SIZE, font_name='helvetica')
        mess.name = self.name
        mess.top = my
        mess.left = mx
        image = ANIMATION_OBJECTS / nps_name / "icon.png"
        icon = arcade.Sprite(image)
        icon.name = self.name
        icon.scale = 0.6
        icon.top = iy
        icon.left = ix
        self.content.append(mess)
        self.content.append(icon)

        x = mess.left + 60
        y = mess.bottom
        for r, t in zip(self.reply_list, self.transition_list):
            reply = Reply(r, x, y-20, t)
            y = reply.bottom
            self.nps_content.extend(reply.content)



class Reply:
    def __init__(self, text, x, y, name):
        self.name = name

        mx = x
        self.ix = mx - 80
        self.iy = y
        my = y
        self.content = arcade.SpriteList()
        mess = arcade.create_text_sprite(text, 0, 0, color=arcade.color.BLACK, font_size=FONT_SIZE, font_name='helvetica')
        print(mess.hit_box)
        sprite = arcade.Sprite()
        # sprite.top = my
        # sprite.left = mx

        mess.name = name
        mess.parent = self



        mess.top = my
        mess.left = mx
        self.bottom = mess.bottom

        icon = arcade.Sprite(CHECK)
        icon.name = name
        icon.parent = self
        icon.scale = 0.6
        icon.top = self.iy
        icon.left = self.ix
        self.content.append(mess)
        self.content.append(icon)

    def set_icon(self):
        print("eeeeeee")
        icon = arcade.Sprite(CHECKGREEN)
        icon.name = self.name
        icon.scale = 0.6
        icon.top = self.iy
        icon.left = self.ix
        self.content.append(icon)





class TextInterface2:
    def __init__(self):
        self.bg_list = arcade.SpriteList()
        self.message_list = arcade.SpriteList()
        self.nps_message_list = arcade.SpriteList()
        self.hover_list = arcade.SpriteList()
        self.bg = Controll(TEXT_INTERFACE_BG2, 'bg')
        self.bg_list.append(self.bg)
        self.width = self.bg.width
        self.height = self.bg.height

        self._visible = False

    def set_visible(self, b):
        self._visible = b

    # def set_hover(self, obj: arcade.Sprite):
    #
    #     obj.parent.set_icon()


    def draw(self):

        if self._visible:
            self.bg_list.draw()
            self.message_list.draw()
            self.nps_message_list.draw()
            # self.message_list.draw_hit_boxes(arcade.color.RED)
            self.hover_list.draw()

    def set_pos(self, x, y):
        self.bg.set_position(x, y)

    def set_message_nps(self, nps, content):
        self.message_list.clear()
        self.nps_message_list.clear()
        m = Message(nps, content, self.bg)
        self.message_list.extend(m.content)
        self.nps_message_list.extend(m.nps_content)


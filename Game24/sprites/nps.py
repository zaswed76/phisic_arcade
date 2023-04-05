import arcade

from pathlib import Path
import os
from const import *
from service import *
from paths import *
import random

class NpsContent:
    def __init__(self, nps_name, level):
        self.name = nps_name
        self._data = load_settings(LEVELS / f"{level}_contact.yaml")[nps_name]
        self.condition = self._data.get("condition")
        self.messages = self._data.get("messages")

    @property
    def content(self):
        return self._data

    def get_message(self, key):
        m = self._data['messages'].get(key, 'exit')
        return m



class Say:
    MEETING_1_NOT_MET = "meeting_1_not_cond"
    MEETING_1_MET = "meeting_1_cond"
    MEETING_OTHER_NOT_MET = "meeting_other_not_cond"
    MEETING_OTHER_MET = "meeting_other_cond"
    NOT_WAITING = "not_waiting"

    def __init__(self, level, nps):
        self.nps = nps
        self.level = level
        self._data = load_settings(LEVELS / f'{level}_contact.yaml')
        self.satat_method = {"meeting_1_not_cond": self.meeting_1_not_cond,
                       "meeting_1_cond": self.meeting_1_cond,
                       "meeting_other_not_cond": self.meeting_other_not_cond,
                       "meeting_other_cond": self.meeting_other_cond,
                       'not_waiting': self.not_waiting}

        self.current_state = Say.MEETING_1_NOT_MET

    def get_condition(self):
        return self._data[self.nps]['condition']

    def change_status(self, cond, number_meet, not_waiting=False):
        if not_waiting:
            self.current_state = Say.NOT_WAITING
            return
        if not cond:
            if number_meet == 0:
                self.current_state = Say.MEETING_1_NOT_MET
            else:
                self.current_state = Say.MEETING_OTHER_NOT_MET
        elif number_meet == 0:
            self.current_state = Say.MEETING_1_MET
        else:
            self.current_state = Say.MEETING_OTHER_MET

    def set_status(self, status):
        print(status)

        if status == Say.NOT_WAITING:


            self._data[self.nps]['condition'] = None
            self.current_state = status

    def get_repl(self):
        return self.satat_method[self.current_state]()


    def meeting_1_not_cond(self):
        return self._data[self.nps]['meeting_1_not_cond'][0]

    def meeting_1_cond(self):
        return self._data[self.nps]['meeting_1_cond'][0]

    def meeting_other_not_cond(self):
        return random.choice(self._data[self.nps]['meeting_other_not_cond'])

    def meeting_other_cond(self):
        return self._data[self.nps]['meeting_other_cond'][0]

    def not_waiting(self):
        s = self._data[self.nps]['not_waiting']

        return random.choice(s)

class Entity(arcade.Sprite):

    def __init__(self, game, obgect, physics_engine):
        super().__init__()
        self.invertory = []
        self.number_meet = 0
        self.physics_engine = physics_engine
        self.obgect = obgect
        self.properties = obgect.properties
        self.game = game
        self.text_list = arcade.SpriteList()
        self.txt = arcade.create_text_sprite("AAAAAAAAA", self.center_x+1300, 0, arcade.csscolor.WHITE, font_size=44)

        self.text_list.append(self.txt)

        self.states = {'wait': 0, 'contact': 1}
        self.state = "wait"
        self.not_witing = False

        self.direct = [RIGHT_FACING, LEFT_FACING]

        self.set_position(*self.obgect.shape)
        self.scale = self.obgect.properties.get('scale', 1)

        path = Path(self.obgect.properties.get('dir'))
        parts = path.parts[1:]
        path = Path()
        self.main_path = path.joinpath(*parts).absolute()
        self.idle_texture_pair = arcade.load_texture_pair(self.main_path / 'stand.png', hit_box_algorithm=None)
        self.icon_texture = arcade.load_texture(self.main_path / 'icon.png', hit_box_algorithm=None)
        self.texture = self.idle_texture_pair[RIGHT_FACING]

        self.set_hit_box(((-256.0, -128.0), (83.0, -128.0), (256.0, 128.0), (-83.0, 128.0)))


    def update_animation(self, delta_time: float = 0.016):
        pass


    def update(self):

        coll = self.collides_with_sprite(self.game.player_sprite)
        if coll and self.state == "wait":

            # print(self.game.curreent_nps)

                if self.game.player_sprite.center_x - self.center_x < 0:
                    self.texture = self.idle_texture_pair[LEFT_FACING]
                else:
                    self.texture = self.idle_texture_pair[RIGHT_FACING]

            # if self.state == "wait":
                self.state = "contact"
                self.game.set_curreent_nps(self)

                self.game.text_interface2.set_visible(True)
                self.nps_content = NpsContent(self.obgect.name, self.game.level)

                nnn = 0
                condition = self.nps_content.condition

                if condition and condition not in self.invertory:
                    # есть условие но его нет в инвертаре нпс
                    cond = False
                else:
                    # есть у нпс или нет условия
                    cond = True
                meet = self.number_meet
                if meet > 0:
                    meet = 1
                key = f'{nnn}, {meet}, {cond}'

                self.set_message(key)
                self.number_meet += 1
                self.game.set_pause(True)

    def set_message(self, key):

        if key == "exit":
            self.game.set_pause(False)
            self.game.text_interface2.set_visible(False)
            self.state = "wait"
            return
        mess = self.nps_content.get_message(key)
        self.game.text_interface2.set_message_nps(self.obgect.name, mess)





class Nps(Entity):
    def __init__(self, game, obgect, physics_engine):
        super().__init__(game, obgect, physics_engine)
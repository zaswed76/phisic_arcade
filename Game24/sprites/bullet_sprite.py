import math
import os

import arcade
from const import *
from paths import *
from sprites.enemy import *

class BulletSingleBlock:
    parent: arcade.Sprite
    DIRECT_TOP = 'top'
    DIRECT_BOTTOM = 'bottom'
    DIRECT_LEFT = 'left'
    DIRECT_RIGHT = 'right'
    PLAYER = 'player'

    def __init__(self, game, parent:arcade.Sprite,
                 name_bullet:str,
                 explosion_texture_list,
                 direction:str, delay=1.0,
                 bullet_scale=1,
                 collision_lists=arcade.SpriteList,
                 physics_engine=None, force=BULLET_MOVE_ENEMIES_FORCE,
                 explosion_scale=1,
                 pos=None,
                 cfg_bullet=None,
                 kill_distance=2000):
        """

        :param game: главное окно
        :param parent: к кому прикрепляем
        :param name_bullet: название пули из каталога bullet
        :param explosion_texture_list: game.py: line 63
        :param direction: имя для словаря направлений self.directs
        :param delay: через сколько появляется пулля
        :param bullet_scale:
        :param collision_lists: list!!! список python который содержит arcade.SpriteList для столкновений
        :param physics_engine:
        :param force:
        :param kill_distance: расстояние на котором пули исчезают - kill()
        :param explosion_scale:
        """
        self.pos = pos
        self.kill_distance = kill_distance
        self.directs = {BulletSingleBlock.DIRECT_BOTTOM: (0, -3000),
                        BulletSingleBlock.DIRECT_TOP: (0, 3000),
                        BulletSingleBlock.DIRECT_RIGHT: (3000, 0),
                        BulletSingleBlock.DIRECT_LEFT: (-3000, 0),
                        BulletSingleBlock.PLAYER: 'player'
                        }
        self.explosion_scale = explosion_scale
        self.force = force
        self.physics_engine = physics_engine
        self.bullet_scale = bullet_scale
        self.collision_lists = collision_lists
        self.cfg_bullet = cfg_bullet

        self.parent = parent
        self.game = game


        self.direction = direction
        self.explosion_texture_list = explosion_texture_list

        self.name_bullet = name_bullet
        self.delay = delay

        self.image = BULLETS / f"{self.name_bullet}.png"




    def get_bullet(self, delta_time: float = 0.016):
            if self.directs[self.direction] == 'player':
                x, y = self.game.player_sprite.position
            else:
                x = self.parent.center_x + self.directs[self.direction][0]
                y = self.parent.center_y + self.directs[self.direction][1]

            bullet = Bullet(self.game, self.parent, self.image, cl=self.collision_lists, damage=50,
                            type=Bullet.BULLET_TYPE, alpha=255,
                            cfg_bullet=self.cfg_bullet,
                            kill_distance=self.kill_distance)

            bullet.set_explosion(self.explosion_texture_list, self.explosion_scale)
            bullet.scale = self.bullet_scale
            bullet.center_x, bullet.center_y = self.parent.get_block_pos(self.pos)
            # print(self.parent.get_block_pos(self.pos), 11111)
            # bullet.center_x = self.parent.center_x
            #
            #
            # bullet.center_y = self.parent.center_y



            dest_x = x + self.game.view_left
            dest_y = y + self.game.view_bottom
            x_diff = dest_x - self.parent.center_x
            y_diff = dest_y - self.parent.bottom
            angle = math.atan2(y_diff, x_diff)

            size = max(self.parent.width, self.parent.height) / 8
            bullet.center_x += size * math.cos(angle)
            bullet.center_y += size * math.sin(angle)
            bullet.angle = math.degrees(angle)


            self.physics_engine.add_sprite(bullet, **self.cfg_bullet)

            self.physics_engine.apply_force(bullet, (self.force, 1))
            if len(self.game.bullet_enemys_list.sprite_list) > 60:
                b = self.game.bullet_enemys_list.pop(0)
                b.kill()

            self.game.bullet_enemys_list.append(bullet)

    def __repr__(self):
        return self.__class__.__name__

class BulletSprite(arcade.SpriteSolidColor):
    """ Bullet Sprite """
    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        """ Handle when the sprite is moved by the physics engine. """
        # If the bullet falls below the screen, remove it
        if self.center_y < -100:
            self.remove_from_sprite_lists()

class BoxSprite(arcade.Sprite):
    """ Player Sprite """
    def __init__(self, scr, scale):
        super().__init__()

        self.texture = arcade.load_texture(scr)
        self.scale = scale
    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        """ Handle when the sprite is moved by the physics engine. """
        # If the bullet falls below the screen, remove it
        if self.center_y < -100:
            self.remove_from_sprite_lists()

class Bullet(arcade.Sprite):
    BULLET_TYPE = "bullet"
    BOX_TYPE = "box"
    def __init__(self, game, parent, scr, scale=1.0, cl=None, damage=10, type="bullet", alpha=255, cfg_bullet=None, explosion_scale=1, kill_distance=2000):
        super().__init__()
        self.kill_distance = kill_distance
        self.touch = 0
        self.cfg_bullet = {} if cfg_bullet is None else cfg_bullet
        self.name = os.path.split(scr)[1].split('.')[0]
        self.explosion_scale = explosion_scale
        self.type = type
        self.game = game
        self._x = self.center_x
        self._y = self.center_y
        self.damage = damage
        self.parent = parent
        self.collisions_lists = arcade.SpriteList()

        if cl is not None:
            [self.collisions_lists.extend(ls) for ls in cl]

        self.texture = arcade.load_texture(scr)
        self.alpha = alpha

        if type == Bullet.BULLET_TYPE:
            self.set_hit_box(HIT_BOX_BULLET )
        self.scale = scale

    def set_explosion(self, texture_list, explosion_scale=1):
        self.explosion_scale = explosion_scale
        self.texture_list = texture_list

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):

        if self.center_y < -100:
            self.kill()


        if self.type == Bullet.BULLET_TYPE:
            if self.parent.name == "Player":
                coll_enemy = self.collides_with_list(self.game.scene[LAYER_NAME_ENEMIES])
                if coll_enemy and self.touch < 2:

                    self.game.create_explosion((self.center_x, self.center_y),
                                           texture_list=self.texture_list, scale=self.explosion_scale)
                    if self.touch < 1:
                        coll_enemy[0].set_damage(self.damage)
                    self.touch +=1
            if arcade.get_distance(self.parent.center_x, self.parent.center_y, self.center_x, self.center_y) > self.kill_distance:
                self.kill()
            coll = self.collides_with_list(self.collisions_lists)
            if coll:

                self.kill()
                if self.texture_list is not None:

                    self.game.create_explosion((self.center_x, self.center_y),
                                           texture_list=self.texture_list, scale=self.explosion_scale)
                if coll[0].properties.get("name") == "Player":
                    coll[0].kill()
                    self.game.setup()
            # coll_player = self.collides_with_sprite(self.game.player_sprite)
            # if coll_player:
            #     self.game.player_sprite.kill()
            #     self.game.setup()

        # ccc = self.collides_with_list(self.sprite_lists[0])
        # # if ccc:
        # #     ccc[0].kill
        # #     self.kill()
        #
        # for list_sprite in self.collisions_lists:
        #     coll = self.collides_with_list(list_sprite)
        #
        #     if coll:
        #
        #         if list_sprite.collision_type == "player":
        #             coll[0].live.current -= self.damage
        #             self.kill()
        #
        #         elif list_sprite.collision_type == "wall":
        #             pass
        #             # self.kill()
        #
        #             # coll[0].kill()






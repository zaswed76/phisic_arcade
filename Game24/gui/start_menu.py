
import arcade
WIDTH = 800
HEIGHT = 600
SPRITE_SCALING = 0.5


class MenuView(arcade.View):
    def __init__(self, size):
        super().__init__()
        self.game = None
        self.width = size[0]
        self.height = size[1]
        self.text = 0
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("www", self.width/2, self.height/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance.", self.width/2, self.height/2-75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        # self.game.setup()
        self.window.show_view(self.game)

    def set_next_view(self, next_view):
        self.game = next_view
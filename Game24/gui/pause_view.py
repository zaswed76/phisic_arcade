import arcade

WIDTH = 800
HEIGHT = 600

class PauseView(arcade.View):
    def __init__(self, game_view, size):
        super().__init__()
        self.game_view = game_view
        self.width = size[0]
        self.height = size[1]
    def on_show(self):
        arcade.set_background_color(arcade.color.ORANGE)

    def on_draw(self):
        arcade.start_render()

        # Draw player, for effect, on pause screen.
        # The previous View (GameView) was passed in
        # and saved in self.game_view.


        # # draw an orange filter over him
        # arcade.draw_lrtb_rectangle_filled(left=player_sprite.left,
        #                                   right=player_sprite.right,
        #                                   top=player_sprite.top,
        #                                   bottom=player_sprite.bottom,
        #                                   color=arcade.color.ORANGE + (200,))

        arcade.draw_text("PAUSED", self.width/2, self.height/2+50,
                         arcade.color.BLACK, font_size=50, anchor_x="center")

        # Show tip to return or reset
        arcade.draw_text("Press Esc. to return",
                         self.width/2,
                         self.height/2,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")
        arcade.draw_text("Press Enter to reset",
                         self.width/2,
                         self.height/2-30,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:   # resume game
            self.window.show_view(self.game_view)
        elif key == arcade.key.ENTER:  # reset game

            self.window.show_view(game)
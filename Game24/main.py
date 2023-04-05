import arcade

from gui.start_menu import MenuView
from game import GameView

def main():
    window = arcade.Window()
    window.set_fullscreen()
    window.set_vsync(True)
    size = window.width, window.height

    game = GameView(size)
    game.setup()
    menu = MenuView(size)
    menu.set_next_view(game)
    game.set_next_view(menu)
    window.show_view(menu)

    arcade.run()


if __name__ == "__main__":
    main()

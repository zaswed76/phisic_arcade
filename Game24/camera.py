
import arcade


class Camera(arcade.Camera):
    def __init__(self, view_left, view_bottom, viewport_width: int = 0,viewport_height: int = 0):
        super().__init__(viewport_width, viewport_height)
        self.view_bottom = view_bottom
        self.view_left = view_left

    def pan_camera_to_user(self, game, player_sprite, panning_fraction=0.1):
        """
        Manage Scrolling

        :param panning_fraction: Number from 0 to 1. Higher the number, faster we
                                 pan the camera to the user.
        """

        # This spot would center on the user
        screen_center_x = player_sprite.center_x - (self.viewport_width / 3)
        screen_center_y = player_sprite.center_y - (
            self.viewport_height / 3
        )
        if screen_center_x > 0:
            game.view_left = screen_center_x
        if screen_center_y > 0:
            game.view_bottom = screen_center_y
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        user_centered = screen_center_x, screen_center_y
        self.move_to(user_centered, panning_fraction)


    def pan_to_mouse(self, x, y, panning_fraction=0.1):
        """
        Manage Scrolling

        :param panning_fraction: Number from 0 to 1. Higher the number, faster we
                                 pan the camera to the user.
        """

        # This spot would center on the user
        screen_center_x = x - (self.viewport_width / 2)
        screen_center_y = y - (
            self.viewport_height / 2
        )
        if screen_center_x > 0:
            self.view_left = screen_center_x
        if screen_center_y > 0:
            self.view_bottom = screen_center_y
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        user_centered = screen_center_x, screen_center_y
        self.move_to(user_centered, panning_fraction)
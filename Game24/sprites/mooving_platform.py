
def update_mooving_platform(layer, physics_engine, delta_time):

    for moving_sprite in layer:
        # print(moving_sprite.properties['active'], moving_sprite.properties['name'], 4444444)
        if moving_sprite.properties['active']:
            print(0)
            if moving_sprite.boundary_right and \
                    moving_sprite.right > moving_sprite.boundary_right:
                moving_sprite.change_x *= -1
            elif moving_sprite.boundary_left and \
                    moving_sprite.change_x < 0 and \
                    moving_sprite.left < moving_sprite.boundary_left:
                moving_sprite.change_x *= -1
            if moving_sprite.boundary_top and \
                    moving_sprite.change_y > 0 and \
                    moving_sprite.top > moving_sprite.boundary_top:
                print(1111)
                moving_sprite.change_y *= -1
            elif moving_sprite.boundary_bottom and \
                    moving_sprite.change_y < 0 and \
                    moving_sprite.bottom < moving_sprite.boundary_bottom:
                moving_sprite.change_y *= -1
                print(2222)
            velocity = (moving_sprite.change_x * 1 / delta_time, moving_sprite.change_y * 1 / delta_time)
            physics_engine.set_velocity(moving_sprite, velocity)
        else:
            physics_engine.set_velocity(moving_sprite, (0, 0))
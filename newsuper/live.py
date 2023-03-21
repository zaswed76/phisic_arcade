import arcade
class Live:
    def __init__(self, max=150, current=150):
        self.current = current
        self.max = max
        self.beginx = 264
        self.beginy = self.beginx+max
        self.midl_diap = (self.beginy - self.beginx)/2
        self.color = arcade.csscolor.RED

    def minus(self, damage):
        if self.current > 0:
            self.current -= damage

    def add(self, live):
        self.current += live
        if self.current > self.max:
            self.current = self.max

    def restore(self):
        self.current = self.max

    def kill(self):
        self.current = 0

    def update(self):

        end = self.beginx+self.current+1
        arcade.draw_lrtb_rectangle_filled(
            self.beginx, self.beginy, 46, 36, arcade.csscolor.WHITE)

        arcade.draw_lrtb_rectangle_filled(
            self.beginx, end, 46, 36, self.color)

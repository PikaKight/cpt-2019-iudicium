import arcade
import random
import settings


player_speedx = 5
player_speedy = 5


class Chapter4View(arcade.View):
    def __init__(self):
        super().__init__()

        # Player Sprite
        player_sprite = "ch4_Sprites/alienBlue_front.png"

        self.player = arcade.Sprite(player_sprite, 0.3)
        self.player.center_x = 100
        self.player.center_y = 200

    def on_show(self):
        arcade.set_background_color(arcade.color.GHOST_WHITE)

    def on_draw(self):
        arcade.start_render()
        # arcade.draw_text("Chapter 4", settings.WIDTH/2, settings.HEIGHT/2,
        #                  arcade.color.BLACK, font_size=30, anchor_x="center")

        # Player Health Bar

        self.player.draw()

        if self.player.center_x >= settings.WIDTH - 10 or self.player.center_x <= 10:
            self.player.change_x = 0
        elif self.player.center_y >= settings.HEIGHT - 20 or self.player.center_y <= 20:
            self.player.change_y = 0

    def update(self, delta_time):
        self.player.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.director.next_view()

        if key == arcade.key.UP:
            self.player.change_y = player_speedy
        elif key == arcade.key.DOWN:
            self.player.change_y = -player_speedy
        elif key == arcade.key.RIGHT:
            self.player.change_x = player_speedx
        elif key == arcade.key.LEFT:
            self.player.change_x = -player_speedx            


    def on_key_release(self, key, modifiers):
        # self.director.next_view()

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.RIGHT or key == arcade.key.LEFT:
            self.player.change_x = 0



if __name__ == "__main__":
    """This section of code will allow you to run your View
    independently from the main.py file and its Director.

    You can ignore this whole section. Keep it at the bottom
    of your code.

    It is advised you do not modify it unless you really know
    what you are doing.
    """
    from utils import FakeDirector
    window = arcade.Window(settings.WIDTH, settings.HEIGHT)
    my_view = Chapter4View()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()

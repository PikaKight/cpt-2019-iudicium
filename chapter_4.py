import arcade
import random
import settings


class Chapter4View(arcade.View):
    def __init__(self):
        super().__init__()

        # Player Sprite
        player_sprite = "ch4_Sprites/alienBlue_front.png"

        self.player = arcade.Sprite(player_sprite, 1)
        self.player.center_x = 100
        self.player.center_y = 200

    def on_show(self):
        arcade.set_background_color(arcade.color.GHOST_WHITE)

    def on_draw(self):
        arcade.start_render()
        # arcade.draw_text("Chapter 4", settings.WIDTH/2, settings.HEIGHT/2,
        #                  arcade.color.BLACK, font_size=30, anchor_x="center")

        self.player.draw()

    def on_key_press(self, key, modifiers):
        self.director.next_view()


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

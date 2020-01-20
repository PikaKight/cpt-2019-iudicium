import arcade

import settings


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.half_height = settings.HEIGHT / 2
        self.half_width = settings.WIDTH / 2
        self.background = arcade.load_texture("Sprites\Iudicium.jpg")
        

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(self.half_width, self.half_height, settings.WIDTH, settings.HEIGHT, self.background)
        arcade.draw_text("IUDICIUM", settings.WIDTH/2, settings.HEIGHT/2 + 100,
                         arcade.color.CRIMSON, font_size=60, anchor_x="center")
        arcade.draw_text("Press Any Key to START", settings.WIDTH/2, settings.HEIGHT/2 - 100,
                         arcade.color.CRIMSON, font_size=60, anchor_x="center")           

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
    my_view = MenuView()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()

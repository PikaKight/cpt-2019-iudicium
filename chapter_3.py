import arcade

import settings


class Ch3View(arcade.View):
    def __init__(self):
        super().__init__()
        # self.music = arcade.Sound("End_of_Time.mp3")
        # self.music.play()
          
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_rectangle_outline(200, 450, 100, 50, arcade.color.AZURE)
        arcade.draw_rectangle_outline(175, 425, 50, 100, arcade.color.AZURE)
        arcade.draw_rectangle_outline(200, 215, 100, 50, arcade.color.AZURE)
        arcade.draw_rectangle_outline(175, 240, 50, 100, arcade.color.AZURE)
        arcade.draw_rectangle_outline(575, 450, 100, 50, arcade.color.AZURE)
        arcade.draw_rectangle_outline(600, 425, 50, 100, arcade.color.AZURE)

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
    my_view = Ch3View()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    # music = arcade.Sound("End_of_Time.mp3")
    # music.play()
    arcade.run()


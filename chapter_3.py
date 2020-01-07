import arcade

import settings

class Ch3View(arcade.View):
    def __init__(self):
        super().__init__()
        # self.music = arcade.Sound("End_of_Time.mp3")
        # self.music.play()
        self.sprite_main = arcade.Sprite(center_x=400, center_y=300)
        self.sprite_main.texture = arcade.make_circle_texture(50, arcade.color.AMAZON)
          
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_rectangle_outline(250, 475, 150, 50, arcade.color.AZURE)
        arcade.draw_rectangle_outline(200, 425, 50, 150, arcade.color.AZURE)
        arcade.draw_rectangle_outline(250, 125, 150, 50, arcade.color.AZURE)
        arcade.draw_rectangle_outline(200, 175, 50, 150, arcade.color.AZURE)
        arcade.draw_rectangle_outline(525, 475, 150, 50, arcade.color.AZURE)
        arcade.draw_rectangle_outline(575, 425, 50, 150, arcade.color.AZURE)
        arcade.draw_rectangle_outline(525, 125, 150, 50, arcade.color.AZURE)
        arcade.draw_rectangle_outline(575, 175, 50, 150, arcade.color.AZURE)
        arcade.draw_rectangle_filled(400, 590, 150, 20, arcade.color.ASH_GREY)
        arcade.draw_circle_filled(50, 50, 50, arcade.color.WHITE)
        arcade.draw_circle_filled(50, 550, 50, arcade.color.WHITE)
        arcade.draw_circle_filled(750, 50, 50, arcade.color.WHITE)
        arcade.draw_circle_filled(750, 550, 50, arcade.color.WHITE)
        self.sprite_main.draw()
        
        
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


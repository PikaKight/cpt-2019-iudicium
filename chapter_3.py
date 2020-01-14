import arcade

import settings
speed = 6
        
class Player(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.center_x < 30:
            self.change_x = 0
        if self.center_x > 770:
            self.change_x = 0
        if self.center_y < 40:
            self.change_y = 0
        if self.center_y > 560:
            self.change_y = 0
        
class Ch3View(arcade.View):
    def __init__(self):
        super().__init__()
        self.button = settings.button
        self.x = 0
        self.puzzle_action = 0
        self.color_1 = arcade.color.WHITE
        self.color_2 = arcade.color.WHITE
        self.color_3 = arcade.color.WHITE
        self.color_4 = arcade.color.WHITE
        # self.music = arcade.Sound("End_of_Time.mp3")
        # self.music.play()
        self.player = Player("Sprites/alienBlue_front.png", .4, 0, 0, 0, 0, 400, 300)
        self.text_sprite = arcade.Sprite("Sprites\Brown.png", .5, 0 ,0, 0, 0, 400, 590)
        self.text_box = arcade.Sprite("Sprites\DialogueBox.png", 1, 0,0,0,0, )
        self.button_1 = arcade.Sprite(self.button, .7, 0 ,0, 0, 0, 50, 570)
        self.button_2 = arcade.Sprite(self.button, .7, 0 ,0, 0, 0, 50, 75)
        self.button_3 = arcade.Sprite(self.button, .7, 0 ,0, 0, 0, 750, 570)
        self.button_4 = arcade.Sprite(self.button, .7, 0 ,0, 0, 0, 750, 75)

 
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
        self.text_sprite.draw()
        self.button_1.draw()
        self.button_2.draw()
        self.button_3.draw()
        self.button_4.draw()
        self.player.draw()
        if self.x == 1:
            self.text_box.draw()
            arcade.draw_text("Hello", 400, 300, arcade.color.WHITE, 40, 0, align="left", font_name="Comic Sans")
        
    
    def update(self, delta_time):
        self.player.update()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            print(x, y)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.director.next_view()

        if key == arcade.key.W:
            self.player.change_y = speed

        elif key == arcade.key.S:
            self.player.change_y = -speed
        
        elif key == arcade.key.A:
            self.player.change_x = -speed
        
        elif key == arcade.key.D:
            self.player.change_x = speed
        
        elif key == arcade.key.SPACE:
            print(self.player.center_x, self.player.center_y)
            
            if (self.player.center_x  >= 340 and self.player.center_x <= 460) and (self.player.center_y >= 555):
                self.x = 1

            elif (self.player.center_x  >= 30 and self.player.center_x <= 88) and (self.player.center_y >= 540 and self.player.center_y <= 564) and self.puzzle_action == 0:
                self.button = settings.button_pressed
                self.puzzle_action = 1

            elif (self.player.center_x  >= 30 and self.player.center_x <= 88) and (self.player.center_y >= 540 and self.player.center_y <= 564 ) and self.puzzle_action == 1:
                self.button = settings.button_pressed
                self.puzzle_action = 0

            # elif (self.player.center_x  >= 0 and self.player.center_x <= 110) and (self.player.center_y >= 100 and self.player.center_y <= 90) and self.puzzle_action == 0:
            #     print("hi")
            #     self.color_2 = arcade.color.GREEN
            #     self.puzzle_action = 1

            # elif (self.player.center_x  >= 0 and self.player.center_x <= 110) and (self.player.center_y >= 100 and self.player.center_y <= 90) and self.puzzle_action == 1:
            #     self.color_2 = arcade.color.WHITE
            #     self.puzzle_action = 0
            
            # elif (self.player.center_x  >= 690 and self.player.center_x <= 700) and (self.player.center_y >= 500) and self.puzzle_action == 0:
            #     self.color_3 = arcade.color.GREEN
            #     print("hi")
            #     self.puzzle_action = 1

            # elif (self.player.center_x  >= 690 and self.player.center_x <= 700) and (self.player.center_y >= 500) and self.puzzle_action == 1:
            #     self.color_3 = arcade.color.WHITE
            #     self.puzzle_action = 0

            # elif (self.player.center_x  >= 690 and self.player.center_x <= 700) and (self.player.center_y >= 100 and self.player.center_y <= 90) and self.puzzle_action == 0:
            #     self.color_4 = arcade.color.GREEN
            #     print("hi")
            #     self.puzzle_action = 1

            # elif (self.player.center_x  >= 690 and self.player.center_x <= 700) and (self.player.center_y >= 100 and self.player.center_y <= 90) and self.puzzle_action == 1:
            #     self.color_4 = arcade.color.WHITE
            #     self.puzzle_action = 0

    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """
        if key == arcade.key.A or key == arcade.key.D:
            self.player.change_x = 0

        elif key == arcade.key.W or key == arcade.key.S:
            self.player.change_y = 0


           
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


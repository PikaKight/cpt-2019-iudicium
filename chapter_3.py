import arcade

import settings
speed = 6

class Ch3View(arcade.View):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.puzzle_action = 0
        self.color_1 = arcade.color.WHITE
        self.color_2 = arcade.color.WHITE
        self.color_3 = arcade.color.WHITE
        self.color_4 = arcade.color.WHITE
        # self.music = arcade.Sound("End_of_Time.mp3")
        # self.music.play()
        self.player = arcade.Sprite("Sprites/alienBlue_front.png", .4)
        self.player.center_x = 400
        self.player.center_y = 300
        self.button_2 = arcade.Sprite(settings.button, .7)
        self.button_2.center_x = 50
        self.button_2.center_y = 75
        
 
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
        arcade.draw_circle_filled(50, 50, 50, self.color_2) # min 100 110, min 100  max 90 y
        arcade.draw_rectangle_outline(50,50, 100, 100, arcade.color.AERO_BLUE)
        arcade.draw_circle_filled(50, 550, 50, self.color_1) # min 100 max 110 x, min 500 y
        arcade.draw_rectangle_outline(50,550, 100, 100, arcade.color.AERO_BLUE)
        arcade.draw_circle_filled(750, 50, 50, self.color_3) # min 690 max 700 x, min 500 y
        arcade.draw_rectangle_outline(750,50, 100, 100, arcade.color.AERO_BLUE)
        arcade.draw_circle_filled(750, 550, 50, self.color_4) # min 690 max 700 x, min 100 max 90 y
        arcade.draw_rectangle_outline(750,550, 100, 100, arcade.color.AERO_BLUE) 
        self.button_2.draw()
        self.player.draw()
        if self.x == 1:
            arcade.draw_rectangle_outline(400, 200, 700, 300, arcade.color.AERO_BLUE, 3)
            arcade.draw_rectangle_filled(400,200,697,297,arcade.color.BLACK)
            arcade.draw_text("Hello", 400, 300, arcade.color.WHITE, 40, 0, align="left", font_name="Comic Sans")
        
    
    def update(self, delta_time):
        self.player.update()
        
        if self.player.center_x < 30:
            self.player.change_x = 0
        if self.player.center_x > 770:
            self.player.change_x = 0
        if self.player.center_y < 40:
            self.player.change_y = 0
        if self.player.center_y > 560:
            self.player.change_y = 0


    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.director.next_view()

        if key == arcade.key.W:
            self.player.change_y = speed
            print(self.player.center_x, self.player.center_y)

        elif key == arcade.key.S:
            self.player.change_y = -speed
            print(self.player.center_x, self.player.center_y)
        
        elif key == arcade.key.A:
            self.player.change_x = -speed
            print(self.player.center_x, self.player.center_y)
        
        elif key == arcade.key.D:
            self.player.change_x = speed
            print(self.player.center_x, self.player.center_y)
        
        if key == arcade.key.SPACE:
            if (self.player.center_x  >= 340 and self.player.center_x <= 460) and (self.player.center_y >= 555):
                print("hi")
                self.x = 1

            if self.x == 1:
                self.x = 0

            elif (self.player.center_x  >= 0 and self.player.center_x <= 110) and (self.player.center_y >= 500) and  self.puzzle_action == 0:
                self.color_1 = arcade.color.GREEN
                self.puzzle_action = 1

            elif (self.player.center_x  >= 0 and self.player.center_x <= 110) and (self.player.center_y >= 500) and  self.puzzle_action == 1:
                self.color_1 = arcade.color.WHITE
                self.puzzle_action = 0

            elif (self.player.center_x  >= 0 and self.player.center_x <= 110) and (self.player.center_y >= 100 and self.player.center_y <= 90) and  self.puzzle_action == 0:
                print("hi")
                self.color_2 = arcade.color.GREEN
                self.puzzle_action = 1

            elif (self.player.center_x  >= 0 and self.player.center_x <= 110) and (self.player.center_y >= 100 and self.player.center_y <= 90) and  self.puzzle_action == 1:
                self.color_2 = arcade.color.WHITE
                self.puzzle_action = 0
            
            elif (self.player.center_x  >= 690 and self.player.center_x <= 700) and (self.player.center_y >= 500) and  self.puzzle_action == 0:
                self.color_3 = arcade.color.GREEN
                print("hi")
                self.puzzle_action = 1

            elif (self.player.center_x  >= 690 and self.player.center_x <= 700) and (self.player.center_y >= 500) and  self.puzzle_action == 1:
                self.color_3 = arcade.color.WHITE
                self.puzzle_action = 0

            elif (self.player.center_x  >= 690 and self.player.center_x <= 700) and (self.player.center_y >= 100 and self.player.center_y <= 90) and  self.puzzle_action == 0:
                self.color_4 = arcade.color.GREEN
                print("hi")
                self.puzzle_action = 1

            elif (self.player.center_x  >= 690 and self.player.center_x <= 700) and (self.player.center_y >= 100 and self.player.center_y <= 90) and  self.puzzle_action == 1:
                self.color_4 = arcade.color.WHITE
                self.puzzle_action = 0

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


import arcade

import settings
speed = 6

class Char:
    def __init__(self, color, position_x, position_y, radius):
        # Take the parameters of the init function above, and create instance variables out of them.
        self.position_x = position_x
        self.position_y = position_y
        self.change_x = 0
        self.change_y = 0
        self.radius = radius
        self.color = color
        self.sprite_main = arcade.Sprite(center_x=self.position_x, center_y=self.position_y)
        self.sprite_main.texture = arcade.make_circle_texture(self.radius, self.color)

    def draw(self):
        """ Draw the balls with the instance variables we have. """
        self.sprite_main.draw()

    def update(self):
        # Move the ball
        self.position_y += self.change_y
        print(self.position_y, self.change_y)
        self.position_x += self.change_x
    
        # See if the ball hit the edge of the screen. If so, change direction
        if self.position_x < self.radius:
            self.position_x = self.radius

        if self.position_x > settings.WIDTH - self.radius:
            self.position_x = settings.WIDTH - self.radius

        if self.position_y < self.radius:
            self.position_y = self.radius

        if self.position_y > settings.HEIGHT - self.radius:
            self.position_y = settings.HEIGHT - self.radius

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
        self.sprite_main = arcade.Sprite(center_x=400, center_y=300)
        self.sprite_main.texture = arcade.make_circle_texture(50, arcade.color.AMAZON)
        # Char(arcade.color.AMAZON, 400, 300, 50)
 
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
        arcade.draw_circle_filled(50, 550, 50, self.color_1) # min 100 max 110 x, min 500 y
        arcade.draw_circle_filled(750, 50, 50, self.color_3) # min 690 max 700 x, min 500 y
        arcade.draw_circle_filled(750, 550, 50, self.color_4) # min 690 max 700 x, min 100 max 90 y 
        self.sprite_main.draw()
        if self.x == 1:
            arcade.draw_rectangle_outline(400, 200, 700, 300, arcade.color.AERO_BLUE, 3)
            arcade.draw_rectangle_filled(400,200,697,297,arcade.color.BLACK)
            arcade.draw_text("Hello", 400, 300, arcade.color.WHITE, 40, 0, align="left", font_name="Comic Sans")
        
    
    def update(self, delta_time):
        self.sprite_main.update()
    
    def on_key_press(self, key, modifiers):

        if key == arcade.key.W:
            self.sprite_main.change_y = speed
            print(self.sprite_main.center_x, self.sprite_main.center_y)

        elif key == arcade.key.S:
            self.sprite_main.change_y = -speed
            print(self.sprite_main.center_x, self.sprite_main.center_y)
        
        elif key == arcade.key.A:
            self.sprite_main.change_x = -speed
            print(self.sprite_main.center_x, self.sprite_main.center_y)
        
        elif key == arcade.key.D:
            self.sprite_main.change_x = speed
            print(self.sprite_main.center_x, self.sprite_main.center_y)
        
        if key == arcade.key.SPACE:
            if (self.sprite_main.center_x  >= 340 and self.sprite_main.center_x <= 460) and (self.sprite_main.center_y >= 555):
                print("hi")
                self.x = 1

            elif (self.sprite_main.center_x  >= 0 and self.sprite_main.center_x <= 110) and (self.sprite_main.center_y >= 500) and  self.puzzle_action == 0:
                self.color_1 = arcade.color.GREEN
                self.puzzle_action = 1

            elif (self.sprite_main.center_x  >= 0 and self.sprite_main.center_x <= 110) and (self.sprite_main.center_y >= 500) and  self.puzzle_action == 1:
                self.color_1 = arcade.color.WHITE
                self.puzzle_action = 0

            elif (self.sprite_main.center_x  >= 0 and self.sprite_main.center_x <= 110) and (self.sprite_main.center_y >= 100 and self.sprite_main.center_y <= 90) and  self.puzzle_action == 0:
                self.color_2 = arcade.color.GREEN
                self.puzzle_action = 1

            elif (self.sprite_main.center_x  >= 0 and self.sprite_main.center_x <= 110) and (self.sprite_main.center_y >= 100 and self.sprite_main.center_y <= 90) and  self.puzzle_action == 1:
                self.color_2 = arcade.color.WHITE
                self.puzzle_action = 0
            
            elif (self.sprite_main.center_x  >= 690 and self.sprite_main.center_x <= 700) and (self.sprite_main.center_y >= 500) and  self.puzzle_action == 0:
                self.color_3 = arcade.color.GREEN
                self.puzzle_action = 1

            elif (self.sprite_main.center_x  >= 690 and self.sprite_main.center_x <= 700) and (self.sprite_main.center_y >= 500) and  self.puzzle_action == 1:
                self.color_3 = arcade.color.WHITE
                self.puzzle_action = 0

            elif (self.sprite_main.center_x  >= 690 and self.sprite_main.center_x <= 700) and (self.sprite_main.center_y >= 100 and self.sprite_main.center_y <= 90) and  self.puzzle_action == 0:
                self.color_4 = arcade.color.GREEN
                self.puzzle_action = 1

            elif (self.sprite_main.center_x  >= 690 and self.sprite_main.center_x <= 700) and (self.sprite_main.center_y >= 100 and self.sprite_main.center_y <= 90) and  self.puzzle_action == 1:
                self.color_4 = arcade.color.WHITE
                self.puzzle_action = 0

    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """
        if key == arcade.key.A or key == arcade.key.D:
            self.sprite_main.change_x = 0

        elif key == arcade.key.W or key == arcade.key.S:
            self.sprite_main.change_y = 0


           
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


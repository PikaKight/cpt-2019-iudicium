import arcade

import settings
speed = 6

class Player(arcade.Sprite):
    def __init__(self, filename=None, scale=1, image_x=0, image_y=0, image_width=0, image_height=0, center_x=0, center_y=0, repeat_count_x=1, repeat_count_y=1):
        super().__init__(filename=filename, scale=scale, image_x=image_x, image_y=image_y, image_width=image_width, image_height=image_height, center_x=center_x, center_y=center_y, repeat_count_x=repeat_count_x, repeat_count_y=repeat_count_y)

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        if self.right > settings.WIDTH:
            self.right = settings.WIDTH

        if self.bottom < 0:
            self.bottom = 3
        if self.top > settings.HEIGHT:
            self.top = settings.HEIGHT
        
        #boundary for inner left of the wall
        if self.left < 230 and self.right > 173: 
            if self.bottom <= 448 and self.top >= 346:
                self.left = 230
            if self.bottom <= 256 and self.top >= 155:
                self.left = 230
        
        #boundray for inner bottom of the wall
        if self.bottom < 155:
            if self.right >= 230 and self.right <= 330:
                self.bottom = 155
            if self.left >= 445 and self.left <= 545:
                self.bottom = 155

        #boundray for inner right of the wall
        if self.right > 545:
            if self.bottom <= 256 and self.top >= 155:
                self.right = 545 
            if self.bottom <= 448 and self.top >= 346:
                self.right = 545
        
        #boundray for inner top of the wall
        if self.top > 448:
            if self.left >= 230 and self.left <= 330:
                self.top = 448
            if self.right >= 445 and self.right <= 545:
                self.top = 448

class Puzzle:
    
    solution = [1, 4, 2, 3]

    def __init__(self):
        self._puzzle = []   

    def clone_puzzle(self):
        self.clone = self._puzzle

    def add_value(self, value):
        self._puzzle.append

    def remove_value(self, value):
        self._puzzle.remove(value)

    def give_puzzle(self):
        return self._puzzle

    def puzzle_checker(self, puzzle, value):
        if len(puzzle) == 1:
            if puzzle[0] is value:
                return True
            else:
                return False

        mid = len(puzzle) // 2

        left =  self.puzzle_checker(puzzle[:mid], value)
        right = self.puzzle_checker(puzzle[mid:], value)

        if left or right is True:
            return True
        else:
            return False       
        
        
class Ch3View(arcade.View):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.half_width = settings.WIDTH * .5
        self.half_height = settings.HEIGHT * .5
        self.button = settings.button
        self.player = Player("Sprites/alienBlue_front.png", .4, 0, 0, 0, 0, 400, 300)
        self.text_sprite = arcade.Sprite("Sprites\Brown.png", .5, 0 ,0, 0, 0, 400, 590)
        self.text_box = arcade.Sprite("Sprites\DialogueBox.png", 1, 0,0,0,0, 400, 300)
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
            super().on_draw()


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
            
            if (self.player.center_x  >= 290 and self.player.center_x <= 515) and (self.player.center_y >= 555):
                self.x = 1

            elif (self.player.center_x  >= 30 and self.player.center_x <= 88) and (self.player.center_y >= 540 and self.player.center_y <= 564) and self.puzzle_action == 0:
                self.button = settings.button_pressed
                self.puzzle_action = 1

            elif (self.player.center_x  >= 30 and self.player.center_x <= 88) and (self.player.center_y >= 540 and self.player.center_y <= 564 ) and self.puzzle_action == 1:
                self.button = settings.button
                self.puzzle_action = 0

            elif (self.player.center_x  >= 30 and self.player.center_x <= 88) and (self.player.center_y >= 48 and self.player.center_y <= 88) and self.puzzle_action == 0:
                self.button = settings.button_pressed
                self.puzzle_action = 1

            elif (self.player.center_x  >= 30 and self.player.center_x <= 88) and (self.player.center_y >= 48 and self.player.center_y <= 88) and self.puzzle_action == 1:
                self.button = settings.button
                self.puzzle_action = 0
            
            elif (self.player.center_x  >= 706 and self.player.center_x <= 772) and (self.player.center_y >= 540 and self.player.center_y <= 564) and self.puzzle_action == 0:
                self.button = settings.button_pressed
                self.puzzle_action = 1

            elif (self.player.center_x  >= 706 and self.player.center_x <= 772) and (self.player.center_y >= 540 and self.player.center_y <= 564) and self.puzzle_action == 1:
                self.button = settings.button
                self.puzzle_action = 0

            elif (self.player.center_x  >= 706 and self.player.center_x <= 772) and (self.player.center_y >= 48 and self.player.center_y <= 88) and self.puzzle_action == 0:
                self.button = settings.button_pressed
                self.puzzle_action = 1

            elif (self.player.center_x  >= 706 and self.player.center_x <= 772) and (self.player.center_y >= 48 and self.player.center_y <= 88) and self.puzzle_action == 1:
                self.button = settings.button
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
    arcade.run()
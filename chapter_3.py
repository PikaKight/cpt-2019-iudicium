import arcade, settings

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

class Wall(arcade.Sprite):
    def __init__(self, center_x=0, center_y=0):
        super().__init__(center_x=center_x, center_y=center_y)

class Puzzle:
    
    solution = [1, 4, 2, 3]

    def __init__(self):
        self._puzzle = []


    def clone_puzzle(self):
        self.clone = self._puzzle
        return self.clone


    def add_value(self, value):
        self._puzzle.append(value)


    def remove_value(self, value):
        self._puzzle.remove(value)


    def give_puzzle(self):
        return self._puzzle


    def value_checker(self, puzzle, value):
        if len(puzzle) == 0:
            return False

        if len(puzzle) == 1:
            if puzzle[0] is value:
                return True
            else:
                return False

        mid = len(puzzle) // 2

        left =  self.value_checker(puzzle[:mid], value)
        right = self.value_checker(puzzle[mid:], value)
   
        return left or right
    

    def checker(self):
        if self._puzzle is Puzzle.solution:
            return True
        
class Ch3View(arcade.View):
    def __init__(self):
        super().__init__()
        self.puzzle = Puzzle()
        self.x = 0
        self.half_width = settings.WIDTH * .5
        self.half_height = settings.HEIGHT * .5
        self.player = Player("Sprites/alienBlue_front.png", .4, 0, 0, 0, 0, 400, 300)
        self.text_sprite = arcade.Sprite("Sprites\Brown.png", .5, 0 ,0, 0, 0, 400, 590)
        self.text_box = arcade.Sprite("Sprites\DialogueBox.png", 1, 0,0,0,0, 400, 300)
        self.background = arcade.load_texture("Sprites/tiledFloor.jpg")



    def button_on(self, value):
        if value is 1:
            self.button_1 = arcade.Sprite(settings.button_pressed, .7, 0 ,0, 0, 0, 50, 570)
        elif value is 2:
            self.button_2 = arcade.Sprite(settings.button_pressed, .7, 0 ,0, 0, 0, 50, 75)
        elif value is 3:   
            self.button_3 = arcade.Sprite(settings.button_pressed, .7, 0 ,0, 0, 0, 750, 570)
        elif value is 4:    
            self.button_4 = arcade.Sprite(settings.button_pressed, .7, 0 ,0, 0, 0, 750, 75)


    def button_off(self, value):    
            if value is 1:
                self.button_1 = arcade.Sprite(settings.button, .7, 0 ,0, 0, 0, 50, 570)
            elif value is 2:
                self.button_2 = arcade.Sprite(settings.button, .7, 0 ,0, 0, 0, 50, 75)
            elif value is 3:   
                self.button_3 = arcade.Sprite(settings.button, .7, 0 ,0, 0, 0, 750, 570)
            elif value is 4:    
                self.button_4 = arcade.Sprite(settings.button, .7, 0 ,0, 0, 0, 750, 75)


    def on_show(self):
        self.button_off(1)
        self.button_off(2)
        self.button_off(3)
        self.button_off(4)


    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(self.half_width, self.half_height, settings.WIDTH, settings.HEIGHT, self.background)
        arcade.draw_rectangle_filled(250, 450, 125, 25, arcade.color.AZURE)
        arcade.draw_rectangle_filled(200, 400, 25, 125, arcade.color.AZURE)
        arcade.draw_rectangle_filled(250, 100, 125, 25, arcade.color.AZURE)
        arcade.draw_rectangle_filled(200, 150, 25, 125, arcade.color.AZURE)
        arcade.draw_rectangle_filled(525, 450, 125, 25, arcade.color.AZURE)
        arcade.draw_rectangle_filled(575, 400, 25, 125, arcade.color.AZURE)
        arcade.draw_rectangle_filled(525, 100, 125, 25, arcade.color.AZURE)
        arcade.draw_rectangle_filled(575, 150, 25, 125, arcade.color.AZURE)
        self.text_sprite.draw()
        self.button_1.draw()
        self.button_2.draw()
        self.button_3.draw()
        self.button_4.draw()
        self.player.draw()
        if self.puzzle.checker() is Puzzle.solution:
            self.director.next_view()


    def update(self, delta_time):
        self.player.update()


    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_RIGHT:
            print(self.puzzle.give_puzzle())
        elif button == arcade.MOUSE_BUTTON_LEFT:
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

            elif (self.player.left  >= 0 and self.player.right <= 120) and (self.player.bottom >= 505) and self.puzzle.value_checker(self.puzzle.clone_puzzle(), 1) is False:
                self.button_on(1)
                self.puzzle.add_value(1)
                
            elif (self.player.left  >= 0 and self.player.right <= 120) and (self.player.bottom >= 505) and self.puzzle.value_checker(self.puzzle.clone_puzzle(), 1):
                self.button_off(1)
                self.puzzle.remove_value(1)
                
            elif (self.player.left  >= 0 and self.player.right <= 120) and (self.player.bottom <= 150) and self.puzzle.value_checker(self.puzzle.clone_puzzle(), 2) is False:
                self.button_on(2)
                self.puzzle.add_value(2)
                
            elif (self.player.left  >= 0 and self.player.right <= 120) and (self.player.bottom <= 150) and self.puzzle.value_checker(self.puzzle.clone_puzzle(), 2):
                self.button_off(2)
                self.puzzle.remove_value(2)
                
            elif (self.player.left  >= 680) and (self.player.bottom >= 505) and self.puzzle.value_checker(self.puzzle.clone_puzzle(), 3) is False:
                self.button_on(3)
                self.puzzle.add_value(3)

            elif (self.player.left  >= 680) and (self.player.bottom >= 505) and self.puzzle.value_checker(self.puzzle.clone_puzzle(), 3):
                self.button_off(3)
                self.puzzle.remove_value(3)
                
            elif (self.player.left  >= 680) and (self.player.bottom <= 150) and self.puzzle.value_checker(self.puzzle.clone_puzzle(), 4) is False:
                self.button_on(4)
                self.puzzle.add_value(4)
        
            elif (self.player.left  >= 680) and (self.player.bottom <= 150) and self.puzzle.value_checker(self.puzzle.clone_puzzle(), 4):
                self.button_off(4)
                self.puzzle.remove_value(4)
                

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
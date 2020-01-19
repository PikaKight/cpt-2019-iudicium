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

        #boundary of wall left up
        if self.right > 185 and self.left < 180 and self.top > 338 and self.bottom < 464:
            self.right = 184
        if self.left < 212 and self.left > 190 and self.bottom < 435 and self.top > 338:
            self.left = 212
        if self.right > 185 and self.left < 312 and self.bottom < 464 and self.top > 460:
            self.bottom = 464
        if self.top > 435 and self.top < 450 and self.left >= 212 and self.left < 311:
            self.top = 435
        if self.top > 336 and self.bottom < 350 and self.left < 211 and self.right > 185:
            self.top = 336
        if self.left < 312 and self.right > 290 and self.bottom < 464 and self.top > 436: 
            self.left = 312

        #boundary of wall right up
        if self.right > 590 and self.left < 586 and self.top > 338 and self.bottom < 464:
            self.left = 586
        if self.right < 560 and self.right > 570 and self.bottom < 435 and self.top > 338:
            self.right = 560
        if self.right > 462 and self.left < 586 and self.bottom < 464 and self.top > 460:
            self.bottom = 464
        if self.top > 435 and self.top < 450 and self.right >= 560 and self.right < 462:
            self.top = 435
        if self.top > 336 and self.bottom < 350 and self.left < 586 and self.right > 560:
            self.top = 336
        if self.left < 440 and self.right > 462 and self.bottom < 464 and self.top > 436: 
            self.right = 462

        #boundary of wall left down  
        if self.right > 185 and self.left < 180 and self.top > 88 and self.bottom < 213:
            self.right = 184
        if self.left < 212 and self.right > 200 and self.bottom > 112 and self.top < 213:
            self.left = 212
        if self.right > 185 and self.left < 312 and self.bottom < 21 and self.top > 88:
            self.top = 88
        if self.bottom < 112 and self.top > 170 and self.left >= 212 and self.left < 311:
            self.bottom = 112
        if self.top > 336 and self.bottom < 213 and self.left < 211 and self.right > 185:
            self.bottom = 213
        if self.left < 312 and self.right > 290 and self.bottom < 464 and self.top > 436: 
            self.left = 312

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

class ch3_MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("Sprites/whiteBorders_blackBackground.jpg")

    def on_show(self):
        pass
    
    def on_draw(self):
        arcade.start_render()

        arcade.draw_texture_rectangle(settings.WIDTH/2, settings.HEIGHT/2,
                                    settings.WIDTH, settings.HEIGHT, self.background)

        arcade.draw_text("Chapter 3", settings.WIDTH/2, settings.HEIGHT/2 + 50, arcade.color.WHITE,
                        font_size=45, bold=True, anchor_x="center")
        arcade.draw_text("Press ENTER to proceed to Game", settings.WIDTH/2, settings.HEIGHT/2,
                        arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Press ESC to Exit Game", settings.WIDTH/2, settings.HEIGHT/2 - 50,
                        arcade.color.WHITE, font_size=20, anchor_x="center")
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            instructions_View = Instructions()
            self.window.show_view(instructions_View)
        elif key == arcade.key.ESCAPE:
            arcade.close_window()
            self.director.next_view()

class Instructions(arcade.View):
    def __init__(self):
        super().__init__()

        self.background = arcade.load_texture("Sprites/blackBackground.jpg")

        self.button = arcade.Sprite("Sprites\switchGreen.png", 0.6)
        self.button.center_x = settings.WIDTH/2 - 70
        self.button.center_y = 200
        self.button_pressed = arcade.Sprite("Sprites\switchGreen_pressed.png", 0.6)
        self.button_pressed.center_x = settings.WIDTH/2 + 70
        self.button_pressed.center_y = 190
    
    def on_show(self):
        arcade.set_background_color(arcade.color.GHOST_WHITE)
    
    def on_draw(self):
        arcade.start_render()

        arcade.draw_texture_rectangle(settings.WIDTH/2, settings.HEIGHT/2,
                                        settings.WIDTH, settings.HEIGHT, self.background)
        arcade.draw_text("INSTRUCTIONS", settings.WIDTH/2, settings.HEIGHT/2 + 150, arcade.color.WHITE,
                        font_size=30, bold=True, anchor_x="center", anchor_y="center")
        arcade.draw_text("""    Use W A S D keys to move around. 
    Space to turn the buttons on and off.

    Press the buttons in 

    """,
                        settings.WIDTH/2, settings.HEIGHT/2 + 40, arcade.color.WHITE,
                        font_size=15, anchor_x="center", anchor_y="center")
        
        self.button.draw()
        self.button_pressed.draw()
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            ch3View = Ch3View()
            self.window.show_view(ch3View)
        elif key == arcade.key.ESCAPE:
            arcade.close_window()
            self.director.next_view()
        
class Ch3View(arcade.View):
    def __init__(self):
        super().__init__()
        self.puzzle = Puzzle()
        self.half_width = settings.WIDTH * .5
        self.half_height = settings.HEIGHT * .5
        self.player = Player("Sprites/alienBlue_front.png", .4, 0, 0, 0, 0, 400, 300)
        self.text_sprite = arcade.Sprite("Sprites\Brown.png", .5, 0 ,0, 0, 0, 400, 590)
        self.background = arcade.load_texture("Sprites/brown-stone-seamless-background-vector-illustration-game-texture-68967465.jpg")


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
        arcade.draw_rectangle_filled(250, 450, 125, 25, arcade.color.BRASS)
        arcade.draw_rectangle_filled(200, 400, 25, 125, arcade.color.BRASS)
        arcade.draw_rectangle_filled(250, 100, 125, 25, arcade.color.BRASS)
        arcade.draw_rectangle_filled(200, 150, 25, 125, arcade.color.BRASS)
        arcade.draw_rectangle_filled(525, 450, 125, 25, arcade.color.BRASS)
        arcade.draw_rectangle_filled(575, 400, 25, 125, arcade.color.BRASS)
        arcade.draw_rectangle_filled(525, 100, 125, 25, arcade.color.BRASS)
        arcade.draw_rectangle_filled(575, 150, 25, 125, arcade.color.BRASS)
        self.text_sprite.draw()
        self.button_1.draw()
        self.button_2.draw()
        self.button_3.draw()
        self.button_4.draw()
        self.player.draw()

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
                pass

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
    my_view = ch3_MenuView()
    # my_view = Ch3View()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()
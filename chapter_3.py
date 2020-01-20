import arcade

import settings

import random

import json

from typing import List

# the player's speed
speed = 10


class Player(arcade.Sprite):
    """ Inherits from arcade.Sprite to create the player sprite and it's movements
    """
    def __init__(
        self, filename=None, scale=1, image_x=0, image_y=0, image_width=0,
        image_height=0, center_x=0, center_y=0, repeat_count_x=1,
            repeat_count_y=1):
                    super().__init__(
                            filename=filename, scale=scale, image_x=image_x,
                            image_y=image_y, image_width=image_width,
                            image_height=image_height, center_x=center_x,
                            center_y=center_y, repeat_count_x=repeat_count_x,
                            repeat_count_y=repeat_count_y)

    def update(self):
        """ Updates the player sprite when user presses the appropriate keys
        """
        self.center_x += self.change_x
        self.center_y += self.change_y

        # boundary for the sides of the screen
        if self.left < 0:
            self.left = 0
        if self.right > settings.WIDTH:
            self.right = settings.WIDTH

        # boundary for the top and bottom of the screen
        if self.bottom < 0:
            self.bottom = 3
        if self.top > settings.HEIGHT:
            self.top = settings.HEIGHT

        # boundary of wall left up
        if (self.right > 185 and self.left < 180 and self.top > 338 and
            self.bottom < 464):
            self.right = 184
        if (self.left < 212 and self.left > 190 and self.bottom < 435 and
            self.top > 338):
            self.left = 212
        if (self.right > 185 and self.left < 312 and self.bottom < 464 and
            self.top > 460):
            self.bottom = 464
        if (self.top > 435 and self.top < 450 and self.left >= 212 and
            self.left < 311):
            self.top = 435
        if (self.top > 336 and self.bottom < 350 and self.left < 211 and
            self.right > 185):
            self.top = 336
        if (self.left < 312 and self.right > 290 and self.bottom < 464 and
            self.top > 436):
            self.left = 312

        # boundary of wall right up
        if (self.right > 590 and self.left < 586 and self.top > 338 and
            self.bottom < 464):
            self.left = 586
        if (self.right > 560 and self.right < 582 and self.bottom < 435 and
            self.top > 338):
            self.right = 560
        if (self.right > 462 and self.left < 586 and self.bottom < 464 and
            self.top > 460):
            self.bottom = 464
        if (self.top > 435 and self.top < 450 and self.right <= 560 and
            self.right > 462):
            self.top = 435
        if (self.top > 336 and self.bottom < 350 and self.left < 586 and
            self.right > 561):
            self.top = 336
        if (self.left < 440 and self.right > 462 and self.bottom < 464 and
            self.top > 436):
            self.right = 462

        # boundary of wall left down
        if (self.right > 185 and self.left < 180 and self.top > 88 and
            self.bottom < 213):
            self.right = 184
        if (self.left < 212 and self.right > 200 and self.top > 111 and
            self.bottom < 213):
            self.left = 212
        if (self.right > 185 and self.left < 312 and self.bottom < 21 and
            self.top > 88):
            self.top = 88
        if (self.bottom < 111 and self.bottom > 100 and self.left >= 212 and
            self.left < 311):
            self.bottom = 112
        if (self.top > 336 and self.bottom < 213 and self.left < 211 and
            self.right > 185):
            self.bottom = 213
        if (self.left < 312 and self.right > 290 and self.top > 88 and
            self.bottom < 111):
            self.left = 312

        # boundary of wall lef right down
        if (self.right > 590 and self.left < 586 and self.top > 88 and
            self.bottom < 213):
            self.left = 586
        if (self.right > 560 and self.right < 582 and self.top > 111 and
            self.bottom < 213):
            self.right = 560
        if (self.right > 462 and self.left < 586 and self.bottom < 21 and
            self.top > 88):
            self.top = 88
        if (self.bottom < 111 and self.bottom > 100 and self.right <= 560 and
            self.right > 462):
            self.bottom = 112
        if (self.top > 336 and self.bottom < 213 and self.left < 586 and
            self.right > 561):
            self.bottom = 213
        if (self.left < 440 and self.right > 462 and self.top > 88 and
            self.bottom < 111):
            self.right = 462


class Puzzle:
    """ Controls the puzzle for this game.
    """

    solution = [1, 4, 2, 3]  # Solution for this chapter

    def __init__(self):

        self._puzzle = []  # Records the button press order

    def clone_puzzle(self) -> List[int]:
        """ creates a clone of self._puzzle so it does not
        affect  the recorded button press.
        """
        self.clone = self._puzzle
        return self.clone

    def add_value(self, value: int) -> List[int]:
        """ adds the button value that was pressed
        Arg:
            value is the order number for the buttons
        """
        self._puzzle.append(value)

    def remove_value(self, value: int) -> List[int]:
        """ removes the button value that was unpressed
        Arg:
            value is the order number for the buttons
        """
        for i, num in enumerate(self._puzzle):
            if num is value:
                return self._puzzle.pop(i)

    def give_puzzle(self) -> List[int]:
        """ gives the list that is self._puzzle
        return:
            self._puzzle
        """
        return self._puzzle

    def value_checker(self, puzzle: List[int], value: int) -> bool:
        """ Checks whether or not a button is pressed
        and their order number is recorded
        Arg:
            puzzle: the list that contains the order of the buttons
            that are currently pressed
            value: the button that is being checked
        """
        if len(puzzle) == 0:
            return False

        if len(puzzle) == 1:
            if puzzle[0] is value:
                return True
            else:
                return False

        mid = len(puzzle) // 2
        left = self.value_checker(puzzle[:mid], value)
        right = self.value_checker(puzzle[mid:], value)

        return left or right

    def checker(self) -> bool:
        """ Checks if the puzzle is solved
        and the buttons are all pressed in the right order
        """
        if self._puzzle == Puzzle.solution:
            return True


class ch3_MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("Sprites/abstract-technology-particle-background_52683-25766.jpg")

    def on_show(self):
        pass

    def on_draw(self):
        arcade.start_render()

        arcade.draw_texture_rectangle(settings.WIDTH/2, settings.HEIGHT/2,
                                      settings.WIDTH, settings.HEIGHT,
                                      self.background)

        arcade.draw_text("Chapter 3", settings.WIDTH/2, settings.HEIGHT/2 + 50,
                         arcade.color.WHITE, font_size=45, bold=True,
                         anchor_x="center")

        arcade.draw_text("Press ENTER to proceed to Game", settings.WIDTH/2,
                         settings.HEIGHT/2, arcade.color.WHITE,
                         font_size=20, anchor_x="center")

        arcade.draw_text("Press ESC to Exit Game", settings.WIDTH/2,
                         settings.HEIGHT/2 - 50, arcade.color.WHITE,
                         font_size=20, anchor_x="center")

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

        self.background = arcade.load_texture("Sprites/abstract-technology-particle-background_52683-25766.jpg")

        self.button = arcade.Sprite("Sprites\switchGreen.png", 0.6)
        self.button.center_x = settings.WIDTH/2 - 70
        self.button.center_y = 200

        self.button_pressed = arcade.Sprite("Sprites\switchGreen_pressed.png", 0.6)
        self.button_pressed.center_x = settings.WIDTH/2 + 70
        self.button_pressed.center_y = 200

        self.star = arcade.Sprite("Sprites\star.png", 1)
        self.star.center_x = settings.WIDTH/2 - 100
        self.star.center_y = settings.HEIGHT / 2

    def on_show(self):
        arcade.set_background_color(arcade.color.GHOST_WHITE)

    def on_draw(self):
        arcade.start_render()

        arcade.draw_texture_rectangle(settings.WIDTH/2, settings.HEIGHT/2,
                                      settings.WIDTH, settings.HEIGHT,
                                      self.background)

        arcade.draw_text("INSTRUCTIONS", settings.WIDTH/2,
                         settings.HEIGHT - 100, arcade.color.WHITE,
                         font_size=30, bold=True, anchor_x="center",
                         anchor_y="center")

        arcade.draw_text("""

        W: UP
        S: DOWN
        A: LEFT
        D: RIGHT
                        """, 0, settings.HEIGHT/2, arcade.color.WHITE,
                         font_size=30, bold=True)

        arcade.draw_text("""

    Press the buttons in a certain order to unlock the next chapter.

    For the riddle move up towards the brown sign and press space.

    Press ENTER to Continue
    """,
                         settings.WIDTH/2 + 100, settings.HEIGHT/2 + 100,
                         arcade.color.WHITE, font_size=15,
                         anchor_x="center", anchor_y="center")

        arcade.draw_text("""
                            Stars are worth 1 pt and will spawn
                            when the first correct button is pressed
                        """, settings.WIDTH/2 + 100, settings.HEIGHT/2,
                         arcade.color.WHITE, font_size=20, anchor_x="center",
                         anchor_y="center")

        self.button.draw()
        self.button_pressed.draw()
        self.star.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            ch3 = Ch3View()
            self.window.show_view(ch3)
        elif key == arcade.key.ESCAPE:
            arcade.close_window()
            self.director.next_view()


class Riddle(arcade.Sprite):
    def __init__(self, filename=None, scale=1, image_x=0, image_y=0,
                 image_width=0, image_height=0, center_x=0, center_y=0,
                 repeat_count_x=1, repeat_count_y=1):
        super().__init__(filename=filename, scale=scale, image_x=image_x,
                         image_y=image_y, image_width=image_width,
                         image_height=image_height, center_x=center_x,
                         center_y=center_y, repeat_count_x=repeat_count_x,
                         repeat_count_y=repeat_count_y)

    def on_draw(self):
        arcade.start_render()
        super().draw()
        arcade.draw_text("INSTRUCTIONS", settings.WIDTH/2,
                         settings.HEIGHT - 100, arcade.color.WHITE,
                         font_size=30, bold=True)

    def update(self, delta_time):
        self.update()


class Ch3View(arcade.View):
    def __init__(self):
        super().__init__()
        self.total_time = 0.0
        self.puzzle = Puzzle()
        self.half_width = settings.WIDTH * .5
        self.half_height = settings.HEIGHT * .5
        self.player = Player("Sprites/alienBlue_front.png", .4, 0, 0, 0, 0, 400, 300)
        self.text_sprite = arcade.Sprite("Sprites\Brown.png", 0.5, 0, 0, 0, 0, 400, 590)
        self.background = arcade.load_texture("Sprites/brown-stone-seamless-background-vector-illustration-game-texture-68967465.jpg")
        self.riddle = Riddle("Sprites\DialogueBox.png", 1, 0, 0, 0, 0,
                             settings.WIDTH / 2, settings.HEIGHT / 2 - 100)
        self.star_sprites = arcade.SpriteList()
        self.x = 0  # Controls whether or not the riddle is shown
        self.star_1 = 0  # Controls whether or not the star sprites spawns
        self.star_2 = 0   # Controls whether or not the star sprites spawns
        self.star_3 = 0   # Controls whether or not the star sprites spawns
        self.score = 0

    def button_on(self, value: int):
        """ creates the different on button sprites for the give value

        Arg:
            value is the number that is given when the button is pressed by the
            user using the space key on the button.

        Return:
            The on button sprite for the given value
        """
        if value is 1:
            self.button_1 = arcade.Sprite(settings.button_pressed, .7, 0, 0, 0,
                                          0, 50, 570)
        elif value is 2:
            self.button_2 = arcade.Sprite(settings.button_pressed, .7, 0, 0, 0,
                                          0, 50, 75)
        elif value is 3:
            self.button_3 = arcade.Sprite(settings.button_pressed, .7, 0, 0, 0,
                                          0, 750, 570)
        elif value is 4:
            self.button_4 = arcade.Sprite(settings.button_pressed, .7, 0, 0, 0,
                                          0, 750, 75)

    def button_off(self, value: int):
        """ creates the different off button sprites for the give value

        Arg:
            value is the number that is given when the button is pressed by the
            user using the space key on the button.
        Return:
            The off button sprite for the given value
        """
        if value is 1:
            self.button_1 = arcade.Sprite(settings.button, .7, 0, 0, 0, 0, 50,
                                          570)
        elif value is 2:
            self.button_2 = arcade.Sprite(settings.button, .7, 0, 0, 0, 0, 50,
                                          75)
        elif value is 3:
            self.button_3 = arcade.Sprite(settings.button, .7, 0, 0, 0, 0, 750,
                                          570)
        elif value is 4:
            self.button_4 = arcade.Sprite(settings.button, .7, 0, 0, 0, 0, 750,
                                          75)

    def star_sprite(self):
        """ Creates a Sprite list of the star sprite when called
        """
        for _ in range(5):
            star = arcade.Sprite("Sprites\star.png", .8)
            star.center_x = random.randrange(0, settings.WIDTH)
            star.center_y = random.randrange(0, settings.HEIGHT)
            self.star_sprites.append(star)

    def on_show(self):
        self.button_off(1)
        self.button_off(2)
        self.button_off(3)
        self.button_off(4)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(self.half_width, self.half_height,
                                      settings.WIDTH, settings.HEIGHT,
                                      self.background)

        # Creates walls for the map
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
        self.star_sprites.draw()
        if self.x % 2 == 1:
            self.riddle.draw()
            arcade.draw_text("""
            The corner walls will lead your way.
            Read it like a book and you should see.
            To the second, tan inverses (800/600).
            Then across you're below the start,
            Head N 37 degres E.
            The path will open once you succeed!""", self.half_width - 350,
                             self.half_height - 200,  arcade.color.WHITE,
                             20, 600, "center", "arial", True)

        # Calculate minutes
        minutes = int(self.total_time) // 60

        # Calculate seconds by using a modulus (remainder)
        seconds = int(self.total_time) % 60

        # Figure out our output
        output = f"Time: {minutes:02d}:{seconds:02d}"

        # Output the timer text.
        arcade.draw_text(output, 270, 565, arcade.color.BLACK, 30, 250,
                         "center", "arial")

    def update(self, delta_time):
        self.player.update()

        self.total_time += delta_time

        for star in self.star_sprites:
            player_in_contact = star.collides_with_sprite(self.player)
            if player_in_contact:
                star.kill()
                self.score += 1

        if self.puzzle.checker() is True:
            with open("Chapter_3_score.json", 'r') as f:
                game = json.load(f)
            # Calculate minutes
            minutes = int(self.total_time) // 60

            # Calculate seconds by using a modulus (remainder)
            seconds = int(self.total_time) % 60

            # Figure out our output
            output = f"{minutes:02d}:{seconds:02d}"

            game[output] = self.score

            with open("Chapter_3_score.json", 'w') as f:
                json.dump(game, f)

            winView = WinView()
            self.window.show_view(winView)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player.change_y = speed

        elif key == arcade.key.S:
            self.player.change_y = -speed

        elif key == arcade.key.A:
            self.player.change_x = -speed

        elif key == arcade.key.D:
            self.player.change_x = speed

        elif key == arcade.key.SPACE:

            if ((self.player.center_x >= 290 and self.player.center_x <= 515) and
                (self.player.top >= 555)):
                self.x += 1

            elif ((self.player.left >= 0 and self.player.right <= 120) and
                  (self.player.bottom >= 505) and
                  self.puzzle.value_checker(self.puzzle.clone_puzzle(), 1) is False):
                self.button_on(1)
                self.star_1 += 1
                if self.star_1 == 1:
                    self.star_sprite()
                self.puzzle.add_value(1)

            elif ((self.player.left >= 0 and self.player.right <= 120) and
                  (self.player.bottom >= 505) and
                  self.puzzle.value_checker(self.puzzle.clone_puzzle(), 1)):
                self.button_off(1)
                self.puzzle.remove_value(1)

            elif ((self.player.left >= 0 and self.player.right <= 120) and
                  (self.player.bottom <= 150) and
                  self.puzzle.value_checker(self.puzzle.clone_puzzle(), 2) is False):
                self.button_on(2)
                self.star_2 += 1
                if self.star_2 == 1:
                    self.star_sprite()
                self.puzzle.add_value(2)

            elif ((self.player.left >= 0 and self.player.right <= 120) and
                  (self.player.bottom <= 150) and
                  self.puzzle.value_checker(self.puzzle.clone_puzzle(), 2)):
                self.button_off(2)
                self.puzzle.remove_value(2)

            elif ((self.player.left >= 680) and (self.player.bottom >= 505) and
                  self.puzzle.value_checker(self.puzzle.clone_puzzle(), 3) is False):
                self.button_on(3)
                self.puzzle.add_value(3)

            elif ((self.player.left >= 680) and (self.player.bottom >= 505) and
                  self.puzzle.value_checker(self.puzzle.clone_puzzle(), 3)):
                self.button_off(3)
                self.puzzle.remove_value(3)

            elif ((self.player.left >= 680) and (self.player.bottom <= 150) and
                  self.puzzle.value_checker(self.puzzle.clone_puzzle(), 4) is False):
                self.button_on(4)
                self.star_3 += 1
                if self.star_3 == 1:
                    self.star_sprite()
                self.puzzle.add_value(4)

            elif ((self.player.left >= 680) and (self.player.bottom <= 150) and
                  self.puzzle.value_checker(self.puzzle.clone_puzzle(), 4)):
                self.button_off(4)
                self.puzzle.remove_value(4)

    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """
        if key == arcade.key.A or key == arcade.key.D:
            self.player.change_x = 0

        elif key == arcade.key.W or key == arcade.key.S:
            self.player.change_y = 0


class WinView(arcade.View):
    def __init__(self):
        super().__init__()
        self.half_width = settings.WIDTH / 2
        self.half_height = settings.HEIGHT/2
        self.background = arcade.load_texture("Sprites/fancy_silhouette.png")

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(self.half_width, self.half_height,
                                      settings.WIDTH, settings.HEIGHT,
                                      self.background)

        with open("Chapter_3_score.json", 'r') as f:
            game = json.load(f)

        for key, value in game.items():
            time = key
        arcade.draw_text(f"""
                    You've Complete Chapter 3!

                            Total Time: {key}

                            Total Star Count: {game[key]}
                        """, settings.WIDTH/2 - 125, settings.HEIGHT/2 - 50,
                         arcade.color.BLACK, font_size=35, anchor_x="center")

        arcade.draw_text("""
                            Press ENTER to see Scoreboard

                           Press ESC to go to Chapter 4
                         """, settings.WIDTH/2 - 125, settings.HEIGHT/2 - 250,
                         arcade.color.BLACK, font_size=35, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            scoreboard_View = Scoreboard()
            self.window.show_view(scoreboard_View)

        elif key == arcade.key.ESCAPE:
            self.director.next_view()


class Scoreboard(arcade.View):
    def __init__(self):
        super().__init__()
        self.half_height = settings.HEIGHT / 2
        self.half_width = settings.WIDTH / 2
        self.scoreboard = arcade.Sprite("Sprites/Menu.png", 0.8, 0, 0, 0, 0,
                                        settings.WIDTH/2, settings.HEIGHT/2)
        self.background = arcade.load_texture("Sprites/fancy_silhouette.png")

        with open("Chapter_3_score.json", 'r') as f:
            self.game = json.load(f)

        keys = []

        # Turns the time into decimal time and adds it to the list keys
        for key, value in self.game.items():
            (m, s) = key.split(':')
            result = int(m) * 60 + int(s)
            keys.append(result)

        self.new_keys = self.sort_scores(keys)
        self.new_game = {}

        # Turns the decimal time back to time
        # and adds it back to Chapter_3_scores.json
        for j in self.new_keys:
            m, s = divmod(j, 60)
            time = f"{m:02d}:{s:02d}"
            self.new_game[time] = self.game[time]

        with open("Chapter_3_score.json", 'w') as f:
            json.dump(self.new_game, f)

    def sort_scores(self, data: List[int]) -> List[int]:
        """ Quick sorts the keys of Chapter_3_scores.json
        Arg:
            data: List of keys as integers
        """
        # Base Case
        if len(data) < 2:
            return data

        pivot = data[0]
        l = self.sort_scores([x for x in data[1:] if x < pivot])
        u = self.sort_scores([x for x in data[1:] if x >= pivot])
        return l + [pivot] + u

    def on_draw(self):
        with open("Chapter_3_score.json", 'r') as f:
            game = json.load(f)

        arcade.start_render()

        arcade.draw_texture_rectangle(self.half_width, self.half_height,
                                      settings.WIDTH, settings.HEIGHT,
                                      self.background)

        self.scoreboard.draw()

        arcade.draw_text("Scoreboard", self.scoreboard.center_x,
                         self.scoreboard.center_y + 260, arcade.color.BLACK,
                         font_size=30, bold=True, anchor_x="center",
                         anchor_y="center")

        arcade.draw_text("    Top 5 Players:", self.scoreboard.center_x,
                         self.scoreboard.center_y + 190, arcade.color.BLACK,
                         font_size=15, anchor_x="center", anchor_y="center")

        placement = 1
        h = 150  # Controls the Height of the text
        # Checks if there are more than five scores in the json file
            # loops through the dictionary for the first 5 scores
            # and places it on the screen
        while placement < 5:
            for key, value in game.items():
                arcade.draw_text(f"{placement}. Time: {key}, Star Score: {game[key]}",
                                -100, self.half_height + h,
                                arcade.color.BLACK, 15, 1000, "center",
                                'arial', True)
                placement += 1
                h -= 50  # Change in Height

        arcade.draw_text("Press ENTER to CONTINUE", self.scoreboard.center_x,
                         self.scoreboard.center_y - 220,
                         arcade.color.BLACK, font_size=15, anchor_x="center",
                         anchor_y="center")

    def update(self, delta_time):
        pass

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
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
    # my_view = ch3_MenuView()
    # my_view = Instructions()
    # my_view = Ch3View()
    # my_view = WinView()
    my_view = Scoreboard()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()

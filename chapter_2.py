import arcade
import settings
import json
from typing import List

Left_ViewPoint_Margin = 150
Right_ViewPoint_Margin = 150
Bottom_ViewPoint_Margin = 50
Top_ViewPoint_Margin = 400
Gravity = 0.5


def linear_search(target: int, numbers: List[int]) -> int:
    """Search for a target value.

    Args:
        target: The int to search for.
        numbers: List of numbers.
    Returns:
        Index location of the found target number. -1 if not found.
    """
    for i, num in enumerate(numbers):
        if num == target:
            return i
    return -1


def merge_sort(numbers: List[int]) -> List[int]:
    if len(numbers) == 1:
        return numbers

    mid = len(numbers) // 2
    left = merge_sort(numbers[:mid])
    right = merge_sort(numbers[mid:])

    left_pointer = 0
    right_pointer = 0
    sorted_list = []
    while left_pointer < len(left) and right_pointer < len(right):
        if left[left_pointer] < right[right_pointer]:
            sorted_list.append(left[left_pointer])
            left_pointer += 1
        else:
            sorted_list.append(right[right_pointer])
            right_pointer += 1

    while left_pointer < len(left):
        sorted_list.append(left[left_pointer])
        left_pointer += 1
    while right_pointer < len(right):
        sorted_list.append(right[right_pointer])
        right_pointer += 1
    return sorted_list


class Player(arcade.Sprite):
    bag = []

    # Create a direction not when the player hit a button
    @classmethod
    def create_direction(cls, button_hit_time: int, center_x: float, center_y: float):
        if button_hit_time == 1:
            return arcade.draw_text("Go Down", center_x - 30, center_y + 70,
                                    arcade.csscolor.RED, 15)
        if button_hit_time == 2:
            return arcade.draw_text("Go Right", center_x - 30, center_y + 70,
                                    arcade.csscolor.RED, 15)
        if button_hit_time == 3:
            return arcade.draw_text("Go Left", center_x - 30, center_y + 70,
                                    arcade.csscolor.RED, 15)
        if button_hit_time == 4:
            return arcade.draw_text("Go Down", center_x - 30, center_y + 70,
                                    arcade.csscolor.RED)

    def __init__(self, filename=None, scale=0.3, center_x=760, center_y=128):
        super().__init__(filename=filename, scale=scale, center_x=center_x, center_y=center_y)
        self._Player_move_speed = 3
        self._Player_jump_speed = 3
        self._view_bottom = 0
        self._view_left = 0
        self._charge_power = 0
        self._coins = 0

        self.open_door = False

    def get_player_move_speed(self):
        return self._Player_move_speed

    def set_player_move_speed(self, value):
        self._Player_move_speed = value

    def get_player_jump_speed(self):
        return self._Player_jump_speed

    def set_player_jump_speed(self, value):
        if value > 15:
            value = 15
        self._Player_jump_speed = value

    def get_view_bottom(self):
        return self._view_bottom

    def set_view_bottom(self, value):
        self._view_bottom = value

    def get_view_left(self):
        return self._view_left

    def set_view_left(self, value):
        self._view_left = value

    def get_coins(self):
        return self._coins

    def set_coins(self, value):
        self._coins = value

    def get_charge_power(self):
        return self._charge_power

    def set_charge_power(self, value):
        self._charge_power = value

    def update(self):

        # Create the view change when player moves
        changed = False

        left_boundary = self.get_view_left() + Left_ViewPoint_Margin
        if self.left < left_boundary:
            self._view_left -= left_boundary - self.left
            changed = True

        # Scroll right
        right_boundary = self.get_view_left() + settings.WIDTH - Right_ViewPoint_Margin
        if self.right > right_boundary:
            self._view_left += self.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.get_view_bottom() + settings.HEIGHT - Top_ViewPoint_Margin
        if self.top > top_boundary:
            self._view_bottom += self.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.get_view_bottom() + Bottom_ViewPoint_Margin
        if self.bottom < bottom_boundary:
            self._view_bottom -= bottom_boundary - self.bottom
            changed = True

        if changed:
            self.set_view_bottom(int(self.get_view_bottom()))
            self.set_view_left(int(self.get_view_left()))

            # Do the scrolling
            arcade.set_viewport(self.get_view_left(),
                                settings.WIDTH + self.get_view_left(),
                                self.get_view_bottom(),
                                settings.HEIGHT + self.get_view_bottom())

    def check_bag(self):
        """
        Check if the player have 10 Coins. If so, he can open the door, else he can't
        :return: if the player can open the door(bool)
        """
        if len(Player.bag) is 10:
            self.open_door = True

    def calculate_jumpspeed(self, presstime, releasetime, Player_jump_speed):
        """
        calculate the jump speed of the player based on the time they press space. Using recursion.
        :param presstime: the time when player press space(int)
        :param releasetime: the time when player release space(int)
        :param Player_jump_speed: the player's original jump speed(int)
        :return: the new jump speed of the player(int)
        """
        if releasetime - presstime <= 0:
            return Player_jump_speed
        else:
            Player_jump_speed += 1
            return self.calculate_jumpspeed(presstime, releasetime - 0.1, Player_jump_speed)

    def display_score(self, scores):
        """
        write the score to the score file and using merge sort the sort the score
        :param scores: the score(time) player did in the run(int)
        """
        with open("chapter_2_scores.json", 'r') as json_file:
            data = json.load(json_file)
            data.append(round(scores, 2))
            data = merge_sort(data)
            if len(data) > 20:
                data.pop()
        with open("chapter_2_scores.json", 'w') as outfile:
            json.dump(data, outfile)


class Chapter2View(arcade.View):

    def __init__(self):
        super().__init__()
        self._Total_time = 0
        self._space_press_time = 0
        self._button_hit_time = 0
        self._button_press_time = 0
        self.score_data = None

        self.up_pressed = False
        self.right_pressed = False
        self.left_pressed = False
        self.end_screen = False

        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.door_list = arcade.SpriteList()
        self.button_list = arcade.SpriteList()

        # Read the tmx file and display the map
        chapter2map = arcade.tilemap.read_tmx("maps/Ch2Map.tmx")
        self.player = Player("Sprites/alienBlue_front.png")
        self.wall_list = arcade.tilemap.process_layer(chapter2map, "Platform_layer", 0.5)
        self.coin_list = arcade.tilemap.process_layer(chapter2map, "Coin_layer", 0.5)
        self.door_list = arcade.tilemap.process_layer(chapter2map, "Door_layer", 0.5)
        self.button_list = arcade.tilemap.process_layer(chapter2map, "Button_layer", 0.5)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.wall_list, Gravity)
        self.score_format = "." * 15
        self.information_text = "Welcome to Jump Game!\nPress Right/Left key to move\n" \
                                "Press Space to jump, the longer you press, the higher you jump\n" \
                                "Collect all the coins and press 'E' in front of the terminal door\n" \
                                "The orange button will give you direction support. Good Luck!"

    def get_total_time(self):
        return self._Total_time

    def set_total_time(self, value):
        self._Total_time = value

    def get_space_press_time(self):
        return self._space_press_time

    def set_space_press_time(self, value):
        self._space_press_time = value

    def get_button_hit_time(self):
        return self._button_hit_time

    def set_button_hit_time(self, value):
        self._button_hit_time = value

    def get_button_press_time(self):
        return self._button_press_time

    def set_button_press_time(self, value):
        self._button_press_time = value

    def on_show(self):
        arcade.set_background_color(arcade.color.BLUE_SAPPHIRE)

    def on_draw(self):
        arcade.start_render()
        self.wall_list.draw()
        self.coin_list.draw()
        self.door_list.draw()
        self.button_list.draw()
        self.player.draw()

        # The number of coins
        coin_text = f"Coins: {self.player.get_coins()}/10"
        arcade.draw_text(coin_text, self.player.center_x, self.player.center_y + 25, arcade.csscolor.BLACK, 12)

        # The charge power rectangle
        arcade.draw_rectangle_outline(self.player.center_x, self.player.center_y - 50, 20, 70, arcade.color.BLACK, 3,
                                      90)
        arcade.draw_rectangle_filled(self.player.center_x, self.player.center_y - 50, 20, self.player.get_charge_power(),
                                     arcade.color.RED, 90)

        # The end screen
        if self.end_screen is True:
            with open("chapter_2_scores.json", "r") as json_file:
                self.score_data = json.load(json_file)
            arcade.draw_rectangle_filled(self.player.center_x - 200, self.player.center_y + 210, 600, 300,
                                         arcade.color.WHITE)

            if round(self.get_total_time(), 2) == self.score_data[0]:
                arcade.draw_text(f"1 {self.score_format} {self.score_data[0]} SEC", self.player.center_x - 350,
                                 self.player.center_y + 290, arcade.csscolor.RED, 30)
            else:
                arcade.draw_text(f"1 {self.score_format} {self.score_data[0]} SEC", self.player.center_x - 350,
                                 self.player.center_y + 290, arcade.csscolor.BLACK, 30)

            try:
                if round(self.get_total_time(), 2) == self.score_data[1]:
                    arcade.draw_text(f"2 {self.score_format} {self.score_data[1]} SEC", self.player.center_x - 350,
                                     self.player.center_y + 240, arcade.csscolor.RED, 30)
                else:
                    arcade.draw_text(f"2 {self.score_format} {self.score_data[1]} SEC", self.player.center_x - 350,
                                     self.player.center_y + 240, arcade.csscolor.BLACK, 30)
            except:
                arcade.draw_text("No Score", self.player.center_x - 350,
                                 self.player.center_y + 240, arcade.csscolor.BLACK, 30)

            try:
                if round(self.get_total_time(), 2) == self.score_data[2]:
                    arcade.draw_text(f"3 {self.score_format} {self.score_data[2]} SEC", self.player.center_x - 350,
                                     self.player.center_y + 190, arcade.csscolor.BLACK, 30)
                else:
                    arcade.draw_text(f"3 {self.score_format} {self.score_data[2]} SEC", self.player.center_x - 350,
                                     self.player.center_y + 190, arcade.csscolor.BLACK, 30)
            except:
                arcade.draw_text("No Score", self.player.center_x - 350,
                                 self.player.center_y + 190, arcade.csscolor.BLACK, 30)

            if self.get_total_time() > self.score_data[2]:
                arcade.draw_text(f"{linear_search(round(self.get_total_time(), 2), self.score_data) + 1} {self.score_format} "
                                 f"{round(self.get_total_time(), 2)} SEC", self.player.center_x - 350,
                                 self.player.center_y + 140, arcade.csscolor.RED, 30)

        # The information text
        arcade.draw_text(self.information_text, 400, 150, arcade.csscolor.BLACK, 15)

        # The direction not showing time
        if (self.get_total_time() - self.get_button_press_time()) < 5:
            self.player.create_direction(self.get_button_hit_time(), self.player.center_x, self.player.center_y)

    def update(self, delta_time: float):
        self.player.check_bag()

        # Check if the player hit the coin, remove it if so
        coin_hit_list = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.player.set_coins(self.player.get_coins()+1)
            Player.bag.append(self.player.get_coins())

        # Check fi the player hit the button, remove it and display the direction if so
        button_hit_list = arcade.check_for_collision_with_list(self.player, self.button_list)
        for button in button_hit_list:
            self.set_button_press_time(self.get_total_time())
            button.remove_from_sprite_lists()
            self.set_button_hit_time(self.get_button_hit_time()+1)

        # Keep counting time if the game is not end
        if self.end_screen is False:
            self.set_total_time(self.get_total_time()+delta_time)

        # Set the charge power length
        if self.up_pressed is False:
            self.player.set_charge_power(0)
        else:
            if self.player.change_y == 0:
                self.player.set_charge_power(self.player.get_charge_power()+1)
                if self.player.get_charge_power() > 69:
                    self.player.set_charge_power(70)

        self.player.update()
        self.physics_engine.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.up_pressed = True
            self.player.set_player_jump_speed(3)
            self.set_space_press_time(self.get_total_time())

        if key == arcade.key.RIGHT:
            if self.end_screen is True:
                self.player.change_x = 0
            else:
                self.right_pressed = True
                self.player.change_x += self.player.get_player_move_speed()

        if key == arcade.key.LEFT:
            if self.end_screen is True:
                self.player.change_x = 0
            else:
                self.left_pressed = True
                self.player.change_x -= self.player.get_player_move_speed()

        if self.player.collides_with_list(self.door_list) and self.player.open_door:
            if key == arcade.key.E:
                self.player.display_score(self.get_total_time())
                self.end_screen = True

        if key == arcade.key.ESCAPE and self.end_screen:
            self.director.next_view()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.up_pressed = False
            self.player.set_player_jump_speed(self.player.calculate_jumpspeed(self.get_space_press_time(),
                                                                              self.get_total_time(),
                                                                              self.player.get_player_jump_speed()))
            if self.player.change_y == 0:
                self.player.change_y += self.player.get_player_jump_speed()

        if key == arcade.key.RIGHT:
            self.right_pressed = False
            self.player.change_x = 0

        if key == arcade.key.LEFT:
            self.left_pressed = False
            self.player.change_x = 0

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        print(x)
        print(y)


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
    my_view = Chapter2View()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()

import arcade
import settings
import json
from typing import List

Left_ViewPoint_Margin = 150
Right_ViewPoint_Margin = 150
Bottom_ViewPoint_Margin = 50
Top_ViewPoint_Margin = 400

WIDTH = 800
HEIGHT = 600

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

    @classmethod
    def create_direction(cls, button_hit_time):
        if button_hit_time == 1 or button_hit_time == 4:
            return arcade.draw_text("Go Down", my_view.player.center_x-30, my_view.player.center_y+ 70, arcade.csscolor.RED, 15)
        if button_hit_time == 2:
            return arcade.draw_text("Go Right", my_view.player.center_x-30, my_view.player.center_y+ 70, arcade.csscolor.RED, 15)
        if button_hit_time == 3:
            return arcade.draw_text("Go Left", my_view.player.center_x-30, my_view.player.center_y+ 70, arcade.csscolor.RED, 15)

    def __init__(self, filename=None, scale=0.3, center_x=128, center_y=128):
        super().__init__(filename=filename, scale=scale, center_x=center_x, center_y=center_y)

        self.Player_move_speed = 3
        self.Player_jump_speed = 3
        self.view_bottom = 0
        self.view_left = 0

        self.coins = 0
        self.bag = []
        self.open_door = False

        self.charge_power = 0
        self.score = 0

    def update(self):
        changed = False

        left_boundary = self.view_left + Left_ViewPoint_Margin
        if self.left < left_boundary:
            self.view_left -= left_boundary - self.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + WIDTH - Right_ViewPoint_Margin
        if self.right > right_boundary:
            self.view_left += self.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + HEIGHT - Top_ViewPoint_Margin
        if self.top > top_boundary:
            self.view_bottom += self.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + Bottom_ViewPoint_Margin
        if self.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.bottom
            changed = True

        if changed:
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                WIDTH + self.view_left,
                                self.view_bottom,
                                HEIGHT + self.view_bottom)

    def check_bag(self):
        if len(self.bag) is 10:
            self.open_door = True

    def calculate_jumpspeed(self, presstime, releasetime, Player_jump_speed):
        if releasetime - presstime <= 0:
            return Player_jump_speed
        else:
            Player_jump_speed += 1
            return self.calculate_jumpspeed(presstime, releasetime-0.1 , Player_jump_speed)

    def display_score(self, scores):
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
        self.Total_time = 0
        self.space_press_time = 0
        self.button_hit_time = 0
        self.button_press_time = 0
        self.direction_draw_time = 0
        self.score_data = None

        self.up_pressed = False
        self.right_pressed = False
        self.left_pressed = False
        self.end_screen = False

        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.door_list = arcade.SpriteList()
        self.button_list = arcade.SpriteList()

        chapter2Map = arcade.tilemap.read_tmx("Ch2Map.tmx")
        self.player = Player("Sprites/alienBlue_front.png")
        self.wall_list = arcade.tilemap.process_layer(chapter2Map, "Platform_layer", 0.5)
        self.coin_list = arcade.tilemap.process_layer(chapter2Map, "Coin_layer", 0.5)
        self.door_list = arcade.tilemap.process_layer(chapter2Map, "Door_layer", 0.5)
        self.button_list = arcade.tilemap.process_layer(chapter2Map, "Button_layer", 0.5)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.wall_list, Gravity)
        self.score_format = "."*15

    def on_show(self):
        arcade.set_background_color(arcade.color.BLUE_SAPPHIRE)

    def on_draw(self):
        arcade.start_render()
        self.wall_list.draw()
        self.coin_list.draw()
        self.door_list.draw()
        self.button_list.draw()
        self.player.draw()

        #The number of coins
        coin_text = f"Coins: {self.player.coins}/10"
        arcade.draw_text(coin_text, self.player.center_x, self.player.center_y + 25, arcade.csscolor.BLACK, 12)

        #The charge power rectangle
        arcade.draw_rectangle_outline(self.player.center_x, self.player.center_y - 50, 20, 70, arcade.color.BLACK, 3, 90)
        arcade.draw_rectangle_filled(self.player.center_x, self.player.center_y - 50, 20, self.player.charge_power, arcade.color.RED, 90)

        #The end screen
        if self.end_screen is True:
            with open("chapter_2_scores.json", "r") as json_file:
                self.score_data = json.load(json_file)
            arcade.draw_rectangle_filled(self.player.center_x-200, self.player.center_y+210, 600, 300, arcade.color.WHITE)

            if round(self.Total_time, 2) == self.score_data[0]:
                arcade.draw_text(f"1 {self.score_format} {self.score_data[0]} SEC", self.player.center_x-350,
                                 self.player.center_y+290, arcade.csscolor.RED, 30)
            else:
                arcade.draw_text(f"1 {self.score_format} {self.score_data[0]} SEC", self.player.center_x - 350,
                                 self.player.center_y + 290, arcade.csscolor.BLACK, 30)

            try:
                if round(self.Total_time, 2) == self.score_data[1]:
                    arcade.draw_text(f"2 {self.score_format} {self.score_data[1]} SEC", self.player.center_x - 350,
                                     self.player.center_y + 240, arcade.csscolor.RED, 30)
                else:
                    arcade.draw_text(f"2 {self.score_format} {self.score_data[1]} SEC", self.player.center_x - 350,
                                     self.player.center_y + 240, arcade.csscolor.BLACK, 30)
            except:
                arcade.draw_text("No Score", self.player.center_x - 350,
                                 self.player.center_y + 240, arcade.csscolor.BLACK, 30)

            try:
                if round(self.Total_time, 2) == self.score_data[2]:
                    arcade.draw_text(f"3 {self.score_format} {self.score_data[2]} SEC", self.player.center_x - 350,
                                     self.player.center_y + 190, arcade.csscolor.BLACK, 30)
                else:
                    arcade.draw_text(f"3 {self.score_format} {self.score_data[2]} SEC", self.player.center_x - 350,
                                     self.player.center_y + 190, arcade.csscolor.BLACK, 30)
            except:
                arcade.draw_text("No Score", self.player.center_x - 350,
                                 self.player.center_y + 190, arcade.csscolor.BLACK, 30)

            if self.Total_time > self.score_data[2]:
                arcade.draw_text(f"{linear_search(round(self.Total_time, 2), self.score_data)+1} {self.score_format} "
                                 f"{round(self.Total_time, 2)} SEC", self.player.center_x-350,
                                 self.player.center_y + 140, arcade.csscolor.RED, 30)

        if (self.Total_time - self.button_press_time) < 5:
            self.player.create_direction(self.button_hit_time)

    def update(self, delta_time: float):
        self.player.check_bag()

        coin_hit_list = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.player.coins += 1
            self.player.bag.append(self.player.coins)

        button_hit_list = arcade.check_for_collision_with_list(self.player, self.button_list)
        for button in button_hit_list:
            self.button_press_time = self.Total_time
            button.remove_from_sprite_lists()
            self.button_hit_time += 1

        if self.end_screen == False:
            self.Total_time += delta_time

        self.player.update()
        self.physics_engine.update()

        if self.up_pressed is False:
            self.player.charge_power = 0
        else:
            self.player.charge_power += 1
            if self.player.charge_power > 69:
                self.player.charge_power = 70

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.up_pressed = True
            self.player.Player_jump_speed = 3
            self.space_press_time = self.Total_time

        if key == arcade.key.RIGHT:
            if self.end_screen is True:
                self.player.change_x = 0
            else:
                self.right_pressed = True
                self.player.change_x += self.player.Player_move_speed

        if key == arcade.key.LEFT:
            if self.end_screen is True:
                self.player.change_x = 0
            else:
                self.left_pressed = True
                self.player.change_x -= self.player.Player_move_speed

        if self.player.collides_with_list(self.door_list) and self.player.open_door:
            if key == arcade.key.E:
                self.player.display_score(self.Total_time)
                self.end_screen = True

        if key == arcade.key.ESCAPE and self.end_screen:
            self.director.next_view()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.up_pressed = False
            self.player.Player_jump_speed = self.player.calculate_jumpspeed(self.space_press_time, self.Total_time, self.player.Player_jump_speed)
            if self.player.Player_jump_speed > 15:
                self.player.Player_jump_speed = 15
            self.player.change_y += self.player.Player_jump_speed

        if key == arcade.key.RIGHT:
            self.right_pressed = False
            self.player.change_x = 0

        if key == arcade.key.LEFT:
            self.left_pressed = False
            self.player.change_x = 0


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

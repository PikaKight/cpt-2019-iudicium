import arcade
import random
import settings
from typing import List
import math

WIDTH = 800
HEIGHT = 600
view_merge = 100

key_k = False
key_k_used_time = 0

end_window = False
open_door = False
end_window_time = 0

_move_speed = 5

TILE_SCALING = 1
SPRITE_SCALING_PLAYER = 0.15
SPRITE_PIXEL_SIZE = 30
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)


class Key(arcade.Sprite):
    """
    create two types of key use classmethod.
    Inheritance from arcade.Sprite to make each key a sprite
    Attrs:
    filename(str): the filename and path of the key
    scale(int): the scale of the key
    type (str): The type of the key

    Return:
        a key sprite with type that is either normal or special
    """

    # a sprite list of all keys
    all_keys = arcade.SpriteList()
    type = None

    def __init__(self, filename: str, scale: int, type: str) -> None:
        super().__init__(filename, scale)
        self._type = type

    def get_type(self):
        return self._type

    def set_type(self, value):
        self._type = value

    def add_key(self, key):
        self.all_keys.append(key)

    @classmethod
    def create_normal_key(cls):
        normal_key = cls("images/key2.png", TILE_SCALING, "normal")
        return normal_key

    @classmethod
    def creat_special_key(cls):
        special_key = cls("images/key.png", TILE_SCALING, "special")
        return special_key


class MyGame(arcade.View):
    """
    All the game function are created in this class
    """

    def __init__(self):
        super().__init__()

        self.player_list = None
        self.wall_list = None
        self.key_list = None
        self.key = Key(None, TILE_SCALING, None)
        self.door = None
        self.score = None
        self.player_sprite = None
        self.physics_engine = None
        self.view_bottom = 0
        self.view_left = 0
        self.frime_count = 0
        self.flag_k = None
        self.introduction = True
        self.endWindow = None
        self.background = None
        arcade.set_background_color(arcade.color.BLACK)
        self.setup()

    def key_place_success(self, key_placed_successfully: bool, normal_key: arcade.Sprite, x_list: List[int],
                          y_list: List[int]):
        """
        Use recursion to check if key place is successful
        Attrs:
        key_placed_successfully(bool): break statement of the recursion function
        normal_key(arcade.Sprite): a key Sprite
        x_list: List[int]: all the x coordinates of the keys has been created
        y_list: List[int]: all the y coordinates of the keys has been created

        Return:
           the position of the key (x, y)
        """
        if key_placed_successfully:
            return normal_key.center_x, normal_key.center_y
        normal_key.center_x = random.randrange(1500)
        normal_key.center_y = random.randrange(1500)

        # See if the key is hitting a wall, hitting another key, or too close from each other
        wall_hit_list = arcade.check_for_collision_with_list(normal_key, self.wall_list)
        key_hit_list = arcade.check_for_collision_with_list(normal_key, self.key_list)
        flag = True
        for item_x in x_list:
            if abs(int(item_x - normal_key.center_x)) < 30:
                flag = False
        for item_y in y_list:
            if abs(int(item_y - normal_key.center_y)) < 20:
                flag = False
        if len(wall_hit_list) == 0 and len(key_hit_list) == 0 and flag:
            key_placed_successfully = True

        return self.key_place_success(key_placed_successfully, normal_key, x_list, y_list)

    # sort the distances between each key and the player
    def sort_key(self, key_list) -> List:
        """
        Use bubble sort to sort all the keys in the list by distances.
        Sort the distance from the closest to the furthest
        Args:
            key_list: A list of key sprites
        Returns:
            a sorted sprite list
        """
        for i in range(len(key_list)):
            for j in range(len(key_list) - 1):
                new_sprite = arcade.SpriteList()
                key_1 = arcade.get_distance_between_sprites(self.player_sprite, key_list[j])
                key_2 = arcade.get_distance_between_sprites(self.player_sprite, key_list[j + 1])
                if key_1 > key_2:
                    # Because of a spritelist cannot be modify, so I use another temperate list to append.
                    temp = None
                    for k in range(len(key_list)):
                        if k == j:
                            temp = key_list[j]
                        elif k == j + 1:
                            new_sprite.append(key_list[k])
                            new_sprite.append(temp)
                        # append values that does not need to be swap
                        else:
                            new_sprite.append(key_list[k])

                    key_list = new_sprite
        self.key.all_keys = key_list
        return key_list

    def linear_search_key(self, target: str, key_list: List) -> bool:
        """
          Use linear search to check if the special key is in the key list
          Args:
              target(str): the type of each key
              key_list: A list of key sprites
          Returns:
              a sorted sprite list
        """
        for key in key_list:
            if key._type == target:
                self.flag_k = True
                return self.flag_k
        return self.flag_k

    def setup(self):
        """
        Create all sprites and sprite lists here
        """
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.key_list = arcade.SpriteList()
        self.background = arcade.SpriteList()
        self.door = arcade.SpriteList()
        self.frime_count = 0
        self.flag_k = False
        self.score = 0

        # Set up the player
        self.player_sprite = arcade.Sprite("Sprites/alienBlue_front.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50

        self.player_list.append(self.player_sprite)

        # Name of map file to load
        map_name = "maps/third-map.tmx"
        # Name of the layer in the file
        platforms_layer_name = 'Platforms'
        door_layer_name = "door"
        background_layer_name = "background"
        my_map = arcade.tilemap.read_tmx(map_name)
        # -- Platforms
        self.wall_list = arcade.tilemap.process_layer(my_map, platforms_layer_name, TILE_SCALING)
        # -- Background
        self.background = arcade.tilemap.process_layer(my_map, background_layer_name, TILE_SCALING)
        # -- door
        self.door = arcade.tilemap.process_layer(my_map, door_layer_name, TILE_SCALING)
        # Set the background color
        if my_map.background_color:
            arcade.set_background_color(my_map.background_color)

        # Create the physics engine
        self.physics_engine = self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

        # Set  the viewport boundaries
        self.view_left = 0
        self.view_bottom = 0

        # make a random value to represent the special key
        special_flag = int(random.randrange(0, 21))
        x_list = []
        y_list = []
        for i in range(21):
            # Create the key using key class and the recursion method
            if i == special_flag:
                new_key = self.key.creat_special_key()
            else:
                new_key = self.key.create_normal_key()
            key_placed_successfully = False
            # keep trying until success
            new_key.center_x, new_key.center_y = self.key_place_success(key_placed_successfully, new_key, x_list,
                                                                        y_list)
            # add each coordinates to the list
            x_list.append(new_key.center_x)
            y_list.append(new_key.center_y)
            self.key.add_key(new_key)

    def on_draw(self):
        """
        Draw all the sprite and sprite in the setup function
        """
        arcade.start_render()

        # draw the intro introduction
        texture = arcade.load_texture("images/introduction.jpeg")
        arcade.draw_texture_rectangle(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT, texture)

        # check if the user press enter and setup the game
        if not self.introduction:
            self.background.draw()
            self.door.draw()
            self.player_list.draw()
            self.wall_list.draw()
            self.key.all_keys.draw()

            output = f"keys:{self.score}"
            arcade.draw_text(output, self.player_sprite.center_x - 20, self.player_sprite.center_y + 20,
                             arcade.color.GOLD,
                             14)

            # check of the player hit the door and press O to open
            if end_window and open_door:
                self.flag_k = False
                if not self.linear_search_key("special", self.key.all_keys):
                    texture = arcade.load_texture("images/ending.png")
                    arcade.draw_texture_rectangle(self.view_left + WIDTH // 2, self.view_bottom + HEIGHT // 2, WIDTH,
                                                  HEIGHT, texture)

                    arcade.draw_text(f"YOUR FINAL SCORE IS: {self.score * 100}", self.view_left + WIDTH // 2,
                                     self.view_bottom + HEIGHT // 2 - 100,
                                     arcade.color.WHITE, font_size=20, anchor_x="center", anchor_y="center")

                # if the special key still in the key list, show text remind player
                else:
                    arcade.draw_text("FIND THE SPECIAL KEY", self.view_left + WIDTH // 2,
                                     self.view_bottom + HEIGHT // 2,
                                     arcade.color.WHITE, font_size=30, anchor_x="center", anchor_y="center")

    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        """
        global end_window, end_window_time, key_k, key_k_used_time, open_door
        # kill every key has been collect
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.key.all_keys)
        for key in hit_list:
            # count the number of time player use K to get the closest key
            if key == self.key.all_keys[0]:
                key_k_used_time += 1
                key_k = False
            key.remove_from_sprite_lists()
            self.score += 1

        # check if the player hit the door
        if len(arcade.check_for_collision_with_list(self.player_sprite, self.door)) == 1:
            end_window = True
            end_window_time = self.frime_count

        # Show the text: 3 seconds
        if self.flag_k:
            if self.frime_count - end_window_time == 180 and end_window:
                end_window = False
                open_door = False

        # update the physics engine
        self.physics_engine.update()

        # get the closest key
        if key_k and key_k_used_time < 1:
            steps = int(arcade.get_distance_between_sprites(self.player_sprite, self.key.all_keys[0]))
            x_delta = 6 * ((self.key.all_keys[0].center_x - self.player_sprite.center_x) / steps)
            y_delta = 6 * ((self.key.all_keys[0].center_y - self.player_sprite.center_y) / steps)
            self.key.all_keys[0].center_x = self.key.all_keys[0].center_x - x_delta
            self.key.all_keys[0].center_y = self.key.all_keys[0].center_y - y_delta

        # ------------- merge the screen view ----------------
        changed = False
        # Scroll left
        left_boundary = self.view_left + view_merge
        if self.player_sprite.left < left_boundary and left_boundary > 100:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + WIDTH - view_merge
        if self.player_sprite.right > right_boundary and right_boundary < 1400:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + HEIGHT - view_merge
        if self.player_sprite.top > top_boundary and top_boundary < 1395:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + view_merge
        if self.player_sprite.bottom < bottom_boundary and bottom_boundary > 105:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        # make sure no rounding errors.
        self.view_left = int(self.view_left)
        self.view_bottom = int(self.view_bottom)

        # If we changed the boundary values, update the view port to match
        if changed:
            arcade.set_viewport(self.view_left, WIDTH + self.view_left - 1, self.view_bottom,
                                HEIGHT + self.view_bottom - 1)

        self.frime_count += 1

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.
        """
        global key_k, key_k_used_time, open_door

        if key == arcade.key.W:
            self.player_sprite.change_y = _move_speed
        elif key == arcade.key.S:
            self.player_sprite.change_y = - _move_speed
        elif key == arcade.key.A:
            self.player_sprite.change_x = - _move_speed
        elif key == arcade.key.D:
            self.player_sprite.change_x = _move_speed
        elif key == arcade.key.ENTER:
            self.introduction = False
        elif key == arcade.key.ESCAPE:
            # arcade.close_window()
            self.director.next_view()

        elif key == arcade.key.K:
            key_k = True
            # sort the distances of the keys
            self.sort_key(self.key.all_keys)

        elif key == arcade.key.O:
            open_door = True

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        # global key_k
        if key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0

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
    my_view = MyGame()

    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()

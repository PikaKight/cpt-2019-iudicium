import arcade
import random
from typing import List
import math

WIDTH = 800
HEIGHT = 600

key_k = False
key_k_used_time = 0
end_window = False
end_window_time = 0
view_merge = 100
move_speed = 10
SPRITE_SCALING_PLAYER = 0.13
TILE_SCALING = 1
SPRITE_PIXEL_SIZE = 30
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)


class Key(arcade.Sprite):
    all_keys = arcade.SpriteList()
    id = None
    type = None

    def __init__(self, filename, scale, type):
        super().__init__(filename, scale)
        self.id = len(self.all_keys)
        self.type = type

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

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.player_list = None
        self.wall_list = None
        self.key_list = None
        self.background = None
        self.key = Key(None, TILE_SCALING, None)
        self.door = None
        self.score = None
        self.bag = []
        self.player_sprite = None
        self.physics_engine = None
        self.view_bottom = 0
        self.view_left = 0
        self.endWindow = None
        self.frime_count = 0
        arcade.set_background_color(arcade.color.BLACK)

    # check if key place is successful
    def key_place_success(self, key_placed_successfully, normal_key, x_list, y_list):
        if key_placed_successfully:
            return [normal_key.center_x, normal_key.center_y]
        normal_key.center_x = random.randrange(1500)
        normal_key.center_y = random.randrange(1500)

        # See if the key is hitting a wall
        wall_hit_list = arcade.check_for_collision_with_list(normal_key, self.wall_list)

        # See if the key is hitting another key
        key_hit_list = arcade.check_for_collision_with_list(normal_key, self.key_list)
        flag = True
        for item_x in x_list:
            if abs(item_x - normal_key.center_x) < 40:
                flag = False
        for item_y in y_list:
            if abs(item_y - normal_key.center_y) < 25:
                flag = False
        if len(wall_hit_list) == 0 and len(key_hit_list) == 0 and flag == True:
            key_placed_successfully = True

        return self.key_place_success(key_placed_successfully, normal_key, x_list, y_list)

    def setup(self):
        # Create your sprites and sprite lists here
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.key_list = arcade.SpriteList()
        self.background = arcade.SpriteList()
        self.door = arcade.SpriteList()
        self.frime_count = 0

        # Score
        self.score = 0

        # Set up the player
        self.player_sprite = arcade.Sprite("images/Player.png",
                                           SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50

        self.player_list.append(self.player_sprite)

        # Name of map file to load
        map_name = "maps/third-map.tmx"
        # Name of the layer in the file that has our platforms/walls
        platforms_layer_name = 'Platforms'
        # Name of the layer that has items for pick-up
        door_layer_name = 'door'

        background_layer_name = "background"

        my_map = arcade.tilemap.read_tmx(map_name)
        # -- Platforms
        self.wall_list = arcade.tilemap.process_layer(my_map, platforms_layer_name, TILE_SCALING)
        # -- Background
        self.background = arcade.tilemap.process_layer(my_map, background_layer_name, TILE_SCALING)
        # -- door
        self.door = arcade.tilemap.process_layer(my_map, door_layer_name, TILE_SCALING)
        # --- Other stuff
        # Set the background color
        if my_map.background_color:
            arcade.set_background_color(my_map.background_color)

        # Create the 'physics engine'
        self.physics_engine = self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

        # Set  the viewport boundaries
        self.view_left = 0
        self.view_bottom = 0

        # make a random value to represent the special key
        special_flag = int(random.randrange(0, 21))

        # draw a list of keys
        x_list = []
        y_list = []
        for i in range(21):
            # Create the key using key class
            if i == special_flag:
                new_key = self.key.creat_special_key()
            else:
                new_key = self.key.create_normal_key()

            key_placed_successfully = False
            # keep trying until success
            new_key.center_x, new_key.center_y = \
                self.key_place_success(key_placed_successfully, new_key, x_list, y_list)

            x_list.append(new_key.center_x)
            y_list.append(new_key.center_y)
            self.key.add_key(new_key)

        # Set  the viewport boundaries
        self.view_left = 0
        self.view_bottom = 0

    def on_draw(self):
        arcade.start_render()  # keep as first line
        # Draw everything below here.
        self.background.draw()
        self.door.draw()
        self.player_list.draw()
        self.wall_list.draw()
        self.key.all_keys.draw()

        output = f"keys:{self.score}"
        arcade.draw_text(output, self.player_sprite.center_x - 20, self.player_sprite.center_y + 20, arcade.color.GOLD,
                         14)

        if end_window:
            self.flag = False
            for i in self.key.all_keys:
                if i.type == "special":
                    self.flag = True
            if not self.flag:
                print("cleawr")
                arcade.draw_rectangle_filled(self.view_left + WIDTH // 2, self.view_bottom + HEIGHT // 2, WIDTH, HEIGHT,
                                             arcade.color.BLACK)

                arcade.draw_text(
                    f"""!!! YOU WIN !!!
\nthe final key you have is {self.score}
                    
                    """ , self.view_left + WIDTH //2, self.view_bottom + HEIGHT//2,
                                 arcade.color.WHITE, font_size= 40, anchor_x="center", anchor_y="center")

            else:
                arcade.draw_rectangle_filled(self.view_left + WIDTH // 2, self.view_bottom + HEIGHT //2, 500, 100,
                                             arcade.color.BLACK)
                arcade.draw_text("FIND THE SPECIAL KEY",self.view_left + WIDTH // 2, self.view_bottom + HEIGHT // 2,
                                 arcade.color.WHITE, font_size=30, anchor_x="center", anchor_y="center")



    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        global end_window, end_window_time, key_k, key_k_used_time
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.key.all_keys)
        for key in hit_list:
            if key == self.key.all_keys[0]:
                key_k_used_time += 1
                key_k = False
            key.remove_from_sprite_lists()
            self.score += 1

        if len(arcade.check_for_collision_with_list(self.player_sprite, self.door)) == 1:
            end_window = True
            end_window_time = self.frime_count
        if not self.flag:
            if self.frime_count - end_window_time == 300 and end_window:
                end_window = False

        self.physics_engine.update()

        # get the closest key
        if key_k and key_k_used_time < 1:

            steps= int(arcade.get_distance_between_sprites(self.player_sprite, self.key.all_keys[0]))
            x_delta= 6*((self.key.all_keys[0].center_x - self.player_sprite.center_x)/steps)
            y_delta= 6*((self.key.all_keys[0].center_y - self.player_sprite.center_y)/steps)
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
        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        global key_k, key_k_used_time

        if key == arcade.key.W:
            self.player_sprite.change_y = move_speed
        elif key == arcade.key.S:
            self.player_sprite.change_y = - move_speed
        elif key == arcade.key.A:
            self.player_sprite.change_x = - move_speed
        elif key == arcade.key.D:
            self.player_sprite.change_x = move_speed

        if key == arcade.key.K:
            key_k = True
            # key_k_used_time += 1
            self.sort_key()
            # self.skill()

    # sort the distances between each key and the player
    def sort_key(self):
        key_list = self.key.all_keys
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

    # def skill(self):
    #     self.sort_key()
    #     # self.key.all_keys.kill()
    #     steps= int(arcade.get_distance_between_sprites(self.player_sprite, self.key.all_keys[0]))
    #     x_delta= (self.key.all_keys[0].center_x - self.player_sprite.center_x)/steps
    #     y_delta= (self.key.all_keys[0].center_y - self.player_sprite.center_y)/steps
    #     for i in range(steps):
    #         self.key.all_keys[0].center_x = self.key.all_keys[0].center_x - 1
    #         self.key.all_keys[0].center_y = self.key.all_keys[0].center_y - 1
    #     # self.key.all_keys[0].change_y = y_delta
    #     # self.key.all_keys[0].change_x = x_delta

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        # global key_k
        if key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0

        # elif key == arcade.key.K:
        #     key_k = False


    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    game = MyGame(WIDTH, HEIGHT, "My Game")
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()

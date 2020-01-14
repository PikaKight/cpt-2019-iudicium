import arcade
import random
import settings

player_speedx = 5
player_speedy = 5

# Health Bar
player_health = 100

# Slime attack power
slime_strength = 5


class Player(arcade.Sprite):
    def update(self):
        # Movement
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Boundaries
        if self.left < 0:
            self.left = 0
        elif self.right > settings.WIDTH:
            self.right = settings.WIDTH
        if self.top > settings.HEIGHT:
            self.top = settings.HEIGHT
        elif self.bottom < 0:
            self.bottom = 0


class Slime(arcade.Sprite):
    # def __init__(self, sprite_scaling):
    #     super().__init__(sprite_scaling)
    #     self.change_x = 0
    #     self.change_y = 0

    def update(self):
        # Movement
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Boundaries
        if self.left < 0 or self.right > settings.WIDTH:
            self.change_x *= -1
        if self.bottom < 0 or self.top > settings.HEIGHT:
            self.change_y *= -1


class Chapter4View(arcade.View):    
    def __init__(self):
        super().__init__()

        # Sprite Lists
        self.all_sprite_list = arcade.SpriteList()
        self.slime_list = arcade.SpriteList()

        # PLAYER Sprite
        self.player = Player("Sprites/alienBlue_front.png", 0.3)
        self.player.center_x = 100
        self.player.center_y = 200

        # Append player to player_list and all_sprites_list
        self.all_sprite_list.append(self.player)

        # SLIME Sprite
        for i in range(7):
            slime_sprite = Slime("Sprites/slimeGreen.png", 0.5)

            slime_sprite.center_x = random.randrange(settings.WIDTH)
            slime_sprite.center_y = random.randrange(settings.HEIGHT)
            slime_sprite.change_x = random.randrange(-4, 4)
            slime_sprite.change_y = random.randrange(-4, 4)
            if slime_sprite.change_x  == 0 or slime_sprite.change_y == 0:
                slime_sprite.change_x = 1
                slime_sprite.change_y = -1

            self.slime_list.append(slime_sprite)
            self.all_sprite_list.append(slime_sprite)
    
    def setup(self):
        pass

    def on_show(self):
        arcade.set_background_color(arcade.color.GHOST_WHITE)

    def on_draw(self):
        arcade.start_render()

        # Draw all sprites
        self.all_sprite_list.draw()

        # PLAYER
        # Player Health Bar
        arcade.draw_xywh_rectangle_filled(10, 570, 200, 20, arcade.color.BLACK)
        arcade.draw_xywh_rectangle_filled(10, 570, player_health*2, 20, arcade.color.GREEN)


    def update(self, delta_time):
        global player_health

        self.all_sprite_list.update()

        collisions = arcade.check_for_collision_with_list(self.player, self.slime_list)

        for collision in collisions:
            player_health -= slime_strength * 2

    def on_key_press(self, key, modifiers):
        global health_bar_width

        if key == arcade.key.ESCAPE:
            self.director.next_view()

        if key == arcade.key.UP:
            self.player.change_y = player_speedy
        elif key == arcade.key.DOWN:
            self.player.change_y = -player_speedy
        elif key == arcade.key.RIGHT:
            self.player.change_x = player_speedx
        elif key == arcade.key.LEFT:
            self.player.change_x = -player_speedx            


    def on_key_release(self, key, modifiers):
        # self.director.next_view()

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.RIGHT or key == arcade.key.LEFT:
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
    my_view = Chapter4View()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()

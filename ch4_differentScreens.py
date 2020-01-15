import arcade
import random
import math
import settings


screen = "chapter4"

player_speedx = 5
player_speedy = 5

# Health Bar
player_health = 100
player_attack = 25
laser_speed = 5

# Slime
slime_health = 100
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
    def update(self):
        # Movement
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Boundaries
        if self.left < 0 or self.right > settings.WIDTH:
            self.change_x *= -1
        if self.bottom < 0 or self.top > settings.HEIGHT:
            self.change_y *= -1


class ch4_Menu(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)
    
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Chapter 4", settings.WIDTH/2 - 50, settings.HEIGHT/2 + 50, arcade.color.BLACK,
                        font_size=30, bold=True, )
        arcade.draw_text("Press ENTER to proceed to Game", settings.WIDTH/2 - 150, settings.HEIGHT/2,
                        arcade.color.BLACK, font_size=25)
        arcade.draw_text("Press ESC to Exit Game", settings.WIDTH/2 - 100, settings.HEIGHT/2 - 50,
                        arcade.color.BLACK, font_size=25)
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            game_View = gameView()
            self.window.show_view(game_View)
        elif key == arcade.key.ESCAPE:
            self.director.next_view()


class gameView(arcade.View):
    def __init__(self):
        super().__init__()

        # Sprite Lists
        self.all_sprite_list = arcade.SpriteList()
        self.slime_list = arcade.SpriteList()
        self.laser_list = arcade.SpriteList()

        # PLAYER Sprite
        self.player = Player("Sprites/alienBlue_front.png", 0.3)
        self.player.center_x = 100
        self.player.center_y = 200

        self.all_sprite_list.append(self.player)

        # Player Attack
        # self.player_attack = 

        # SLIME Sprite
        for i in range(8):
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

    def on_show(self):
        arcade.set_background_color(arcade.color.GHOST_WHITE)
    
    def on_draw(self):
        arcade.start_render()

        self.all_sprite_list.draw()

        # Player Health Bar
        arcade.draw_xywh_rectangle_filled(10, 570, 200, 20, arcade.color.BLACK)
        arcade.draw_xywh_rectangle_filled(10, 570, player_health*2, 20, arcade.color.GREEN)
    
    def on_update(self, delta_time):
        global player_health

        self.all_sprite_list.update()

        # Player and Slime Collision
        collisions = arcade.check_for_collision_with_list(self.player, self.slime_list)

        for collision in collisions:
            player_health -= slime_strength * 2
        
        # Player Attacks Slime
        for laser in self.laser_list:
            if arcade.check_for_collision_with_list(laser, self.slime_list):
                laser.remove_from_sprite_lists()

            # Laser flies off screen
            if laser.right > settings.WIDTH or laser.left < 0 or laser.top > settings.HEIGHT or laser.bottom < 0:
                laser.remove_from_sprite_lists()
        
        # Player Health reaches 0
        if player_health <= 0:
            gameOverView = gameOverView()
            self.window.show_view(gameOverView)
    
    def on_mouse_press(self, x, y, button, modifiers):
        self.laser = arcade.Sprite("Sprites/laserBlue.png", 0.5)

        # Position laser at player location
        self.laser.center_x = self.player.center_x
        self.laser.center_y = self.player.center_y

        # Target Co-ordinates
        self.target_x = x
        self.target_y = y

        # Calculate angle of laser
        x_diff = self.target_x - self.player.center_x
        y_diff = self.target_y - self.player.center_y
        angle = math.atan2(y_diff, x_diff)

        # Angle the laser sprite
        self.laser.angle = math.degrees(angle)

        # Laser Speed
        self.laser.change_x = math.cos(angle) * laser_speed
        self.laser.change_y = math.sin(angle) * laser_speed

        # Add laser to list
        self.laser_list.append(self.laser)
        self.all_sprite_list.append(self.laser)

    def on_key_press(self, key, modifiers):
        global health_bar_width

        if key == arcade.key.UP:
            self.player.change_y = player_speedy
        elif key == arcade.key.DOWN:
            self.player.change_y = -player_speedy
        elif key == arcade.key.RIGHT:
            self.player.change_x = player_speedx
        elif key == arcade.key.LEFT:
            self.player.change_x = -player_speedx
        elif key == arcade.key.ESCAPE:
            self.director.next_view()       

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.RIGHT or key == arcade.key.LEFT:
            self.player.change_x = 0


class gameOverView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK_OLIVE)
    
    def on_draw(self):
        arcade.draw_text("""GAME OVER
  YOU DIED""", settings.WIDTH/2 - 100, settings.HEIGHT/2 + 50, arcade.color.WHITE, font_size=30, bold=True)
        arcade.draw_text("Press Enter to Restart", settings.WIDTH/2 - 150, settings.HEIGHT/2,
                        arcade.color.WHITE, font_size=25)
        arcade.draw_text("Press ESC to Exit Game", settings.WIDTH/2 - 150, settings.HEIGHT/2 - 50,
                        arcade.color.WHITE, font_size=25)
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            game_View = gameView()
            self.window.show_view(game_View)
        elif key == arcade.key.ESCAPE:
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
    my_view = ch4_Menu()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()

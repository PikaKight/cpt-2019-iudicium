import arcade
import random
import math
import settings


# Player
player_speedx = 5
player_speedy = 5
player_strength = 25
laser_speed = 8

# Health Bar
# player_health = 100
health_barx = 10
health_bary = 570
health_bar_height = 20
health_bar_width = 200

# Slime
slime_health = 100
slime_strength = 10

# Fish
recovery_points = 15


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


class Fish(Slime):
    pass


def fish(self):
    # global player_health

    if len(self.fish_list) == 0:
        if self.player_health <= 50 and self.frame_count % 200 == 0:
            self.fish = Fish("Sprites/fishPink.png", 0.3)
            self.fish.center_x = random.randrange(20, settings.WIDTH - 20)
            self.fish.center_y = random.randrange(20, settings.HEIGHT - 20)
            self.fish.change_x = random.randrange(-4, 4)
            self.fish.change_y = random.randrange(-4, 4)

            self.fish_list.append(self.fish)
            self.all_sprite_list.append(self.fish)

    if len(self.fish_list) <= 1 and arcade.check_for_collision_with_list(self.player, self.fish_list):
        self.player_health += recovery_points
        self.fish.remove_from_sprite_lists()
        fish(self)


class ch4_MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("Sprites/whiteBorders_blackBackground.jpg")

    def on_show(self):
        pass
    
    def on_draw(self):
        arcade.start_render()

        arcade.draw_texture_rectangle(settings.WIDTH/2, settings.HEIGHT/2,
                                    settings.WIDTH, settings.HEIGHT, self.background)

        arcade.draw_text("Chapter 4", settings.WIDTH/2, settings.HEIGHT/2 + 50, arcade.color.WHITE,
                        font_size=45, bold=True, anchor_x="center")
        arcade.draw_text("Press ENTER to proceed to Game", settings.WIDTH/2, settings.HEIGHT/2,
                        arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Press ESC to Exit Game", settings.WIDTH/2, settings.HEIGHT/2 - 50,
                        arcade.color.WHITE, font_size=20, anchor_x="center")
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            user_name = Username()
            self.window.show_view(user_name)
        elif key == arcade.key.ESCAPE:
            self.director.next_view()


class Username(arcade.View):
    def __init__(self):
        super().__init__()

        self.dialogue_box = arcade.Sprite("Sprites/DialogueBox.png", 1)
        self.dialogue_box.center_x = settings.WIDTH/2
        self.dialogue_box.center_y = settings.HEIGHT/2

        self.text = ""
        self.center_x = self.dialogue_box.center_x
        self.center_y = self.dialogue_box.center_y

    def setup(self):
        self.textbox_list.append(arcade.gui.TextBox(self.center_x - 125, self.center_y))
        self.button_list.append(arcade.gui.SubmitButton(self.textbox_list[0], self.on_submit, self.center_x,
                                                        self.center_y))

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        super().on_draw()
        arcade.start_render()

        self.dialogue_box.draw()

        arcade.draw_text("Username", self.dialogue_box.center_x, self.dialogue_box.center_y + 190,
                        arcade.color.BLACK, font_size=25, bold=True, anchor_x="center", anchor_y="center")
        arcade.draw_text("Enter a username that will be saved onto the scoreboard",
                        self.dialogue_box.center_x, self.dialogue_box.center_y + 90, arcade.color.BLACK,
                        font_size=15, anchor_x="center",anchor_y="center")

        if self.text:
            arcade.draw_text(f"{self.text}", self.dialogue_box.center_x, self.dialogue_box.center_y,
                            arcade.color.BLACK, 24)

    def on_submit(self):
        self.text = self.textbox_list[0].text_storage.text

    def update(self, delta_time):
        self.dialogue_box.update()

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            game_View = gameView()
            self.window.show_view(game_View)
        elif key == arcade.key.ESCAPE:
            self.director.next_view()


class gameView(arcade.View):
    def __init__(self):
        super().__init__()
        
        # Background
        self.background = arcade.load_texture("Sprites/tiledFloor.jpg")

        # Frame Count
        self.frame_count = 0

        # Timer
        self.total_time = 0.0

        # Total Lasers
        self.total_lasers = 0

        # Total Damage
        self.total_damage = 0

        # Sprite Lists
        self.all_sprite_list = arcade.SpriteList()
        self.slime_list = arcade.SpriteList()
        self.laser_list = arcade.SpriteList()
        self.fish_list = arcade.SpriteList()

        # PLAYER Sprite
        self.player = Player("Sprites/alienBlue_front.png", 0.3)
        self.player.center_x = settings.WIDTH/2
        self.player.center_y = settings.HEIGHT/2
        self.player_health = 100

        self.all_sprite_list.append(self.player)

        # SLIME Sprite
        for i in range(8):
            self.slime_sprite = Slime("Sprites/slimeGreen.png", 0.5)

            self.slime_sprite.center_x = random.randrange(settings.WIDTH)
            self.slime_sprite.center_y = random.randrange(settings.HEIGHT)
            self.slime_sprite.change_x = random.randrange(-4, 4)
            self.slime_sprite.change_y = random.randrange(-4, 4)
            self.slime_health = 100
            if self.slime_sprite.change_x  == 0 or self.slime_sprite.change_y == 0:
                self.slime_sprite.change_x = 1
                self.slime_sprite.change_y = -1

            self.slime_list.append(self.slime_sprite)
            self.all_sprite_list.append(self.slime_sprite)

    def on_show(self):
        arcade.set_background_color(arcade.color.GHOST_WHITE)

    def on_draw(self):
        arcade.start_render()

        # Draw Background
        arcade.draw_texture_rectangle(settings.WIDTH/2, settings.HEIGHT/2,
                                    settings.WIDTH, settings.HEIGHT, self.background)

        self.all_sprite_list.draw()

        # Calculate time
        minutes = int(self.total_time) // 60
        seconds = int(self.total_time) % 60

        output = f"Time: {minutes:02d}:{seconds:02d}"

        # Timer
        arcade.draw_text(output, settings.WIDTH - 50, settings.HEIGHT - 25,
                        arcade.color.BLACK_LEATHER_JACKET, font_size=15, anchor_x="center")

        # Player Health Bar
        arcade.draw_xywh_rectangle_filled(health_barx, health_bary, health_bar_width,
                                            health_bar_height, arcade.color.BLACK)
        arcade.draw_xywh_rectangle_filled(health_barx, health_bary, self.player_health*2,
                                            health_bar_height, arcade.color.GUPPIE_GREEN)
        arcade.draw_text(f"{self.player_health}/100", health_barx, health_bary - 25,
                        arcade.color.BLACK, font_size=15)

        # Fish
        fish(self)

    def on_update(self, delta_time):
        global slime_health #player_health

        self.all_sprite_list.update()

        self.frame_count += 1
        self.total_time += delta_time

        # Player and Slime Collision
        collisions = arcade.check_for_collision_with_list(self.player, self.slime_list)

        # Decrease Player Health when collision with slime and every 10 frames
        for collision in collisions:
            if self.frame_count % 10 == 0:
                self.total_damage += slime_strength
                self.player_health -= slime_strength
        
        # Player Attacks Slime
        for slime in self.slime_list:
            for laser in self.laser_list:
                if arcade.check_for_collision_with_list(laser, self.slime_list):
                    self.slime_health -= player_strength
                    laser.remove_from_sprite_lists()

            # Laser flies off screen
                if laser.left > settings.WIDTH or laser.right < 0 or laser.bottom > settings.HEIGHT or laser.top < 0:
                    laser.remove_from_sprite_lists()

        # Slime HP reaches 0
            if self.slime_health <= 0:
                slime.remove_from_sprite_lists()

        # Player HP reaches 0
        if self.player_health <= 0:
            gameOver_View = gameOverView()
            self.window.show_view(gameOver_View)
    
    def on_mouse_press(self, x, y, button, modifiers):
        self.laser = arcade.Sprite("Sprites/laserBlue.png", 0.8)

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

        # Add laser to list and update total laser count
        self.total_lasers += 1
        self.laser_list.append(self.laser)
        self.all_sprite_list.append(self.laser)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player.change_y = player_speedy
        elif key == arcade.key.S:
            self.player.change_y = -player_speedy
        elif key == arcade.key.D:
            self.player.change_x = player_speedx
        elif key == arcade.key.A:
            self.player.change_x = -player_speedx
        elif key == arcade.key.ESCAPE:
            self.director.next_view()       

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S:
            self.player.change_y = 0
        elif key == arcade.key.D or key == arcade.key.A:
            self.player.change_x = 0


class gameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("Sprites/gameOver_screen.jpg")

    def on_show(self):
        pass
    
    def on_draw(self):
        arcade.start_render()

        arcade.draw_texture_rectangle(settings.WIDTH/2, settings.HEIGHT/2,
                                        settings.WIDTH, settings.HEIGHT, self.background)

        arcade.draw_text("Press Enter to Restart", settings.WIDTH/2, settings.HEIGHT/2 - 150,
                        arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Press ESC to Exit Game", settings.WIDTH/2, settings.HEIGHT/2 - 200,
                        arcade.color.WHITE, font_size=20, anchor_x="center")
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            menu_View = ch4_MenuView()
            self.window.show_view(menu_View)
        elif key == arcade.key.ESCAPE:
            self.director.next_view()


class winView(arcade.View):
    def __init__(self):
        super().__init__()
    
    def on_show(self):
        arcade.set_background_color(arcade.color.GHOST_WHITE)
    
    def on_draw(self):
        arcade.start_render()
    
    def on_mouse_press(self, x, y, button, modifiers):
        pass


class Scoreboard(arcade.View):
    def __init__(self):
        super().__init__()
    
    def on_show(self):
        arcade.set_background_color(arcade.color.GHOST_WHITE)
    
    def on_draw(self):
        arcade.start_render()
    
    def update(self, delta_time):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
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
    my_view = gameView()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()

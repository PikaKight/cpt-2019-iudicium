import arcade
import random
import math
import json
from typing import List
import settings


# Player
player_speedx = 5
player_speedy = 5
player_strength = 25
laser_speed = 8

# Health Bar
health_barx = 10
health_bary = 570
health_bar_height = 20
health_bar_width = 200

# Slime
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
    "Draws a fish"
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


def sort_times(numbers: List[int]) -> List[int]:
    """Sort a list of numbers (lowest -> highest)

    Arg:
        numbers: int list (all players' times)
    Returns:
        List of all the players' times in order
    """
    if len(numbers) == 1:
        return numbers

    midpoint = len(numbers)//2

    left_side = sort_times(numbers[:midpoint])
    right_side = sort_times(numbers[midpoint:])
    sorted_list = []

    left_marker = 0
    right_marker = 0
    while left_marker < len(left_side) and right_marker < len(right_side):
        if left_side[left_marker] < right_side[right_marker]:
            sorted_list.append(left_side[left_marker])
            left_marker += 1
        else:
            sorted_list.append(right_side[right_marker])
            right_marker += 1

    while right_marker < len(right_side):
        sorted_list.append(right_side[right_marker])
        right_marker += 1

    while left_marker < len(left_side):
        sorted_list.append(left_side[left_marker])
        left_marker += 1

    return sorted_list


class ch4_MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("Sprites/whiteBorders_blackBackground.jpg")

    def on_draw(self):
        arcade.start_render()

        arcade.draw_texture_rectangle(settings.WIDTH/2, settings.HEIGHT/2,
                                      settings.WIDTH, settings.HEIGHT,
                                      self.background)

        arcade.draw_text("Chapter 4", settings.WIDTH/2, settings.HEIGHT/2 + 50,
                         arcade.color.WHITE, font_size=45, bold=True,
                         anchor_x="center", anchor_y="center")
        arcade.draw_text("Press ENTER to proceed to Game", settings.WIDTH/2,
                         settings.HEIGHT/2, arcade.color.WHITE, font_size=20,
                         anchor_x="center")
        arcade.draw_text("Press ESC to Exit Game", settings.WIDTH/2,
                         settings.HEIGHT/2 - 50, arcade.color.WHITE,
                         font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            instructions_View = Instructions()
            self.window.show_view(instructions_View)
        elif key == arcade.key.ESCAPE:
            arcade.close_window()


class Instructions(arcade.View):
    def __init__(self):
        super().__init__()

        self.background = arcade.load_texture("Sprites/blackBackground.jpg")

        self.slime = arcade.Sprite("Sprites/slimeGreen.png", 0.6)
        self.slime.center_x = settings.WIDTH/2 - 70
        self.slime.center_y = 200
        self.fish = arcade.Sprite("Sprites/fishPink.png", 0.6)
        self.fish.center_x = settings.WIDTH/2 + 70
        self.fish.center_y = 190

    def on_show(self):
        arcade.set_background_color(arcade.color.GHOST_WHITE)

    def on_draw(self):
        arcade.start_render()

        arcade.draw_texture_rectangle(settings.WIDTH/2, settings.HEIGHT/2,
                                      settings.WIDTH, settings.HEIGHT,
                                      self.background)
        arcade.draw_text("INSTRUCTIONS", settings.WIDTH/2,
                         settings.HEIGHT/2 + 150, arcade.color.WHITE,
                         font_size=30, bold=True, anchor_x="center",
                         anchor_y="center")
        arcade.draw_text("""    Use W A S D keys to move around.
    Left-click on the mouse to shoot.


    Slimes are the enemy.

    Fish are food that will recover your health.


    GOAL: Defeat all the enemies as fast as possible using
    the least amount of lasers.
    Press ESC at any time to exit the game.""",
                         settings.WIDTH/2, settings.HEIGHT/2 + 40,
                         arcade.color.WHITE, font_size=15,
                         anchor_x="center", anchor_y="center")

        self.slime.draw()
        self.fish.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            game_View = gameView()
            self.window.show_view(game_View)
        elif key == arcade.key.ESCAPE:
            arcade.close_window()


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
        for i in range(2):
            slime_sprite = Slime("Sprites/slimeGreen.png", 0.5)

            slime_sprite.center_x = random.randrange(5, settings.WIDTH - 5)
            slime_sprite.center_y = random.randrange(5, settings.HEIGHT - 5)
            slime_sprite.change_x = random.randrange(-4, 4)
            slime_sprite.change_y = random.randrange(-4, 4)
            slime_sprite.health = 100
            if slime_sprite.change_x == 0 or slime_sprite.change_y == 0:
                slime_sprite.change_x = 1
                slime_sprite.change_y = -1

            self.slime_list.append(slime_sprite)
            self.all_sprite_list.append(slime_sprite)

    def on_draw(self):
        arcade.start_render()

        # Draw Background
        arcade.draw_texture_rectangle(settings.WIDTH/2, settings.HEIGHT/2,
                                      settings.WIDTH, settings.HEIGHT,
                                      self.background)

        self.all_sprite_list.draw()

        # Calculate time
        minutes = int(self.total_time) // 60
        seconds = int(self.total_time) % 60

        output = f"Time: {minutes:02d}:{seconds:02d}"

        # Timer
        arcade.draw_text(output, settings.WIDTH - 50, settings.HEIGHT - 25,
                         arcade.color.BLACK_LEATHER_JACKET, font_size=15,
                         anchor_x="center")

        # Player Health Bar
        arcade.draw_xywh_rectangle_filled(health_barx, health_bary,
                                          health_bar_width,
                                          health_bar_height,
                                          arcade.color.BLACK)
        arcade.draw_xywh_rectangle_filled(health_barx, health_bary,
                                          self.player_health*2,
                                          health_bar_height,
                                          arcade.color.GUPPIE_GREEN)
        arcade.draw_text(f"{self.player_health}/100", health_barx,
                         health_bary - 25, arcade.color.BLACK,
                         font_size=15)

        # Fish
        fish(self)

    def on_update(self, delta_time):
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
                if arcade.check_for_collision(laser, slime):
                    slime.health -= player_strength
                    laser.remove_from_sprite_lists()

            # Laser flies off screen
                if laser.left > settings.WIDTH or laser.right < 0 or laser.bottom > settings.HEIGHT or laser.top < 0:
                    laser.remove_from_sprite_lists()

        # Slime HP reaches 0
            if slime.health <= 0:
                slime.remove_from_sprite_lists()

        # Player HP reaches 0
        if self.player_health <= 0:
            gameOver_View = gameOverView()
            self.window.show_view(gameOver_View)

        # All slimes defeated
        if len(self.slime_list) == 0:
            with open("chapter_4_scores.json") as json_file:
                data = json.load(json_file)

            game_stats = {"Total Time": round(self.total_time, 2), "Total Damage": self.total_damage, "Total Lasers Used": self.total_lasers}
            data["game_stats"].append(game_stats)

            with open("chapter_4_scores.json", "w") as f:
                json.dump(data, f)

            win_View = winView()
            self.window.show_view(win_View)

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
            arcade.close_window()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S:
            self.player.change_y = 0
        elif key == arcade.key.D or key == arcade.key.A:
            self.player.change_x = 0


class gameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("Sprites/gameOver_screen.jpg")

    def on_draw(self):
        arcade.start_render()

        arcade.draw_texture_rectangle(settings.WIDTH/2, settings.HEIGHT/2,
                                      settings.WIDTH, settings.HEIGHT,
                                      self.background)

        arcade.draw_text("Press Enter to Restart", settings.WIDTH/2,
                         settings.HEIGHT/2 - 150, arcade.color.WHITE,
                         font_size=20, anchor_x="center")
        arcade.draw_text("Press ESC to Exit Game", settings.WIDTH/2,
                         settings.HEIGHT/2 - 200, arcade.color.WHITE,
                         font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            menu_View = ch4_MenuView()
            self.window.show_view(menu_View)
        elif key == arcade.key.ESCAPE:
            arcade.close_window()


class winView(arcade.View):
    def __init__(self):
        super().__init__()

        self.confetti = arcade.Sprite("Sprites/confetti.png", 1)
        self.confetti.center_x = settings.WIDTH/2
        self.confetti.center_y = settings.HEIGHT/2

    def on_show(self):
        arcade.set_background_color(arcade.color.GHOST_WHITE)

    def on_draw(self):
        arcade.start_render()

        self.confetti.draw()

        arcade.draw_text("CONGRATULATIONS! YOU WIN", settings.WIDTH/2,
                         settings.HEIGHT/2 + 100, arcade.color.BLACK,
                         font_size=30, bold=True, anchor_x="center",
                         anchor_y="center")

        # Present Player Score
        with open("chapter_4_scores.json") as json_file:
            data = json.load(json_file)

        arcade.draw_text(f"""Your Score
        Time: {data["game_stats"][-1]}""",
                         settings.WIDTH/2, settings.HEIGHT/2,
                         arcade.color.BLACK, font_size=20,
                         anchor_x="center", anchor_y="center")

        arcade.draw_text("""Press ENTER to see Scoreboard
    
    Press SPACE to Play Again

    Press ESC to Exit Game""", settings.WIDTH/2, settings.HEIGHT/2 - 100,
                         arcade.color.BLACK, font_size=20, anchor_x="center",
                         anchor_y="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            scoreboard_View = Scoreboard()
            self.window.show_view(scoreboard_View)
        elif key == arcade.key.SPACE:
            menu_View = ch4_MenuView()
            self.window.show_view(menu_View)
        elif key == arcade.key.ESCAPE:
            arcade.close_window()


class Scoreboard(arcade.View):
    def __init__(self):
        super().__init__()

        self.menu = arcade.Sprite("Sprites/Menu.png", 0.8)
        self.menu.center_x = settings.WIDTH/2
        self.menu.center_y = settings.HEIGHT/2

        self.sorted_times_list = None

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def update(self, delta_time):
        # Place Player times into separate list
        with open("chapter_4_scores.json") as json_file:
            data = json.load(json_file)

        time_list = []
        for i in data["game_stats"]:
            time_list.append(i["Total Time"])

        # Sort the list of player times
        self.sorted_times_list = sort_times(time_list)

    def on_draw(self):
        arcade.start_render()

        self.menu.draw()

        arcade.draw_text("Scoreboard", self.menu.center_x,
                         self.menu.center_y + 260, arcade.color.BLACK,
                         font_size=30, bold=True, anchor_x="center",
                         anchor_y="center")
        arcade.draw_text("""    Shortest amount of time
    taken to complete the game:""", self.menu.center_x,
                         self.menu.center_y + 190, arcade.color.BLACK,
                         font_size=15, anchor_x="center", anchor_y="center")

        n = 0
        l = 130
        for i in self.sorted_times_list:
            a = self.sorted_times_list[n]
            arcade.draw_text(f"{n+1}. {a} s", self.menu.center_x,
                             self.menu.center_y + l, arcade.color.BLACK,
                             font_size=15, anchor_x="center",
                             anchor_y="center")
            n += 1
            l -= 18

            if n == 5:
                break

        # Search through game stats list for first place game stats
        with open("chapter_4_scores.json") as json_file:
            data = json.load(json_file)
        game_stats = data["game_stats"]

        for i in game_stats:
            if i["Total Time"] == self.sorted_times_list[0]:
                arcade.draw_text(f"""       First Place Game Stats:

            Total Damage Recieved: {i["Total Damage"]}
            Total Lasers Used: {i["Total Lasers Used"]}""",
                                 self.menu.center_x, self.menu.center_y,
                                 arcade.color.BLACK, font_size=15,
                                 anchor_x="center", anchor_y="center")

        arcade.draw_text("""Press ESC to Exit Game
        Press ENTER to Play Again""", self.menu.center_x,
                         self.menu.center_y - 220, arcade.color.BLACK,
                         font_size=15, anchor_x="center", anchor_y="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        elif key == arcade.key.ENTER:
            menu_View = ch4_MenuView()
            self.window.show_view(menu_View)


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
    my_view = ch4_MenuView()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()

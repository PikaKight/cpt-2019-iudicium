import arcade

WIDTH = 800
HEIGHT = 600


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.WHITE)

        # If you have sprite lists, you should create them here,
        # and set them to None

        self.sprite1 = arcade.Sprite(center_x=100, center_y=100)
        self.sprite1.texture = arcade.make_soft_square_texture(50, arcade.color.BLACK, outer_alpha=200)
        self.sprite1.change_x = 3

        self.sprite2 = arcade.Sprite(center_x=500, center_y=500)
        self.sprite2.texture = arcade.make_soft_square_texture(100, arcade.color.BLUE, outer_alpha=1)
        self.sprite2.change_y = -3

    def setup(self):
        # Create your sprites and sprite lists here
        pass

    def on_draw(self):
        arcade.start_render()  # keep as first line

        # Draw everything below here.
        self.sprite1.draw()
        self.sprite2.draw()

    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.sprite1.update()
        self.sprite2.update()

        if self.sprite1.collides_with_sprite(self.sprite2):
            self.sprite2.texture = arcade.make_soft_square_texture(50, arcade.color.YELLOW)

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.
        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

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
# Basic arcade shooter

# Imports
import arcade
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Arcade Space Shooter"
SCALING = 2.0


class SpaceShooter(arcade.Window):
    """Space Shooter side scroller game
    Player starts on the left, enemies appear on the right
    Player can move anywhere, but not off screen
    Enemies fly to the left at variable speed
    Collisions end the game
    """

    def __init__(self, width: int, height: int, title: str):
        """Initialize the game"""
        super().__init__(width, height, title)

        # Set up the empty sprite lists
        self.enemies_list = arcade.SpriteList()
        self.clouds_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()

    def setup(self):
        """Get the game ready to play
        """
        print("setup")
        # Set the background color
        arcade.set_background_color(arcade.color.SKY_BLUE)

        # Set up the player
        self.player = arcade.Sprite("pvz_images/zombie_2.png", SCALING)
        self.player.center_y = self.height / 2
        self.player.left = 10
        self.all_sprites.append(self.player)

        # Spawn a new enemy every 0.25 seconds
        arcade.schedule(self.add_enemy, 0.25)

        # Spawn a new cloud every second
        arcade.schedule(self.add_cloud, 1.0)

    def add_enemy(self, delta_time: float):
        """Adds a new enemy to the screen

        Arguments:
            delta_time {float} -- How much time has passed since the last call
        """
        print("add_enemy")
        # First, create the new enemy sprite
        enemy = arcade.Sprite("pvz_images/pea_1.png", SCALING)

        # Set its position to a random height and off screen right
        enemy.left = random.randint(self.width, self.width + 80)
        enemy.top = random.randint(10, self.height - 10)

    def on_draw(self):
        """Draw all game objects
        """
        print("on_draw")
        arcade.start_render()
        self.all_sprites.draw()


# Main code entry point
if __name__ == "__main__":
    # Create a new Space Shooter window
    space_game = SpaceShooter(
        int(SCREEN_WIDTH * SCALING), int(SCREEN_HEIGHT * SCALING), SCREEN_TITLE
    )
    # Setup to play
    space_game.setup()
    # Run the game
    arcade.run()
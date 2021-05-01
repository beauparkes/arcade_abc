# PvZ Game
#

# Imports
import arcade
import random
import os

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "PvZ Game"
SCALING = 2.0

RIGHT_FACING = 0
LEFT_FACING = 1


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]

# Classes

class FlyingSprite(arcade.Sprite):
    """Base class for all flying sprites
    Flying sprites include enemies and clouds
    """

    def update(self):
        """Update the position of the sprite
        When it moves off screen to the left, remove it
        """

        # Move the sprite
        #super().update()

        # Remove us if we're off screen
        #if self.left < 400:
        #    self.remove_from_sprite_lists()


class pvz(arcade.Window):
    """Space Shooter side scroller game
    Player starts on the left, enemies appear on the right
    Player can move anywhere, but not off screen
    Enemies fly to the left at variable speed
    Collisions end the game
    """

    def __init__(self, width: int, height: int, title: str):
        """Initialize the game"""
        super().__init__(width, height, title)

        # Setup the empty sprite lists
        self.pea_list = arcade.SpriteList()
        self.plants_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()

    def setup(self):
        """Get the game ready to play"""

        # Set the background color
        arcade.set_background_color(arcade.color.SKY_BLUE)

        global skill_level
        skill_level = 0

        # setup scoreboard
        self.time = 0
        arcade.schedule(self.set_time, 1)

        # Set mouse vis off
        self.set_mouse_visible(False)

        # Setup the player
        self.player = arcade.Sprite()
        global player_texture
        player_texture = load_texture_pair(resource_path("pvz_images/zombie_2.png"))
        self.player.texture = player_texture[0]
        self.player.scale = SCALING * 0.1
        self.player.center_y = self.height / 2
        self.player.left = 10
        self.all_sprites.append(self.player)

        # Spawn a new plant
        self.add_plant(0)

        # Spawn a new enemy every second
        arcade.schedule(self.add_pea, 2)

        # pvz sound fx
        self.background_music = arcade.load_sound(resource_path("pvz_sounds/Grasswalk.mp3"))

        self.pea_sound = arcade.load_sound(resource_path("pvz_sounds/pea.wav"))

        self.collision_sound = arcade.load_sound(resource_path("pvz_sounds/Collision.wav"))

        # Start the background music
        arcade.play_sound(self.background_music)

        # Unpause everything and reset the collision timer
        self.paused = False
        self.collided = False
        self.collision_timer = 0.0

    def set_time(self, interval):
        self.time += 1

    def add_plant(self, delta_time: float):
        """Adds a new cloud to the screen
        Arguments:
            delta_time {float} -- How much time has passed since the last call
        """

        # First, create the new cloud sprite

        plant = arcade.Sprite(resource_path("pvz_images/plant_2.png"), SCALING*0.05)
        # Set its position to a random height and off screen right
        #spacing = [100, 300, 500, 700, 900]
        plant.right = self.width - 20
        plant.top = 700
        # Add it to the enemies list
        self.plants_list.append(plant)
        self.all_sprites.append(plant)
        plant.velocity = (0, random.randint(-200, -50))

    def add_pea(self, delta_time: float):
        """Adds a new enemy to the screen
        Arguments:
            delta_time {float} -- How much time has passed since the last call
        """

        # Setup pea
        self.pea = FlyingSprite(resource_path("pvz_images/pea_1.png"), SCALING*0.05)

        # Set its position to a random height and off screen right
        self.pea.right = self.width - 170
        self.pea.top = self.plants_list[0].top - 20
        # Set its speed to a random speed heading left
        self.pea.velocity = (random.randint(-200, -50), 0)

        # Add it to the pea list
        self.pea_list.append(self.pea)
        self.all_sprites.append(self.pea)

        # Add sound effect
        arcade.play_sound(self.pea_sound)

        global skill_level
        arcade.unschedule(self.add_pea)
        speedMin = 3
        speedMax = 4
        skill_level = 0
        if self.time > 20:
            speedMin = 2
            speedMax = 4
            skill_level = 1
        if self.time > 40:
            speedMin = 2
            speedMax = 3
            skill_level = 2
        if self.time > 60:
            speedMin = 2
            speedMax = 2
            skill_level = 3
        if self.time > 80:
            speedMin = 1
            speedMax = 2
            skill_level = 4
        if self.time > 100:
            speedMin = 1
            speedMax = 1
            skill_level = 5
        arcade.schedule(self.add_pea, random.randint(speedMin, speedMax))

    def on_key_press(self, symbol: int, modifiers: int):
        """Handle user keyboard input
        Q: Quit the game
        P: Pause the game
        I/J/K/L: Move Up, Left, Down, Right
        Arrows: Move Up, Left, Down, Right
        Arguments:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed
        """
        if symbol == arcade.key.Q:
            # Quit immediately
            arcade.close_window()

        if symbol == arcade.key.P:
            self.paused = not self.paused

        if symbol == arcade.key.I or symbol == arcade.key.UP:
            self.player.change_y = 250
            #arcade.play_sound(self.move_up_sound)

        if symbol == arcade.key.K or symbol == arcade.key.DOWN:
            self.player.change_y = -250
            #arcade.play_sound(self.move_down_sound)

        if symbol == arcade.key.J or symbol == arcade.key.LEFT:
            self.player.change_x = -250
            self.player.texture = player_texture[1]

        if symbol == arcade.key.L or symbol == arcade.key.RIGHT:
            self.player.change_x = 250
            self.player.texture = player_texture[0]

    def on_key_release(self, symbol: int, modifiers: int):
        """Undo movement vectors when movement keys are released
        Arguments:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed
        """
        if (
            symbol == arcade.key.I
            or symbol == arcade.key.K
            or symbol == arcade.key.UP
            or symbol == arcade.key.DOWN
        ):
            self.player.change_y = 0

        if (
            symbol == arcade.key.J
            or symbol == arcade.key.L
            or symbol == arcade.key.LEFT
            or symbol == arcade.key.RIGHT
        ):
            self.player.change_x = 0

    def on_update(self, delta_time: float):
        """Update the positions and statuses of all game objects
        If we're paused, do nothing
        Once everything has moved, check for collisions between
        the player and the list of enemies
        Arguments:
            delta_time {float} -- Time since the last update
        """

        # Did we collide with something earlier? If so, update our timer
        if self.collided:
            self.collision_timer += delta_time
            # If we've paused for two seconds, we can quit
            if self.collision_timer > 5.0:
                arcade.close_window()
            # Stop updating things as well
            return

        # If we're paused, don't update anything
        if self.paused:
            return

        # Did we hit anything? If so, end the game
        if self.player.collides_with_list(self.pea_list):
            arcade.unschedule(self.set_time)
            self.collided = True
            self.collision_timer = 0.0
            arcade.play_sound(self.collision_sound)

        for pea in self.pea_list:
            if pea.left < 0:
              pea.remove_from_sprite_lists()

        # Update everything
        for sprite in self.all_sprites:
            sprite.center_x = int(
                sprite.center_x + sprite.change_x * delta_time
            )
            sprite.center_y = int(
                sprite.center_y + sprite.change_y * delta_time
            )

        # Keep the player on screen
        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0

        # Keep the plant on screen
        if self.plants_list[0].top > self.height:
            self.plants_list[0].velocity = (0, -random.randint(150, 250))
        if self.plants_list[0].bottom < 0:
            self.plants_list[0].velocity = (0, random.randint(150, 250))

    def on_draw(self):
        """Draw all game objects"""

        arcade.start_render()
        self.all_sprites.draw()

        # Put the text on the screen.
        if not self.collided:
            output = f"Score: {self.time}"
            skill = {0: (255,255,255), 1: (50,50,255), 2: (50,180,50), 3: (150,50,255), 4: (150,100,100), 5: (255,50,50)}
            arcade.draw_text(output, self.width/2.3, self.height-50, skill[skill_level], 30)

        if self.collided:
            output = f"Total Score: {self.time}"
            arcade.draw_text(output, self.width/3.5, self.height - self.height/2, arcade.color.WHITE, 100)


if __name__ == "__main__":
    # Create a new Space Shooter window
    space_game = pvz(
        int(SCREEN_WIDTH * SCALING), int(SCREEN_HEIGHT * SCALING), SCREEN_TITLE
    )
    # Setup to play
    space_game.setup()
    # Run the game
    arcade.run()

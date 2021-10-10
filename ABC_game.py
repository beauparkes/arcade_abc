import arcade
import random
import os
import sys
import time
import math
from array import array
from dataclasses import dataclass

# Main constants
WIDTH = 1300
HEIGHT = 1300
TITLE = "BP ABC GAME"
SPRITE_SCALE = 1
ROW = 3
GAME_OVER_SCORE = 0
KEYS = {
    "97": "A",
    "98": "B",
    "99": "C",
    "100": "D",
    "101": "E",
    "102": "F",
    "103": "G",
    "104": "H",
    "105": "I",
    "106": "J",
    "107": "K",
    "108": "L",
    "109": "M",
    "110": "N",
    "111": "O",
    "112": "P",
    "113": "Q",
    "114": "R",
    "115": "S",
    "116": "T",
    "117": "U",
    "118": "v",
    "119": "W",
    "120": "x",
    "121": "Y",
    "122": "Z",
}

# Particle constants
PARTICLE_COUNT = 100000
MIN_FADE_TIME = 0.1
MAX_FADE_TIME = 2.0
antPos = [
    [-0.7,0.35],
    [-0.7,0.35],
    [-0.7,0.0],
    [-0.7,-0.5],
    [-0.65,-0.95],
    [-0.35,-0.95],
    [-0.1,-0.9],
    [-0.1,-0.6],
    [0.02,-0.25],
    [0.025,-0.9],
    [-0.4,-0.95],
]


@dataclass
class Burst:
    """ Track for each burst. """
    buffer: arcade.gl.Buffer
    vao: arcade.gl.Geometry
    start_time: float

def getKey(key):
    str_key = str(key)
    return KEYS[str_key]


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        print("1st {}".format(base_path))
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class MyWindow(arcade.Window):
    """ Main window"""
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        self.burst_list = []

        # Program to visualize the points
        self.program = self.ctx.load_program(
            vertex_shader="shader/vertex_shader.glsl",
            fragment_shader="shader/fragment_shader.glsl",
        )

        self.ctx.enable_only(self.ctx.BLEND)

class mushroom(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.mushroom_images = []
        for i in range(11):
            mush = arcade.load_texture(
                resource_path("abc_images/mush_{}.png".format(i + 1))
            )
            self.mushroom_images.append(mush)
        self.texture = self.mushroom_images[0]

    def update_animation(self, lose_score):
        if lose_score < 11:
            self.texture = self.mushroom_images[lose_score]
        else:
            return

    def row_score_hit(self, lose_score):
        self.texture = self.mushroom_images[lose_score - 1]


class letter:
    def __init__(self):
        pass

    def rand(self):
        self.current_letter_dict = random.choice(list(KEYS.items()))
        let = self.current_letter_dict[1]
        self.current_letter_display = "{0}{1}".format(let.upper(), let.lower())


class MenuView(arcade.View):
    """Class that manages the 'menu' view."""


    def on_resize(self, WIDTH, HEIGHT):
        #super().on_resize(WIDTH, HEIGHT)
        print(f"Window resized to: {WIDTH}, {HEIGHT}")

    
    def on_show(self):
        """Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """Draw the menu"""
        arcade.start_render()
        self.menu_screen = arcade.draw_text(
            "Hit Enter to begin",
            WIDTH / 2,
            HEIGHT / 2,
            arcade.color.GOLDEN_YELLOW,
            font_size=30,
            anchor_x="center",
            font_name='SEGOEPR'
        )

    def on_key_press(self, key, _modifiers):
        """If user hits enter, begin gameview"""
        if key == arcade.key.ENTER:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)


class GameView(arcade.View):
    """Manage the 'game' view for our program."""

    def __init__(self):
        super().__init__()

        # Sprite lists
        self.player_list = None
        self.lose_score = 0
        self.row_score = 0
        self.row_score_max = ROW
        self.playerScore = 0
        self.seed = random.SystemRandom(9)

    def on_resize(self, WIDTH, HEIGHT):
        print(f"Window resized to: {WIDTH}, {HEIGHT}")
        self.on_draw()

    def setup(self):
        """This should set up your game and get it ready to play"""
        self.lose_score = 0
        self.playerScore = 0
        self.player_list = arcade.SpriteList()
        self.mushroom = mushroom()

        self.mushroom.center_x = WIDTH // 2
        self.mushroom.center_y = HEIGHT // 2.75
        self.mushroom.scale = 2
        self.player_list.append(self.mushroom)

        letter.rand(self)

    def on_show(self):
        """Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLUE_GREEN)

    def on_draw(self):
        """Draw everything for the game."""
        arcade.start_render()

        # Draw sprites
        self.player_list.draw()

        arcade.draw_text(
            self.current_letter_display,
            WIDTH / 2,
            HEIGHT / 1.5,
            arcade.color.GOLD,
            font_size=200,
            anchor_x="center",
            font_name='TAHOMA',
        )

        arcade.draw_text(
            "Your Score: {}".format(str(self.playerScore)),
            WIDTH / 1.2,
            HEIGHT / 1.1,
            arcade.color.BLACK,
            font_size=30,
            anchor_x="center",
        )

        #self.window.clear()

        # Set the particle size
        self.window.ctx.point_size = 2 * self.window.get_pixel_ratio()

        # Loop through each burst
        for burst in self.window.burst_list:

            # Set the uniform data
            self.window.program['time'] = time.time() - burst.start_time

            # Render the burst
            burst.vao.render(self.window.program, mode=self.window.ctx.POINTS)
            
    def on_update(self, delta_time):

        self.player_list.update()

        self.player_list.update_animation(self.lose_score)
        if self.lose_score > 10:
            game_over_view = GameOverView()
            self.window.show_view(game_over_view)
        
        temp_list = self.window.burst_list.copy()
        for burst in temp_list:
            if time.time() - burst.start_time > MAX_FADE_TIME:
               self.window.burst_list.remove(burst)

    def on_key_press(self, key, _modifiers):
        """Handle keypresses. In this case, we'll just count a 'space' as
        game over and advance to the game over view."""

        def _gen_initial_data(initial_x, initial_y):
            """ Generate data for each particle """
            for i in range(PARTICLE_COUNT):
                angle = random.gauss(0, 2 * math.pi)
                speed = random.gauss(0.0, 0.3)
                dx = math.sin(angle) * speed
                dy = math.cos(angle) * speed
                red = random.uniform(0.5, 1.0)
                green = random.uniform(0, red)
                blue = 0
                fade_rate = random.uniform(1 / MAX_FADE_TIME, 1 / MIN_FADE_TIME)
                yield initial_x
                yield initial_y
                yield dx
                yield dy
                yield red
                yield green
                yield blue
                yield fade_rate

        def _antExplosion():
            # calculate the coordinates for OpenGL system with
            # 0, 0 at the center.
            x2 = antPos[self.lose_score][0]
            y2 = antPos[self.lose_score][1]
            #print(str(x2) + " " + str(y2))
            #print(self.lose_score)

            # Get initial particle data
            initial_data = _gen_initial_data(x2, y2)

            # Create a buffer with that data
            buffer = self.window.ctx.buffer(data=array('f', initial_data))

            # Create a buffer description that says how the buffer data is formatted.
            buffer_description = arcade.gl.BufferDescription(buffer,
                                                            '2f 2f 3f f',
                                                            ['in_pos',
                                                            'in_vel',
                                                            'in_color',
                                                            'in_fade_rate'])
            # Create our Vertex Attribute Object
            vao = self.window.ctx.geometry([buffer_description])

            # Create the Burst object and add it to the list of bursts
            burst = Burst(buffer=buffer, vao=vao, start_time=time.time())
            self.window.burst_list.append(burst)

        if key != int(self.current_letter_dict[0]):
            self.lose_score += 1
            self.row_score = 0

        if key == int(self.current_letter_dict[0]):
            self.playerScore += 1
            self.row_score += 1
            if self.row_score == self.row_score_max and self.lose_score > 0:
                self.lose_score -= 1
                self.mushroom.row_score_hit(self.lose_score)
                self.row_score = 0
                _antExplosion()
            if self.row_score == self.row_score_max and self.lose_score == 0:
                self.row_score = 0
            global GAME_OVER_SCORE
            GAME_OVER_SCORE = self.playerScore
            letter.rand(self)


class GameOverView(arcade.View):
    """Class to manage the game over view"""

    def on_show(self):
        """Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """Draw the game over view"""
        arcade.start_render()
        arcade.draw_text(
            "Game Over!",
            WIDTH / 2,
            HEIGHT / 1.9,
            arcade.color.WHITE,
            50,
            anchor_x="center",
        )

        arcade.draw_text(
            "Your best score was {}".format(str(GAME_OVER_SCORE)),
            WIDTH / 2,
            HEIGHT / 2.2,
            arcade.color.WHITE,
            font_size=30,
            anchor_x="center",
        )

    def on_key_press(self, key, _modifiers):
        """If user hits escape, go back to the main menu view"""
        if key == arcade.key.ESCAPE:
            menu_view = MenuView()
            self.window.show_view(menu_view)


def main(WIDTH, HEIGHT):
    """Startup"""
    theWindow = MyWindow()
    menu_view = MenuView()
    theWindow.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main(WIDTH, HEIGHT)

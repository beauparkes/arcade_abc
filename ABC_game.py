import arcade
import random
import os
import sys

WIDTH = 1300
HEIGHT = 1300
TITLE = "BP ABC GAME"
SPRITE_SCALE = 1
gameOverScore = 0
keys = {
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


def getKey(key):
    str_key = str(key)
    return keys[str_key]


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        print("1st {}".format(base_path))
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


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
        self.current_letter_dict = random.choice(list(keys.items()))
        let = self.current_letter_dict[1]
        self.current_letter_display = "{0}{1}".format(let.upper(), let.lower())


class MenuView(arcade.View):
    """Class that manages the 'menu' view."""

    def on_show(self):
        """Called when switching to this view"""
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """Draw the menu"""
        arcade.start_render()
        arcade.draw_text(
            "Menu Screen - Hit Enter to begin",
            WIDTH / 2,
            HEIGHT / 2,
            arcade.color.BLACK,
            font_size=30,
            anchor_x="center",
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
        self.row_score_max = 10
        self.playerScore = 0
        self.seed = random.SystemRandom(9)

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
            arcade.color.BLACK,
            font_size=200,
            anchor_x="center",
        )

        arcade.draw_text(
            "Your Score: {}".format(str(self.playerScore)),
            WIDTH / 1.2,
            HEIGHT / 1.1,
            arcade.color.BLACK,
            font_size=30,
            anchor_x="center",
        )

    def on_update(self, delta_time):

        self.player_list.update()

        self.player_list.update_animation(self.lose_score)
        if self.lose_score > 10:
            game_over_view = GameOverView()
            self.window.show_view(game_over_view)

    def on_key_press(self, key, _modifiers):
        """Handle keypresses. In this case, we'll just count a 'space' as
        game over and advance to the game over view."""

        # print("row_score = {}".format(self.row_score))
        # print("lose score = {}".format(self.lose_score))

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
            if self.row_score == self.row_score_max and self.lose_score == 0:
                self.row_score = 0
            global gameOverScore
            gameOverScore = self.playerScore
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
            "Your best score was {}".format(str(gameOverScore)),
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


def main():
    """Startup"""
    window = arcade.Window(WIDTH, HEIGHT, TITLE)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()

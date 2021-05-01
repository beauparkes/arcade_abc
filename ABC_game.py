import arcade
# import random
import os
import sys

WIDTH = 800
HEIGHT = 800
TITLE = "BP ABC GAME"
SPRITE_SCALE = 1


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        print("1st {}".format(base_path))
    except Exception:
        base_path = os.path.abspath(".")
        print("1st {}".format(base_path))

    return os.path.join(base_path, relative_path)


class mushroom(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.mushroom_images = []
        for i in range(11):
            mush = arcade.load_texture("abc_images/mush_{}.png".format(i+1))
            self.mushroom_images.append(mush)
        self.texture = self.mushroom_images[0]

    def update_animation(self, score):
        if score:
            if score < 11:
                self.texture = self.mushroom_images[score]
            else:
                return


class MenuView(arcade.View):
    """ Class that manages the 'menu' view. """

    def on_show(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """ Draw the menu """
        arcade.start_render()
        arcade.draw_text("Menu Screen - Click to begin", WIDTH/2, HEIGHT/2,
                         arcade.color.BLACK, font_size=30, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ Use a mouse press to advance to the 'game' view. """
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


class GameView(arcade.View):
    """ Manage the 'game' view for our program. """

    def __init__(self):
        super().__init__()

        # Sprite lists
        self.player_list = None
        self.score = 0

    def setup(self):
        """ This should set up your game and get it ready to play """
        self.score = 0
        self.player_list = arcade.SpriteList()
        self.mushroom = mushroom()

        self.mushroom.center_x = WIDTH // 2
        self.mushroom.center_y = HEIGHT // 2
        self.mushroom.scale = 1
        self.player_list.append(self.mushroom)

    def on_show(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.ORANGE_PEEL)

    def on_draw(self):
        """ Draw everything for the game. """
        arcade.start_render()

        # Draw sprites
        self.player_list.draw()

    def on_update(self, delta_time):

        self.player_list.update()

        self.player_list.update_animation(self.score)
        if self.score > 10:
            game_over_view = GameOverView()
            self.window.show_view(game_over_view)

    def on_key_press(self, key, _modifiers):
        """ Handle keypresses. In this case, we'll just count a 'space' as
        game over and advance to the game over view. """

        if key != arcade.key.SPACE:
            self.score += 1

        if key == arcade.key.SPACE:
            game_over_view = GameOverView()
            self.window.show_view(game_over_view)


class GameOverView(arcade.View):
    """ Class to manage the game over view """
    def on_show(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """ Draw the game over view """
        arcade.start_render()
        arcade.draw_text("Game Over!", WIDTH/2, HEIGHT/2,
                         arcade.color.WHITE, 30, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        """ If user hits escape, go back to the main menu view """
        if key == arcade.key.ESCAPE:
            menu_view = MenuView()
            self.window.show_view(menu_view)


def main():
    """ Startup """
    window = arcade.Window(WIDTH, HEIGHT, TITLE)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()

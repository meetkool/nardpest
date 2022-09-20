"""
sniffpest - a clone of a game i never played
"""
import arcade
import random
import math

OUTER_POINTS = ((288, 135),
                (360, 175),
                (420, 230),
                (466, 355),
                (445, 560),
                (380, 610),
                (260, 625),
                (107, 575),
                (70,  530),
                (90,  324),
                (140, 225),
                (220, 168))

INNER_POINTS = ((277, 324),
                (292, 332),
                (305, 345),
                (315, 370),
                (310, 416),
                (292, 425),
                (270, 428),
                (239, 420),
                (233, 410),
                (235, 363),
                (246, 341),
                (262, 329))

LINE_COLOR = arcade.color.BRIGHT_GREEN
PLAYER_COLOR = arcade.color.CANDY_APPLE_RED


def midpoint(p1, p2):
    x = (p1[0] + p2[0]) / 2
    y = (p1[1] + p2[1]) / 2
    return x, y


class Laser:
    def __init__(self, position):
        p1 = position
        p2 = (position + 1) % len(OUTER_POINTS)
        self.start = midpoint(OUTER_POINTS[p1], OUTER_POINTS[p2])
        self.target = midpoint(INNER_POINTS[p1], INNER_POINTS[p2])
        self.angle = math.atan2(-(self.target[1] - self.start[1]),
                                self.target[0] - self.start[0])
        self.current = self.start
        self.speed = 10

    def update(self):
        """ move towards center """
        d_y = -self.speed * math.sin(self.angle)
        d_x = self.speed * math.cos(self.angle)
        self.current = (self.current[0] + d_x, self.current[1] + d_y)

    def draw(self):
        arcade.draw_circle_filled(*self.current, 3, arcade.color.ANDROID_GREEN)


class Enemy:
    def __init__(self, position):
        p1 = position
        p2 = (position + 1) % len(INNER_POINTS)
        self.start = midpoint(INNER_POINTS[p1], INNER_POINTS[p2])
        self.target = midpoint(OUTER_POINTS[p1], OUTER_POINTS[p2])
        self.angle = math.atan2(-(self.target[1] - self.start[1]),
                                self.target[0] - self.start[0])
        self.current = self.start
        self.speed = 0.8

    def update(self):
        """ move towards outer """
        d_y = -self.speed * math.sin(self.angle)
        d_x = self.speed * math.cos(self.angle)
        self.current = (self.current[0] + d_x, self.current[1] + d_y)

    def draw(self):
        arcade.draw_circle_filled(*self.current, 10, arcade.color.CADMIUM_RED)


class Sniffpest(arcade.Window):
    """ da fuckin game """
    def __init__(self, width, height, title):
        """ init """
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)

        self.player_pos = 0
        self.l0dey_alpha = 0
        self.lasers = None
        self.enemies = None
        self.score = 0
        self.laser_sound = None
        self.bg_music = None

    def setup(self):
        """ reset the level """
        self.player_pos = 0
        self.l0dey_alpha = 0
        self.lasers = []
        self.enemies = []
        self.score = 0
        self.laser_sound = arcade.load_sound(':resources:sounds/laser2.wav')
        self.bg_music = arcade.Sound('unh.mp3', streaming=True)
        self.bg_music.play()
        arcade.schedule(self.add_enemy, 2)

    def on_update(self, delta_time):
        """ called on every update """
        for laser in self.lasers:
            laser.update()
            if arcade.is_point_in_polygon(*laser.current, INNER_POINTS):
                self.lasers.remove(laser)
        for enemy in self.enemies:
            enemy.update()
            for laser in self.lasers:
                if arcade.get_distance(*laser.current, *enemy.current) < 10:
                    self.enemies.remove(enemy)
                    self.lasers.remove(laser)
                    self.score += 1
        self.l0dey_alpha = self.score

    def on_draw(self):
        """ draw da fuckin screen """
        arcade.start_render()
        # l0dey
        l0dey = arcade.load_texture('l0de.png')
        arcade.draw_texture_rectangle(550 / 2, 750 / 2, 512, 512,
                                      l0dey, 0, self.l0dey_alpha)
        # gameboard
        arcade.draw_polygon_outline(OUTER_POINTS, LINE_COLOR, 2)
        arcade.draw_polygon_outline(INNER_POINTS, LINE_COLOR, 2)
        for outer_point, inner_point in zip(OUTER_POINTS, INNER_POINTS):
            arcade.draw_line(*outer_point, *inner_point, LINE_COLOR, 1)
        # player
        p1 = self.player_pos
        p2 = (self.player_pos + 1) % len(OUTER_POINTS)
        p1 = OUTER_POINTS[p1]
        p2 = OUTER_POINTS[p2]
        arcade.draw_line(*p1, *p2, PLAYER_COLOR, 10)
        # lasers
        for laser in self.lasers:
            laser.draw()
        for enemy in self.enemies:
            enemy.draw()

        arcade.draw_text(f'Score: {self.score}', 10, 10, arcade.color.WHITE)

    def on_key_press(self, key, modifier):
        """ handle key presses """
        # Q or Esc to quit
        if key in (arcade.key.Q, arcade.key.ESCAPE):
            arcade.close_window()
        # Move around the board
        if key == arcade.key.LEFT:
            self.player_pos = (self.player_pos + 1) % len(OUTER_POINTS)
        elif key == arcade.key.RIGHT:
            self.player_pos = (self.player_pos - 1) % len(OUTER_POINTS)
        # Shoot yer lasers
        if key == arcade.key.SPACE:
            laser = Laser(self.player_pos)
            self.lasers.append(laser)
            self.laser_sound.play()

    def add_enemy(self, delta_time):
        position = random.randrange(len(OUTER_POINTS))
        enemy = Enemy(position)
        self.enemies.append(enemy)

if __name__ == '__main__':
    sniffpest = Sniffpest(550, 750, 'Sniffpest')
    sniffpest.setup()
    arcade.run()

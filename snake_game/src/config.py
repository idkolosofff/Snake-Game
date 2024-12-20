#MAIN
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
LOCAL_IP = '127.0.0.1'

#MENU
MENU_OPTIONS = [("1", "Start New Game"), ("2", "Multiplayer"), ("3", "Show Personal Records"), ("4", "Colors"), ("5", "Quit")]
TITLE_FONT = 48
MENU_FONT = 36

TITLE_HEIGHT = 80
CAPTION_HEIGHT = 160
OPTIONS_HEIGHT_GAP = 40
OPTIONS_HEIGHT_POS = 60

#COLORS

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
CYAN = (0, 200, 200)
LIGHT_BROWN = (204, 102, 0)
GREY = (50, 50, 50)
LIGHT_BLUE = (0, 128, 255)
GOLDEN = (252, 252, 20)
BROWN = (51, 25, 0)
BLUE = (0, 0, 255)
PINK = (255, 51, 255)
YELLOW = (255, 255, 0)
PURPLE = (178, 102, 255)
ORANGE = (255, 153, 51)
ROYAL_PURPLE = (102, 0, 204)

DEFAULT_SNAKE_COLOR = GREEN

COLOR_OPTIONS = [
    GREEN,
    RED,
    BLUE,
    PINK,
    YELLOW,
    PURPLE,
    ORANGE
]
COLOR_NAMES = [
    "GREEN",
    "RED",
    "BLUE",
    "PINK",
    "YELLOW",
    "PURPLE",
    "ORANGE"
]

#GAME
PANEL_HEIGHT = 50
BONUS_SPAWN_INTERVAL = 20000
SCREEN_EDGE_SIZE = 20

UP = (0, 1)
DOWN = (0, -1)
LEFT = (1, 0)
RIGHT = (-1, 0)

GAME_OVER_DELAY = 1000 # milliseconds

SNAKE_GROWTH_RATE = 10
SNAKE_INCREMENT = 200 # Determines when the tail starts to calculate collision
TERRAIN_SLOW_RATE = 0.999
TERRAIN_SPEEDUP_RATE = 1.0003
HOLY_GRAIL_ADD = 0.1
UPDATE_DELAY = 5
BONUS_POINTS = 5
CLOCK_TICK = 120

#SNAKE
START_POS = (400, 300)
SNAKE_SIZE = 14
START_SPEED = 4
HEAD_SPEED_PARAMETER = 4
PASSIVE_SPEED_INCREMENT = 0.00005
DEFAULT_SPEED_FACTOR = 1.2
DEFAULT_SLOW_FACTOR = 0.5
#DRAWING
PANEL_BORDER_THICKNESS = 2
PANEL_FONT = 18

POINTS_POS = 10
LENGTH_POS = 150
SPEED_POS = 290
TIME_POS = 430
#FOOD
FOOD_SIZE = 20

#BONUS
DEFAULT_BONUS_SIZE = 15
BONUS_SIZES = {
    "speed_up": 15,
    "add_points": 10,
    "slow_down": 5
}

#TERRAIN
TERRAIN_SIZES = {
    "speed_up": 35,
    "wall": 50,
    "slow_down": 25,
    "mushroom": 10,
    "holy_grail" : 3
}
TERRAIN_COLORS = {
    "speed_up": CYAN,
    "wall": WHITE,
    "slow_down": LIGHT_BROWN,
    "mushroom": ROYAL_PURPLE,
    "holy_grail" : BLACK
}
DEFAULT_TERRAIN_SIZE = 20
GRAIL_CHANGE_TIME = 60000
MUSHROOM_GROW_TIME = 50000

#LEVEL_SELECTION
LEVELS_LINES_GAP = 40
LEVELS_TEXT_HEIGHT = 60
LEVELS_FONT = 36

#COLOR_SELECTION
COLOR_TITLE_HEIGHT = 50
OPTION_SPACING = 50
COLOR_OPTION_X = 100
COLOR_OPTION_Y = 100
COLOR_SIZE = 30
CLR_TEXT_DIST = 20

#HIGHSCORE
SCORES_LINES_GAP = 40
SCORES_TEXT_HEIGHT = 160
TOP_SELECTION = 10
SCORE_FONT = 36

#MULTIPLAYER
MULTIPLAYER_OPTIONS = [
    ("1", "Host Game"),
    ("2", "Join Game"),
    ("3", "Back"),
]
DEFAULT_LEVEL = 1
WAIT_LIST_SIZE = 5
BYTES_RECV = 4096
MAGIC_NUMBER = b'SKNG'  # 4-byte magic number for message validation
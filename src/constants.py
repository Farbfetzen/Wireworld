import pygame.freetype


FPS = 60
SPS = 4  # steps per second
SPS_MIN = 1
SPS_MAX = 256

DEEFAULT_WINDOW_SIZE = (1001, 801)  # +1 so that the rightmost and bottommost grid lines are visible
DEFAULT_CELL_WIDTH = 20
CAMERA_MOVE_SPEED_KEYBOARD = 750

BACKGROUND_COLOR = pygame.Color(32, 32, 32)
GRID_COLOR = pygame.Color(64, 64, 64)
MOUSE_HIGHLIGHT_COLOR = pygame.Color(0, 255, 0)
CONDUCTOR_COLOR = pygame.Color(184, 115, 51)
ELECTRON_HEAD_COLOR = pygame.Color(0, 64, 255)
ELECTRON_TAIL_COLOR = pygame.Color(255, 64, 0)

pygame.freetype.init()
DEBUG_FONT = pygame.freetype.SysFont("consolas, inconsolate, monospace", 16)
DEBUG_FONT.pad = True
DEBUG_FONT.fgcolor = (255, 255, 255)
DEBUG_LINE_SPACING = pygame.Vector2(0, DEBUG_FONT.get_sized_height())
DEBUG_MARGIN = pygame.Vector2(5, 5)

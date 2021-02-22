import pygame

from src import cell
from src import constants


class Camera:
    def __init__(self, window_size, cell_width, cells):
        self.window = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Wireworld")
        self.cells = cells
        self.cell_width = cell_width
        self.cell_size = (cell_width, cell_width)
        self.background = self.create_background(window_size)
        self.cell_images = cell.create_cell_images(self.cell_size)  # TODO: Resize images when zooming
        self.mouse_grid_position = None  # highlighted cell coordinates
        self.mouse_position_snapped = None  # mouse position snapped to the grid

    def create_background(self, window_size):
        background = pygame.Surface(window_size)
        background.fill(constants.BACKGROUND_COLOR)
        window_width, window_height = window_size
        for x in range(0, window_width, self.cell_width):
            pygame.draw.line(background, constants.GRID_COLOR, (x, 0), (x, window_height))
        for y in range(0, window_height, self.cell_width):
            pygame.draw.line(background, constants.GRID_COLOR, (0, y), (window_width, y))
        return background

    def update_mouse_positions(self):
        if pygame.mouse.get_focused():
            screen_x, screen_y = pygame.mouse.get_pos()
            grid_x = screen_x // self.cell_width
            grid_y = screen_y // self.cell_width
            self.mouse_grid_position = (grid_x, grid_y)
            self.mouse_position_snapped = (grid_x * self.cell_width, grid_y * self.cell_width)
        else:
            self.mouse_grid_position = None
            self.mouse_position_snapped = None

    def draw(self):
        self.window.blit(self.background, (0, 0))

        for c in self.cells.values():
            c.draw(self.window)

        if self.mouse_grid_position is not None:
            pygame.draw.rect(
                self.window,
                constants.MOUSE_HIGHLIGHT_COLOR,
                (self.mouse_position_snapped, self.cell_size),
                1
            )

        pygame.display.flip()

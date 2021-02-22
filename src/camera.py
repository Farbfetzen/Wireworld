import pygame

from src import cell
from src import constants


class Camera:
    def __init__(self, window_size, cell_width, cells):
        self.window_width, self.window_height = window_size
        self.window = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Wireworld")
        self.cells = cells
        self.cell_width = cell_width
        self.cell_size = (cell_width, cell_width)
        self.cell_images = cell.create_cell_images(self.cell_size)  # TODO: Resize images when zooming
        self.mouse_grid_position = None  # highlighted cell coordinates
        self.mouse_position_snapped = None
        self.x_f = 0.
        self.y_f = 0.
        self.rect = pygame.Rect(self.x_f, self.y_f, self.window_width, self.window_height)
        self.rect_for_cell_drawing = pygame.Rect(
            self.x_f,
            self.y_f,
            self.window_width + self.cell_width,
            self.window_height + self.cell_width
        )
        self.rect_for_cell_drawing.bottomright = self.rect.bottomright

    def scroll(self, rel_x, rel_y):
        self.x_f -= rel_x
        self.y_f -= rel_y
        self.rect.topleft = (self.x_f, self.y_f)
        # print(self.rect.topleft)
        # TODO: Should scroll speed depend on zoom level?

        for c in self.cells.values():
            c.update_screen_position(self.rect.x, self.rect.y)

    def scroll_keyboard(self, direction_x, direction_y, dt):
        if direction_x != 0 and direction_y != 0:
            scroll_speed_times_dt = constants.WORLD_SCROLL_SPEED * dt
            self.scroll(
                direction_x * scroll_speed_times_dt,
                direction_y * scroll_speed_times_dt
            )

    def update_mouse_positions(self):
        if pygame.mouse.get_focused():
            # FIXME: Does not work currently. Cells jump around when map is moved.
            #  And highlight rect lags behind grid.

            screen_x, screen_y = pygame.mouse.get_pos()
            world_x, world_y = self.screen_to_world_position(screen_x, screen_y)
            grid_x = world_x // self.cell_width
            grid_y = world_y // self.cell_width
            self.mouse_grid_position = (grid_x, grid_y)
            # screen_x, screen_y = self.world_to_screen_position(grid_x * self.cell_width, grid_y * self.cell_width)
            # self.mouse_position_snapped = (screen_x // self.cell_width * self.cell_width, screen_y // self.cell_width * self.cell_width)
            self.mouse_position_snapped = self.world_to_screen_position(grid_x * self.cell_width, grid_y * self.cell_width)
            # print(self.mouse_position_snapped)
        else:
            self.mouse_grid_position = None
            self.mouse_position_snapped = None

    def screen_to_world_position(self, screen_x, screen_y):
        return screen_x + self.rect.x, screen_y + self.rect.y

    def world_to_screen_position(self, world_x, world_y):
        return world_x - self.rect.x, world_y - self.rect.y

    def draw(self):
        self.window.fill(constants.BACKGROUND_COLOR)
        self.draw_grid()
        self.draw_cells()

        if self.mouse_position_snapped is not None:
            pygame.draw.rect(
                self.window,
                constants.MOUSE_HIGHLIGHT_COLOR,
                (self.mouse_position_snapped, self.cell_size),
                1
            )

        pygame.draw.circle(self.window, (255, 0, 0), self.world_to_screen_position(0, 0), 2)

        pygame.display.flip()

    def draw_grid(self):
        for x in range(self.cell_width - (self.rect.x % self.cell_width),
                       self.rect.width,
                       self.cell_width):
            pygame.draw.line(self.window, constants.GRID_COLOR, (x, 0), (x, self.window_height))

        for y in range(self.cell_width - (self.rect.y % self.cell_width),
                       self.rect.height,
                       self.cell_width):
            pygame.draw.line(self.window, constants.GRID_COLOR, (0, y), (self.window_width, y))

    def draw_cells(self):
        for c in self.cells.values():
            if c.is_visible(self.rect_for_cell_drawing):
                self.window.blit(c.image, (c.screen_position_x, c.screen_position_y))

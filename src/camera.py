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
        self.cell_images = cell.create_cell_images(self.cell_size)
        self.mouse_grid_position = None
        self.mouse_position_snapped = None
        self.x_f = 0.
        self.y_f = 0.
        self.rect = pygame.Rect(self.x_f, self.y_f, self.window_width, self.window_height)
        self.rect_for_cell_drawing = self.rect.copy()

        self.show_debug_info = False
        self.debug_font = pygame.freetype.SysFont(
            "consolas, inconsolate, monospace",
            16
        )
        self.debug_font.pad = True
        self.debug_font.fgcolor = (255, 255, 255)
        self.debug_line_spacing = pygame.Vector2(
            0, self.debug_font.get_sized_height()
        )
        self.debug_margin = pygame.Vector2(5, 5)
        self.n_visible_cells = 0

    def scroll(self, rel_x, rel_y):
        self.x_f -= rel_x
        self.y_f -= rel_y
        self.rect.topleft = (self.x_f, self.y_f)
        # TODO: Should scroll speed depend on zoom level?

        for c in self.cells.values():
            c.update_screen_position()

    def scroll_keyboard(self, direction_x, direction_y, dt):
        # TODO: Implement this. See code in project dimetric.
        pass

    def zoom(self):
        # TODO: Implement this. With mouse wheel and keyboard.
        pass

    def update_mouse_positions(self):
        if pygame.mouse.get_focused():
            screen_x, screen_y = pygame.mouse.get_pos()
            grid_x = (screen_x + self.rect.x) // self.cell_width
            grid_y = (screen_y + self.rect.y) // self.cell_width
            self.mouse_grid_position = (grid_x, grid_y)
            self.mouse_position_snapped = (
                grid_x * self.cell_width - self.rect.x,
                grid_y * self.cell_width - self.rect.y
            )
        else:
            self.mouse_grid_position = None
            self.mouse_position_snapped = None

    def world_to_screen_position(self, world_x, world_y):
        return world_x - self.rect.x, world_y - self.rect.y

    def draw(self):
        self.window.fill(constants.BACKGROUND_COLOR)
        self.draw_grid()
        self.draw_cells()
        if self.mouse_position_snapped is not None:
            self.draw_mouse_rect()
        if self.show_debug_info:
            self.draw_debug_info()
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
        visible_cells = self.rect_for_cell_drawing.collidedictall(self.cells, True)
        for _, c in visible_cells:
            self.window.blit(c.image, c.rect)
        self.n_visible_cells = len(visible_cells)

    def draw_mouse_rect(self):
        pygame.draw.rect(
            self.window,
            constants.MOUSE_HIGHLIGHT_COLOR,
            (self.mouse_position_snapped, self.cell_size),
            1
        )

    def draw_debug_info(self):
        pygame.draw.circle(self.window, (255, 0, 0), self.world_to_screen_position(0, 0), 3)
        self.debug_font.render_to(
            self.window,
            self.debug_margin,
            f"mouse grid position: {self.mouse_grid_position}"
        )
        self.debug_font.render_to(
            self.window,
            self.debug_margin + self.debug_line_spacing,
            f"mouse position snapped: {self.mouse_position_snapped}"
        )
        self.debug_font.render_to(
            self.window,
            self.debug_margin + self.debug_line_spacing * 2,
            f"number of visible cells: {self.n_visible_cells}"
        )

import pygame

from src import constants


class Camera:
    def __init__(self, window_size, cell_width, cell_size, cells):
        self.window_width, self.window_height = window_size
        self.window = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Simulation")
        self.cells = cells
        self.cell_width = cell_width
        self.cell_size = cell_size
        self.mouse_grid_position = (0, 0)
        self.mouse_rect = pygame.Rect(self.mouse_grid_position, cell_size)
        self.mouse_is_in_window = pygame.mouse.get_focused()
        self.position = pygame.Vector2()
        self.rect = self.window.get_rect()
        self.rect_for_cell_drawing = self.rect.copy()
        self.keyboard_scoll_direction = pygame.Vector2()
        self.keyboard_scroll_speed = pygame.Vector2(constants.KEYBOARD_SCROLL_SPEED)

        self.show_debug_info = False
        self.n_visible_cells = 0

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                self.show_debug_info = not self.show_debug_info
            elif event.key == pygame.K_w:
                self.keyboard_scoll_direction.y += 1
            elif event.key == pygame.K_a:
                self.keyboard_scoll_direction.x += 1
            elif event.key == pygame.K_s:
                self.keyboard_scoll_direction.y -= 1
            elif event.key == pygame.K_d:
                self.keyboard_scoll_direction.x -= 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.keyboard_scoll_direction.y -= 1
            elif event.key == pygame.K_a:
                self.keyboard_scoll_direction.x -= 1
            elif event.key == pygame.K_s:
                self.keyboard_scoll_direction.y += 1
            elif event.key == pygame.K_d:
                self.keyboard_scoll_direction.x += 1
        elif event.type == pygame.MOUSEMOTION and event.buttons[2]:  # 2 = right mouse button
            self.scroll(event.rel)

    def update(self, dt):
        if self.keyboard_scoll_direction != (0, 0):
            self.scroll(
                self.keyboard_scoll_direction.elementwise()
                * self.keyboard_scroll_speed
                * dt
            )

    def scroll(self, rel):
        self.position -= rel
        self.rect.topleft = self.position
        # TODO: Should scroll speed depend on zoom level?
        for cell in self.cells.values():
            cell.update_screen_position()

    def zoom(self):
        # TODO: Implement this. With mouse wheel and keyboard.
        pass

    def update_mouse_position(self):
        if pygame.mouse.get_focused():
            self.mouse_is_in_window = True
            screen_x, screen_y = pygame.mouse.get_pos()
            grid_x = (screen_x + self.rect.x) // self.cell_width
            grid_y = (screen_y + self.rect.y) // self.cell_width
            self.mouse_grid_position = (grid_x, grid_y)
            self.mouse_rect.topleft = (
                grid_x * self.cell_width - self.rect.x,
                grid_y * self.cell_width - self.rect.y
            )
        else:
            self.mouse_is_in_window = False

    def world_to_screen_position(self, world_x, world_y):
        return world_x - self.rect.x, world_y - self.rect.y

    def draw(self):
        self.window.fill(constants.BACKGROUND_COLOR)
        self.draw_grid()
        self.draw_cells()
        if self.mouse_is_in_window:
            pygame.draw.rect(self.window, constants.MOUSE_HIGHLIGHT_COLOR, self.mouse_rect, 1)
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
        for _, cell in visible_cells:
            self.window.blit(cell.image, cell.rect)
        self.n_visible_cells = len(visible_cells)

    def draw_debug_info(self):
        pygame.draw.circle(self.window, (255, 0, 0), self.world_to_screen_position(0, 0), 3)
        constants.DEBUG_FONT.render_to(
            self.window,
            constants.DEBUG_MARGIN,
            f"mouse grid position: {self.mouse_grid_position}"
        )
        constants.DEBUG_FONT.render_to(
            self.window,
            constants.DEBUG_MARGIN + constants.DEBUG_LINE_SPACING,
            f"mouse rect screen position: {self.mouse_rect.topleft}"
        )
        constants.DEBUG_FONT.render_to(
            self.window,
            constants.DEBUG_MARGIN + constants.DEBUG_LINE_SPACING * 2,
            f"number of visible cells: {self.n_visible_cells}"
        )

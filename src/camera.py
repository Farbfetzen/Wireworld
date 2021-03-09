import pygame

from src.constants import *


class Camera:
    def __init__(self, window_size, cell_width, cell_size, cells):
        self.window_width, self.window_height = window_size
        self.window = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Wireworld")
        self.cells = cells
        self.cell_width = cell_width
        self.cell_size = cell_size
        self.mouse_grid_position = (0, 0)  # no Vector2 because I want integers
        self.mouse_rect = pygame.Rect(self.mouse_grid_position, cell_size)
        self.mouse_screen_position = pygame.Vector2()
        self.position = pygame.Vector2()
        self.zoom_level_current = 1
        self.zoom_level_new = self.zoom_level_current
        self.rect = self.window.get_rect()
        self.surface = pygame.Surface(self.rect.size)
        self.test_rect = self.rect.copy()  # DEBUG
        self.rect_for_cell_drawing = self.rect.copy()
        self.keyboard_move_direction = pygame.Vector2()
        self.mouse_movement_rel = pygame.Vector2()
        self.n_visible_cells = 0

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.keyboard_move_direction.y += 1
            elif event.key == pygame.K_a:
                self.keyboard_move_direction.x += 1
            elif event.key == pygame.K_s:
                self.keyboard_move_direction.y -= 1
            elif event.key == pygame.K_d:
                self.keyboard_move_direction.x -= 1
            elif event.key == pygame.K_PAGEUP:
                self.zoom_level_new += CAMERA_ZOOM_STEP
            elif event.key == pygame.K_PAGEDOWN:
                self.zoom_level_new -= CAMERA_ZOOM_STEP
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.keyboard_move_direction.y -= 1
            elif event.key == pygame.K_a:
                self.keyboard_move_direction.x -= 1
            elif event.key == pygame.K_s:
                self.keyboard_move_direction.y += 1
            elif event.key == pygame.K_d:
                self.keyboard_move_direction.x += 1
        elif event.type == pygame.MOUSEMOTION and event.buttons[2]:  # 2 = right mouse button
            self.mouse_movement_rel += event.rel
        elif event.type == pygame.MOUSEWHEEL:
            self.zoom_level_new += event.y * CAMERA_ZOOM_STEP

    def update(self, dt):
        # I collect all move and zoom events before updating the camera
        # because there often are multiple such events per frame.
        self.move(dt)
        self.zoom()

        self.update_mouse_position()  # must be done AFTER moving and zooming the camera!

    def move(self, dt):
        distance = (self.mouse_movement_rel
                    + self.keyboard_move_direction
                    * CAMERA_MOVE_SPEED_KEYBOARD
                    * dt)
        if distance != (0, 0):
            self.position -= distance
            self.rect.topleft = self.position
            # TODO: Should move speed depend on zoom level?
            for cell in self.cells.values():
                cell.update_screen_position()
            self.mouse_movement_rel.update(0, 0)

    def zoom(self):
        self.zoom_level_new = max(min(self.zoom_level_new, CAMERA_ZOOM_MAX), CAMERA_ZOOM_MIN)
        if self.zoom_level_new != self.zoom_level_current:
            diff = self.zoom_level_new - self.zoom_level_current
            self.test_rect.inflate_ip(self.rect.width * diff, self.rect.height * diff)
            self.zoom_level_current = self.zoom_level_new

    def update_mouse_position(self):
        screen_x, screen_y = pygame.mouse.get_pos()
        grid_x = (screen_x + self.rect.x) // self.cell_width
        grid_y = (screen_y + self.rect.y) // self.cell_width
        self.mouse_grid_position = (grid_x, grid_y)
        self.mouse_rect.topleft = (
            grid_x * self.cell_width - self.rect.x,
            grid_y * self.cell_width - self.rect.y
        )

    def world_to_screen_position(self, world_x, world_y):
        return world_x - self.rect.x, world_y - self.rect.y

    def draw(self, debug_mode, fps):
        self.window.fill(BACKGROUND_COLOR)
        self.draw_grid()
        self.draw_cells()
        pygame.draw.rect(self.window, MOUSE_HIGHLIGHT_COLOR, self.mouse_rect, 1)
        if debug_mode:
            self.draw_debug_info(fps)

        pygame.draw.rect(self.window, MOUSE_HIGHLIGHT_COLOR, self.test_rect, 1)

        pygame.display.flip()

    def draw_grid(self):
        for x in range(self.cell_width - (self.rect.x % self.cell_width),
                       self.rect.width,
                       self.cell_width):
            pygame.draw.line(self.window, GRID_COLOR, (x, 0), (x, self.window_height))

        for y in range(self.cell_width - (self.rect.y % self.cell_width),
                       self.rect.height,
                       self.cell_width):
            pygame.draw.line(self.window, GRID_COLOR, (0, y), (self.window_width, y))

    def draw_cells(self):
        visible_cells = self.rect_for_cell_drawing.collidedictall(self.cells, True)
        for _, cell in visible_cells:
            self.window.blit(cell.image, cell.rect)
        self.n_visible_cells = len(visible_cells)

    def draw_debug_info(self, fps):
        pygame.draw.circle(self.window, (255, 0, 0), self.world_to_screen_position(0, 0), 3)
        DEBUG_FONT.render_to(
            self.window,
            DEBUG_MARGIN,
            f"fps: {fps:.0f}"
        )
        DEBUG_FONT.render_to(
            self.window,
            DEBUG_MARGIN + DEBUG_LINE_SPACING,
            f"mouse grid position: {self.mouse_grid_position}"
        )
        DEBUG_FONT.render_to(
            self.window,
            DEBUG_MARGIN + DEBUG_LINE_SPACING * 2,
            f"mouse rect screen position: {self.mouse_rect.topleft}"
        )
        DEBUG_FONT.render_to(
            self.window,
            DEBUG_MARGIN + DEBUG_LINE_SPACING * 3,
            f"number of visible cells: {self.n_visible_cells}"
        )
        DEBUG_FONT.render_to(
            self.window,
            DEBUG_MARGIN + DEBUG_LINE_SPACING * 4,
            f"zoom level: {self.zoom_level_current:.2f}"
        )

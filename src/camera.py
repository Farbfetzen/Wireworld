import pygame

from src.constants import *


class Camera:
    def __init__(self, window_size, cells):
        self.window_width, self.window_height = window_size
        self.window = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Wireworld")
        self.cells = cells
        self.mouse_grid_position = (0, 0)  # no Vector2 because I want integers
        self.mouse_rect = pygame.Rect(self.mouse_grid_position, CELL_SIZE)
        self.mouse_screen_position = pygame.Vector2()
        self.zoom_level = CAMERA_DEFAULT_ZOOM_LEVEL
        self.zoom_level_new = self.zoom_level
        self.window_size = self.window.get_size()
        self.surface_rect = self.window.get_rect()
        self.surface = pygame.Surface(self.surface_rect.size)
        self.position = pygame.Vector2(self.surface_rect.center)
        self.keyboard_move_amount = pygame.Vector2()
        self.mouse_movement_rel = pygame.Vector2()
        self.camera_has_changed = False
        self.n_visible_cells = 0  # for debugging

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.keyboard_move_amount.y += CAMERA_MOVE_SPEED_KEYBOARD
            elif event.key == pygame.K_a:
                self.keyboard_move_amount.x += CAMERA_MOVE_SPEED_KEYBOARD
            elif event.key == pygame.K_s:
                self.keyboard_move_amount.y -= CAMERA_MOVE_SPEED_KEYBOARD
            elif event.key == pygame.K_d:
                self.keyboard_move_amount.x -= CAMERA_MOVE_SPEED_KEYBOARD
            elif event.mod & pygame.KMOD_CTRL:
                if event.key in (pygame.K_PLUS, pygame.K_KP_PLUS):
                    self.zoom_level_new -= CAMERA_ZOOM_STEP
                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    self.zoom_level_new += CAMERA_ZOOM_STEP
                elif event.key in (pygame.K_0, pygame.K_KP_0):
                    self.zoom_level_new = CAMERA_DEFAULT_ZOOM_LEVEL
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.keyboard_move_amount.y -= CAMERA_MOVE_SPEED_KEYBOARD
            elif event.key == pygame.K_a:
                self.keyboard_move_amount.x -= CAMERA_MOVE_SPEED_KEYBOARD
            elif event.key == pygame.K_s:
                self.keyboard_move_amount.y += CAMERA_MOVE_SPEED_KEYBOARD
            elif event.key == pygame.K_d:
                self.keyboard_move_amount.x += CAMERA_MOVE_SPEED_KEYBOARD
        elif event.type == pygame.MOUSEMOTION and event.buttons[2]:  # right mouse button
            self.mouse_movement_rel += event.rel
        elif event.type == pygame.MOUSEWHEEL:
            self.zoom_level_new -= event.y * CAMERA_ZOOM_STEP
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:  # middle mouse button
            self.zoom_level_new = CAMERA_DEFAULT_ZOOM_LEVEL

    def update(self, dt):
        # I collect all move and zoom events before updating the camera
        # because there often are multiple such events per frame. That's why
        # I move and zoom here in update() and not in process_event().
        self.move(dt)
        self.zoom()
        if self.camera_has_changed:
            for cell in self.cells.values():
                cell.update_screen_position(self.surface_rect.topleft)
            self.camera_has_changed = False

        self.update_mouse_position()  # Must be done AFTER moving and zooming the camera!

    def move(self, dt):
        distance = self.mouse_movement_rel + self.keyboard_move_amount * dt
        if distance != (0, 0):
            distance *= self.zoom_level
            self.position -= distance
            self.surface_rect.center = self.position
            self.mouse_movement_rel.update(0, 0)
            self.camera_has_changed = True

    def zoom(self):
        self.zoom_level_new = max(min(self.zoom_level_new, CAMERA_ZOOM_MAX), CAMERA_ZOOM_MIN)
        if self.zoom_level_new != self.zoom_level:
            diff = self.zoom_level_new - self.zoom_level
            self.surface_rect.inflate_ip(self.window_size[0] * diff, self.window_size[1] * diff)
            self.surface = pygame.Surface(self.surface_rect.size)
            self.zoom_level = self.zoom_level_new
            self.camera_has_changed = True

    def screen_to_world_position(self, screen_x, screen_y):
        return (
            screen_x * self.zoom_level + self.surface_rect.x,
            screen_y * self.zoom_level + self.surface_rect.y,
        )

    def world_to_screen_position(self, world_x, world_y):
        return (
            (world_x - self.surface_rect.x) / self.zoom_level,
            (world_y - self.surface_rect.y) / self.zoom_level
        )

    def update_mouse_position(self):
        world_x, world_y = self.screen_to_world_position(*pygame.mouse.get_pos())
        grid_x = world_x // CELL_WIDTH
        grid_y = world_y // CELL_WIDTH
        self.mouse_grid_position = (grid_x, grid_y)
        # Note that mouse_rect is positioned on the surface, not the window.
        # Therefore the zoom level is irrelevant here.
        self.mouse_rect.topleft = (
            grid_x * CELL_WIDTH - self.surface_rect.x,
            grid_y * CELL_WIDTH - self.surface_rect.y
        )

    def draw(self):
        self.surface.fill(BACKGROUND_COLOR)
        self.draw_grid()
        self.draw_cells()
        pygame.draw.rect(self.surface, MOUSE_HIGHLIGHT_COLOR, self.mouse_rect, 1)
        pygame.transform.smoothscale(self.surface, self.window_size, self.window)

    def draw_grid(self):
        for x in range(CELL_WIDTH - (self.surface_rect.x % CELL_WIDTH),
                       self.surface_rect.width,
                       CELL_WIDTH):
            pygame.draw.line(self.surface, GRID_COLOR, (x, 0), (x, self.surface_rect.height))

        for y in range(CELL_WIDTH - (self.surface_rect.y % CELL_WIDTH),
                       self.surface_rect.height,
                       CELL_WIDTH):
            pygame.draw.line(self.surface, GRID_COLOR, (0, y), (self.surface_rect.width, y))

    def draw_cells(self):
        visible_cells = self.surface_rect.collidedictall(self.cells, True)
        for _, cell in visible_cells:
            self.surface.blit(cell.image, cell.screen_position)
        self.n_visible_cells = len(visible_cells)

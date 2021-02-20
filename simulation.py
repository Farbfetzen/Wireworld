import pygame

import cell


BACKGROUND_COLOR = pygame.Color(32, 32, 32)
GRID_COLOR = pygame.Color(64, 64, 64)
MOUSE_HIGHLIGHT_COLOR = pygame.Color(0, 255, 0)
FPS = 60
SPS = 4  # steps per second
SPS_MIN = 1
SPS_MAX = 256


class Wireworld:
    def __init__(self, window_size, cell_width):
        pygame.init()
        self.window = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Wireworld")
        self.cell_width = cell_width
        self.cell_size = (cell_width, cell_width)
        self.background = self.create_background(window_size)
        self.cell_images = cell.create_cell_images(self.cell_size)
        self.cells = {}
        self.mouse_grid_position = None  # highlighted cell coordinates
        self.mouse_position_snapped = None  # mouse position snapped to the grid
        self.mouse_is_pressed = False
        self.mouse_pressed_button = None
        self.last_changed_cell_position = None
        self.sps = SPS
        self.simulation_is_running = False

    def create_background(self, window_size):
        background = pygame.Surface(window_size)
        background.fill(BACKGROUND_COLOR)
        window_width, window_height = window_size
        for x in range(0, window_width, self.cell_width):
            pygame.draw.line(background, GRID_COLOR, (x, 0), (x, window_height))
        for y in range(0, window_height, self.cell_width):
            pygame.draw.line(background, GRID_COLOR, (0, y), (window_width, y))
        return background

    def run(self):
        # all times are in milliseconds
        time_per_step = 1000 / self.sps
        time_since_last_step = 0
        clock = pygame.time.Clock()

        while True:
            dt = clock.tick(FPS)

            self.update_mouse_positions()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_SPACE:
                        if self.simulation_is_running:
                            self.simulation_is_running = False
                        else:
                            self.simulation_is_running = True
                            time_since_last_step = time_per_step - dt
                    elif event.key in (pygame.K_PLUS, pygame.K_KP_PLUS):
                        self.sps = min(self.sps * 2, SPS_MAX)
                        time_per_step = 1000 / self.sps
                    elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                        self.sps = max(self.sps / 2, SPS_MIN)
                        time_per_step = 1000 / self.sps
                    elif event.key == pygame.K_s:
                        self.step()
                        if self.simulation_is_running:
                            self.simulation_is_running = False
                    elif event.key == pygame.K_BACKSPACE:
                        if event.mod & pygame.KMOD_CTRL:
                            self.cells = {}
                        else:
                            for c in self.cells.values():
                                c.remove_electricity()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button in (1, 3):  # 1 = left click, 3 = right click
                        self.mouse_pressed_button = event.button
                        self.mouse_is_pressed = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_is_pressed = False
                    self.last_changed_cell_position = None

            if self.mouse_is_pressed:
                self.process_mouse_press()

            if self.simulation_is_running:
                time_since_last_step += dt
                while time_since_last_step >= time_per_step:
                    time_since_last_step -= time_per_step
                    self.step()

            self.draw()

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

    def process_mouse_press(self):
        if (self.mouse_grid_position is None
                or self.mouse_grid_position == self.last_changed_cell_position):
            return
        self.last_changed_cell_position = self.mouse_grid_position
        selected_cell = self.cells.get(self.mouse_grid_position, None)
        if selected_cell is None:
            self.cells[self.mouse_grid_position] = cell.Cell(
                self.mouse_grid_position,
                self.mouse_position_snapped,
                self.mouse_pressed_button - 1,
                self.cells,
                self.cell_images
            )
        else:
            if self.mouse_pressed_button == 1:
                selected_cell.increment_state()
            else:
                selected_cell.decrement_state()

    def step(self):
        # All cells must be prepared before they are all updated. Otherwise
        # the count of the neighboring electron heads would be wrong.
        # This is why there are two loops here instead of one.
        for c in self.cells.values():
            c.prepare_update()
        for c in self.cells.values():
            c.update()

    def draw(self):
        self.window.blit(self.background, (0, 0))
        for c in self.cells.values():
            c.draw(self.window)
        if self.mouse_grid_position is not None:
            pygame.draw.rect(
                self.window,
                MOUSE_HIGHLIGHT_COLOR,
                (self.mouse_position_snapped, self.cell_size),
                1
            )
        pygame.display.flip()

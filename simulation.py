import pygame
import pygame.freetype

import cell


BACKGROUND_COLOR = pygame.Color(32, 32, 32)
GRID_COLOR = pygame.Color(64, 64, 64)
MOUSE_HIGHLIGHT_COLOR = pygame.Color(0, 255, 0)

FPS = 60
SPS = 4  # steps per second
SPS_MIN = 1
SPS_MAX = 128

# Window sizes are +1 so the rightmost and bottomost gridlines are also visible.
WINDOW_WIDTH = 1000 + 1
WINDOW_HEIGHT = 800 + 1
assert (WINDOW_WIDTH - 1) % cell.CELL_WIDTH == 0
assert (WINDOW_HEIGHT - 1) % cell.CELL_WIDTH == 0
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)


class Wireworld:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Wireworld")
        self.background = self.create_background()
        self.cells = {}
        self.mouse_grid_position = None  # highlighted cell coordinates
        self.mouse_position_snapped = None  # mouse position snapped to the grid
        self.mouse_is_pressed = False
        self.mouse_pressed_button = None
        self.last_changed_cell_position = None
        self.sps = SPS
        self.simulation_is_running = False

    @staticmethod
    def create_background():
        background = pygame.Surface(WINDOW_SIZE)
        background.fill(BACKGROUND_COLOR)
        for x in range(0, WINDOW_WIDTH, cell.CELL_WIDTH):
            pygame.draw.line(background, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, cell.CELL_WIDTH):
            pygame.draw.line(background, GRID_COLOR, (0, y), (WINDOW_WIDTH, y))
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
                                c.state = 0
                                c.next_state = 0
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button in (1, 3):  # 1 = left click, 3 = right click
                        self.mouse_pressed_button = event.button
                        self.mouse_is_pressed = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_is_pressed = False
                    self.last_changed_cell_position = None

            if self.mouse_is_pressed:
                self.process_mouse()

            if self.simulation_is_running:
                time_since_last_step += dt
                while time_since_last_step >= time_per_step:
                    time_since_last_step -= time_per_step
                    self.step()

            self.draw()

    def update_mouse_positions(self):
        if pygame.mouse.get_focused():
            screen_x, screen_y = pygame.mouse.get_pos()
            grid_x = screen_x // cell.CELL_WIDTH
            grid_y = screen_y // cell.CELL_WIDTH
            self.mouse_grid_position = (grid_x, grid_y)
            self.mouse_position_snapped = (grid_x * cell.CELL_WIDTH, grid_y * cell.CELL_WIDTH)
        else:
            self.mouse_grid_position = None
            self.mouse_position_snapped = None

    def process_mouse(self):
        if self.mouse_grid_position == self.last_changed_cell_position:
            return
        self.last_changed_cell_position = self.mouse_grid_position
        selected_cell = self.cells.get(self.mouse_grid_position, None)
        if selected_cell is None:
            self.cells[self.mouse_grid_position] = cell.Cell(
                self.mouse_grid_position,
                self.mouse_position_snapped,
                self.mouse_pressed_button - 1,
                self.cells
            )
        else:
            if self.mouse_pressed_button == 1:
                selected_cell.state += 1
                if selected_cell.state > 2:
                    selected_cell.delete()
            else:
                selected_cell.state -= 1
                if selected_cell.state < 0:
                    selected_cell.delete()

    def step(self):
        for c in self.cells.values():
            c.get_next_state()
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
                (self.mouse_position_snapped, cell.CELL_SIZE),
                1
            )
        pygame.display.flip()

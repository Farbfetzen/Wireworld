import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame


BACKGROUND_COLOR = pygame.Color(32, 32, 32)
GRID_COLOR = pygame.Color(64, 64, 64)
MOUSE_HIGHLIGHT_COLOR = pygame.Color(0, 255, 0)
CELL_COLORS = (
    pygame.Color("#b87333"),  # conductor, state 0
    pygame.Color(0, 64, 255),  # electron head, state 1
    pygame.Color(255, 64, 0)  # electron tail, state 2
)

FPS = 60
SPS = 4  # steps per second
SPS_MIN = 1
SPS_MAX = 128

CELL_WIDTH = 20
CELL_SIZE = (CELL_WIDTH, CELL_WIDTH)
# Window sizes are +1 so the rightmost and bottomost gridlines are also visible.
WINDOW_WIDTH = 1000 + 1
WINDOW_HEIGHT = 800 + 1
assert (WINDOW_WIDTH - 1) % CELL_WIDTH == 0
assert (WINDOW_HEIGHT - 1) % CELL_WIDTH == 0
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)


class Cell:
    def __init__(self, grid_pos, screen_pos, state, cells):
        self.grid_pos = grid_pos
        self.screen_pos = screen_pos
        self.state = state  # 0 = conductor, 1 = electron head, 2 = electron tail
        self.next_state = state
        self.neighbors = self.get_neighbors(cells)

    def get_neighbors(self, cells):
        neighbors = []
        x, y = self.grid_pos
        for dx, dy in ((-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)):
            neighbor = cells.get((x + dx, y + dy), None)
            if neighbor is not None:
                neighbors.append(neighbor)
                neighbor.neighbors.append(self)
        return neighbors

    def get_next_state(self):
        if self.state == 0:
            # conductor -> electron head if one or two neighbors are electron heads
            n_neighbor_heads = sum(1 for n in self.neighbors if n.state == 1)
            if n_neighbor_heads in (1, 2):
                self.next_state = 1
        elif self.state == 1:
            # electron head -> electron tail
            self.next_state = 2
        else:
            # electron tail -> conductor
            self.next_state = 0

    def update(self):
        self.state = self.next_state

    def draw(self, target_surface):
        pygame.draw.rect(
            target_surface,
            CELL_COLORS[self.state],
            (self.screen_pos, CELL_SIZE)
        )

    def delete(self, cells):
        del cells[self.grid_pos]
        for neighbor in self.neighbors:
            neighbor.neighbors.remove(self)


class Wireworld:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Wireworld")
        self.background = self.create_background()
        self.mouse_grid_position = None  # highlighted cell coordinates
        self.mouse_position_snapped = None  # mouse position snapped to the grid
        self.cells = {}
        self.mouse_is_pressed = False
        self.mouse_pressed_button = None
        self.last_changed_cell_position = None
        self.simulation_is_running = False

    @staticmethod
    def create_background():
        background = pygame.Surface(WINDOW_SIZE)
        background.fill(BACKGROUND_COLOR)
        for x in range(0, WINDOW_WIDTH, CELL_WIDTH):
            pygame.draw.line(background, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, CELL_WIDTH):
            pygame.draw.line(background, GRID_COLOR, (0, y), (WINDOW_WIDTH, y))
        return background

    def run(self):
        sps = SPS
        # all times are in milliseconds
        time_per_step = 1000 / sps
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
                        sps = min(sps * 2, SPS_MAX)
                        time_per_step = 1000 / sps
                    elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                        sps = max(sps / 2, SPS_MIN)
                        time_per_step = 1000 / sps
                    elif event.key == pygame.K_s:
                        self.step()
                        if self.simulation_is_running:
                            self.simulation_is_running = False
                    elif event.key == pygame.K_BACKSPACE:
                        if event.mod & pygame.KMOD_CTRL:
                            self.cells = {}
                        else:
                            for cell in self.cells.values():
                                cell.state = 0
                                cell.next_state = 0
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
            grid_x = screen_x // CELL_WIDTH
            grid_y = screen_y // CELL_WIDTH
            self.mouse_grid_position = (grid_x, grid_y)
            self.mouse_position_snapped = (grid_x * CELL_WIDTH, grid_y * CELL_WIDTH)
        else:
            self.mouse_grid_position = None
            self.mouse_position_snapped = None

    def process_mouse(self):
        if self.mouse_grid_position == self.last_changed_cell_position:
            return
        self.last_changed_cell_position = self.mouse_grid_position
        cell = self.cells.get(self.mouse_grid_position, None)
        if cell is None:
            self.cells[self.mouse_grid_position] = Cell(
                self.mouse_grid_position,
                self.mouse_position_snapped,
                self.mouse_pressed_button - 1,
                self.cells
            )
        else:
            if self.mouse_pressed_button == 1:
                cell.state += 1
                if cell.state > 2:
                    cell.delete(self.cells)
            else:
                cell.state -= 1
                if cell.state < 0:
                    cell.delete(self.cells)

    def step(self):
        for cell in self.cells.values():
            cell.get_next_state()
        for cell in self.cells.values():
            cell.update()

    def draw(self):
        self.window.blit(self.background, (0, 0))
        for cell in self.cells.values():
            cell.draw(self.window)
        if self.mouse_grid_position is not None:
            pygame.draw.rect(
                self.window,
                MOUSE_HIGHLIGHT_COLOR,
                (self.mouse_position_snapped, CELL_SIZE),
                1
            )
        pygame.display.flip()


Wireworld().run()

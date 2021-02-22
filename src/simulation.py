import pygame

from src import camera
from src import cell
from src import constants


class Wireworld:
    def __init__(self, window_size, cell_width):
        pygame.init()
        self.cells = {}
        self.camera = camera.Camera(window_size, cell_width, self.cells)
        self.cell_width = cell_width
        self.mouse_is_pressed = False
        self.mouse_pressed_button = None
        self.last_changed_cell_position = None
        self.sps = constants.SPS
        self.simulation_is_running = False

    def run(self):
        # all times are in milliseconds
        time_per_step = 1000 / self.sps
        time_since_last_step = 0
        clock = pygame.time.Clock()

        while True:
            dt = clock.tick(constants.FPS)

            self.camera.update_mouse_positions()
            # TODO: Put event stuff into separate method.
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
                        self.sps = min(self.sps * 2, constants.SPS_MAX)
                        time_per_step = 1000 / self.sps
                    elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                        self.sps = max(self.sps / 2, constants.SPS_MIN)
                        time_per_step = 1000 / self.sps
                    elif event.key == pygame.K_s:
                        self.step()
                        if self.simulation_is_running:
                            self.simulation_is_running = False
                    elif event.key == pygame.K_BACKSPACE:
                        if event.mod & pygame.KMOD_CTRL:
                            self.cells.clear()
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

            self.camera.draw()

    def process_mouse_press(self):
        if (self.camera.mouse_grid_position is None
                or self.camera.mouse_grid_position == self.last_changed_cell_position):
            return
        self.last_changed_cell_position = self.camera.mouse_grid_position
        selected_cell = self.cells.get(self.camera.mouse_grid_position, None)
        if selected_cell is None:
            self.cells[self.camera.mouse_grid_position] = cell.Cell(
                self.camera.mouse_grid_position,
                self.camera.mouse_position_snapped,
                self.mouse_pressed_button - 1,
                self.cells,
                self.camera.cell_images
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

import pygame

from src.constants import *
from src.cell import Cell


class Simulation:
    def __init__(self, camera, cells):
        self.cells = cells
        self.camera = camera
        self.mouse_is_pressed = False
        self.last_changed_cell_position = None
        self.sps = SPS
        self.simulation_is_running = False
        self.time_per_step = 1 / self.sps
        self.time_since_last_step = 0

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.simulation_is_running:
                    self.simulation_is_running = False
                else:
                    self.simulation_is_running = True
                    self.time_since_last_step = self.time_per_step
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                if self.simulation_is_running:
                    self.simulation_is_running = False
                self.step()
            elif not event.mod & pygame.KMOD_CTRL:
                # Ignore these keypresses if ctrl is pressed to not interfere with camera zooming.
                if event.key in (pygame.K_PLUS, pygame.K_KP_PLUS):
                    self.sps = min(self.sps * 2, SPS_MAX)
                    self.time_per_step = 1 / self.sps
                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    self.sps = max(self.sps / 2, SPS_MIN)
                    self.time_per_step = 1 / self.sps
            elif event.key == pygame.K_BACKSPACE:
                if event.mod & pygame.KMOD_CTRL:
                    self.cells.clear()
                else:
                    for c in self.cells.values():
                        c.remove_electricity()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # left click
            self.mouse_is_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_is_pressed = False
            self.last_changed_cell_position = None

    def update(self, dt):
        if self.mouse_is_pressed:
            self.process_mouse_press()

        if self.simulation_is_running:
            self.time_since_last_step += dt
            while self.time_since_last_step >= self.time_per_step:
                self.time_since_last_step -= self.time_per_step
                self.step()

    def process_mouse_press(self):
        if self.camera.mouse_grid_position != self.last_changed_cell_position:
            self.last_changed_cell_position = self.camera.mouse_grid_position
            selected_cell = self.cells.get(self.camera.mouse_grid_position, None)
            erase_mode = pygame.key.get_mods() & pygame.KMOD_CTRL
            if selected_cell is None:
                if not erase_mode:
                    self.cells[self.camera.mouse_grid_position] = Cell(self.camera)
            else:
                if erase_mode:
                    selected_cell.delete()
                else:
                    selected_cell.increment_state()

    def step(self):
        # All cells must be prepared before they are all updated. Otherwise
        # the count of the neighboring electron heads would be wrong.
        # This is why there are two loops here instead of one.
        cells = self.cells.values()
        for cell in cells:
            cell.prepare_update()
        for cell in cells:
            cell.update_state()

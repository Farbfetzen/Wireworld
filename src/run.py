import pygame

from src import constants
from src.simulation import Simulation
from src.camera import Camera
from src.cell import Cell


def run(window_size, cell_width):
    pygame.init()
    cells = {}
    cell_size = (cell_width, cell_width)
    camera = Camera(window_size, cell_width, cell_size, cells)
    Cell.init_class_variables(cell_width, cell_size, camera, cells)
    simulation = Simulation(camera, cell_width, cells)
    clock = pygame.time.Clock()
    fps = constants.FPS
    debug_mode = False

    while True:
        dt = clock.tick(fps) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_F1:
                    debug_mode = not debug_mode
            camera.process_event(event)
            simulation.process_event(event)
        camera.update(dt)
        simulation.update(dt)
        camera.draw(debug_mode, clock.get_fps())

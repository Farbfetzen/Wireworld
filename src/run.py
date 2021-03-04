import pygame

from src import constants
from src.simulation import Simulation
from src.camera import Camera


def run(window_size, cell_width):
    pygame.init()
    cells = {}
    camera = Camera(window_size, cell_width, cells)
    simulation = Simulation(cells, camera, cell_width)
    clock = pygame.time.Clock()

    while True:
        dt = clock.tick(constants.FPS)
        camera.update_mouse_positions()
        for event in pygame.event.get():
            if (event.type == pygame.QUIT
                    or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return
            simulation.process_event(event, dt)
            camera.process_event(event, dt)
        simulation.update(dt)
        camera.draw()

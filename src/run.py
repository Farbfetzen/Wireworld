import pygame

from src.constants import *
from src.simulation import Simulation
from src.camera import Camera
from src.cell import Cell


def run(window_size):
    pygame.init()
    cells = {}
    camera = Camera(window_size, cells)
    Cell.static_init(camera, cells)
    simulation = Simulation(camera, cells)
    clock = pygame.time.Clock()
    debug_mode = False

    while True:
        dt = clock.tick(FPS) / 1000
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

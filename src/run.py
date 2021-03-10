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
        camera.draw()
        if debug_mode:
            show_debug_info(camera, simulation, clock.get_fps())
        pygame.display.flip()


def show_debug_info(camera, simulation, fps):
    pygame.draw.circle(camera.window, (255, 0, 0), camera.world_to_screen_position(0, 0), 3)
    DEBUG_FONT.render_to(
        camera.window,
        DEBUG_MARGIN,
        f"fps: {fps:.0f}"
    )
    DEBUG_FONT.render_to(
        camera.window,
        DEBUG_MARGIN + DEBUG_LINE_SPACING,
        f"mouse grid position: {camera.mouse_grid_position}"
    )
    DEBUG_FONT.render_to(
        camera.window,
        DEBUG_MARGIN + DEBUG_LINE_SPACING * 2,
        f"mouse rect screen position: {camera.mouse_rect.topleft}"
    )
    DEBUG_FONT.render_to(
        camera.window,
        DEBUG_MARGIN + DEBUG_LINE_SPACING * 3,
        f"number of visible cells: {camera.n_visible_cells}"
    )
    DEBUG_FONT.render_to(
        camera.window,
        DEBUG_MARGIN + DEBUG_LINE_SPACING * 4,
        f"zoom level: {camera.zoom_level:.2f}"
    )
    DEBUG_FONT.render_to(
        camera.window,
        DEBUG_MARGIN + DEBUG_LINE_SPACING * 5,
        f"steps per second: {simulation.sps:.0f}"
    )
    DEBUG_FONT.render_to(
        camera.window,
        DEBUG_MARGIN + DEBUG_LINE_SPACING * 6,
        f"simulation is running: {simulation.simulation_is_running}"
    )

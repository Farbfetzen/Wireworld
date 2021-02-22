import pygame

from src import constants


def create_cell_images(cell_size):
    conductor_image = pygame.Surface(cell_size)
    conductor_image.fill(constants.CONDUCTOR_COLOR)
    head_image = pygame.Surface(cell_size)
    head_image.fill(constants.ELECTRON_HEAD_COLOR)
    tail_image = pygame.Surface(cell_size)
    tail_image.fill(constants.ELECTRON_TAIL_COLOR)
    return conductor_image, head_image, tail_image


class Cell:
    def __init__(self, grid_pos, screen_pos, cells, images):
        self.grid_position = grid_pos
        self.screen_position_x_original, self.screen_position_y_original = screen_pos
        self.screen_position_x, self.screen_position_y = screen_pos
        self.state = 0  # 0 = conductor, 1 = electron head, 2 = electron tail
        self.next_state = self.state
        self.cells = cells
        self.images = images
        self.image = images[self.state]
        self.neighbors = self.get_neighbors()

    def get_neighbors(self):
        neighbors = []
        x, y = self.grid_position
        for dx, dy in ((-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)):
            neighbor = self.cells.get((x + dx, y + dy), None)
            if neighbor is not None:
                neighbors.append(neighbor)
                neighbor.neighbors.append(self)
        return neighbors

    def prepare_update(self):
        if self.state == 0:
            # conductor -> electron head if one or two neighbors are electron heads
            n_neighbor_heads = sum(1 for neighbor in self.neighbors if neighbor.state == 1)
            if n_neighbor_heads in (1, 2):
                self.next_state = 1
            else:
                self.next_state = 0
        elif self.state == 1:
            # electron head -> electron tail
            self.next_state = 2
        else:
            # electron tail -> conductor
            self.next_state = 0

    def update(self):
        self.state = self.next_state
        self.image = self.images[self.state]

    def update_screen_position(self, camera_x, camera_y):
        self.screen_position_x = self.screen_position_x_original - camera_x
        self.screen_position_y = self.screen_position_y_original - camera_y

    def is_visible(self, camera_rect):
        return camera_rect.collidepoint(self.screen_position_x, self.screen_position_y)

    def increment_state(self):
        self.state += 1
        if self.state > 2:
            self.delete()
        else:
            self.image = self.images[self.state]

    def remove_electricity(self):
        self.state = 0
        self.next_state = 0
        self.image = self.images[self.state]

    def delete(self):
        del self.cells[self.grid_position]
        for neighbor in self.neighbors:
            neighbor.neighbors.remove(self)

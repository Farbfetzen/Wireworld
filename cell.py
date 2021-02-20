import pygame


CONDUCTOR_COLOR = pygame.Color(184, 115, 51)
ELECTRON_HEAD_COLOR = pygame.Color(0, 64, 255)
ELECTRON_TAIL_COLOR = pygame.Color(255, 64, 0)


def create_cell_images(cell_size):
    conductor_image = pygame.Surface(cell_size)
    conductor_image.fill(CONDUCTOR_COLOR)
    head_image = pygame.Surface(cell_size)
    head_image.fill(ELECTRON_HEAD_COLOR)
    tail_image = pygame.Surface(cell_size)
    tail_image.fill(ELECTRON_TAIL_COLOR)
    return conductor_image, head_image, tail_image


class Cell:
    def __init__(self, grid_pos, screen_pos, state, cells, images):
        self.grid_pos = grid_pos
        self.screen_pos = screen_pos
        self.state = state  # 0 = conductor, 1 = electron head, 2 = electron tail
        self.next_state = state
        self.cells = cells
        self.images = images
        self.image = images[self.state]
        self.neighbors = self.get_neighbors()

    def get_neighbors(self):
        neighbors = []
        x, y = self.grid_pos
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

    def draw(self, target_surface):
        target_surface.blit(self.image, self.screen_pos)

    def increment_state(self):
        self.state += 1
        if self.state > 2:
            self.delete()
        else:
            self.image = self.images[self.state]

    def decrement_state(self):
        self.state -= 1
        if self.state < 0:
            self.delete()
        else:
            self.image = self.images[self.state]

    def remove_electricity(self):
        self.state = 0
        self.next_state = 0
        self.image = self.images[self.state]

    def delete(self):
        del self.cells[self.grid_pos]
        for neighbor in self.neighbors:
            neighbor.neighbors.remove(self)

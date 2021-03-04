import pygame


class Cell:
    def __init__(self, camera, cells, width):
        self.camera = camera
        self.cells = cells
        self.width = width
        self.grid_position = camera.mouse_grid_position
        self.grid_x, self.grid_y = self.grid_position
        self.world_position_x = self.grid_x * self.width
        self.world_position_y = self.grid_y * self.width
        self.rect = pygame.Rect(0, 0, self.width, self.width)
        self.update_screen_position()
        self.state = 0  # 0 = conductor, 1 = electron head, 2 = electron tail
        self.next_state = self.state
        self.images = camera.cell_images
        self.image = self.images[self.state]
        self.neighbors = self.get_neighbors()

    def get_neighbors(self):
        neighbors = []
        for dx, dy in ((-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)):
            neighbor = self.cells.get((self.grid_x + dx, self.grid_y + dy), None)
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

    def update_screen_position(self):
        self.rect.x = self.world_position_x - self.camera.rect.x
        self.rect.y = self.world_position_y - self.camera.rect.y

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

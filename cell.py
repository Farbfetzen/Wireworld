import pygame


CELL_COLORS = (
    pygame.Color(184, 115, 51),  # conductor
    pygame.Color(0, 64, 255),  # electron head
    pygame.Color(255, 64, 0)  # electron tail
)
CELL_WIDTH = 20
CELL_SIZE = (CELL_WIDTH, CELL_WIDTH)


class Cell:
    def __init__(self, grid_pos, screen_pos, state, cells):
        self.grid_pos = grid_pos
        self.screen_pos = screen_pos
        self.state = state  # 0 = conductor, 1 = electron head, 2 = electron tail
        self.next_state = state
        self.cells = cells
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

    def get_next_state(self):
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

    def draw(self, target_surface):
        pygame.draw.rect(
            target_surface,
            CELL_COLORS[self.state],
            (self.screen_pos, CELL_SIZE)
        )

    def delete(self):
        del self.cells[self.grid_pos]
        for neighbor in self.neighbors:
            neighbor.neighbors.remove(self)

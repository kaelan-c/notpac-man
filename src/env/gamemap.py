import pygame
from env.gridcell import GridCell

class GameMap:
  def __init__(self, filename):
    self.width = 0
    self.height = 0
    self.grid = []
    self.load_map(filename)

  def load_map(self, filename):
    with open(filename, 'r') as file:
      self.width, self.height = map(int, file.readline().strip().split(','))

      for line in file:
        row = []
        for cell_type in line.strip():
          row.append(GridCell(cell_type))
        self.grid.append(row)

  def get_cell(self, x, y):
    return self.grid[y][x]

  def is_wall(self, x, y):
    if 0 <= x < self.width and 0 <= y < self.height:
      return self.grid[y][x].is_wall
    return False  # Out of bounds is considered a wall

  def create_map_surface(self):
    cell_size = 20  # Size of each cell in pixels
    wall_color = (0, 0, 255)  # Blue color for walls
    out_of_map_color = (0, 0, 0)  # Black color for out-of-map areas
    dot_color = (255, 255, 255)  # White color for dots
    powerup_color = (255, 0, 0)  # Red color for power-ups
    dot_radius = cell_size // 8  # Adjust radius as needed
    powerup_radius = cell_size // 4  # Adjust radius as needed
    # Additional colors for other elements
    # ...
    self.map_surface = pygame.Surface((self.width * cell_size, self.height * cell_size))

    for y, row in enumerate(self.grid):
      for x, cell in enumerate(row):
        center = (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2)
        rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
        if cell.is_wall:
          pygame.draw.rect(self.map_surface, wall_color, rect)
        elif cell.is_out_of_map:
          pygame.draw.rect(self.map_surface, out_of_map_color, rect)
        elif cell.is_regular_dot:
          pygame.draw.circle(self.map_surface, dot_color, center, dot_radius)
        elif cell.is_powerup_dot:
          pygame.draw.circle(self.map_surface, powerup_color, center, powerup_radius)
          
  def eat_dot(self, x, y):
    cell = self.get_cell(x, y)
    cell.consume_dot()
    self.create_map_surface()  # Update the map surface

  def draw(self, screen):
    screen.blit(self.map_surface, (0, 0))
    # Draw dynamic elements here (like Pac-Man, ghosts, and disappearing dots)
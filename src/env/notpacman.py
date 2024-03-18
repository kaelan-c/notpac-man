import pygame

class NotPacMan:
  def __init__(self, x, y):
    self.grid_x = x  # Pac-Man's x-coordinate on the grid
    self.grid_y = y  # Pac-Man's y-coordinate on the grid
    self.direction = 'RIGHT'  # Current moving direction
    self.desired_direction = 'RIGHT'  # Desired direction
    self.move_timer = 0
    self.move_frequency = 15  # Number of frames between each move

  def can_move(self, game_map, direction):
    new_x, new_y = self.grid_x, self.grid_y

    if direction == "LEFT":
      new_x -= 1
    elif direction == "RIGHT":
      new_x += 1
    elif direction == "UP":
      new_y -= 1
    elif direction == "DOWN":
      new_y += 1

    return not game_map.is_wall(new_x, new_y)
  
  def move(self, game_map):
    if self.can_move(game_map, self.desired_direction):
      self.direction = self.desired_direction  # Update current direction if possible

    if self.can_move(game_map, self.direction):
      self.move_timer += 1
      if self.move_timer >= self.move_frequency:
        self.move_timer = 0
        if self.can_move(game_map, self.direction):
          if self.direction == "LEFT":
            self.grid_x -= 1
          elif self.direction == "RIGHT":
            self.grid_x += 1
          elif self.direction == "UP":
            self.grid_y -= 1
          elif self.direction == "DOWN":
            self.grid_y += 1

  def draw(self, screen):
    cell_size = 20  # Assuming this is your cell size
    pixel_x = self.grid_x * cell_size
    pixel_y = self.grid_y * cell_size
    radius = cell_size // 2  # Adjust radius as needed
    pygame.draw.circle(screen, (255, 255, 0), (pixel_x + radius, pixel_y + radius), radius)
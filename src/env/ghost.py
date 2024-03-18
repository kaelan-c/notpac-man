import random
import pygame

class Ghost:

  def __init__(self, x, y, colour):
    self.grid_x = x
    self.grid_y = y
    self.direction = random.choice(["LEFT", "RIGHT", "UP", "DOWN"])
    self.colour = colour
    self.move_time = 0
    self.move_frequency = 20

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
  
  def move (self, game_map):

    if self.move_time < self.move_frequency:
      self.move_time += 1
      return
    
    self.move_time = 0
    directions = ["LEFT", "RIGHT", "UP", "DOWN"]
    random.shuffle(directions)

    for direciton in directions:
      if self.can_move(game_map, direciton):
        self.direction = direciton
        break
    
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
    pygame.draw.circle(screen, self.colour, (pixel_x + radius, pixel_y + radius), radius)   
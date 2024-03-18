import random
import pygame

class Ghost:

  def __init__(self, x, y, colour, scatter_target):
    self.grid_x = x
    self.grid_y = y
    self.colour = colour
    self.move_timer = 0
    self.move_frequency = 20
    self.current_direction = "UP"
    self.mode_timings = [("SCATTER", 7), ("CHASE", 20)]
    self.mode = "SCATTER"  # Initial mode
    self.last_mode_change_time = 0  # Tracks when the last mode change occurred
    self.mode_duration = 0  # Duration of the current mode
    self.scatter_target = scatter_target  # Define scatter targets for each ghost
    self.frightened_timer = 0
    self.frightened_duration = 20  # Duration of frightened mode

  def update_mode(self, game_time, frightened=False):
    if frightened:
      self.last_mode = self.mode
      self.mode = "FRIGHTENED"
      self.frightened_timer = self.frightened_duration
      self.last_mode_change_time = game_time
      return

    if self.mode == "FRIGHTENED":
      self.frightened_timer -= 1
      if self.frightened_timer <= 0:
        self.mode = self.last_mode
        self.last_mode_change_time = game_time
      return

    time_since_last_change = game_time - self.last_mode_change_time
    if time_since_last_change >= self.mode_duration:
      # Cycle through the mode timings
      current_mode_index = [index for index, mode in enumerate(self.mode_timings) if mode[0] == self.mode][0]
      next_mode_index = (current_mode_index + 1) % len(self.mode_timings)
      self.mode, self.mode_duration = self.mode_timings[next_mode_index]
      self.last_mode_change_time = game_time
    
  def move(self, game_map, pacman_position, pacman_direction):
      if self.grid_x == 0 and self.grid_y == 14:
        self.grid_x = 26
      elif self.grid_x == 27 and self.grid_y == 14:
        self.grid_x = 1
      self.move_timer += 1
      if self.move_timer >= self.move_frequency:
        self.move_timer = 0
        target_tile = self.select_target_tile(pacman_position, pacman_direction)

        possible_directions = self.get_possible_directions(game_map)
        best_direction = self.get_best_direction(possible_directions, target_tile, game_map)
        self.update_position(best_direction)

  def get_possible_directions(self, game_map):
    directions = ["LEFT", "RIGHT", "UP", "DOWN"]
    # Exclude the opposite of current direction to prevent reversing
    opposite_direction = {"LEFT": "RIGHT", "RIGHT": "LEFT", "UP": "DOWN", "DOWN": "UP"}
    if self.current_direction in directions:
        directions.remove(opposite_direction[self.current_direction])
    return [dir for dir in directions if self.can_move(game_map, dir)]
  
  def get_best_direction(self, possible_directions, target_tile, game_map):
    # Choose the direction that minimizes the distance to the target tile
    # This could be implemented using Manhattan distance
    best_direction = None
    min_distance = float('inf')
    for direction in possible_directions:
      new_x, new_y = self.get_new_position(direction)
      distance = self.calculate_distance((new_x, new_y), target_tile)
      if distance < min_distance:
        min_distance = distance
        best_direction = direction
    return best_direction
  
  def update_position(self, direction):
    if direction == "LEFT":
        self.grid_x -= 1
    elif direction == "RIGHT":
        self.grid_x += 1
    elif direction == "UP":
        self.grid_y -= 1
    elif direction == "DOWN":
        self.grid_y += 1
    self.current_direction = direction

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
  
  def get_new_position(self, direction):
    new_x, new_y = self.grid_x, self.grid_y

    if direction == "LEFT":
        new_x -= 1
    elif direction == "RIGHT":
        new_x += 1
    elif direction == "UP":
        new_y -= 1
    elif direction == "DOWN":
        new_y += 1

    return new_x, new_y
  
  def calculate_distance(self, position1, position2):
      x1, y1 = position1
      x2, y2 = position2
      return abs(x1 - x2) + abs(y1 - y2)

  def draw(self, screen):
    cell_size = 20  # Assuming this is your cell size
    pixel_x = self.grid_x * cell_size
    pixel_y = self.grid_y * cell_size
    radius = cell_size // 2  # Adjust radius as needed
    pygame.draw.circle(screen, self.colour, (pixel_x + radius, pixel_y + radius), radius)


# Blinky (The Red Ghost):
#   In CHASE mode Blinky targets !PacMans exact grid location.
#   In SCATTER mode Blinky targets the Top Right Corner of the map.
#
#   Blinky Starts outside of the Ghost Home.
class Blinky(Ghost):
  def __init__(self):
    super().__init__(14, 11, (255, 0, 0), (1, 1))
  def select_target_tile(self, pacman_position, pacman_direction):
    if self.mode == "CHASE":
      return pacman_position
    else:
      return self.scatter_target

# Pinky(The Pink Ghost):
#   In CHASE mode Pinky targets 4 tiles ahead of !PacMans grid location.
#   In SCATTER mode Blinky targets the Top Left Corner of the map.
#
#   Pinky starts inside the ghost home in the middle of Inky and Clyde.
class Pinky(Ghost):
  def __init__(self):
    super().__init__(14, 11, (255, 184, 255), (1, 1))
  def select_target_tile(self, pacman_position, pacman_direction):
    offset = 4
    if self.mode == "CHASE":
      target_x, target_y = pacman_position
      if pacman_direction == "LEFT":
        target_x -= offset
      elif pacman_direction == "RIGHT":
        target_x += offset
      elif pacman_direction == "UP":
        target_y -= offset
      elif pacman_direction == "DOWN":
        target_y += offset
      return(target_x,target_y)
    else:
      return self.scatter_target

# Inky (The Blue Ghost):
#   In CHASE mode Inky targets both Bliny and !PacMans grid locations.
#   In SCATTER mode Inky targets the Bottom Right Corner of the map.
#
#   Inky starts on the lefthand side of the ghost home, next to Pinky.
class Inky(Ghost):
  def __init__(self, blinky):
    super().__init__(14, 11, (0, 255, 255), (30, 26))
    self.blinky = blinky
  def select_target_tile(self, pacman_position, pacman_direction):
    offset = 2
    if self.mode == "CHASE":
      blinky_x, blinky_y = self.blinky.grid_x, self.blinky.grid_y
      pac_x, pac_y = pacman_position

      if pacman_direction == "LEFT":
        pac_x -= offset
      elif pacman_direction == "RIGHT":
        pac_x += offset
      elif pacman_direction == "UP":
        pac_y -= offset
      elif pacman_direction == "DOWN":
        pay_y += offset

      target_x = blinky_x + 2 * (pac_x - blinky_x)
      target_y = blinky_y + 2 * (pac_y - blinky_y)

      return (target_x, target_y)
    else:
      return self.scatter_target

# Clyde (The Orange Ghost)
#   In CHASE mode Clyde targets !PacMans grid location but when he gets
#     within 8 blocks of !Pacman he retreats to his scatter location.
#   In SCATTER mode Clyde targets the Bottom Left Corner of the map.
#
#   Clyde starts on the righthand side of the ghost home, next to Pinky.
class Clyde(Ghost):
  def __init__(self):
    super().__init__(14, 11, (255, 184, 82), (1, 30))
  def select_target_tile(self, pacman_position, pacman_direction):
    if self.mode == "CHASE":
      pac_x, pac_y = pacman_position
      if abs(self.grid_x - pac_x) + abs(self.grid_y - pac_y) < 8:
        return self.scatter_target
      else:
        return pacman_position
    else:
      return self.scatter_target
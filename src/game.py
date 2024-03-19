import pygame
from env.notpacman import NotPacMan
from env.gamemap import GameMap
from env.ghost import Blinky, Inky, Pinky, Clyde

class Game:
  def __init__(self, screen, tick_rate, cell_size, num_ghosts, map_file, headless=False):
    self.headless = headless  # Rendering flag
    self.tick_rate = tick_rate
    self.game_time = 0
    self.score = 0
    self.lives = 3
    self.state = "PLAYING"
    self.screen = screen
    self.cell_size = cell_size
    self.game_map = GameMap(map_file)
    self.game_map.create_map_surface()
    self.notpacman = NotPacMan(cell_size)
    self.num_ghosts = num_ghosts

    blinky = Blinky(cell_size) if self.num_ghosts > 0 else None
    pinky = Pinky(cell_size) if self.num_ghosts > 1 else None
    inky = Inky(cell_size, blinky) if self.num_ghosts > 2 and blinky is not None else None
    clyde = Clyde(cell_size) if self.num_ghosts > 3 else None

    # Create the ghosts list based on the number of ghosts
    self.ghosts = [g for g in [blinky, pinky, inky, clyde] if g is not None]

  def get_state(self):
    pacman_pos = (self.notpacman.grid_x, self.notpacman.grid_y)
    nearest_ghost_dist, nearest_ghost_dir = self.get_nearest_ghost_info(pacman_pos)
    nearest_dot_dist, nearest_dot_dir = self.get_nearest_dot_info(pacman_pos)
    dots_remaining = self.game_map.dots_total

    state = (pacman_pos, nearest_ghost_dist, nearest_ghost_dir, nearest_dot_dist, nearest_dot_dir, dots_remaining)
    return state

  def get_nearest_dot_info(self, pacman_pos):
    min_dist = float('inf')
    nearest_dot_dir = None

    for y, row in enumerate(self.game_map.grid):
        for x, cell in enumerate(row):
            if cell.is_regular_dot or cell.is_powerup_dot:
                dot_pos = (x, y)
                dot_dist = self.manhattan_distance(pacman_pos, dot_pos)

                if dot_dist < min_dist:
                    min_dist = dot_dist
                    nearest_dot_dir = self.get_direction(pacman_pos, dot_pos)

    return min_dist, nearest_dot_dir

  def get_nearest_ghost_info(self, pacman_pos):
      nearest_ghost_dist = float('inf')
      nearest_ghost_dir = None

      for ghost in self.ghosts:
          if (ghost.grid_x < 11 or ghost.grid_x > 17) and (ghost.grid_y < 12 or ghost.grid_y > 15):
            ghost_pos = (ghost.grid_x, ghost.grid_y)
            dist = self.manhattan_distance(pacman_pos, ghost_pos)

            if dist < nearest_ghost_dist:
                nearest_ghost_dist = dist
                nearest_ghost_dir = self.get_direction(pacman_pos, ghost_pos)

      return nearest_ghost_dist, nearest_ghost_dir

  def manhattan_distance(self, pos1, pos2):
      return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

  def get_direction(self, from_pos, to_pos):
      dx, dy = to_pos[0] - from_pos[0], to_pos[1] - from_pos[1]
      if abs(dx) > abs(dy):
          return 0 if dx < 0 else 1
      else:
          return 2 if dy < 0 else 3
  
  def agent_action(self, action):
    if action == 0:
      self.notpacman.desired_direction = "LEFT"
    if action == 1:
      self.notpacman.desired_direction = "RIGHT"
    if action == 2:
      self.notpacman.desired_direction = "UP"
    if action == 3:
      self.notpacman.desired_direction = "DOWN"
  
  def calc_reward(self):
    reward = 0

    # Reward for eating dots
    if self.score_change > 0:
        reward += self.score_change
    
    # Penalty for each step to encourage movement
    reward -= 1

    # Penalty for losing a life
    if self.life_lost:
        reward -= 100

    # Reward for winning
    if self.won:
        reward += 500

    # Big penalty for losing
    if self.lost:
        reward -= 500

    # Reset flags for the next calculation
    self.score_change = 0
    self.life_lost = False
    self.won = False
    self.lost = False

    return reward
  
  def is_done(self):
    return self.lives <= 0 or self.game_map.dots_total == 0

  def step(self, action):
    prev_score = self.score
    prev_lives = self.lives

    self.agent_action(action)

    self.update()

    self.score_change = self.score - prev_score
    self.life_lost = self.lives < prev_lives
    self.won = self.game_map.dots_total == 0
    self.lost = self.lives <= 0

    state = self.get_state()
    reward = self.calc_reward()
    done = self.is_done()
    return state, reward, done
  
  def render(self):
    if not self.headless:
      self.draw()
      return

  def update(self):
    self.notpacman.move(self.game_map)
    current_cell = self.game_map.get_cell(self.notpacman.grid_x, self.notpacman.grid_y)

    for ghost in self.ghosts:
      ghost.update_mode(self.game_time)
      ghost.move(self.game_map, (self.notpacman.grid_x, self.notpacman.grid_y), self.notpacman.direction, self.game_time)

    if current_cell.is_regular_dot:
      self.score += 10
      self.game_map.eat_dot(self.notpacman.grid_x, self.notpacman.grid_y)

    if current_cell.is_powerup_dot:
      self.score += 50
      self.game_map.eat_dot(self.notpacman.grid_x, self.notpacman.grid_y)
      self.trigger_frightened_mode()
    
    for ghost in self.ghosts:
      if self.check_collision(ghost):
        self.game_time = 0
        if ghost.mode == "FRIGHTENED":
          self.score += 100
          ghost.grid_x = 11
          ghost.grid_y = 9
          ghost.released = False
          ghost.release_time = 5
          ghost.mode = "SCATTER"
        else:
          self.lives -= 1
          self.notpacman.grid_x = 11
          self.notpacman.grid_y = 11

          blinky = Blinky(self.cell_size) if self.num_ghosts > 0 else None
          pinky = Pinky(self.cell_size) if self.num_ghosts > 1 else None
          inky = Inky(self.cell_size, blinky) if self.num_ghosts > 2 and blinky is not None else None
          clyde = Clyde(self.cell_size) if self.num_ghosts > 3 else None

          # Create the ghosts list based on the number of ghosts
          self.ghosts = [g for g in [blinky, pinky, inky, clyde] if g is not None]

          if self.lives == 0:
           #print("Game Over")
            if not self.headless:
              self.game_over()
              pygame.quit()

    if self.game_map.dots_total == 0:
      print("You Win!")
      if not self.headless:
        self.you_win()
        pygame.quit()

    self.game_time += 1

  def trigger_frightened_mode(self):
    for ghost in self.ghosts:
      if ghost.released == True:
        ghost.update_mode(self.game_time, frightened=True)

  def check_collision(self, ghost):
      pacman_prev_x, pacman_prev_y = self.notpacman.prev_grid_x, self.notpacman.prev_grid_y
      ghost_prev_x, ghost_prev_y = ghost.prev_grid_x, ghost.prev_grid_y

      if (self.notpacman.grid_x == ghost.grid_x and self.notpacman.grid_y == ghost.grid_y) or \
        (pacman_prev_x == ghost.grid_x and pacman_prev_y == ghost.grid_y and \
          ghost_prev_x == self.notpacman.grid_x and ghost_prev_y == self.notpacman.grid_y):
          return True
      else:
          return False

  def game_over(self):
    # Display a game over message or screen
    self.screen.fill((0, 0, 0))  # Example: black screen
    font = pygame.font.SysFont(None, 55)
    text = font.render('Game Over', True, (255, 255, 255))
    self.screen.blit(text, (100, 100))  # Adjust position as needed
    pygame.display.flip()
    pygame.time.wait(3000)  # Wait for 3 seconds

  def you_win(self):
    # Display a victory message
    self.screen.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 55)
    text = font.render('You Win!', True, (255, 255, 255))
    self.screen.blit(text, (100, 100))
    pygame.display.flip()
    pygame.time.wait(3000)

  def draw_scoreboard(self):
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
    lives_text = font.render(f'Lives: {self.lives}', True, (255, 255, 255))
    self.screen.blit(score_text, (5, 5))
    self.screen.blit(lives_text, (5, 40))

  def draw(self):
    self.screen.fill((0, 0, 0))  # Clear screen
    self.game_map.draw(self.screen)
    self.notpacman.draw(self.screen)
    for ghost in self.ghosts:
      ghost.draw(self.screen)
    self.draw_scoreboard()
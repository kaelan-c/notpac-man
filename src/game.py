import pygame
from env.notpacman import NotPacMan
from env.gamemap import GameMap
from env.ghost import Blinky, Inky, Pinky, Clyde

class Game:
  def __init__(self, screen):
    self.game_time = 0
    self.score = 0
    self.lives = 3
    self.state = "PLAYING"
    self.screen = screen
    self.game_map = GameMap("env/maps/basicmap.txt")
    self.game_map.create_map_surface()
    self.notpacman = NotPacMan()
    blinky = Blinky()
    pinky = Pinky()
    inky = Inky(blinky)
    clyde = Clyde()

    self.ghosts = [blinky, pinky, inky, clyde]

  def update(self):
    # Handle key inputs and update game state
    self.handle_human_input()
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
        if ghost.mode == "FRIGHTENED":
          self.score += 100
          ghost.grid_x = 13
          ghost.grid_y = 14
          ghost.released = False
          ghost.release_time = 5 + self.game_time
          ghost.mode = "SCATTER"
        else:
          self.lives -= 1
          self.notpacman.grid_x = 14
          self.notpacman.grid_y = 17

          self.ghosts[0].grid_x = 14
          self.ghosts[0].grid_y = 11
          self.ghosts[0].mode = "CHASE"
                    
          self.ghosts[1].grid_x = 12
          self.ghosts[1].grid_y = 14
          self.ghosts[1].mode = "SCATTER"
          self.ghosts[1].released = False
          self.ghosts[1].release_time += self.game_time

          self.ghosts[2].grid_x = 13
          self.ghosts[2].grid_y = 14 
          self.ghosts[1].mode = "SCATTER"
          self.ghosts[1].released = False
          self.ghosts[1].release_time += self.game_time
                    
          self.ghosts[3].grid_x = 14
          self.ghosts[3].grid_y = 14
          self.ghosts[1].mode = "SCATTER"
          self.ghosts[1].released = False
          self.ghosts[1].release_time += self.game_time
          
          if self.lives == 0:
            print("Game Over")
            self.game_over()

    if self.game_map.dots_total == 0:
      print("You Win!")
      self.you_win()

    self.game_time = pygame.time.get_ticks() / 1000

  def trigger_frightened_mode(self):
    for ghost in self.ghosts:
      if ghost.released == True:
        ghost.update_mode(self.game_time, frightened=True)

  def check_collision(self, ghost):
    if self.notpacman.grid_x == ghost.grid_x and self.notpacman.grid_y == ghost.grid_y:
      return True
    else:
      return False

  def handle_human_input(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
      self.notpacman.desired_direction = "LEFT"
    elif keys[pygame.K_RIGHT]:
      self.notpacman.desired_direction = "RIGHT"
    elif keys[pygame.K_UP]:
      self.notpacman.desired_direction = "UP"
    elif keys[pygame.K_DOWN]:
      self.notpacman.desired_direction = "DOWN"

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
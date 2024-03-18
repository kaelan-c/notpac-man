import pygame
from env.notpacman import NotPacMan
from env.gamemap import GameMap
from env.ghost import Ghost

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.game_map = GameMap("env/maps/basicmap.txt")
        self.game_map.create_map_surface()
        self.notpacman = NotPacMan(1, 1)
        self.ghosts = [
          Ghost(12, 11, (255, 0, 0)),  # Red Ghost
          Ghost(13, 11, (255, 128, 0)),  # Orange Ghost
          Ghost(14, 11, (0, 255, 0)),  # Green Ghost
          Ghost(15, 11, (0, 0, 255))   # Blue Ghost
        ]
        # Other initialization

    def update(self):
        # Handle key inputs and update game state
        self.handle_human_input()
        self.notpacman.move(self.game_map)
        current_cell = self.game_map.get_cell(self.notpacman.grid_x, self.notpacman.grid_y)
        if current_cell.is_regular_dot or current_cell.is_powerup_dot:
            self.game_map.eat_dot(self.notpacman.grid_x, self.notpacman.grid_y)
        for ghost in self.ghosts:
          ghost.move(self.game_map)
          # Check for collision with NotPacMan
          #if self.notpacman.grid_x == ghost.grid_x and self.notpacman.grid_y == ghost.grid_y:
        # Other updates

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

    def draw(self):
        self.screen.fill((0, 0, 0))  # Clear screen
        self.game_map.draw(self.screen)
        self.notpacman.draw(self.screen)
        for ghost in self.ghosts:
          ghost.draw(self.screen)
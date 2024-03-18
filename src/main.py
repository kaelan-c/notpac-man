import pygame
import sys
from game import Game

def main():
  pygame.init()
  cell_size = 20  # Size of each cell in pixels
  wall_color = (0, 0, 255)  # Blue color for walls
  out_of_map_color = (0, 0, 0)  # Black color for out-of-map areas
  screen = pygame.display.set_mode((28 * cell_size, 31 * cell_size))
  clock = pygame.time.Clock()
  pygame.display.set_caption("Pac-Man")

  clock = pygame.time.Clock()
  game = Game(screen)

    # Main game loop
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    game.update()
    game.draw()

    pygame.display.flip()
    clock.tick(60)  # Limit the frame rate to 60 FPS

if __name__ == "__main__":
    main()

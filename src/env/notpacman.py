import pygame

class NotPacMan:
    # Initialize the Pac-Man character
    def __init__(self, cell_size):
        # # Pac-Man's initial position on the grid classicmap.txt
        # self.grid_x = 14
        # self.grid_y = 17

        # Pac-Man's initial position on the grid classicmap.txt
        self.grid_x = 11
        self.grid_y = 11

        # Current and desired moving directions (initially set to 'RIGHT')
        self.direction = 'RIGHT'
        self.desired_direction = 'RIGHT'

        # Previous grid position for collision and movement logic
        self.prev_grid_x = 11
        self.prev_grid_y = 11

        # Cell size for drawing purposes
        self.cell_size = cell_size

    # Check if Pac-Man can move in a specified direction
    def can_move(self, game_map, direction):
        # Store previous position before attempting to move
        self.prev_grid_x = self.grid_x
        self.prev_grid_y = self.grid_y

        # Calculate new position based on the current direction
        new_x, new_y = self.grid_x, self.grid_y
        if direction == "LEFT":
            new_x -= 1
        elif direction == "RIGHT":
            new_x += 1
        elif direction == "UP":
            new_y -= 1
        elif direction == "DOWN":
            new_y += 1

        # Check if the new position is a wall
        return not game_map.is_wall(new_x, new_y)
  
    # Move Pac-Man based on the current and desired directions
    def move(self, game_map):
        # Handling for Pac-Man's teleportation through tunnel
        if self.grid_x == -1 and self.grid_y == 9:
            self.grid_x = 18
            return
        elif self.grid_x == 18 and self.grid_y == 9:
            self.grid_x = 0
            return
        
        # Update current direction if desired direction is possible
        if self.can_move(game_map, self.desired_direction):
            self.direction = self.desired_direction
        
        # Move Pac-Man in the current direction if possible
        if self.can_move(game_map, self.direction):
            if self.direction == "LEFT":
                self.grid_x -= 1
            elif self.direction == "RIGHT":
                self.grid_x += 1
            elif self.direction == "UP":
                self.grid_y -= 1
            elif self.direction == "DOWN":
                self.grid_y += 1

    # Draw Pac-Man on the screen
    def draw(self, screen):
        # Calculate Pac-Man's position in pixels
        pixel_x = self.grid_x * self.cell_size
        pixel_y = self.grid_y * self.cell_size
        radius = self.cell_size // 2  # Radius for the Pac-Man circle

        # Draw Pac-Man as a yellow circle
        pygame.draw.circle(screen, (255, 255, 0), (pixel_x + radius, pixel_y + radius), radius)

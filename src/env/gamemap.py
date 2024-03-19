import pygame
from env.gridcell import GridCell

class GameMap:
    # Initialization of the GameMap
    def __init__(self, filename):
        # Initializing dimensions and grid
        self.width = 0
        self.height = 0
        self.cell_size = 0
        self.num_ghosts = 0
        self.dots_total = 246  # Total number of dots available in the game
        self.grid = []  # Grid representing the game map
        self.load_map(filename)  # Load the map from the given filename

    # Load the game map from a file
    def load_map(self, filename):
        with open(filename, 'r') as file:
            # Read the first line to get map dimensions and settings
            self.width, self.height, self.cell_size, self.num_ghosts = map(int, file.readline().strip().split(','))

            # Process the remaining lines to build the grid
            for line in file:
                row = []
                for cell_type in line.strip():
                    row.append(GridCell(cell_type))  # Create a GridCell for each character
                self.grid.append(row)

    # Retrieve a specific cell from the grid
    def get_cell(self, x, y):
        return self.grid[y][x]

    # Check if a specific coordinate is a wall
    def is_wall(self, x, y):
        # Ensure coordinates are within bounds
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x].is_wall
        return False  # Treat out-of-bounds as walls

    # Create a visual representation of the game map
    def create_map_surface(self):
        # Set up drawing parameters
        cell_size = self.cell_size
        wall_color = (0, 0, 255)  # Color for walls
        dot_color = (255, 255, 255)  # Color for dots
        powerup_color = (255, 0, 0)  # Color for power-ups
        dot_radius = cell_size // 8
        powerup_radius = cell_size // 4

        # Create a surface for the game map
        self.map_surface = pygame.Surface((self.width * cell_size, self.height * cell_size))

        # Draw each cell in the grid
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                center = (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2)
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                # Draw different elements based on the cell type
                if cell.is_wall:
                    pygame.draw.rect(self.map_surface, wall_color, rect)
                elif cell.is_regular_dot:
                    pygame.draw.circle(self.map_surface, dot_color, center, dot_radius)
                elif cell.is_powerup_dot:
                    pygame.draw.circle(self.map_surface, powerup_color, center, powerup_radius)

    # Consume a dot at a specific coordinate
    def eat_dot(self, x, y):
        cell = self.get_cell(x, y)
        cell.consume_dot()
        self.dots_total -= 1
        self.create_map_surface()  # Redraw the map to reflect the change

    # Draw the game map on the screen
    def draw(self, screen):
        screen.blit(self.map_surface, (0, 0))
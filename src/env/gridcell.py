# GridCell class is used to represent each cell in the game map
class GridCell:
    # Cell types
    WALL = '#'
    OUT_OF_MAP = '/'
    POWERUP_DOT = '@'
    REGULAR_DOT = '.'
    EMPTY_SPACE = '0'

    # Initialize a cell with a given type
    def __init__(self, cell_type):
        self.type = cell_type
        self.is_wall = cell_type == GridCell.WALL
        self.is_out_of_map = cell_type == GridCell.OUT_OF_MAP
        self.is_powerup_dot = cell_type == GridCell.POWERUP_DOT
        self.is_regular_dot = cell_type == GridCell.REGULAR_DOT
        self.is_empty_space = cell_type == GridCell.EMPTY_SPACE

    # Update the cell to reflect a consumed dot
    def consume_dot(self):
        if self.is_regular_dot or self.is_powerup_dot:
            self.type = GridCell.EMPTY_SPACE
            self.is_regular_dot = False
            self.is_powerup_dot = False
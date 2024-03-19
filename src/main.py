import pygame
import sys
import os
import pickle
from game import Game
from agent import QLearningAgent

def load_q_table(filename='q_table.pkl'):
    # Load a Q-table from the specified file if it exists.
    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    return None

def get_map_dimensions(filename):
    # Read the first line of the map file to get map dimensions.
    with open(filename, 'r') as file:
        dimensions = file.readline().strip().split(',')
        if len(dimensions) != 4:
            raise ValueError("Map file does not have the correct number of dimensions")
        return int(dimensions[0]), int(dimensions[1]), int(dimensions[2]), int(dimensions[3])

def main():
    pygame.init()  # Initialize the Pygame library

    map_file = 'env/maps/simplemap.txt'  # Specify the path to the map file
    # Extract the map dimensions from the file
    width, height, cell_size, num_ghosts = get_map_dimensions(map_file)
    # Set up the Pygame display window
    screen = pygame.display.set_mode((width * cell_size, height * cell_size))
    pygame.display.set_caption("!Pac-Man")  # Set the window title

    q_table = load_q_table()  # Load the Q-table for the AI agent
    action_space = 4  # Define the number of possible actions (UP, DOWN, LEFT, RIGHT)
    # Create an AI agent with the loaded Q-table
    agent = QLearningAgent(action_space, learning_rate=0, discount_factor=0, epsilon=0, q_table=q_table)

    tick_rate = 10  # Define the game's update speed
    # Initialize the game environment with the given parameters
    game = Game(screen, tick_rate, cell_size, num_ghosts, map_file)

    # Main game loop
    while True:
        for event in pygame.event.get():
            # Handle the window close event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        state = game.get_state()  # Get the current state of the game
        action = agent.choose_action(state)  # Let the AI agent choose an action
        game.step(action)  # Update the game with the chosen action

        game.render()  # Render the game state to the screen
        pygame.display.flip()  # Update the display
        pygame.time.wait(int(1500 / tick_rate))  # Control game speed for better observation

if __name__ == "__main__":
    main()  # Run the main function when the script is executed

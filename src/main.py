import pygame
import sys
import os
import pickle
from game import Game
from agent import QLearningAgent

def load_q_table(filename='q_table.pkl'):
    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    return None

def main():
    pygame.init()
    cell_size = 20  # Size of each cell in pixels
    screen = pygame.display.set_mode((28 * cell_size, 31 * cell_size))
    pygame.display.set_caption("!Pac-Man")

    q_table = load_q_table()
    action_space = 4  # UP, DOWN, LEFT, RIGHT
    agent = QLearningAgent(action_space, learning_rate=0, discount_factor=0, epsilon=0, q_table=q_table)

    # Set a lower tick rate to slow down the game
    tick_rate = 10  # Adjust this value as needed
    game = Game(screen, tick_rate=tick_rate)

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        state = game.get_state()
        action = agent.choose_action(state)
        game.step(action)

        game.render()
        pygame.display.flip()
        pygame.time.wait(int(1500 / tick_rate))  # Wait to control the game speed

if __name__ == "__main__":
    main()

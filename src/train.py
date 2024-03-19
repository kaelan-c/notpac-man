# Import necessary libraries
import pickle
import os
import pygame
from game import Game
from agent import QLearningAgent

# Training configuration constants
NUM_EPISODES = 1000  # Total number of episodes for training
PRINT_EVERY = 100    # Frequency for printing average rewards
FILE_NAME = "pacman_training_data.txt"  # File name for saving training data

# Function to save the Q-table to a file
def save_q_table(agent, filename='q_table.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(agent.q_table, f)

# Function to load a Q-table from a file
def load_q_table(filename='q_table.pkl'):
    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    return None

# Function to read and return map dimensions from a file
def get_map_dimensions(filename):
    with open(filename, 'r') as file:
        dimensions = file.readline().strip().split(',')
        if len(dimensions) != 4:
            raise ValueError("Map file does not have the correct number of dimensions")
        return int(dimensions[0]), int(dimensions[1]), int(dimensions[2]), int(dimensions[3])

# Main training function
def train():
    # Initialize Pygame
    pygame.init()

    # Load map configurations
    map_file = 'env/maps/simplemap.txt'
    width, height, cell_size, num_ghosts = get_map_dimensions(map_file)

    # Agent and training parameters
    action_space = 4  # Number of possible actions (UP, DOWN, LEFT, RIGHT)
    learning_rate = 0.1
    discount_factor = 0.99
    epsilon = 0.1
    q_table = load_q_table()

    # Initialize the Q-Learning agent
    agent = QLearningAgent(action_space, learning_rate, discount_factor, epsilon, q_table)
    total_reward_for_print = 0

    # Training loop over episodes
    for episode in range(NUM_EPISODES):
        # Initialize the game environment
        game = Game(screen=None, tick_rate=30000, cell_size=cell_size, num_ghosts=num_ghosts, map_file=map_file, headless=True)
        done = False
        total_reward = 0
        state = game.get_state()

        # Loop for each step within an episode
        while not done:
            # Agent selects an action based on the current state
            action = agent.choose_action(state)
            # Perform the action and receive new state and reward
            new_state, reward, done = game.step(action)
            # Agent updates its Q-table based on the experience
            agent.learn(state, action, reward, new_state)

            state = new_state
            total_reward += reward

        # Print and save training progress
        total_reward_for_print += total_reward
        if (episode + 1) % PRINT_EVERY == 0:
            avg_reward = total_reward_for_print / PRINT_EVERY
            print(f"Episode: {episode+1}, Average Reward: {avg_reward}")
            total_reward_for_print = 0
            with open(FILE_NAME, 'a') as f:
                f.write(f"Episode: {episode+1}, Average Reward: {avg_reward}\n")

        # Save the Q-table periodically
        if (episode + 1) % 100 == 0:
            save_q_table(agent)

    # Save the Q-table after training completion
    save_q_table(agent)

if __name__ == "__main__":
    train()

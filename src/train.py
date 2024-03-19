import pickle
import os
import pygame
from game import Game
from agent import QLearningAgent

NUM_EPISODES = 1000
PRINT_EVERY = 100  # for averaging stats
FILE_NAME = "pacman_training_data.txt"

def save_q_table(agent, filename='q_table.pkl'):
  with open(filename, 'wb') as f:
      pickle.dump(agent.q_table, f)

def load_q_table(filename='q_table.pkl'):
  if os.path.isfile(filename):
      with open(filename, 'rb') as f:
          return pickle.load(f)
  return None

def train():
    pygame.init()
    action_space = 4  # UP, DOWN, LEFT, RIGHT
    learning_rate = 0.1
    discount_factor = 0.99
    epsilon = 0.1
    q_table = load_q_table()

    agent = QLearningAgent(action_space, learning_rate, discount_factor, epsilon, q_table)
    total_reward_for_print = 0

    for episode in range(NUM_EPISODES):
        game = Game(screen=None, tick_rate=30000, headless=True)
        done = False
        total_reward = 0
        state = game.get_state()

        while not done:
            action = agent.choose_action(state)
            new_state, reward, done = game.step(action)
            agent.learn(state, action, reward, new_state)

            state = new_state
            total_reward += reward

        total_reward_for_print += total_reward

        if (episode + 1) % PRINT_EVERY == 0:
            avg_reward = total_reward_for_print / PRINT_EVERY
            print(f"Episode: {episode+1}, Average Reward: {avg_reward}")
            total_reward_for_print = 0
            with open(FILE_NAME, 'a') as f:
                f.write(f"Episode: {episode+1}, Average Reward: {avg_reward}\n")

        # Save the Q-table at intervals
        if (episode + 1) % 1000 == 0:
            save_q_table(agent)

    save_q_table(agent)  # Final save after training

if __name__ == "__main__":
    train()
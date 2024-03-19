import numpy as np
import random

class QLearningAgent:
    # Initialization of the Q-learning agent
    def __init__(self, action_space, learning_rate, discount_factor, epsilon, q_table=None):
        # Q-table which stores the Q-values for state-action pairs
        self.q_table = q_table if q_table is not None else {}

        # Learning rate determines how much new information overrides old information
        self.learning_rate = learning_rate

        # Discount factor indicates the importance of future rewards
        self.discount_factor = discount_factor

        # Epsilon value for epsilon-greedy strategy (balance between exploration and exploitation)
        self.epsilon = epsilon

        # Number of actions available in the action space
        self.action_space = action_space

    # Method for choosing an action based on the current state
    def choose_action(self, state):
        # Convert state to a tuple for consistency and use as a key in the Q-table
        state_tuple = tuple(state)

        # Initialize Q-values for a new state in the Q-table
        if state_tuple not in self.q_table:
            self.q_table[state_tuple] = [0 for _ in range(self.action_space)]

        # Epsilon-greedy action selection
        if random.uniform(0, 1) < self.epsilon:
            # Exploration: Choose a random action
            return random.randint(0, self.action_space - 1)
        else:
            # Exploitation: Choose the best known action (max Q-value)
            return np.argmax(self.q_table[state_tuple])

    # Method for updating the Q-table based on the agent's experience
    def learn(self, state, action, reward, next_state):
        # Convert states to tuples for consistency
        state_tuple = tuple(state)
        next_state_tuple = tuple(next_state)

        # Initialize Q-values for a new next state in the Q-table
        if next_state_tuple not in self.q_table:
            self.q_table[next_state_tuple] = [0 for _ in range(self.action_space)]

        # Q-function update formula
        predict = self.q_table[state_tuple][action]
        target = reward + self.discount_factor * max(self.q_table[next_state_tuple])
        self.q_table[state_tuple][action] += self.learning_rate * (target - predict)

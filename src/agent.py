import numpy as np
import random

class QLearningAgent:
    def __init__(self, action_space, learning_rate, discount_factor, epsilon, q_table=None):
        self.q_table = q_table if q_table is not None else {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.action_space = action_space

    def choose_action(self, state):
        state_tuple = tuple(state)  # Convert state to tuple
        if state_tuple not in self.q_table:
            self.q_table[state_tuple] = [0 for _ in range(self.action_space)]

        if random.uniform(0, 1) < self.epsilon:
            return random.randint(0, self.action_space - 1)  # Explore
        else:
            return np.argmax(self.q_table[state_tuple])  # Exploit

    def learn(self, state, action, reward, next_state):
        state_tuple = tuple(state)
        next_state_tuple = tuple(next_state)

        if next_state_tuple not in self.q_table:
            self.q_table[next_state_tuple] = [0 for _ in range(self.action_space)]

        predict = self.q_table[state_tuple][action]
        target = reward + self.discount_factor * max(self.q_table[next_state_tuple])
        self.q_table[state_tuple][action] += self.learning_rate * (target - predict)
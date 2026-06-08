import numpy as np
import json
import random


class QAgent:
    def __init__(self, name, n_states, n_actions, lr=0.1, gamma=0.9,
                 epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995):
        self.name = name
        self.n_states = n_states
        self.n_actions = n_actions
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.q_table = np.zeros((n_states, n_actions))

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, self.n_actions - 1)
        return int(np.argmax(self.q_table[state]))

    def update(self, state, action, reward, next_state, done):
        future = 0 if done else np.max(self.q_table[next_state])
        td_target = reward + self.gamma * future
        td_error = td_target - self.q_table[state, action]
        self.q_table[state, action] += self.lr * td_error

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def export_q_table(self, filename, state_decoder=None):
        state_descriptions = None
        if state_decoder:
            state_descriptions = []
            for i in range(self.n_states):
                state_descriptions.append(state_decoder(i))

        data = {
            "agent": self.name,
            "n_states": self.n_states,
            "n_actions": self.n_actions,
            "action_names": self.ACTIONS if hasattr(self, 'ACTIONS') else [f"a{i}" for i in range(self.n_actions)],
            "q_table": self.q_table.tolist(),
            "state_descriptions": state_descriptions,
            "hyperparameters": {
                "learning_rate": self.lr,
                "gamma": self.gamma,
                "epsilon": self.epsilon
            }
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"[{self.name}] Q-table exported -> {filename}")
        return filename

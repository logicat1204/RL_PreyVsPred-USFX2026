import random
import numpy as np
from QAgent import QAgent
from Environment import Environment


class Predator(QAgent):
    PS_LEVELS = 3
    HB_LEVELS = 3
    PJ_LEVELS = 2

    N_STATES = PS_LEVELS * HB_LEVELS * PJ_LEVELS
    N_ACTIONS = 5

    ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT", "STAY"]
    DIRS = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1), "STAY": (0, 0)}

    _shared_q = None

    def __init__(self, name, lr=0.1, gamma=0.9, epsilon=1.0):
        if Predator._shared_q is None:
            Predator._shared_q = np.zeros((Predator.N_STATES, Predator.N_ACTIONS))
        self.name = name
        self.n_states = Predator.N_STATES
        self.n_actions = Predator.N_ACTIONS
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.q_table = Predator._shared_q

        self.hambre = 100
        self.max_hambre = 100
        self.pos = None
        self.alive = True
        self.repro_cooldown = 0
        self.steps_hambre_cero = 0

    def reset(self, pos):
        self.pos = pos
        self.hambre = 100
        self.alive = True
        self.repro_cooldown = 0
        self.steps_hambre_cero = 0

    def get_state(self, env):
        preys = env.PosPreys()

        if not preys:
            pres = 0
        else:
            d = min(env.manhattan(self.pos, p) for p in preys)
            pres = 2 if d < 3 else 1

        ratio = self.hambre / self.max_hambre
        hs = 0 if ratio > 0.7 else (1 if ratio > 0.3 else 2)

        preds = env.PosPreds()
        others = [p for p in preds if p != self.pos]
        ps = 1 if others else 0

        return (pres +
                hs * self.PS_LEVELS +
                ps * self.PS_LEVELS * self.HB_LEVELS)

    def apply_action(self, env, action_idx):
        dx, dy = self.DIRS[self.ACTIONS[action_idx]]
        new_pos = (self.pos[0] + dx, self.pos[1] + dy)
        reward = -1

        if not env.is_valid(new_pos):
            return reward

        target = env.get_cell(new_pos)

        if target == Environment.EMPTY:
            env.set_cell(self.pos, Environment.EMPTY)
            env.set_cell(new_pos, Environment.PREDATOR)
            self.pos = new_pos

        elif target == Environment.PREY:
            env.set_cell(self.pos, Environment.EMPTY)
            env.set_cell(new_pos, Environment.PREDATOR)
            self.pos = new_pos
            self.hambre = min(self.max_hambre, self.hambre + 60)
            reward += 20

        else:
            reward -= 2

        self.hambre = max(0, self.hambre - 2)
        if self.hambre == 0:
            self.steps_hambre_cero += 1
            reward -= 10
            if self.steps_hambre_cero >= 5:
                self.alive = False
        else:
            self.steps_hambre_cero = 0

        if self.repro_cooldown > 0:
            self.repro_cooldown -= 1

        return reward

    def try_reproduce(self, env, all_preds):
        if not self.alive or self.hambre <= 70 or self.repro_cooldown > 0:
            return []

        has_mate = any(
            o is not self and o.alive and o.hambre > 50
            and env.manhattan(self.pos, o.pos) <= 2
            for o in all_preds
        )
        if not has_mate:
            return []

        n = random.randint(1, 3)
        cells = env.nearest_empty(self.pos, n)
        offspring = []
        for pos in cells:
            child = Predator(f"{self.name}_hijo_{len(all_preds) + len(offspring)}",
                             self.lr, self.gamma, self.epsilon)
            child.pos = pos
            child.hambre = 50
            child.repro_cooldown = 10
            child.q_table = Predator._shared_q
            env.set_cell(pos, Environment.PREDATOR)
            offspring.append(child)

        self.hambre = max(0, self.hambre - 20)
        self.repro_cooldown = 10
        return offspring

    @staticmethod
    def decode_state(idx):
        ps = idx // (Predator.PS_LEVELS * Predator.HB_LEVELS)
        rem = idx % (Predator.PS_LEVELS * Predator.HB_LEVELS)
        hs = rem // Predator.PS_LEVELS
        pres = rem % Predator.PS_LEVELS
        return {
            "state_idx": idx,
            "presa": {0: "ninguna", 1: "lejana", 2: "cercana"}[pres],
            "hambre": {0: "satisfecho", 1: "hambriento", 2: "hambriento_critico"}[hs],
            "pareja": {0: "sin_pareja", 1: "con_pareja"}[ps]
        }

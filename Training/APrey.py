import random
import numpy as np
from QAgent import QAgent
from Environment import Environment


class Prey(QAgent):
    RS_LEVELS = 3
    HB_LEVELS = 3
    PJ_LEVELS = 2
    PR_LEVELS = 3

    N_STATES = RS_LEVELS * HB_LEVELS * PJ_LEVELS * PR_LEVELS
    N_ACTIONS = 5

    ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT", "STAY"]
    DIRS = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1), "STAY": (0, 0)}

    _shared_q = None

    def __init__(self, name, lr=0.1, gamma=0.9, epsilon=1.0):
        if Prey._shared_q is None:
            Prey._shared_q = np.zeros((Prey.N_STATES, Prey.N_ACTIONS))
        self.name = name
        self.n_states = Prey.N_STATES
        self.n_actions = Prey.N_ACTIONS
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.q_table = Prey._shared_q

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
        recursos = env.PosRecursos()
        preds = env.PosPreds()
        preys = env.PosPreys()

        if not recursos:
            rs = 0
        else:
            d = min(env.manhattan(self.pos, r) for r in recursos)
            rs = 2 if d <= 1 else 1

        ratio = self.hambre / self.max_hambre
        hs = 0 if ratio > 0.7 else (1 if ratio > 0.3 else 2)

        others = [p for p in preys if p != self.pos]
        ps = 1 if others else 0

        if not preds:
            prs = 0
        else:
            d = min(env.manhattan(self.pos, p) for p in preds)
            prs = 2 if d < 3 else 1

        return (rs +
                hs * self.RS_LEVELS +
                ps * self.RS_LEVELS * self.HB_LEVELS +
                prs * self.RS_LEVELS * self.HB_LEVELS * self.PJ_LEVELS)

    def apply_action(self, env, action_idx):
        dx, dy = self.DIRS[self.ACTIONS[action_idx]]
        new_pos = (self.pos[0] + dx, self.pos[1] + dy)
        reward = -1

        if not env.is_valid(new_pos):
            return reward

        target = env.get_cell(new_pos)

        if target == Environment.EMPTY:
            env.set_cell(self.pos, Environment.EMPTY)
            env.set_cell(new_pos, Environment.PREY)
            self.pos = new_pos

        elif target == Environment.RESOURCE:
            env.set_cell(self.pos, Environment.EMPTY)
            env.set_cell(new_pos, Environment.PREY)
            self.pos = new_pos
            self.hambre = min(self.max_hambre, self.hambre + 40)
            reward += 10

        elif target == Environment.PREDATOR:
            reward -= 3

        else:
            reward -= 2

        self.hambre = max(0, self.hambre - 1)
        if self.hambre == 0:
            self.steps_hambre_cero += 1
            reward -= 5
            if self.steps_hambre_cero >= 5:
                self.alive = False
        else:
            self.steps_hambre_cero = 0

        if self.repro_cooldown > 0:
            self.repro_cooldown -= 1

        return reward

    def try_reproduce(self, env, all_preys):
        if not self.alive or self.hambre <= 70 or self.repro_cooldown > 0:
            return []

        has_mate = any(
            o is not self and o.alive and o.hambre > 50
            and env.manhattan(self.pos, o.pos) <= 2
            for o in all_preys
        )
        if not has_mate:
            return []

        n = random.randint(1, 3)
        cells = env.nearest_empty(self.pos, n)
        offspring = []
        for pos in cells:
            child = Prey(f"{self.name}_hijo_{len(all_preys) + len(offspring)}",
                         self.lr, self.gamma, self.epsilon)
            child.pos = pos
            child.hambre = 50
            child.repro_cooldown = 10
            child.q_table = Prey._shared_q
            env.set_cell(pos, Environment.PREY)
            offspring.append(child)

        self.hambre = max(0, self.hambre - 20)
        self.repro_cooldown = 10
        return offspring

    @staticmethod
    def decode_state(idx):
        prs = idx // (Prey.RS_LEVELS * Prey.HB_LEVELS * Prey.PJ_LEVELS)
        rem = idx % (Prey.RS_LEVELS * Prey.HB_LEVELS * Prey.PJ_LEVELS)
        ps = rem // (Prey.RS_LEVELS * Prey.HB_LEVELS)
        rem2 = rem % (Prey.RS_LEVELS * Prey.HB_LEVELS)
        hs = rem2 // Prey.RS_LEVELS
        rs = rem2 % Prey.RS_LEVELS
        return {
            "state_idx": idx,
            "recurso": {0: "ninguno", 1: "lejano", 2: "cercano"}[rs],
            "hambre": {0: "satisfecho", 1: "hambriento", 2: "hambriento_critico"}[hs],
            "pareja": {0: "sin_pareja", 1: "con_pareja"}[ps],
            "depredador": {0: "ninguno", 1: "lejano", 2: "cercano"}[prs]
        }

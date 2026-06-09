import random
import numpy as np
from QAgent import QAgent
from Environment import Environment


class Predator(QAgent):
    PRES_LEVELS = 3
    PREDIR_LEVELS = 5
    HB_LEVELS = 3
    RR_LEVELS = 2

    N_STATES = PRES_LEVELS * PREDIR_LEVELS * HB_LEVELS * RR_LEVELS
    N_ACTIONS = 5

    ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT", "STAY"]
    DIRS = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1), "STAY": (0, 0)}

    _shared_q = None

    def __init__(self, name, lr=0.1, gamma=0.9, epsilon=1.0):
        if Predator._shared_q is None:
            Predator._shared_q = Predator.initial_q_table()
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

    @staticmethod
    def direction_to(src, dst):
        dx = dst[0] - src[0]
        dy = dst[1] - src[1]
        if dx == 0 and dy == 0:
            return 0
        if abs(dx) >= abs(dy):
            return 1 if dx < 0 else 2
        return 3 if dy < 0 else 4

    def nearest_info(self, env, positions):
        if not positions:
            return None, 0
        target = min(positions, key=lambda p: env.manhattan(self.pos, p))
        return env.manhattan(self.pos, target), self.direction_to(self.pos, target)

    def get_state(self, env):
        preys = env.PosPreys()

        prey_dist, prey_dir = self.nearest_info(env, preys)
        if prey_dist is None:
            pres = 0
        elif prey_dist <= 1:
            pres = 2
        elif prey_dist <= 5:
            pres = 1
        else:
            pres = 0

        ratio = self.hambre / self.max_hambre
        hs = 0 if ratio > 0.7 else (1 if ratio > 0.3 else 2)

        nearby_mate = any(
            p != self.pos and env.manhattan(self.pos, p) <= 2
            for p in env.PosPreds()
        )
        rr = 1 if nearby_mate else 0

        return (pres +
                prey_dir * self.PRES_LEVELS +
                hs * self.PRES_LEVELS * self.PREDIR_LEVELS +
                rr * self.PRES_LEVELS * self.PREDIR_LEVELS * self.HB_LEVELS)

    def apply_action(self, env, action_idx):
        before_prey, _ = self.nearest_info(env, env.PosPreys())

        dx, dy = self.DIRS[self.ACTIONS[action_idx]]
        new_pos = (self.pos[0] + dx, self.pos[1] + dy)
        reward = -1

        if not env.is_valid(new_pos):
            reward -= 4
        else:
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
                reward += 40

            else:
                reward -= 3

        after_prey, _ = self.nearest_info(env, env.PosPreys())
        if before_prey is not None and after_prey is not None:
            if after_prey < before_prey:
                reward += 3
            elif after_prey > before_prey:
                reward -= 2

        if action_idx == self.ACTIONS.index("STAY"):
            reward -= 2

        self.hambre = max(0, self.hambre - 1)
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

    def try_reproduce(self, env, all_preds, max_population=None):
        if not self.alive or self.hambre <= 70 or self.repro_cooldown > 0:
            return []
        if max_population is not None and len(all_preds) >= max_population:
            return []

        has_mate = any(
            o is not self and o.alive and o.hambre > 50
            and env.manhattan(self.pos, o.pos) <= 2
            for o in all_preds
        )
        if not has_mate:
            return []

        n = random.randint(1, 3)
        if max_population is not None:
            n = min(n, max_population - len(all_preds))
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
    def initial_q_table():
        q = np.full((Predator.N_STATES, Predator.N_ACTIONS), -1.0)
        action_dir = [1, 2, 3, 4, 0]
        opposite = {1: 2, 2: 1, 3: 4, 4: 3}

        for s in range(Predator.N_STATES):
            idx = Predator.decode_indices(s)
            q[s, 4] -= 2.0

            if idx["prey_dir"] > 0:
                chase = 10.0 if idx["prey_level"] == 2 else 5.0
                if idx["hunger"] == 2:
                    chase += 4.0
                for a, d in enumerate(action_dir):
                    if d == idx["prey_dir"]:
                        q[s, a] += chase
                    elif d == opposite.get(idx["prey_dir"]):
                        q[s, a] -= 3.0

        return q

    @staticmethod
    def decode_indices(idx):
        rr = idx // (Predator.PRES_LEVELS * Predator.PREDIR_LEVELS * Predator.HB_LEVELS)
        rem = idx % (Predator.PRES_LEVELS * Predator.PREDIR_LEVELS * Predator.HB_LEVELS)
        hs = rem // (Predator.PRES_LEVELS * Predator.PREDIR_LEVELS)
        rem = rem % (Predator.PRES_LEVELS * Predator.PREDIR_LEVELS)
        prey_dir = rem // Predator.PRES_LEVELS
        pres = rem % Predator.PRES_LEVELS
        return {
            "prey_level": pres,
            "prey_dir": prey_dir,
            "hunger": hs,
            "mate_near": rr
        }

    @staticmethod
    def decode_state(idx):
        decoded = Predator.decode_indices(idx)
        pres = decoded["prey_level"]
        prey_dir = decoded["prey_dir"]
        hs = decoded["hunger"]
        rr = decoded["mate_near"]
        return {
            "state_idx": idx,
            "presa": {0: "lejana_o_ninguna", 1: "media", 2: "adyacente"}[pres],
            "dir_presa": {0: "ninguna", 1: "arriba", 2: "abajo", 3: "izquierda", 4: "derecha"}[prey_dir],
            "hambre": {0: "satisfecho", 1: "hambriento", 2: "hambriento_critico"}[hs],
            "buscar_pareja": {0: "no", 1: "si"}[rr]
        }

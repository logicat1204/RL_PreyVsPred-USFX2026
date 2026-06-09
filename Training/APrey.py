import random
import numpy as np
from QAgent import QAgent
from Environment import Environment


class Prey(QAgent):
    RS_LEVELS = 3
    RD_LEVELS = 5
    HB_LEVELS = 3
    RR_LEVELS = 2
    PR_LEVELS = 3
    PD_LEVELS = 5

    N_STATES = RS_LEVELS * RD_LEVELS * HB_LEVELS * RR_LEVELS * PR_LEVELS * PD_LEVELS
    N_ACTIONS = 5

    ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT", "STAY"]
    DIRS = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1), "STAY": (0, 0)}

    _shared_q = None

    def __init__(self, name, lr=0.1, gamma=0.9, epsilon=1.0):
        if Prey._shared_q is None:
            Prey._shared_q = Prey.initial_q_table()
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
        recursos = env.PosRecursos()
        preds = env.PosPreds()

        resource_dist, rd = self.nearest_info(env, recursos)
        if resource_dist is None:
            rs = 0
        elif resource_dist <= 1:
            rs = 2
        elif resource_dist <= 5:
            rs = 1
        else:
            rs = 0

        ratio = self.hambre / self.max_hambre
        hs = 0 if ratio > 0.7 else (1 if ratio > 0.3 else 2)

        nearby_mate = any(
            p != self.pos and env.manhattan(self.pos, p) <= 2
            for p in env.PosPreys()
        )
        rr = 1 if nearby_mate else 0

        predator_dist, pd = self.nearest_info(env, preds)
        if predator_dist is None:
            prs = 0
        elif predator_dist < 3:
            prs = 2
        elif predator_dist <= 5:
            prs = 1
        else:
            prs = 0

        return (rs +
                rd * self.RS_LEVELS +
                hs * self.RS_LEVELS * self.RD_LEVELS +
                rr * self.RS_LEVELS * self.RD_LEVELS * self.HB_LEVELS +
                prs * self.RS_LEVELS * self.RD_LEVELS * self.HB_LEVELS * self.RR_LEVELS +
                pd * self.RS_LEVELS * self.RD_LEVELS * self.HB_LEVELS * self.RR_LEVELS * self.PR_LEVELS)

    def apply_action(self, env, action_idx):
        before_resource, _ = self.nearest_info(env, env.PosRecursos())
        before_predator, _ = self.nearest_info(env, env.PosPreds())

        dx, dy = self.DIRS[self.ACTIONS[action_idx]]
        new_pos = (self.pos[0] + dx, self.pos[1] + dy)
        reward = -1

        if not env.is_valid(new_pos):
            reward -= 4

        else:
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
                reward += 25

            elif target == Environment.PREDATOR:
                reward -= 25

            else:
                reward -= 3

        after_resource, _ = self.nearest_info(env, env.PosRecursos())
        after_predator, _ = self.nearest_info(env, env.PosPreds())

        if before_resource is not None and after_resource is not None and self.hambre <= 70:
            if after_resource < before_resource:
                reward += 2
            elif after_resource > before_resource:
                reward -= 1

        if before_predator is not None and after_predator is not None and before_predator <= 5:
            if after_predator > before_predator:
                reward += 3
            elif after_predator < before_predator:
                reward -= 4

        if action_idx == self.ACTIONS.index("STAY"):
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

    def try_reproduce(self, env, all_preys, max_population=None):
        if not self.alive or self.hambre <= 70 or self.repro_cooldown > 0:
            return []
        if max_population is not None and len(all_preys) >= max_population:
            return []

        has_mate = any(
            o is not self and o.alive and o.hambre > 50
            and env.manhattan(self.pos, o.pos) <= 2
            for o in all_preys
        )
        if not has_mate:
            return []

        n = random.randint(1, 3)
        if max_population is not None:
            n = min(n, max_population - len(all_preys))
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
    def initial_q_table():
        q = np.full((Prey.N_STATES, Prey.N_ACTIONS), -1.0)
        action_dir = [1, 2, 3, 4, 0]
        opposite = {1: 2, 2: 1, 3: 4, 4: 3}

        for s in range(Prey.N_STATES):
            idx = Prey.decode_indices(s)
            q[s, 4] -= 2.0

            if idx["predator_dir"] in opposite and idx["predator_level"] > 0:
                danger = 8.0 if idx["predator_level"] == 2 else 4.0
                for a, d in enumerate(action_dir):
                    if d == idx["predator_dir"]:
                        q[s, a] -= danger
                    elif d == opposite[idx["predator_dir"]]:
                        q[s, a] += danger

            if idx["resource_dir"] > 0 and idx["hunger"] > 0:
                food = 8.0 if idx["resource_level"] == 2 else 4.0
                if idx["hunger"] == 2:
                    food += 3.0
                for a, d in enumerate(action_dir):
                    if d == idx["resource_dir"]:
                        q[s, a] += food
                    elif d == opposite.get(idx["resource_dir"]):
                        q[s, a] -= 2.0

        return q

    @staticmethod
    def decode_indices(idx):
        pd = idx // (Prey.RS_LEVELS * Prey.RD_LEVELS * Prey.HB_LEVELS * Prey.RR_LEVELS * Prey.PR_LEVELS)
        rem = idx % (Prey.RS_LEVELS * Prey.RD_LEVELS * Prey.HB_LEVELS * Prey.RR_LEVELS * Prey.PR_LEVELS)
        prs = rem // (Prey.RS_LEVELS * Prey.RD_LEVELS * Prey.HB_LEVELS * Prey.RR_LEVELS)
        rem = rem % (Prey.RS_LEVELS * Prey.RD_LEVELS * Prey.HB_LEVELS * Prey.RR_LEVELS)
        rr = rem // (Prey.RS_LEVELS * Prey.RD_LEVELS * Prey.HB_LEVELS)
        rem = rem % (Prey.RS_LEVELS * Prey.RD_LEVELS * Prey.HB_LEVELS)
        hs = rem // (Prey.RS_LEVELS * Prey.RD_LEVELS)
        rem = rem % (Prey.RS_LEVELS * Prey.RD_LEVELS)
        rd = rem // Prey.RS_LEVELS
        rs = rem % Prey.RS_LEVELS
        return {
            "resource_level": rs,
            "resource_dir": rd,
            "hunger": hs,
            "mate_near": rr,
            "predator_level": prs,
            "predator_dir": pd
        }

    @staticmethod
    def decode_state(idx):
        decoded = Prey.decode_indices(idx)
        rs = decoded["resource_level"]
        rd = decoded["resource_dir"]
        hs = decoded["hunger"]
        rr = decoded["mate_near"]
        prs = decoded["predator_level"]
        pd = decoded["predator_dir"]
        return {
            "state_idx": idx,
            "recurso": {0: "lejano_o_ninguno", 1: "medio", 2: "adyacente"}[rs],
            "dir_recurso": {0: "ninguna", 1: "arriba", 2: "abajo", 3: "izquierda", 4: "derecha"}[rd],
            "hambre": {0: "satisfecho", 1: "hambriento", 2: "hambriento_critico"}[hs],
            "buscar_pareja": {0: "no", 1: "si"}[rr],
            "depredador": {0: "lejano_o_ninguno", 1: "medio", 2: "peligro"}[prs],
            "dir_depredador": {0: "ninguna", 1: "arriba", 2: "abajo", 3: "izquierda", 4: "derecha"}[pd]
        }

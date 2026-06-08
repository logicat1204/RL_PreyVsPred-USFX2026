import os
import time
import random
import numpy as np
from Environment import Environment
from APrey import Prey
from APred import Predator

GRID_ROWS, GRID_COLS = 20, 20
N_INITIAL_PREY = 5
N_INITIAL_PRED = 5
N_RESOURCES = 15
MAX_RESOURCES = 20
N_EPISODES = 8000
MAX_STEPS = 100


def setup_episode(env, n_prey, n_pred, n_res):
    env.clear_all()
    n_total = n_prey + n_pred + n_res
    cells = random.sample(env.FreeSpaces(), min(n_total, len(env.FreeSpaces())))

    preys, preds = [], []

    for i in range(n_prey):
        p = Prey(f"Prey{i}")
        p.pos = cells[i]
        env.set_cell(cells[i], Environment.PREY)
        preys.append(p)

    offset = n_prey
    for i in range(n_pred):
        d = Predator(f"Pred{i}")
        d.pos = cells[offset + i]
        env.set_cell(cells[offset + i], Environment.PREDATOR)
        preds.append(d)

    offset += n_pred
    for i in range(n_res):
        env.set_cell(cells[offset + i], Environment.RESOURCE)

    return preys, preds


def collect_alive(agents):
    return [a for a in agents if a.alive]


GRID_SYM = {
    Environment.EMPTY: '.',
    Environment.PREY: 'P',
    Environment.PREDATOR: 'D',
    Environment.RESOURCE: 'R'
}

ACTION_ARROWS = {"UP": "^", "DOWN": "v", "LEFT": "<", "RIGHT": ">", "STAY": "o"}


def render_step(env, all_preys, all_preds, actions_log, episode, step):
    os.system('cls')

    alive_p = [p for p in all_preys if p.alive]
    alive_d = [d for d in all_preds if d.alive]
    recursos = env.PosRecursos()
    total = len(alive_p) + len(alive_d)
    pct_p = (len(alive_p) / total * 100) if total else 0
    pct_d = (len(alive_d) / total * 100) if total else 0

    sep = "=" * (env.cols * 2 + 1)
    print(f"  .{sep}.")
    print(f"  | Ep {episode} Paso {step} | P:{len(alive_p)}({pct_p:.0f}%) D:{len(alive_d)}({pct_d:.0f}%) R:{len(recursos)}")
    print(f"  |{'-' * (env.cols * 2 + 1)}|")

    for i in range(env.rows):
        line = ' '.join(GRID_SYM.get(env.grid[i][j], '?') for j in range(env.cols))
        print(f"  |{line}|")

    print(f"  '{sep}'")

    if actions_log:
        prey_acts = [a for _, a, t in actions_log if t == 'P']
        pred_acts = [a for _, a, t in actions_log if t == 'D']

        print(f"  Presas ({len(prey_acts)}): ", end="")
        for a in Prey.ACTIONS:
            cnt = prey_acts.count(a)
            arrow = ACTION_ARROWS.get(a, a)
            if cnt:
                print(f"{arrow}{cnt} ", end="")
        print()

        print(f"  Depred ({len(pred_acts)}): ", end="")
        for a in Predator.ACTIONS:
            cnt = pred_acts.count(a)
            arrow = ACTION_ARROWS.get(a, a)
            if cnt:
                print(f"{arrow}{cnt} ", end="")
        print()

    print()
    time.sleep(0.50)


def train(render_every=0):
    env = Environment(GRID_ROWS, GRID_COLS)

    _ = Prey("_seed", lr=0.1, gamma=0.9, epsilon=1.0)
    _ = Predator("_seed", lr=0.1, gamma=0.9, epsilon=1.0)

    prey_rewards_log = []
    pred_rewards_log = []
    pop_log = []

    prey_eps = 1.0
    pred_eps = 1.0
    EPS_MIN = 0.01
    EPS_DECAY = 0.997

    do_render = render_every > 0

    print(f"Grid: {GRID_ROWS}x{GRID_COLS}")
    print(f"Inicial: {N_INITIAL_PREY} presas, {N_INITIAL_PRED} depredadores, {N_RESOURCES} recursos")
    print(f"Presa: {Prey.N_STATES} estados | Depredador: {Predator.N_STATES} estados")
    print(f"Episodios: {N_EPISODES} | Pasos max: {MAX_STEPS}")
    if do_render:
        print(f"Render cada {render_every} episodios (activo)")
    print("-" * 80)
    import sys; sys.stdout.flush()

    for ep in range(N_EPISODES):
        render_this = do_render and (ep % render_every == 0)

        all_preys, all_preds = setup_episode(env, N_INITIAL_PREY, N_INITIAL_PRED, N_RESOURCES)

        for p in all_preys:
            p.epsilon = prey_eps
        for d in all_preds:
            d.epsilon = pred_eps

        total_r_prey = 0
        total_r_pred = 0
        n_steps = 0
        actions_log = []

        if render_this:
            render_step(env, all_preys, all_preds, [], ep + 1, 0)

        for step in range(MAX_STEPS):
            alive_preys = collect_alive(all_preys)
            alive_preds = collect_alive(all_preds)
            if not alive_preys or not alive_preds:
                n_steps = step
                break

            prey_states = [p.get_state(env) for p in alive_preys]
            pred_states = [d.get_state(env) for d in alive_preds]

            random.shuffle(alive_preys)
            prey_data = []
            actions_log.clear()
            for p, s in zip(alive_preys, prey_states):
                a = p.choose_action(s)
                r = p.apply_action(env, a)
                prey_data.append((p, s, a, r))
                actions_log.append((p.name, Prey.ACTIONS[a], 'P'))

            random.shuffle(alive_preds)
            pred_data = []
            for d, s in zip(alive_preds, pred_states):
                a = d.choose_action(s)
                r = d.apply_action(env, a)
                pred_data.append((d, s, a, r))
                actions_log.append((d.name, Predator.ACTIONS[a], 'D'))

            current_preys = env.PosPreys()
            for p, _, _, _ in prey_data:
                if p.alive and p.pos not in current_preys:
                    p.alive = False

            for p in list(all_preys):
                if p.alive:
                    offspring = p.try_reproduce(env, all_preys)
                    for c in offspring:
                        c.epsilon = prey_eps
                    all_preys.extend(offspring)

            for d in list(all_preds):
                if d.alive:
                    offspring = d.try_reproduce(env, all_preds)
                    for c in offspring:
                        c.epsilon = pred_eps
                    all_preds.extend(offspring)

            for p, s, a, r in prey_data:
                if p.alive:
                    ns = p.get_state(env)
                    p.update(s, a, r, ns, done=False)
                    total_r_prey += r
                else:
                    p.update(s, a, r, 0, done=True)
                    total_r_prey += r - 50

            for d, s, a, r in pred_data:
                if d.alive:
                    ns = d.get_state(env)
                    d.update(s, a, r, ns, done=False)
                    total_r_pred += r
                else:
                    d.update(s, a, r, 0, done=True)
                    total_r_pred += r

            if random.random() < 0.3:
                env.spawn_resource(MAX_RESOURCES)

            n_steps = step + 1

            if render_this:
                render_step(env, all_preys, all_preds, actions_log, ep + 1, step)

        if render_this:
            if n_steps < MAX_STEPS:
                render_step(env, all_preys, all_preds, actions_log, ep + 1, n_steps)
            input(f"\n  Episodio {ep+1} finalizado ({n_steps} pasos). Presiona Enter para continuar...")

        prey_eps = max(EPS_MIN, prey_eps * EPS_DECAY)
        pred_eps = max(EPS_MIN, pred_eps * EPS_DECAY)

        alive_preys = collect_alive(all_preys)
        alive_preds = collect_alive(all_preds)

        prey_rewards_log.append(total_r_prey / max(1, n_steps))
        pred_rewards_log.append(total_r_pred / max(1, n_steps))
        pop_log.append((len(alive_preys), len(alive_preds)))

        if (ep + 1) % 200 == 0 or ep == 0:
            avg_rp = np.mean(prey_rewards_log[-100:]) if len(prey_rewards_log) >= 100 else np.mean(prey_rewards_log)
            avg_rd = np.mean(pred_rewards_log[-100:]) if len(pred_rewards_log) >= 100 else np.mean(pred_rewards_log)
            avg_prey_pop = np.mean([p for p, _ in pop_log[-100:]])
            avg_pred_pop = np.mean([d for _, d in pop_log[-100:]])
            pop_total = avg_prey_pop + avg_pred_pop
            pct_p = (avg_prey_pop / pop_total * 100) if pop_total else 0
            pct_d = (avg_pred_pop / pop_total * 100) if pop_total else 0

            print(f"Ep {ep+1:>4}/{N_EPISODES}  "
                  f"Presa R:{avg_rp:>+6.1f}  Depredador R:{avg_rd:>+6.1f}  "
                  f"Poblacion: {pct_p:>5.1f}% / {pct_d:>5.1f}%  "
                  f"({int(avg_prey_pop)}P / {int(avg_pred_pop)}D)  "
                  f"eps:{prey_eps:.3f}/{pred_eps:.3f}")

    # --- final ---
    print("-" * 80)
    print("Entrenamiento completado")
    print(f"Poblacion final ep: {pop_log[-1][0]} presas, {pop_log[-1][1]} depredadores")
    print(f"Max presas: {max(p[0] for p in pop_log)} | Max depredadores: {max(p[1] for p in pop_log)}")

    prey_file = Prey._seed if hasattr(Prey, '_seed') else all_preys[0]
    pred_file = Predator._seed if hasattr(Predator, '_seed') else all_preds[0]

    # export using any instance (all share same q_table)
    for p in all_preys:
        if p.alive:
            p.export_q_table("Prey_QTable.json", Prey.decode_state)
            break
    else:
        all_preys[0].export_q_table("Prey_QTable.json", Prey.decode_state)

    for d in all_preds:
        if d.alive:
            d.export_q_table("Pred_QTable.json", Predator.decode_state)
            break
    else:
        all_preds[0].export_q_table("Pred_QTable.json", Predator.decode_state)

    print("Archivos: Prey_QTable.json, Pred_QTable.json")


if __name__ == "__main__":
    import sys
    render = 0
    if len(sys.argv) > 1:
        try:
            render = int(sys.argv[1])
        except ValueError:
            print("Uso: python training.py [render_cada_N_episodios]")
            print("  Ej: python training.py          (sin render)")
            print("  Ej: python training.py 50        (render cada 50 episodios)")
            sys.exit(1)
    train(render_every=render)

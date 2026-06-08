import json
import sys


def load_qtable(filename):
    with open(filename) as f:
        return json.load(f)


def print_qtable(data):
    name = data["agent"]
    n_states = data["n_states"]
    actions = data["action_names"]
    q_table = data["q_table"]
    descriptions = data.get("state_descriptions")

    print(f"\n{'='*80}")
    print(f"  Q-Table: {name}  ({n_states} estados, {len(actions)} acciones)")
    print(f"{'='*80}\n")

    header = f"{'Estado':<8}" + "".join(f"{a:>12}" for a in actions)
    print(header)
    print("-" * len(header))

    for s in range(n_states):
        row_vals = q_table[s]
        # Skip rows where all values are 0.0 (unvisited states) to reduce noise
        if all(v == 0.0 for v in row_vals):
            continue
        line = f"{s:<8}" + "".join(f"{v:>12.3f}" for v in row_vals)
        print(line)
        if descriptions and s < len(descriptions):
            desc = descriptions[s]
            if isinstance(desc, dict):
                label = " | ".join(f"{k}:{v}" for k, v in desc.items() if k != "state_idx")
                print(f"{'':>8}{label}")
            else:
                print(f"{'':>8}{desc}")

    visited = sum(1 for row in q_table if any(v != 0.0 for v in row))
    zero = n_states - visited
    print(f"\n  Estados visitados: {visited} / {n_states}  (no visitados: {zero})")
    print()


def print_compact(data):
    name = data["agent"]
    actions = data["action_names"]
    q_table = data["q_table"]
    n_states = data["n_states"]
    descriptions = data.get("state_descriptions")

    print(f"\n{'='*100}")
    print(f"  Q-Table: {name}")
    print(f"{'='*100}\n")

    best_actions = []
    for s in range(n_states):
        best = max(range(len(actions)), key=lambda a: q_table[s][a])
        best_val = q_table[s][best]
        if best_val == 0:
            best_actions.append("-")
        else:
            best_actions.append(actions[best])

    header = (f"{'Estado':<6}" +
              f"{'Recurso':<12}{'Hambre':<20}{'Pareja':<14}{'Predador':<14}" +
              "".join(f"{a:>10}" for a in actions) +
              f"{'Mejor':>10}")
    print(header)
    print("-" * len(header))

    for s in range(n_states):
        row_vals = q_table[s]
        if all(v == 0.0 for v in row_vals):
            continue

        desc = descriptions[s] if descriptions and s < len(descriptions) else {}

        r = desc.get("recurso", "-")[:10]
        h = desc.get("hambre", "-")[:18]
        pj = desc.get("pareja", "-")[:12]
        pr = desc.get("depredador", desc.get("presa", "-"))[:12]

        vals = "".join(f"{v:>10.2f}" for v in row_vals)
        best = actions[max(range(len(actions)), key=lambda a: row_vals[a])]

        print(f"{s:<6}{r:<12}{h:<20}{pj:<14}{pr:<14}{vals}{best:>10}")


if __name__ == "__main__":
    files = sys.argv[1:] if len(sys.argv) > 1 else ["Prey_QTable.json", "Pred_QTable.json"]
    mode = "normal"
    if "-c" in files:
        mode = "compact"
        files.remove("-c")

    for f in files:
        try:
            data = load_qtable(f)
            if mode == "compact":
                print_compact(data)
            else:
                print_qtable(data)
        except FileNotFoundError:
            print(f"Archivo no encontrado: {f}")

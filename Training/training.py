import APred, APrey, Environment

Prey1 = APrey.Prey("Prey1")
Pred1 = APred.Predator("Pred1")
Env = Environment(Prey1, Pred1,  [[0, 0, 0, 0, 0],
                                      [0, 1, 0, 3, 0],
                                      [0, 0, 0, 0, 0],
                                      [0, 2, 0, 0, 0],
                                      [0, 0, 0, 0, 0]])

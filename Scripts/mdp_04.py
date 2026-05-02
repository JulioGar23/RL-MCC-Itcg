# Markov Decision Process
# The Agent–Environment Interface
# Can - Robot

import random
# Equation p(s',r | s,a) -> Deterministic (Rules do not change)

# Dictionary to represent the dynamics of the Can-Robot environment
# The tuple (s, a, s_next, r) represents:
# (s: actual, a: action, s_next: next state, r: reward): probability
can_robot_dynamics = {
                      ("search", "grab", "can_found", 10): 0.7,        # 70% success.
                      ("search", "grab", "search", -1): 0.3            # 30% failure.
}

def simulate_trial(state, action):
    dynamics = []
    probabilities = []
    
    for (s, a, s_next, r), prob in can_robot_dynamics.items():
        if s == state and a == action:
            dynamics.append((s_next, r))
            probabilities.append(prob)

    return random.choices(dynamics, weights=probabilities, k=1)[0]

s, a = "search", "grab"

print(f"Action analysis '{a}' in state '{s}' ---")

print(f"\n 1. (Eq 3.2):")
prob_success = can_robot_dynamics.get((s, a, "can_found", 10), 0.0)
prob_failure = can_robot_dynamics.get((s, a, "search", -1), 0.0)
print(f" p(can_found, 10 | search, grab) = {prob_success}")
print(f" p(search, -1 | search, grab) = {prob_failure}")

print(f"\n 2. Simulation 10 trials):")
for i in range(1, 11):
    result = simulate_trial(s, a)
    print(f" Trial {i}: Result {result}")
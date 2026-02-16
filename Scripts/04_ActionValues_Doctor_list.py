# Bandits Problem - Action-Value Estimation
# Normal Script-type for the medical bottles experiment
# First version by JAGR.
# Sample average method to update action-values.

import random

# Bottles
bottle_actions = ["P", "Y", "B"]
q_values = [0.0, 0.0, 0.0]  
counts = [0, 0, 0] 
acum_rewards = [0, 0, 0]   

# Real World Simulation (Hidden Probabilities, Hidden Distributions)
# Hidden to the agent
real_probabilities=[0.25, 0.75, 0.50]

for t in range(1, 500): # iterations
    selected_index = random.randint(0, 2)   # Random action selection (0, 1, or 2)
    action = bottle_actions[selected_index]
    r = random.random()

    if r < real_probabilities[selected_index]:
        reward = 1
    else:
        reward = 0

    counts[selected_index] += 1
    acum_rewards[selected_index] += reward

    q_values[selected_index] = acum_rewards[selected_index] / counts[selected_index]
    #print(f'Random index = {selected_index}')
    #print(f'Random number = {r}')
    #print(f"Iteration {t}: Selected Bottle: {action}, Reward: {reward}, Q-values: {q_values}, Acumulated Rewards: {acum_rewards}, Counts: {counts}")

# Final Q-values after all iterations
print(f"Final Q-values: {q_values}")
print(f"Count: {counts}")
print(f"Accum Rewards: {acum_rewards}")
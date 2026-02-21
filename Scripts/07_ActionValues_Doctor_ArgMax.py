
# Bandits Problem - Action-Value Estimation
# Normal Script-type for the medical bottles experiment
# Greedy action selection (Argmax).
# Sample average method to update action-values.

import random

# Bottles
bottle_actions = ["P", "Y", "B"]
q_values = [0.0, 0.0, 0.0]     # With q_values initialized to zero, the agent git stuck always choosing the first bottle

#q_values = [random.random() for _ in range(3)]   #With q_values initialized randomly, the agent can explore all bottles. The agent does "some exploration indirectly"
#q_values = [1.0, 1.0, 1.0]   #With q_values initialized optimistically, force the agent  to try all bottles at least once.

counts = [0, 0, 0] 
acum_rewards = [0, 0, 0]   

# Real World Simulation (Hidden Probabilities, Hidden Distributions)
# Hidden to the agent
real_probabilities=[0.25, 0.75, 0.50]

for t in range(1, 2500): # 5 iterations
    selected_index = q_values.index(max(q_values))   # Random action selection (0, 1, or 2)
    action = bottle_actions[selected_index]

    if random.random() < real_probabilities[selected_index]:
        reward = 1
    else:
        reward = 0

    counts[selected_index] += 1
    acum_rewards[selected_index] += reward

    q_values[selected_index] = acum_rewards[selected_index] / counts[selected_index]

    #print(f"Iteration {t}: Selected Bottle: {action}, Reward: {reward}, Q-values: {q_values}, Acumulated Rewards: {acum_rewards}, Counts: {counts}")

# Final Q-values after all iterations
print(f"Final Q-values: {q_values}")
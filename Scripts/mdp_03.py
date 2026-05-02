# Markov Decision Process
# The Agent–Environment Interface
# Third version by JAGR.

import random
import time

class rabbit_mdp_env:
    def __init__(self):
        self.hunger = 3 # Initial state of hunger
        self.terminated = False
    
    def execute_action(self, action): #Hunger increases each turn (temporal consequence).
        if action == "carrot":  # High Reward, High Risk
            if random.random() < 0.5: # Tiger risk
                self.terminated = True
                return -100, "Tiger had Dinner"
            else:
                self.hunger = 0  # Reset hunger after eating carrot
                return 10, f'Full (Hunger: {self.hunger})'
        
        elif action == "broccoli":
            pass     
        
        self.hunger += 1
        
        if self.hunger >= 5:
            print("The rabbit has starved to death. Game Over.")
            self.terminated = True
            return -50, "Rabbit starved"  # Negative reward for starving
        
        return 1, f'Hungrier (Hunger: {self.hunger})'
    
        
def intelligent_agent(current_hunger): #Here the agent's decision is based on the current hunger level. If the rabbit is very hungry, it will take the risk of eating the carrot. If it's not too hungry, it will play it safe with the broccoli.
    if current_hunger >= 3: # If hunger is 3 or more, take the risk of eating the carrot.
        return "carrot"
    else:                   # If hunger is less than 3, play it safe with the broccoli.
        return "broccoli"

# Simulation
env = rabbit_mdp_env()
total_reward = 0

for turn in range(1, 11):
    if env.terminated:
        print("The agent cannot continue making decisions.")
        break
        
    action = intelligent_agent(env.hunger)
    reward, state = env.execute_action(action)
    total_reward += reward
    print(f"Turn {turn}: Action={action}, Reward={reward}, State={state}")
    time.sleep(1)

print(f"Simulation ended after {turn} turns.")
print(f"Total reward: {total_reward}")
# Markov Decision Process
# The Agent–Environment Interface
# Second version by JAGR.
# The Rabbit's dilemma!. Now with an intelligent agent that decides based on the current hunger level.

import random
import time

class rabbit_mdp_env:
    def __init__(self):
        self.hunger = 3  
        self.terminated = False
    
    def execute_action(self, action):
        reward = 0
        state = ""

        if action == "carrot":
            if random.random() < 0.5: 
                self.terminated = True
                return -100, "Tiger had Dinner" 
            else:
                self.hunger = 0 
                reward = 10
                state = "Full"
        
        elif action == "broccoli":
            self.hunger -= 1 
            reward = 1
            state = "Got broccoli"

        self.hunger += 1 # temporal consequence: hunger increases each turn
        
        if self.hunger >= 5:
            self.terminated = True
            return -50, "Rabbit starved to death"
        
        return reward, f"{state} (Hunger: {self.hunger})"

def intelligent_agent(current_hunger):
    # Policy: If hunger is 3 or more, take the risk of eating the carrot. If it's less than 3, play it safe with the broccoli.
    if current_hunger >= 3:
        return "carrot"
    else:
        return "broccoli"

# Simulation
env = rabbit_mdp_env()
total_reward = 0

print("Simulation started")
print(f"Initial hunger level: {env.hunger}\n")

for turn in range(1, 11):
    if env.terminated:
        break
        
    action = intelligent_agent(env.hunger)
    reward, state = env.execute_action(action)
    total_reward += reward
    
    print(f"Turn {turn}: Action = {action.upper()} | Reward = {reward} | State = {state}")
    time.sleep(2)

print(f"Simulation ended after {turn} turns.")
print(f"Total reward: {total_reward}")


# JAGR NOTES: 
# This intelligent agent is a simple rule-based policy that decides based on the current hunger level. 
# It tries to maximize long-term reward by taking the risk of eating the carrot when hunger is high, and playing it safe with the broccoli when hunger is low. 
# The simulation runs for a maximum of 10 turns or until the rabbit either gets caught by the tiger or starves to death.
# Fact 01. The agent is not "stuck" due to a mistake, but has found a strategy that allows him to achieve his goal (not to die) with zero risk.
# Fact 02. The agent remains "intelligent" but in a very conservative way, that is, without taking risks.
# Fact 03. This agent achieves its objective because if it always chooses broccoli: It gains +1 per turn indefinitely and never dies. (Long-term maximization). 
# Fact 04. If it chooses the carrot: It could gain +10, but it has a 50%, 80%, chance of dying and ceasing to gain points forever (long-term impact).
# Fact 05. Mathematically, if the game is long, the "always broccoli" strategy is superior because life expectancy is infinite. 
#          The agent has "hacked" the system to remain in a safe comfort zone.
# Fact 06. In a Bandits problem, you'd choose the carrot because it gives more immediate points and there's no "hunger state" forcing you to think about the future.
# Fact 07. In the MDP, the agent uses broccoli as a tool to manage their state. They don't choose it simply because they like broccoli; they choose it because it keeps their hunger from reaching the point of death.

# CLASS CHALLENGES: 
# 1. Increasing Hunger: Time adds +2 to hunger instead of +1. Broccoli would no longer be enough to compensate for the passage of time.
# 2. Variable Rewards: The reward for eating the carrot could vary randomly between +5 and +15, making the decision more complex.
# 3. Limited resource: Broccoli runs out after 3 turns.
# 4. Multiple actions: Introduce a new action, like "search for food", which has a chance to find more broccoli or a carrot, but also has a risk of encountering the tiger.
# 5. Penalization reward: If the rabbit doesn't eat the carrot, its "reward score" will go down, forcing it to seek the bigger prize.



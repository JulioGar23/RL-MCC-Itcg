# Markov Decision Process
# The Agent–Environment Interface
# First version by JAGR.
# Win or die satisfied. The Rabbit's dilemma!.
# Try to maximize your long-term reward, but be careful with the tiger!

import random
import time

class rabbit_env:
    def __init__(self):
        self.actual_state = "Start" 
        self.terminated = False

    def execute_action(self, action):
        print(f"Rabbit choose go for: {action}")

        if action == "carrot":  #High Reward, High Risk" 
            reward = 10
            prob_tiger = 0.5
            
            if random.random() < prob_tiger:
                print("Oh no! The rabbit got caught by the tiger!. Game Over.")
                self.actual_state = "Tiger had Dinner"
                self.terminated = True
                return reward - 100, self.actual_state  # Negative reward for getting caught
            else:
                print("Lucky rabbit. You ate the carrot and the tiger didn't see you.")
                self.actual_state = "Start"
                return reward, self.actual_state  # Positive reward for eating the carrot
        
        elif action == "brocoli":  #Low Reward, Low Risk
            reward = 1
            print("Rabbit ate the brocoli. Not as tasty as the carrot, but safe.")
            self.actual_state = "Start"
            return reward, self.actual_state  # Positive reward for eating the brocoli

#Simulation
env = rabbit_env()
total_reward = 0
turns = 5

print("Welcome to Game: Win or die satisfied. The Rabbit's dilemma!")

for turn in range(1, turns+1):
    if env.terminated:
        break

    print(f"\nTurn {turn}:")
    print("Actual Reward: ", total_reward)
    action = input("Choose an action (carrot/brocoli): ").strip().lower()
    
    if action not in ["carrot", "brocoli"]:
        print("Invalid action. Please choose 'carrot' or 'brocoli'.")
        continue
    
    reward, state = env.execute_action(action)
    total_reward += reward
    print(f"Reward received: {reward}")
   
    time.sleep(2)

print(f"\nGame Over! Total Reward: {total_reward}")



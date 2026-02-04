# Random variable: Coin Toss
# JAGR 2026

import random
import matplotlib.pyplot as plt

# Part A
# Number of experiments
# Shift + Alt + A to comment/uncomment block

""" N=5

# Outcomes
outcomes = []

for _ in range(N):
    coin = random.choice(["Heads","Tails"])
    outcomes.append(coin)

print("Outcomes:", outcomes) """

""" 
# Part B
N=1000

# Random variable values
X=[]

for _ in range(N):
    coin = random.choice(["Heads","Tails"])

    if coin == "Heads":
        X.append(1)
    else:
        X.append(0)

print("RV:", X)  """


""" # Plot histogram of the RV
plt.hist(X, bins=[-0.5, 0.5, 1.5], rwidth=0.8, align='mid', color='skyblue', edgecolor='black')
plt.xticks([0,1])
plt.xlabel("Value of the RV X") 
plt.ylabel("Frequency")
plt.title("Histogram of Random Variable X (Coin Toss)")
plt.show() 
 """

# Part C
""" N=1500
X=[]

for _ in range(N):
    die = random.randint(1,6)  # Random integer between 1 and 6
    X.append(die)

#print("RV:", X)

# Plot histogram of the RV
plt.hist(X, bins=[0.5,1.5,2.5,3.5,4.5,5.5,6.5], rwidth=0.8, align='mid', color='lightgreen', edgecolor='black')
plt.xticks([1,2,3,4,5,6])
plt.xlabel("Value of the RV X")
plt.ylabel("Frequency")
plt.title("Histogram of Random Variable X (Die Roll)")
plt.show() """


# Part D
""" N=10
X=[]

for _ in range(N):
    heads = 0

    for _ in range(3):  # Toss the coin 3 times
        if random.choice(["Heads","Tails"]) == "Heads":
            heads += 1
    
    X.append(heads)

print("RV:", X)  """



# Part E
# RV as a dictionary
""" omega = ["H", "T"]
X={"H":1, "T":0}

for outcome in omega:
    print(outcome, "->", X[outcome])
 """

# Part F
# RV die roll with square function
def X(omega):
    return omega**2

omega = [1,2,3,4,5,6]

for outcome in omega:
    print(outcome, "->", X(outcome)) 

# Part G   
# RV as number of heads in 2 tosses
""" 
omega = ["HH", "HT", "TH", "TT"]
def X(outcome):
    return outcome.count("H")

for outcome in omega:
    print(outcome, "->", X(outcome))     """

# Part H 
# RV induced by simulation
""" import random
def X(outcome):
    return 1 if outcome == "H" else 0

# Experiment Simulation
outcome = random.choice(["H","T"])
value = X(outcome)
print("Outcome:", outcome)
print("X(outcome):", value) """
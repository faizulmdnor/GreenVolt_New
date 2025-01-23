import math
def birthday_probability(N):
    if N > 365:
        return 1.0  #More than 365 people guarantees a shared birthday
    probability = 1.0
    for i in range(N):
        probability *= (365 - i) / 365
    return 1 - probability

#Example: Number of people attended
N = 6
print(f"The probability of at least two people having the same birthday in a group of {N} is {birthday_probability(N):.2f}")
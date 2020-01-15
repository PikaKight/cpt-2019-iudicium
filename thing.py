import random

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
random_order = random.sample(alphabet, 26)

print(random_order)

for i, letter in enumerate(random_order):
    if i <= 5:
        print(letter)
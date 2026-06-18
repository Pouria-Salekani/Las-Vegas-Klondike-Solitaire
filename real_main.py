
# from solit_play import Solitaire 
import matplotlib.pyplot as plt
import numpy as np
from piles import Pile
from mcts import MCTS
from solit_play import Solitaire

RUNS = 1000

distribution = {k: 0 for k in range(0, 261, 5)}
break_even = 0
wins = 0
total_payout = 0

for _ in range(RUNS):
    p = Pile()
    solitaire = Solitaire(p)
    solitaire.simulate()

    payout = solitaire.money_made
    distribution[payout] += 1
    total_payout += payout

    if payout >= 52:
        break_even += 1

    if payout == 260:
        wins += 1

win_percent = (wins / RUNS) * 100
break_even_percent = (break_even / RUNS) * 100
avg_payout = total_payout / RUNS
expected_profit = avg_payout - 52



print("Win %:", win_percent)
print("Break-even %:", break_even_percent)
print("Average payout:", avg_payout)
print("Expected profit per game:", expected_profit)
print("Distribution:", distribution)


keys = list(distribution.keys())
values = list(distribution.values())
probabilities = [count / RUNS for count in values]

plt.bar(keys, probabilities, width=4, align='center')
plt.xticks(keys)
plt.xlabel('Payout')
plt.ylabel('Probability')
plt.title('Probability Distribution')
plt.show()

# from solit_play import Solitaire 
import matplotlib.pyplot as plt
import numpy as np
from piles import Pile
from mcts import MCTS
from solit_play import Solitaire

RUNS = 1

distribution = {k: 0 for k in range(0, 261, 5)}
break_even = 0
wins = 0
total_payout = 0

for i in range(RUNS):
    p = Pile()
    solitaire = Solitaire(p)
    solitaire.simulate()

    payout = solitaire.money_made
    distribution[payout] += 1
    total_payout += payout

    for k, v in solitaire.print_values.items():
        if i == 0:
            print()
        print(f'MOVE {k}')
        for vals in v:
            print(vals, '\n')
        print('---------------------------------------------------------------------------------------------------------------------------------------')


    if 200 <= solitaire.money_made <= 255:
        print(" hit ", solitaire.money_made, "  again...")
        print('foundation ', solitaire.pile.foundation)
        print('pilea ', solitaire.pile.piles)
        print(solitaire.pile.waste, '|||||', solitaire.pile.deck)
        print('\n')


    #this is to print out every legal move and see what it does
    if solitaire.money_made == 260:
        for k, v in solitaire.print_values.items():
            print(f'MOVE {k} -->')
            for vals in v:
                print(vals, '\n')
            print('---------------------------------------------------------------------------------------------------------------------------------------')


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
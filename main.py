
from piles import Pile
from solit_play import Solitaire
import matplotlib.pyplot as plt

distribution = {i:0 for i in range(0,261,5)}
break_even = 0
wins = 0
total_money = 0

RUNS = 2000    #----THIS IS THE NUMBER OF TIMES THE ENITRE GAME WILL BE RAN----

#====== A *WIN* is defined by placing ALL cards back into foundation (i.e. all 52 cards back)
    # the 'distribution' is the $ value as keys. So, 10 cards played back: 5 * 10 = 50,
    # all cards played back 5 * 52 = 260, break-even point 5 * 11 = 55 (11 cards played back) ======  #

#===== A *WIN* is defined by placing ALL cards back into foundation (i.e. all 52 cards back)
    # the 'distribution' has the number of cards played back onto the pile as its keys.
    # In Las Vegas Klondike Solitaire, each card in the foundation pile is $5, so if all 52 cards played = 260 ==> a WIN ===== #
def start_game():
    global total_money, break_even, wins

    for i in range(RUNS):
        pile = Pile()
        solitaire = Solitaire(pile)
        solitaire.simulate() #starts the game

        #when done....
        money_made = solitaire.money_made
        distribution[money_made] += 1
        total_money += money_made

        if money_made >= 240 and money_made < 260:
            print("FOUND NEAR WIN IN MAIN")
            print("money:", money_made)
            print("cards:", money_made // 5)
            print("foundation:", solitaire.pile.foundation)
            print("waste:", solitaire.pile.waste)
            print("stock:", solitaire.pile.stock)
            print("piles:", solitaire.pile.piles)
            break

        # for k, v in solitaire.print_values.items():
        #     if i == 0:
        #         print()
        #     print(f'MOVE {k}')
        #     for vals in v:
        #         print(vals, '\n')
        #     print('---------------------------------------------------------------------------------------------------------------------------------------')


        if money_made >= 52: #we made our money back
            break_even += 1
        if money_made == 260:
            wins += 1

if __name__ == '__main__':
    start_game()

    win_percent = (wins / RUNS) * 100
    break_even_percent = (break_even / RUNS) * 100
    avg_payout = total_money / RUNS
    expected_profit = avg_payout - 52

    print()
    print('=========== STATUS OF GAMES PLAYED ===========')
    print('Win %:', win_percent)
    print('Break-even $:', break_even_percent)
    print(f'Average payout in {RUNS} game(s):', avg_payout)
    print('Expected profit per game:', expected_profit)
    print(f'Distribution of money made across {RUNS} game(s):', {k//5:v for k,v in distribution.items()})


    #shows the probabilities of that specific number of cards being played back
    #the higher, the more probable that state can be played 
    keys = list(distribution.keys())
    keys = [int(k)/5 for k in keys]
    values = list(distribution.values())
    total_count = sum(values)
    probabilities = [count / total_count for count in values]

    plt.figure(figsize=(12,8))
    plt.bar(keys, probabilities, width=0.75, align='center')
    plt.xticks(keys)  
    plt.xlabel('Values')
    plt.ylabel('Probability')
    plt.title('Probability Distribution')
    plt.show()


#====== A *WIN* is defined by placing ALL cards back into foundation (i.e. all 52 cards back)
    # the 'distribution' is the number of cards played back into the foundation pile.
    # Each card in a foundation pile is worth $5. So you, if you play ALL 52 cards back, you win $260 ======  #


from piles import Pile
from solit_play import Solitaire
import matplotlib.pyplot as plt

distribution = {i:0 for i in range(0,261,5)}
break_even = 0
wins = 0
total_money = 0

RUNS = 1    #----THIS IS THE NUMBER OF TIMES THE ENITRE GAME WILL BE RAN----
            #----To see the moves of each play, keep RUNS = 1 and uncomment the moves code below----
                #To see the *ACCURATE* win %, break-even %, and more, make RUNS = 3000 and COMMENT OUT the moves code below----
                    #(the more # runs, the slower but accurate results)

def start_game():
    global total_money, break_even, wins

    for i in range(RUNS):
        pile = Pile()
        solitaire = Solitaire(pile)
        solitaire.simulate() #starts the game

        #when done
        money_made = solitaire.money_made
        distribution[money_made] += 1
        total_money += money_made


        ##====UNCOMMENT TO SEE ALL MOVES PER RUN=====##
        for k, v in solitaire.print_values.items():
            if i == 0:
                print()
            print(f'MOVE {k}')
            for vals in v:
                print(vals, '\n')
            print('---------------------------------------------------------------------------------------------------------------------------------------')


        if money_made >= 55: #we made our money back
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
    print('Break-even %:', break_even_percent)
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


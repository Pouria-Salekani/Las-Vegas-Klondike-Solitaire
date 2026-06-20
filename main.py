
from piles import Pile
from solit_play import Solitaire
#from ns_soli import Solitaire
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
    plt.xticks(keys)  # Set x-ticks explicitly
    plt.xlabel('Values')
    plt.ylabel('Probability')
    plt.title('Probability Distribution')
    plt.show()




# # from solit_play import Solitaire 
# import matplotlib.pyplot as plt
# import numpy as np
# from piles import Pile
# from mcts import MCTS
# from solit_play import Solitaire



# #ONE BASIC RULE OF SOLITAIRE
# #GIVEN EMPTY PILES, ONLY A KING CAN BE MOVED AROUND, NOT ANY CARD CAN MOVE AROUND, ONLY A ~~KING~~


# # run it n times and compute expectation

# distribution = {k: 0 for k in range(0, 261, 5)}
# total = 0
# wins = 0

# def start_game():
#     global total
#     break_even = 0

#     # state = Pile()
#     # mcts = MCTS(state)

#     # i = 0
#     # while not state.is_game_over():
#     #     print('available moves ', state.check_legal_moves())
#     #     user_move = input('enter a move: ')
#     #     state.execute_legal_move(user_move)
#     #     mcts.move(user_move)

#     #     if state.is_game_over():
#     #         print('game over')


#     #     ###BIG TODO: MERGE SOLIT WITH PILE AND SEE WHAT HAPENS


#     #     mcts.search(4)
#     #     num_rollouts, run_time = mcts.statistics()
#     #     print("Statistics: ", num_rollouts, "rollouts in", run_time, "seconds")
#     #     best_move = mcts.best_move()

#     #     print('CPU chose ', best_move)

#     #     state.execute_legal_move(best_move)
#     #     mcts.move(best_move)

#     #     if state.is_game_over():
#     #         print('game over')
        

#     #huh
#     # p = Pile()
#     # p.run_solit()

#     # without even realizing, this entire program, is just a monte carlo stimulation lool
#     # at each loop creates a new instance
#     for _ in range(10000):
#         p = Pile()
#         # p.run_solit()
#         solitaire = Solitaire(p)
#         solitaire.simulate()
#         # p = Pile()
#         # p.run_solit()

#         #pass


#         # 200 to 255 SHOULD BE SOLVABLE
#         # if it keeps popping up, one solution is to make every loop separate, i.e., make every loop for each priority
#         #     separate
        
#         for k, v in solitaire.print_values.items():
#                 print(f'MOVE {k} -->')
#                 for vals in v:
#                     print(vals, '\n')
#                 print('---------------------------------------------------------------------------------------------------------------------------------------')


#         if 200 <= solitaire.money_made <= 255:
#             print(" hit ", solitaire.money_made, "  again...")
#             print('foundation ', solitaire.pile.foundation)
#             print('pilea ', solitaire.pile.piles)
#             print(solitaire.pile.waste, '|||||', solitaire.pile.deck)
#             print('\n')


#         #this is to print out every legal move and see what it does
#         if solitaire.money_made == 260:
#             for k, v in solitaire.print_values.items():
#                 print(f'MOVE {k} -->')
#                 for vals in v:
#                     print(vals, '\n')
#                 print('---------------------------------------------------------------------------------------------------------------------------------------')
#             return


        
#         if solitaire.money_made >= 52:
#             break_even += 1

#         distribution[solitaire.money_made] += 1

#     total = (break_even / 10000) * 100         # (~8.958% when at 0.57% winrate)

# if __name__ == '__main__':
#     start_game()
#     print('winning ','%', distribution)
#     print(distribution)
#     print('break-even ', total)

#     # Assuming 'histogram' is your histogram-like representation (a dictionary)
#     # Convert to NumPy array
#     data = np.array(list(distribution.keys())).reshape(-1, 1)

#     # # Instantiate and Fit GMM Model
#     # gmm = GaussianMixture(n_components=2)  # You can adjust the number of components as needed
#     # gmm.fit(data)

#     # # Predict Labels
#     # labels = gmm.predict(data)

#     # # Visualize the Results
#     # import matplotlib.pyplot as plt
#     # plt.scatter(data, np.zeros_like(data), c=labels, cmap='viridis')
#     # plt.xlabel('Value')
#     # plt.title('GMM Clustering')
#     # plt.colorbar()
#     # plt.show()

    
#     #UNCOMMENT CODE BELOW WHEN DONE EXPERIMENTING
#     keys = list(distribution.keys())
#     values = list(distribution.values())
#     probabilities = [count / 10000 for count in values]

#     total_count = sum(probabilities) #previously was probabilities.values()
#     normalized_probabilities = {key: value / total_count for key, value in distribution.items()}
#     print(normalized_probabilities)

#     plt.bar(keys, probabilities, width=4, align='center')
#     plt.xticks(keys)  # Set x-ticks explicitly
#     plt.xlabel('Values')
#     plt.ylabel('Probability')
#     plt.title('Probability Distribution')
#     plt.show()

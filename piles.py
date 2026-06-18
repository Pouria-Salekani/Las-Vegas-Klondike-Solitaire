import random
from card import Card 
from collections import defaultdict

class Pile:
    def __init__(self) -> None:
        self.deck = self.make_deck()
        self.piles = defaultdict(list)

        self.occupy_pile()

        self.stock = self.deck
        self.waste = []
        self.foundation = {}     # ace piles
        self.foundation['\u2665'] = []
        self.foundation['\u2666'] = []
        self.foundation['\u2663'] = []
        self.foundation['\u2660'] = []

        self.i = 0
        self.game_hash = None

        #this is okay btw
        # from solit_play import Solitaire
        # self.solitaire = Solitaire(self)



    
    def make_deck(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['\u2665', '\u2666', '\u2663', '\u2660']

        deck = [Card(suit, rank) for rank in ranks for suit in suits]
        random.shuffle(deck)

        return deck

    
    def occupy_pile(self):
        for i in range(1,8):
            remove_random = random.sample(self.deck, i)      # randomly samples (unique) i cards from deck
            for j in range(1, i+1):
                if j != i:
                    self.piles[i].append({remove_random[j-1]: False})          # false means it is face-down (hidden)
                else:
                    self.piles[i].append({remove_random[i-1]: True})         # true mean it is face-up (shown)
            

            # remove from the deck (52), tableau pile should have 28 cards left
            for r in remove_random:
                if r in self.deck:
                    self.deck.remove(r)

    # flips through the stock
    def flip_thru(self):

        #restock
        if not self.stock:
            self.stock = self.waste.copy()
            self.waste.clear()
            return
    
        self.waste.append(self.stock[0])
        self.stock.pop(0)


    def pr_found(self):
        return self.foundation
    

# MCTS, dont need it
    
#     # flips through the stock
#     def flip_thru(self):

#         #restock
#         if not self.stock:
#             self.stock = self.waste.copy()
#             self.waste.clear()
#             return
    
#         self.waste.append(self.stock[0])
#         self.stock.pop(0)


#     def pr_found(self):
#         return self.foundation
    
#     def check_legal_moves(self)->list:

#         foundation = self.solitaire.CHECK_pile_to_foundation()
#         waste = self.solitaire.CHECK_waste_to_pile()
#         split = self.solitaire.CHECK_split_deck()
#         #special_split = self.solitaire.CHECK_special_split_deck()

#         #hash = {'foundation':foundation, 'waste':waste, 'split':split, 'special_split':special_split}
#         hash = {'foundation': foundation, 'split':split}
        
#         #this deepcopy thing is needed for the MCTS node in the MCTS class
#             #test the deepcopy thing at each iteration in main.py
#         # print('normal ', solit.pile.piles)
#         # d = deepcopy(solit.pile.piles)
#         # print('deep copy /,', d)


#         #ready to implement this
#         self.game_hash = [k for k,v in hash.items() if v]
#         return [k for k,v in hash.items() if v]


#     #gets the list from above and executes ONE OF THEM RANDOMLY them (IDK IF THIS SHOULD BE HERE SINCE MCTS IS IN CHARGE OF EXECUTING MOVES)
#         #the MCTS code will RANDOMLY PICK IT OUT but we still gotta actually execute the code if that makes sense
#     def execute_legal_move(self, some_move):
#         if some_move == 'foundation':
#             self.solitaire.pile_to_foundation() #execute foundation; all the methods return something but dw about it now
#         elif some_move == 'waste':
#             self.solitaire.waste_to_pile() #execute waste
#         elif some_move == 'split':
#             self.solitaire.split_deck() #execute split
#         elif some_move == 'special_split':
#             self.solitaire.special_split_deck() #execute special split


#     def is_game_over(self)->bool:
#         # foundation = self.solitaire.CHECK_pile_to_foundation()
#         # waste = self.solitaire.CHECK_waste_to_pile()
#         # split = self.solitaire.CHECK_split_deck()
#         # special_split = self.solitaire.CHECK_special_split_deck()    

#         if self.i == 0:
#             self.check_legal_moves()
#             self.i += 1

#         #lost
#         if not self.game_hash: #not (foundation or waste or split or special_split):
#             self.solitaire.foundation_count()
#             return True
        
#         #keep going
#         else:
#             return False
        
#     #returns 1 if win
#     #returns -1 if loss
#     #for now I will be messing around with this
#     #this function gets called ONLY when game is over
#     def game_result(self)->int:
#         # if self.is_game_over():
#         #     return -1
#         # else:
#         #     return 1
#         #I should probably return the $$ won; I'll do it later
#         if self.solitaire.money_made >= 200:
#             return 1
#         else:
#             return -1333333


    

#     def run_solit(self):
#         print('PILE BEFORE IMPORT ', self.piles)
#         print('THE STOCK ', self.stock)
#         print('PILE AFTER IMPORT ', self.piles)
#         # for _ in range(2):
#         #solitaire = Solitaire(self) #this fixed my entire problem
#                                     #instead of doing the circular loop, i passed the ENTIRE CLASS'S *INSTANCE* (so everything is the same) to solit_play and
#                                     #it uses what was generated here as arguments over there
#         print('PILE NOW ', self.piles)
#         self.solitaire.simulate()

#         for k, v in self.solitaire.print_values.items():
#                 print(f'MOVE {k} -->')
#                 for vals in v:
#                     print(vals, '\n')
#                 print('---------------------------------------------------------------------------------------------------------------------------------------')

#         # print(self.piles)
#         print(self.solitaire.money_made)
#         print('END')
#         # print(solitaire.pile.piles)


    

# #try running the solit.py program from here and see if it responds well, if so, pile.py is our gamestate
# x = Pile()
# x.run_solit()  
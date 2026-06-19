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
  
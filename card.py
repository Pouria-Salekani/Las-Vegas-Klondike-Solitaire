
class Card:
    def __init__(self, suit, rank, face_up=False) -> None:
        self.suit = suit
        self.rank = rank
        self.face_up = face_up

    @staticmethod
    def decipher_hash(h):        
        items = h.items()
        key, value = next(iter(items))  #O(1) time complexity!!!

        return key.rank_value(), key.suit_value(), value

    def card_color(self):
        if self.suit in {'\u2665', '\u2666'}:
            return 'red'
        elif self.suit in {'\u2663', '\u2660'}:
            return 'black'

    def suit_value(self):
        return str(self.suit)

    def rank_value(self):
        return str(self.rank)

    def __str__(self) -> str:
        return f'{self.rank}{self.suit}'
    
    def __repr__(self) -> str:
        return self.__str__()

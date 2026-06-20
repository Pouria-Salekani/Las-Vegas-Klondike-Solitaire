from card import Card
from collections import deque, defaultdict

class Solitaire:
    def __init__(self, pile_instance) -> None:

        self.pile = pile_instance
        self.money_made = 0     # each card in foundation is $5
        self.moves_made = -1
        

        self.ace_spades_count = 0
        self.ace_clubs_count = 0
        self.ace_hearts_count = 0
        self.ace_diamonds_count = 0

        self.seen = {}

        self.print_values = defaultdict(list)
        self.print_indx = 0

        print('START STOCK ', self.pile.stock, '\n')
        print('START PILE ', self.pile.piles, '\n')
        print('=========================================')

        # ##uncomment when u wanna see all legal moves played of one game
        # print('BEGINNING START!!!   ', self.pile.piles, '\n')

   
 

    # flip the [-1] card in the key-th pile
    def flip_card(self, key=None):
        if self.pile.piles[key]:
            items_ = self.pile.piles[key][-1].items()   #the [-1] item is a hashmap
            inner_key, card_face = next(iter(items_))
            if card_face == False: # flip only when false
                self.pile.piles[key][-1][inner_key] = not self.pile.piles[key][-1][inner_key]

    
    def check_empty_pile(self):
        for key in self.pile.piles:
            if not self.pile.piles[key]:
                return key
            
    # Klondike rules; rank -1 difference and color must be different
    def check_card_for_waste(self, curr_card):
        if self.pile.waste:
            if curr_card.rank_value().isdigit() and self.pile.waste[-1].rank_value().isdigit():
                if int(curr_card.rank_value()) - int(self.pile.waste[-1].rank_value()) == 1 and curr_card.card_color() != self.pile.waste[-1].card_color():
                    return True
                
            elif curr_card.rank_value().isalpha() and self.pile.waste[-1].rank_value().isalpha():
                if (curr_card.rank_value() == 'K' and self.pile.waste[-1].rank_value() == 'Q') and curr_card.card_color() != self.pile.waste[-1].card_color():
                    return True
                
                if (curr_card.rank_value() == 'Q' and self.pile.waste[-1].rank_value() == 'J') and curr_card.card_color() != self.pile.waste[-1].card_color():
                    return True
                
            elif curr_card.rank_value() == 'J' and self.pile.waste[-1].rank_value() == '10':
                if curr_card.card_color() != self.pile.waste[-1].card_color():
                    return True

            return False
        

    def check_card_for_pile(self, curr_card, some_pile):
        if some_pile:     #some i-th pile...
            item = some_pile[0].items()
            card_info, card_face  = next(iter(item))

            if curr_card.rank_value().isdigit() and card_info.rank_value().isdigit():
                if int(curr_card.rank_value()) - int(card_info.rank_value()) == 1 and curr_card.card_color() != card_info.card_color():
                    return True
                
            elif curr_card.rank_value().isalpha() and card_info.rank_value().isalpha():
                if (curr_card.rank_value() == 'K' and card_info.rank_value() == 'Q') and curr_card.card_color() != card_info.card_color():
                    return True
                
                if (curr_card.rank_value() == 'Q' and card_info.rank_value() == 'J') and curr_card.card_color() != card_info.card_color():
                    return True
                
            elif curr_card.rank_value() == 'J' and card_info.rank_value() == '10':
                if curr_card.card_color() != card_info.card_color():
                    return True

            return False


    def check_card_for_foundation(self, curr_card):
        some_card = self.pile.foundation[curr_card.suit_value()][-1]
        
        if some_card.suit_value() == curr_card.suit_value():
            if some_card.rank_value() == 'A' and curr_card.rank_value() == '2':
                return True
            
            elif some_card.rank_value().isdigit() and curr_card.rank_value().isdigit():
                if int(curr_card.rank_value()) - int(some_card.rank_value()) == 1:
                    return True
                
            elif some_card.rank_value().isalpha() and curr_card.rank_value().isalpha():
                if some_card.rank_value() == 'J' and curr_card.rank_value() == 'Q':
                    return True
                
                if some_card.rank_value() == 'Q' and curr_card.rank_value() == 'K':
                    return True
                
            elif some_card.rank_value() == '10' and curr_card.rank_value() == 'J':
                return True



    def insert_card(self, key):
        new_card = self.pile.waste.pop()
        self.pile.piles[key].append({new_card: True})


    def select_cards(self, key):
        card_ls = deque()
        ith_card = -1

        for i, v in enumerate(self.pile.piles[key][::-1]):
            item = v.items()
            card_info, card_face = next(iter(item))
            if card_face == True:   # is face-up (shown)
                card_ls.appendleft({card_info:card_face})
                ith_card = len(self.pile.piles[key]) - 1 - i

        return card_ls, ith_card
    

    def remove_cards(self, key, card_list):
        move_to_pile = []
        for i, card in reversed(list(enumerate(self.pile.piles[key]))):     #used to preserve the order of the hashmap
            if card in card_list:
                move_to_pile.append(self.pile.piles[key].pop(i))

        return move_to_pile[::-1]


    def make_nice_number(self, key):
        if key == 1:
            return str(key)+'st'
        if key == 2:
            return str(key)+'nd'
        if key == 3:
            return str(key)+'rd'
        if 4 <= key <= 7:
            return str(key)+'th'



    # move 1: check if pile --> foundation; check the ith most index in the ith pile
    def pile_to_foundation(self):
        # first, make sure Aces are being occupied (before that make sure if it already has aces, then dont check this)
        can_play = False
        for key in self.pile.piles:
            if not self.pile.piles[key]:
                continue
            
            items_ = self.pile.piles[key][-1].items()
            k, v = next(iter(items_))

            # priority 1; ace(s) from pile ---> foundation pile
            if v == True and k.rank_value() == 'A':
                if not (self.ace_spades_count and self.ace_clubs_count and self.ace_diamonds_count and self.ace_hearts_count):
                    self.pile.piles[key].pop()
                    self.pile.foundation[k.suit_value()].append(k)

                    if k.suit_value() == '\u2665': #hearts
                        self.ace_hearts_count += 1
                    if k.suit_value() == '\u2666': #diamonds
                        self.ace_diamonds_count += 1
                    if k.suit_value() == '\u2663': #clubs
                        self.ace_clubs_count += 1
                    if k.suit_value() == '\u2660': #spades
                        self.ace_spades_count += 1

                    self.flip_card(key)
                    can_play = True
                    self.moves_made += 1
                    self.record_moves(f'Moved {k} from pile {key} into the {k.suit_value()} foundation pile ({self.pile.foundation})')

                  
            # priority 2; regular card from pile ---> foundation pile
            if self.pile.foundation[k.suit_value()]:
                if v == True and self.check_card_for_foundation(k):
                    self.pile.piles[key].pop()
                    self.pile.foundation[k.suit_value()].append(k)
                    
                    self.flip_card(key)
                    self.moves_made += 1
                    can_play = True
                    self.record_moves(f'Moved {k} from pile {key} into the {k.suit_value()} foundation pile ({self.pile.foundation})')
        return can_play   

    # move 2: waste ---> pile; 3 scenarios, if waste[i] has a king and there is an empty and if possible to move any waste to a pile
    def waste_to_pile(self):
        can_play = False
        for _ in list(self.pile.stock):
            self.pile.flip_thru()

            #priority 1; Ace card to foundation
            if self.pile.waste and self.pile.waste[-1].rank_value() == 'A':
                ace_suit = self.pile.waste[-1].suit_value()
                ace_card = self.pile.waste.pop()
                self.pile.foundation[ace_suit].append(ace_card)

                if ace_suit == '\u2665': #hearts
                    self.ace_hearts_count += 1
                if ace_suit == '\u2666': #diamonds
                    self.ace_diamonds_count += 1
                if ace_suit == '\u2663': #clubs
                    self.ace_clubs_count += 1
                if ace_suit == '\u2660': #spades
                    self.ace_spades_count += 1

              
                self.moves_made += 1
                can_play = True
                self.record_moves(f'[FROM WASTE], moved {ace_card} into the {ace_suit} foundation pile')


            # priority 2; regular card from waste ---> foundation
            try:
                if self.pile.waste and self.pile.foundation[self.pile.waste[-1].suit_value()] and self.check_card_for_foundation(self.pile.waste[-1]):
                    card = self.pile.waste.pop()
                    self.pile.foundation[card.suit_value()].append(card)
                   
                    can_play = True
                    self.moves_made += 1
                    self.record_moves(f'[FROM WASTE], moved {card} into the {card.suit_value()} foundation pile')

            except IndexError:
                print('INDEX ERROR ', self.pile.foundation)
                print('..and... ', card)
            


            #priority 3; King, check empty pile, -1 is top value
            key = self.check_empty_pile()
            if self.pile.waste and self.pile.waste[-1].rank_value() == 'K' and key:
                card = self.pile.waste.pop()
                self.pile.piles[key].append({card: True}) 
                self.moves_made += 1
                self.record_moves(f'[FROM WASTE], moved {card} into an EMPTY PILE {self.pile.piles[key]} --- {self.make_nice_number(key)} pile')
                can_play = True
            
            
            #priority 4; waste to pile any card || rank must be -1 lower and color must be diff
            for k in self.pile.piles:
                if self.pile.piles[k]:
                    items_ = self.pile.piles[k][-1].items()
                    card_info, card_face = next(iter(items_))

                    #if true (card_info), call insert card
                    check_card = self.check_card_for_waste(card_info)
                    if check_card:
                        waste_card = self.pile.waste[-1]
                        self.insert_card(k)     # inserts the card from 'waste list' into pile[k]
                        self.moves_made += 1
                        self.record_moves(f'[FROM WASTE], moved {waste_card} into the {self.pile.piles[k]} --- {self.make_nice_number(k)} pile')
                        can_play = True
        
        self.pile.flip_thru()   # restock
        return can_play
        
    # move 3
    def split_deck(self):
        # combining ALL priorities in the main loop, if it does not work out well, can always revert back
        can_play = False
        for start_pile in self.pile.piles:
            for cur_pile in self.pile.piles:
                if start_pile == cur_pile or not self.pile.piles[cur_pile] or not self.pile.piles[start_pile]:
                    continue

                # for priority 1 and 2
                c_pile_selected_cards, c_index = self.select_cards(cur_pile)
                cur_p_card_ls = list(c_pile_selected_cards)
                cur_p_rank,cur_p_suit, cur_p_face = Card.decipher_hash(self.pile.piles[cur_pile][c_index-1]) if c_index > 0 else Card.decipher_hash(self.pile.piles[cur_pile][0])
                
                start_card = self.pile.piles[start_pile][-1].items()
                start_card_info, start_card_face = next(iter(start_card))

                
                # for priority 3
                s_pile_selected_cards, s_index = self.select_cards(start_pile)
                start_s_card_ls = list(s_pile_selected_cards)
                st_p_rank,st_p_suit, st_p_face = Card.decipher_hash(self.pile.piles[start_pile][s_index-1]) if s_index > 0 else Card.decipher_hash(self.pile.piles[start_pile][0])
                
                cur_card = self.pile.piles[cur_pile][-1].items()
                cur_card_info, cur_card_face = next(iter(cur_card))

                
                # priority 1
                #last condition basically checks if moving cards from cur pile will make it an EMPTY PILE
                if self.check_card_for_pile(start_card_info, cur_p_card_ls) and start_card_face and (len(self.pile.piles[cur_pile]) - len(cur_p_card_ls) == 0):
                    move_to_start_pile = self.remove_cards(cur_pile, cur_p_card_ls)

                    # add the new cards to the start_pile that we started on
                    self.pile.piles[start_pile].extend(move_to_start_pile)

                    self.moves_made += 1
                    self.record_moves(f'[GENERAL SPLIT DECK/LEAVES an empty pile], moved {cur_p_card_ls} from {self.make_nice_number(cur_pile)} pile to {self.make_nice_number(start_pile)} pile')
                    can_play = True
                
                # priority 2
                elif self.check_card_for_pile(start_card_info, cur_p_card_ls) and not cur_p_face and start_card_face:
                    move_to_start_pile = self.remove_cards(cur_pile, cur_p_card_ls)
                    self.pile.piles[start_pile].extend(move_to_start_pile)
                    self.flip_card(cur_pile)

                 
                    self.moves_made += 1
                    self.record_moves(f'[GENERAL SPLIT DECK/REVEALS a card], moved {cur_p_card_ls} from {self.make_nice_number(cur_pile)} pile to {self.make_nice_number(start_pile)} pile')
                    can_play = True

                # priority 3
                elif self.check_card_for_pile(cur_card_info, start_s_card_ls) and cur_card_face and (len(self.pile.piles[start_pile]) - len(start_s_card_ls) < len(self.pile.piles[cur_pile]) + len(start_s_card_ls)):
                    if self.pile.piles[start_pile]:     # just in-case
                        move_to_cur_pile = self.remove_cards(start_pile, start_s_card_ls)

                    self.pile.piles[cur_pile].extend(move_to_cur_pile)

                    # only flip_card if the i-1 was false for the start_pile, since we are moving cards from start_pile to cur_pile
                    if not st_p_face:
                        self.flip_card(start_pile)
                    can_play = True
                    self.moves_made += 1
                    self.record_moves(f'[GENERAL SPLIT DECK/general], moved {start_s_card_ls} from {self.make_nice_number(start_pile)} pile to {self.make_nice_number(cur_pile)} pile')
        
        return can_play


    # move 4; when there are [J,Q,K] left only, it is a guaranteed win that requires a special code
        # 3 cards * 4 suits = 12
        # money is 12 * 5 = 60; so start checking when >=200
    # a special move that occurs when they are empty piles
        # so when startpile_i is empty, we check current pile and see if cards can be move around
    def special_split_deck(self):
        can_play = False
        for start_pile in self.pile.piles:
            for cur_pile in self.pile.piles:
                if start_pile == cur_pile or not self.pile.piles[cur_pile]:
                    continue

                if self.pile.piles[start_pile]:
                    continue

                c_pile_selected_cards, c_index = self.select_cards(cur_pile)
                cur_p_card_ls = list(c_pile_selected_cards) #SHOWS THE SUBSET thats starts of as TRUE i.e. face up
                cur_p_rank,cur_p_suit, cur_p_face = Card.decipher_hash(cur_p_card_ls[0])
                
                
                #this is how we stop the infinite cycle of moving onto an empty pile
                    #cur_p_card_ls is a SUBSET of piles[cur_pile], where the subset is the FIRST INSTANCE all cards are FACE UP (true)
                    #so, if == 0, then all cards face up, we don't need to move them. This prevents the infinite cycle
                hidden_cards_in_pile = len(self.pile.piles[cur_pile]) - len(cur_p_card_ls)
                if hidden_cards_in_pile == 0:
                    continue


                if cur_p_face and cur_p_rank == 'K':
                    move_to_start_pile = self.remove_cards(cur_pile, cur_p_card_ls)
                    self.pile.piles[start_pile].extend(move_to_start_pile)
                    self.flip_card(cur_pile)

                    can_play = True
                    self.moves_made += 1
                    self.record_moves(f'[!SPECIAL! SPLIT DECK], moved {cur_p_card_ls} from {self.make_nice_number(cur_pile)} pile to {self.make_nice_number(start_pile)} pile')

        return can_play      

    def foundation_count(self):
        self.money_made = sum(len(self.pile.foundation[suits]) * 5 for suits in self.pile.foundation)

        return self.money_made
    

    def count_pile(self):
        count = 0
        for k in self.pile.piles:
            count += len(self.pile.piles[k])
        return count
    

    def print_pile(self):
        for k, v in self.pile.piles.items():
            print('pile ',k,' ',v,'\n')
    

    def record_moves(self, value):
        self.print_values[self.moves_made].append(value)
    
    def simulate(self):
        #called in order of priority
        self.moves_made += 1
        #self.record_moves(f'{self.pile.piles}')
        

        foundation = self.pile_to_foundation()
        waste = self.waste_to_pile()
        split = self.split_deck()
        special_split = self.special_split_deck()       
        
        # UNCOMMENT IF THE ABOVE DOESNT MAKE SENSE
        # cards_left = self.count_pile()

        # if cards_left <= 12:
        #     # print('recalling again')
        #     # print('the pile  ', self.pile.piles)
        #     # print('foundation ', self.pile.foundation)
        #     split = self.special_split_deck()

    
        if not (foundation or waste or split or special_split):
            print('GAME OVER!!!!!!!!!!')
            print('Here is how much money you made... ', "$"+str(self.foundation_count()))
            print('----------------------------------------------------------------')
            print('END PILE  ', self.pile.piles)
            print('----------------------------------------------------------------')
            print('END STOCK ', self.pile.stock)
            print('----------------------------------------------------------------')
            print('END FOUNDTATION ', self.pile.foundation)
            print('----------------------------------------------------------------')
            print('Total moves made ', self.moves_made - 1)
            print('Total cards remaining (the higher, the worse)', len(self.pile.waste) + self.count_pile() + len(self.pile.stock))
            #self.record_moves(f'FINAL {self.pile.piles}') this is the final pile but we already print it
            #self.foundation_count()
            return
        
        else:
            print('STATUS OF THE FOUNDATION ', self.pile.pr_found())
            self.simulate()



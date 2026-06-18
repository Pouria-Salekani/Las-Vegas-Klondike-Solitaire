

'''

Will include Klondike Solitaire game rules. Pile is already set-up from the piles.py class.
Big 3 are
    - moving a card away from a pile then the i-1st card becomes face-up and gets 'revealed'. This pile also decreases as time goes on
    - moving singular card around that depends on i-1 rank and diff colors
    - moving multiple cards around that depends on the topmost number and that is less than the ith piles top most card

    (either can move based on bottom most card or top most card, middle ones will come later since that shit is rlly hard)

'''


from card import Card
from collections import deque, defaultdict
#from piles import Pile

class Solitaire:
    def __init__(self, pile_instance) -> None:
        #from piles import Pile

        #needed for the self thingy
        self.pile = pile_instance
        ####self.pile = Pile()
        self.money_made = 0     # each card in foundation is $5
        self.moves_made = 0
        

        self.ace_spades_count = 0
        self.ace_clubs_count = 0
        self.ace_hearts_count = 0
        self.ace_diamonds_count = 0

        self.seen = {}

        self.print_values = defaultdict(list)
        self.print_indx = 0

        print('START STOCK ', self.pile.stock, '\n')
        print('START PILE ', self.pile.piles, '\n')

        # ##uncomment when u wanna see all legal moves played of one game
        # print('BEGINNING START!!!   ', self.pile.piles, '\n')

   
    '''
    All of the 3 big moves will be here
    '''


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
        for i, card in reversed(list(enumerate(self.pile.piles[key]))):     #used to perserve the order of the hashmap
            if card in card_list:
                move_to_pile.append(self.pile.piles[key].pop(i))

        return move_to_pile[::-1]


    def check_move_status(self):
        pass


    '''
        TODO: once done with priority 1 and 2, make a MANUAL tester and see how they work out [DONE]
        TODO 2: do I make all options in one loop or separate loops, not sure [DONE, made it all into one loop]
        TODO 3: it hasn't happened yet, but, during split-decks I should check if the the x_piles are/are not empty for some operations [DONE]
        TODO 4: the big one, hasn't happened yet, but here is a chance that when you move a card from pile 1 ---> pile 2, the card that gets flipped
            might be somehow the same and in generally it will bring the card back to pile 1 again, maybe a visit set() should do it [NOT POSSIBLE, SO DONE]

        update: 12/31/2023
            next is fixing the flip_thru with waste pile so they somehow work together [DONE]
            and I need to make sure when move has been made, it returns true so the program knows to keep running [DONE]
            then next steps after that is figuring out if the split deck should all be in one loop or several or maybe even several functions [DONE]
    
    '''
        
    # go thru the pile and see if u can bring cards from the pile to the foundation in their respective suit
    # also for the ace count, I can probably bring it inside of the loop and separate the stuff

    # move 1: check if pile --> foundation; check the ith most index in the ith pile
    def pile_to_foundation(self):
        #can_play = False
        # first, make sure Aces are being occupied (before that make sure if it already has aces, then dont check this)
        for key in self.pile.piles:
            # for i, val in enumerate(self.pile.piles[key]):        #just in case shit breaks, I will revert back to this
            #     for k, v in val.items():
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
                    #can_play = True
                    self.record_moves(f'Moved {k}{v} from pile {key} into the {k.suit_value()} foundation pile ({self.pile.foundation})')

                    # print('priority 1 CALLED')
                    # print('foundation ', self.pile.foundation)
                    # print('entire pile ', self.pile.piles)
            
                    #return True
            
            # priority 2; regular card from pile ---> foundation pile
            if self.pile.foundation[k.suit_value()]:
                if v == True and self.check_card_for_foundation(k):
                    self.pile.piles[key].pop()
                    self.pile.foundation[k.suit_value()].append(k)
                    
                    self.flip_card(key)
                    #can_play = True
                    self.record_moves(f'Moved {k}{v} from pile {key} into the {k.suit_value()} foundation pile ({self.pile.foundation})')
                    
                    # print('priority 2 CALLED')
                    # print('foundation ', self.pile.foundation)
                    # print('entire pile ', self.pile.piles)
            
        
        # 'can_play' returns false if no moves were played    
        #return can_play


    # move 2: waste ---> pile; 3 scenarios, if waste[i] has a king and there is an empty and if possible to move any waste to a pile
    #TODO: implement regular card from waste ---> foundation
    def waste_to_pile(self):
        #flip_thru and waste combined
        #can_play = False

        for xj in list(self.pile.stock):
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

                #print('PRIORITY 1 CALLED ', self.pile.waste, ' ||| ', self.pile.foundation)
                #can_play = True
                self.record_moves(f'[FROM WASTE], moved {ace_card}--{xj} into the {ace_suit} foundation pile')

                # print('ACE WASTE GOT CALLED')
                # print('waste ', self.pile.waste)
                # print('foundation ', self.pile.foundation)
                # print(self.pile.foundation[ace_suit][0])
                #return True

            # priority 2; regular card from waste ---> foundation
            try:
                #print('WASTE BEFORE ', self.pile.waste)
                if self.pile.waste and self.pile.foundation[self.pile.waste[-1].suit_value()] and self.check_card_for_foundation(self.pile.waste[-1]):
                    card = self.pile.waste.pop()
                    self.pile.foundation[card.suit_value()].append(card)
                    #can_play = True
                    self.record_moves(f'[FROM WASTE], moved {card}--{xj} into the {card.suit_value()} foundation pile')

                    # print('REG CARD FROM WASTE CALLED ---> ', self.pile.foundation)
                    # print('MOVED ', card)
                    # print('WASTE NOW ', self.pile.waste)

            except IndexError:
                print('INDEX ERROR ', self.pile.foundation)
                print('..and... ', card)
            


            #priority 3; King, check empty pile, -1 is top value
            key = self.check_empty_pile()
            if self.pile.waste and self.pile.waste[-1].rank_value() == 'K' and key:
                card = self.pile.waste.pop()
                self.pile.piles[key].append({card: True}) 
                #print('priority 2 called ')
                #return True
                #can_play = True
                self.record_moves(f'[FROM WASTE], moved {card} into the EMPTY PILE {self.pile.piles[key]}--{key}')

            
            
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
                        #print('PRIORITY 3 CALLED ', self.pile.piles)
                        #return True
                        #can_play = True
                        self.record_moves(f'[FROM WASTE], moved {waste_card} into the {self.pile.piles[k]}--{k} pile')
        
        self.pile.flip_thru()   # restock
        #return can_play
        
        
    # move 3
    def split_deck(self):
        # can_play = False       # **for this move I wanna test if just returning true after a move works better** 

        # combining ALL priorities in the main loop, if it does not work out well, can always revert back
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

                    # print('PRIORITY 1 HIT!')
                    # print('after ', self.pile.piles)

                    # can_play = True
                    self.record_moves(f'[GENERAL SPLIT DECK/LEAVES an empty pile], moved {cur_p_card_ls} from {cur_pile} to {start_pile}')
                    #return True
                
                # # move king onto empty pile if it reveals
                # elif
                
                # priority 2
                elif self.check_card_for_pile(start_card_info, cur_p_card_ls) and not cur_p_face and start_card_face:
                    move_to_start_pile = self.remove_cards(cur_pile, cur_p_card_ls)
                    self.pile.piles[start_pile].extend(move_to_start_pile)
                    self.flip_card(cur_pile)

                    # print('PRIORITY 2 HIT!')
                    # print('after ', self.pile.piles)
                    # print('START_PILE ', start_card_info, ' and cur_card_ls ', cur_p_card_ls)

                    # can_play = True
                    self.record_moves(f'[GENERAL SPLIT DECK/REVEALS a card], moved {cur_p_card_ls} from {cur_pile} to {start_pile}')
                    #return True

                # priority 3
                elif self.check_card_for_pile(cur_card_info, start_s_card_ls) and cur_card_face and (len(self.pile.piles[start_pile]) - len(start_s_card_ls) < len(self.pile.piles[cur_pile]) + len(start_s_card_ls)):
                    if self.pile.piles[start_pile]:     # just in-case
                        move_to_cur_pile = self.remove_cards(start_pile, start_s_card_ls)

                    self.pile.piles[cur_pile].extend(move_to_cur_pile)

                    # only flip_card if the i-1 was false for the start_pile, since we are moving cards from start_pile to cur_pile
                    if not st_p_face:
                        self.flip_card(start_pile)

                    # print('PRIORITY 3 HIT!')
                    # print('after ', self.pile.piles)

                    #can_play = True
                    self.record_moves(f'[GENERAL SPLIT DECK/general], moved {start_s_card_ls} from {start_pile} to {cur_pile}')
                    #return True
                
        #return False



    # move 4; when there are [J,Q,K] left only, it is a guaranteed win that requires a special code
        # 3 cards * 4 suits = 12
        # money is 12 * 5 = 60; so start checking when >=200
    # a special move that occurs when they are empty piles
        # so when startpile_i is empty, we check current pile and see if cards can be move around
    
    def special_split_deck(self):
        for start_pile in self.pile.piles:
            for cur_pile in self.pile.piles:
                if start_pile == cur_pile or not self.pile.piles[cur_pile]:
                    continue

                c_pile_selected_cards, c_index = self.select_cards(cur_pile)
                cur_p_card_ls = list(c_pile_selected_cards)

                frozen_sets = [frozenset(card.items()) for card in cur_p_card_ls]
                card_tuple = tuple(frozen_sets)

                if card_tuple in self.seen and not self.seen[card_tuple]:
                    continue  # Skip this move, as it has been seen and determined to be invalid


                if not self.pile.piles[start_pile] and len(self.pile.piles[cur_pile]) >= 2:
                    # print('BEFORE MOVING THE PILE ', self.pile.piles)
                    # print('====================================================================')
                    move_to_start_pile = self.remove_cards(cur_pile, cur_p_card_ls)
                    self.pile.piles[start_pile].extend(move_to_start_pile)
                    self.flip_card(cur_pile)
                    self.seen[card_tuple] = False

                    # print('AFTER MOVING THE PILE ', self.pile.piles)
                    # print('FOUNDATION ', self.pile.foundation)
                    # print('\n')

                    self.record_moves(f'[!SPECIAL! SPLIT DECK], moved {cur_p_card_ls} from {cur_pile} to {start_pile}')
                    #return True
                
                
        #return False
    

    '''
    Below is for the check_legal_move(); checks if moves can be made WITHOUT actually doing the moves
    might have to adjust the executor moves so it doesnt actually check again, rather, just executes...
        the modification to the executor moves can be done by REMOVING FOR LOOPS and just passing relevant info in the parameters
        so they can execute it
    '''


#MCTS code, dont need it

    # # move 1: check if pile --> foundation; check the ith most index in the ith pile
    # def CHECK_pile_to_foundation(self):
    #     can_play = False
    #     # first, make sure Aces are being occupied (before that make sure if it already has aces, then dont check this)
    #     for key in self.pile.piles:
    #         # for i, val in enumerate(self.pile.piles[key]):        #just in case shit breaks, I will revert back to this
    #         #     for k, v in val.items():
    #         if not self.pile.piles[key]:
    #             continue
            
    #         items_ = self.pile.piles[key][-1].items()
    #         k, v = next(iter(items_))

    #         # priority 1; ace(s) from pile ---> foundation pile
    #         if v == True and k.rank_value() == 'A':
    #             if not (self.ace_spades_count and self.ace_clubs_count and self.ace_diamonds_count and self.ace_hearts_count):
    #                 can_play = True
    #                 self.record_moves(f'Moved {k}{v} from pile {key} into the {k.suit_value()} foundation pile ({self.pile.foundation})')

    #                 # print('priority 1 CALLED')
    #                 # print('foundation ', self.pile.foundation)
    #                 # print('entire pile ', self.pile.piles)
            
    #                 #return True
            
    #         # priority 2; regular card from pile ---> foundation pile
    #         if self.pile.foundation[k.suit_value()]:
    #             if v == True and self.check_card_for_foundation(k):
    #                 can_play = True
    #                 self.record_moves(f'Moved {k}{v} from pile {key} into the {k.suit_value()} foundation pile ({self.pile.foundation})')
                    
    #                 # print('priority 2 CALLED')
    #                 # print('foundation ', self.pile.foundation)
    #                 # print('entire pile ', self.pile.piles)
            
        
    #     # 'can_play' returns false if no moves were played    
    #     return can_play

    # # move 2: waste ---> pile; 3 scenarios, if waste[i] has a king and there is an empty and if possible to move any waste to a pile
    # #TODO: implement regular card from waste ---> foundation [DONE, forgot to update the above]
    # def CHECK_waste_to_pile(self):
    #     #flip_thru and waste combined
    #     can_play = False

    #     for xj in self.pile.stock:
    #         self.pile.flip_thru()

    #         #priority 1; Ace card to foundation
    #         if self.pile.waste and self.pile.waste[-1].rank_value() == 'A':
    #             #ace_suit = self.pile.waste[-1].suit_value()
                
    #             #not here, in executor
    #             # if ace_suit == '\u2665': #hearts
    #             #     self.ace_hearts_count += 1
    #             # if ace_suit == '\u2666': #diamonds
    #             #     self.ace_diamonds_count += 1
    #             # if ace_suit == '\u2663': #clubs
    #             #     self.ace_clubs_count += 1
    #             # if ace_suit == '\u2660': #spades
    #             #     self.ace_spades_count += 1

    #             #print('PRIORITY 1 CALLED ', self.pile.waste, ' ||| ', self.pile.foundation)
    #             #can_play = True
    #             return True

    #             # print('ACE WASTE GOT CALLED')
    #             # print('waste ', self.pile.waste)
    #             # print('foundation ', self.pile.foundation)
    #             # print(self.pile.foundation[ace_suit][0])
    #             #return True

    #         # priority 2; regular card from waste ---> foundation
    #         try:
    #             #print('WASTE BEFORE ', self.pile.waste)
    #             if self.pile.waste and self.pile.foundation[self.pile.waste[-1].suit_value()] and self.check_card_for_foundation(self.pile.waste[-1]):
    #                 #can_play = True
    #                 return True
    #                 # print('REG CARD FROM WASTE CALLED ---> ', self.pile.foundation)
    #                 # print('MOVED ', card)
    #                 # print('WASTE NOW ', self.pile.waste)

    #         except IndexError:
    #             print('INDEX ERROR ', self.pile.foundation)
    #             #print('..and... ', card)
            


    #         #priority 3; King, check empty pile, -1 is top value
    #         key = self.check_empty_pile()
    #         if self.pile.waste and self.pile.waste[-1].rank_value() == 'K' and key:
    #             #can_play = True
    #             return True

            
            
    #         #priority 4; waste to pile any card || rank must be -1 lower and color must be diff
    #         for k in self.pile.piles:
    #             if self.pile.piles[k]:
    #                 items_ = self.pile.piles[k][-1].items()
    #                 card_info, card_face = next(iter(items_))

    #                 #if true (card_info), call insert card
    #                 check_card = self.check_card_for_waste(card_info)
    #                 if check_card:
    #                     #can_play = True
    #                     return True
        
    #     self.pile.flip_thru()   # restock
    #     #return can_play
    #     return False


    # # move 3
    # def CHECK_split_deck(self):
    #     # can_play = False       # **for this move I wanna test if just returning true after a move works better** 

    #     # combining ALL priorities in the main loop, if it does not work out well, can always revert back
    #     for start_pile in self.pile.piles:
    #         for cur_pile in self.pile.piles:
    #             if start_pile == cur_pile or not self.pile.piles[cur_pile] or not self.pile.piles[start_pile]:
    #                 continue

    #             # for priority 1 and 2
    #             c_pile_selected_cards, c_index = self.select_cards(cur_pile)
    #             cur_p_card_ls = list(c_pile_selected_cards)
    #             cur_p_rank,cur_p_suit, cur_p_face = Card.decipher_hash(self.pile.piles[cur_pile][c_index-1]) if c_index > 0 else Card.decipher_hash(self.pile.piles[cur_pile][0])
                
    #             start_card = self.pile.piles[start_pile][-1].items()
    #             start_card_info, start_card_face = next(iter(start_card))

                
    #             # for priority 3
    #             s_pile_selected_cards, s_index = self.select_cards(start_pile)
    #             start_s_card_ls = list(s_pile_selected_cards)
    #             st_p_rank,st_p_suit, st_p_face = Card.decipher_hash(self.pile.piles[start_pile][s_index-1]) if s_index > 0 else Card.decipher_hash(self.pile.piles[start_pile][0])
                
    #             cur_card = self.pile.piles[cur_pile][-1].items()
    #             cur_card_info, cur_card_face = next(iter(cur_card))

                
    #             # priority 1
    #             #last condition basically checks if moving cards from cur pile will make it an EMPTY PILE
    #             if self.check_card_for_pile(start_card_info, cur_p_card_ls) and start_card_face and (len(self.pile.piles[cur_pile]) - len(cur_p_card_ls) == 0):
    #                 self.record_moves(f'[GENERAL SPLIT DECK/LEAVES an empty pile], moved {cur_p_card_ls} from {cur_pile} to {start_pile}')
    #                 return True
                
    #             # # move king onto empty pile if it reveals
    #             # elif
                
    #             # priority 2
    #             elif self.check_card_for_pile(start_card_info, cur_p_card_ls) and not cur_p_face and start_card_face:
    #                 self.record_moves(f'[GENERAL SPLIT DECK/REVEALS a card], moved {cur_p_card_ls} from {cur_pile} to {start_pile}')
    #                 return True

    #             # priority 3
    #             elif self.check_card_for_pile(cur_card_info, start_s_card_ls) and cur_card_face and (len(self.pile.piles[start_pile]) - len(start_s_card_ls) < len(self.pile.piles[cur_pile]) + len(start_s_card_ls)):
    #                 self.record_moves(f'[GENERAL SPLIT DECK/general], moved {start_s_card_ls} from {start_pile} to {cur_pile}')
    #                 return True
                
    #     return False


    # # move 4; 
    # # a special move that occurs when they are empty piles
    #     # so when startpile_i is empty, we check current pile and see if cards can be move around
    
    # def CHECK_special_split_deck(self):
    #     for start_pile in self.pile.piles:
    #         for cur_pile in self.pile.piles:
    #             if start_pile == cur_pile or not self.pile.piles[cur_pile]:
    #                 continue

    #             c_pile_selected_cards, c_index = self.select_cards(cur_pile)
    #             cur_p_card_ls = list(c_pile_selected_cards)

    #             #for the executor
    #             # frozen_sets = [frozenset(card.items()) for card in cur_p_card_ls]
    #             # card_tuple = tuple(frozen_sets)

    #             # if card_tuple in self.seen and not self.seen[card_tuple]:
    #             #     continue  # Skip this move, as it has been seen and determined to be invalid


    #             if not self.pile.piles[start_pile] and len(self.pile.piles[cur_pile]) >= 2:
    #                 # print('BEFORE MOVING THE PILE ', self.pile.piles)
    #                 # print('====================================================================')
                    
    #                 ##4 BELOW FOR THE EXECUTOR
    #                 # move_to_start_pile = self.remove_cards(cur_pile, cur_p_card_ls)
    #                 # self.pile.piles[start_pile].extend(move_to_start_pile)
    #                 # self.flip_card(cur_pile)
    #                 # self.seen[card_tuple] = False

    #                 # print('AFTER MOVING THE PILE ', self.pile.piles)
    #                 # print('FOUNDATION ', self.pile.foundation)
    #                 # print('\n')

    #                 self.record_moves(f'[!SPECIAL! SPLIT DECK], moved {cur_p_card_ls} from {cur_pile} to {start_pile}')
    #                 return True
                
                
    #     return False


    # MAKE THIS LATER
    # # move 4
    # def stock_to_foundation(self):
    #     for i, card in list(enumerate(self.pile.stock)):
    #         if self.check_card_for_foundation(card):
    #             print('STOCK TO FOUNDATIONNNNNNNNNNNNNN CHECK ', card)
    #             self.pile.stock.pop(i)
    #             self.pile.foundation[card.suit_value()].append(card)


    def foundation_count(self):
        for suits in self.pile.foundation:
            self.money_made += len(self.pile.foundation[suits]) * 5 if self.pile.foundation else 0

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
        #self.print_indx += 1
        self.print_values[self.moves_made].append(value)
    

    def simulate(self):
        #called in order of priority
        self.moves_made += 1
        self.record_moves(f'{self.pile.piles}')
        

        foundation = self.pile_to_foundation()
        waste = self.waste_to_pile()
        split = self.split_deck()
        special_split = self.special_split_deck()       #NOTE: just by adding this I am averaging 12.7% win-rate... holy fuck
        #special_split = self.                          #If I think this is too high, I can revert back to the one below
                                                        # if 'special_split' is getting called then it must be added to the if statement

        # UNCOMMENT IF THE ABOVE DOESNT MAKE SENSE
        # cards_left = self.count_pile()

        # if cards_left <= 12:
        #     # print('recalling again')
        #     # print('the pile  ', self.pile.piles)
        #     # print('foundation ', self.pile.foundation)
        #     split = self.special_split_deck()

    
        if not (foundation or waste or split or special_split):
            print('GAME OVER!!!!!!!!!!')
            print('here is how much money you made... ', self.foundation_count())
            print('END PILE  ', self.pile.piles)
            print('\n')
            print('END STOCK ', self.pile.stock)
            print('END FOUNDTATION ', self.pile.foundation)
            print('moves made ', self.moves_made)
            print('total len ', self.count_pile() + len(self.pile.stock))
            self.record_moves(f'{self.pile.piles}')
            self.foundation_count()
            return
        

        else:
            print('STATUS OF THE FOUNDATION ', self.pile.pr_found())
            self.simulate()



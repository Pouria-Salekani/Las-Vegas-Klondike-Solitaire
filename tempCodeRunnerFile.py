 if money_made >= 240 and money_made < 260:
            print("FOUND NEAR WIN IN MAIN")
            print("money:", money_made)
            print("cards:", money_made // 5)
            print("foundation:", solitaire.pile.foundation)
            print("waste:", solitaire.pile.waste)
            print("stock:", solitaire.pile.stock)
            print("piles:", solitaire.pile.piles)
            break
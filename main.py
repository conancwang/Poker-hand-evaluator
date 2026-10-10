import random
from collections import Counter

import math
from itertools import combinations

#mini interface for poker equity calculator, will be able to input the cards and it will calculate the equity of each player based on the known cards and the unknown cards
def main():
    h_num = ask_for_player()
    hands = []
    deck = Deck()
    board = []
    deck.shuffle()
    #User input for each player's cards, will be able to input the cards and it will remove them from the deck and add them to the player's hand
    for i in range(h_num):
        print(f"Enter Player: {i+1}'s cards")
        card_o = deck.deal_card_choice(ask_for_card(deck, "Enter the first card: "))
        card_t = deck.deal_card_choice(ask_for_card(deck,"Enter the second card: "))
        hands.append([card_o,card_t])
        print(f"Player {i+1}'s cards are: {card_o}, {card_t}")
        print(hands)

    print("Preflop probabilities: " + str(equity(hands, board)))
    #User input for the flop cards, will be able to input the cards and it will remove them from the deck and add them to the board
    streets = [("flop", 3), ("turn", 1), ("river", 1)]
    for count, item in enumerate(streets):
            for j in range(item[1]):
                card = ask_for_card(deck, "Enter the card(s) for " + item[0] + ": ")
                board.append(deck.deal_card_choice(card))
            print("Probabilities: " + str(equity(hands, board)))
            print(f"Current board is: {board}")
    
    
    



#Error trapper for cards to ensure inputs are valid and cards are not already used
def ask_for_card(deck, prompt):
    valid = False
    while not valid:
        try:
            card = parse_cards(input(prompt))
            if card in deck.Deck_Cards:
                valid = True
                return card
            else:
                print("Card is already used, please try again")
        except(ValueError, IndexError):
            print("Invalid option, please try again.")

#Error trapper for number of players to make sure its within range        
def ask_for_player():
    valid = False
    while not valid:
        try:
            players = int(input("How many players are there?: "))
            if 2 <= players <= 10:
                valid = True
                return players
            else:
                print("Please enter number a number from 2 to 10.")
        except(ValueError, IndexError):
                print("Invalid option, please try again.")        



#Equity function that calculates chances of winning. Monte Carlo during preflop and exact win percentage for flop, turn and river
def equity(hands, board, samples = 20000):
        known_cards = []
        for hand in hands:
            known_cards += hand
        known_cards += board



        full_deck = [Card(r,s) for r in range(2,15) for s in"hdsc"]
        unseen = [c for c in full_deck if c not in known_cards]
        to_deal = 5-len(board)

        #deal how many times

        if math.comb(len(unseen), to_deal) <= samples:
            runouts = list(combinations(unseen, to_deal))
        else:
            runouts = []
            for i in range(samples):
                runouts.append(random.sample(unseen, to_deal))



        wins = [0] * len(hands)

        for runout in runouts:
            collection = []
            winners = []
            for hand in hands:
                collection.append(evaluation(hand+board+list(runout)))
            best_hand = max(collection)

            for i, samplehand in enumerate(collection):
                if best_hand == samplehand:
                    winners.append(i)

            for i in winners:
                wins[i] += 1 / len(winners) 
        return [w / len(runouts) for w in wins]





           







def evaluation(cards):

    ranks = [card.rank for card in cards] 
    suits = [card.suit for card in cards] 

    rank_counts = Counter(ranks)
    suit_counts = Counter(suits)

    #duplicate logic
    pairs = []
    for r,n in rank_counts.items():
        if n == 2:
            pairs.append(r)


    trips = []
    for r,n in rank_counts.items():
        if n == 3:
            trips.append(r)

    quads = []
    for r,n in rank_counts.items():
        if n== 4:
            quads.append(r)
    #flush logic

    flush_suit = None
    for s,n in suit_counts.items():
        if n >= 5:
            flush_suit = s
    flush_ranks = []
    for card in cards:
        if card.suit == flush_suit:
            flush_ranks.append(card.rank)


    #straight logic
    def straight_high(ranks):
        straight_col = set(ranks)
        consec = 0
        for i in range(14, 1, -1):
            if i in straight_col:
                consec += 1
                if consec == 5:
                    straight_high = i+4
                    return (straight_high)
            else:
                consec = 0
        return None

    straight = straight_high(ranks)
    straight_flush = straight_high(flush_ranks)




    #straight flush/royal flush
    if straight_flush is not None:
        return(9, straight_flush)
    #quads
    elif len(quads) == 1:
        top_quads = max(quads)
        kicker = sorted([r for r in ranks if r != top_quads], reverse = True)[:1]
        return (8, top_quads, *kicker)
    # full house
    elif len(trips) and (pairs or len(trips) >= 2):
        top_set = max(trips)
        if len(trips) == 1:
            top_pair = max(pairs)
        else:
            top_pair = sorted(trips, reverse = True)[1]
        return(7, top_set, top_pair)

    elif flush_suit is not None:
        return (6, *sorted(flush_ranks, reverse=True))[:5]
    # straight
    elif straight is not None:
        return (5, straight)
    # set
    elif len(trips) == 1:
        top_set = max(trips)
        kicker = sorted([r for r in ranks if r != top_set], reverse=True)[:2]
        return (4, top_set, *kicker)
    # two pair
    elif len(pairs) >= 2:
        top_p, sec_p = sorted(pairs, reverse=True)[:2]
        kicker = sorted([r for r in ranks if r != top_p and r != sec_p], reverse=True)[:1]
        return (3, top_p, sec_p, *kicker)
    # pairs
    elif len(pairs) == 1:
        top_pair = max(pairs)
        kicker = sorted([r for r in ranks if r != top_pair], reverse = True)[:3]
        return (2, top_pair, *kicker)#return a tuple that can be compared with other ones, *splits it all into a list of numbers
    #high card
    else:
        kicker = sorted(ranks, reverse = True)[:5]
        return (1, *kicker)






#Converts entered values into object
def parse_cards(input):
    RANK_CHARS = "23456789TJQKA"
    rank = RANK_CHARS.index(input[0].upper())+2
    suit = input[1].lower()
    return Card(rank,suit)




class Card: 
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __hash__(self):
        return hash((self.rank, self.suit))

    def __repr__(self):
        return f"{self.rank}{self.suit}"

class Deck:
    deck = Deck_Cards = []
    def __init__(self):
        self.deck = Deck_Cards = []
        for rank in range(2,15):
            for suit in "hdcs":
                card = Card(rank,suit)
                self.Deck_Cards.append(card)
    def shuffle(self):
        random.shuffle(self.Deck_Cards)
    def deal_card(self, num_deal):
        return [self.Deck_Cards.pop() for num in range(num_deal)]
        
    def deal_card_choice(self, selected_card):
        self.Deck_Cards.remove(selected_card)
        return selected_card


main()
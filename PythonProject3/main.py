import random
from collections import Counter

import math
from itertools import combinations


def simulation():

    h_num = int(input("How many players are there?: "))
    hands = []
    deck = Deck()
    deck.shuffle()
    for i in range(h_num):
        print(f"Enter Player: {i+1}'s cards")
        card_o = parse_cards(input("Enter the first card: "))
        card_t = parse_cards(input("Enter the second card: "))
        hands.append([deck.deal_to_hand(card_o), deck.deal_to_hand(card_t)])
        print(f"Player {i+1}'s cards are: {card_o}, {card_t}")
        print(hands)


    #beginning to evaluate cards
    board = deck.deal_card(5)


    # top_hand = None
    # for hand in hands:
    #     preflop.append(evaluation(hand))
    #     flop.append(evaluation(hand+board[:3]))
    #     turn.append(evaluation(hand + board[:4]))
    #     river.append(evaluation(hand + board[:5]))

    for street, n in [("Preflop: ", 0), ("Flop: ", 3), ("Turn: ", 4), ("River", 5)]:
        print(street, equity(hands, board[:n]))


def equity(hands, board, samples = 20000):#the idea here is to decrease the amount of samples I run as the unknowns decrease, for preflop i wouldn't know the equity but for flop and after i can know exact
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



        wins = [0] * len(hands)  # 2 players → [0, 0]

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
                wins[i] += 1 / len(winners)  # tie → split
        return [w / len(runouts) for w in wins]





           







def evaluation(cards):

    ranks = [card.rank for card in cards] #pretty much isolate only the ranks
    suits = [card.suit for card in cards] #isolates the suits
    #purpose is so that later we can rank sort and count the card directly instead of the object

    #this step i need to find pairs and sort them, first step is to use counter to make dictionary of the rank specifically and then I
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

    #straight set up, going to make this in function so i can use later on for straight flush
    # straight_col = set(ranks)
    # straight_high = None
    # consec = 0
    # for i in range(14, 1, -1):
    #     if i in straight_col:
    #         consec += 1
    #         if consec == 5:
    #             straight_high = i+4
    #             break
    #     else:
    #         consec = 0

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
        # kicker  = []  #remove the pair and look at the rest and see what's highest to take it
        # for r in ranks:
        #     if r != top_pair:
        #         kicker.append(r)
        # kicker.sort(reverse  = True)
        # kicker = kicker[:3]
        kicker = sorted([r for r in ranks if r != top_pair], reverse = True)[:3]
        return (2, top_pair, *kicker)#return a tuple that can be compared with other ones, *splits it all into a list of numbers
    #high card
    else:
        kicker = sorted(ranks, reverse = True)[:5]
        return (1, *kicker)

















    #i like doing a point system, set points for flush, and set points for straight(won't work because i'd have to stagger the points)
    #logic for
    #1. Royal Flush, highest straight and same suits -->
    #2. Straight Flush, same suit straight
    #3. Same 4 cards, counts logic        -done
    #4. Full House, counts logic
    #5. Flush, counts logic
    #6. Straight, consecutive logic
    #7. Trips, count logic                -done
    #8. Two Pair, count                   -done
    #9. Pair, count -->                   -done
    #10. High card, count--> can use sort -later







def parse_cards(input):#this one makes it so that the input will be turned into an object, before it was just a string
    RANK_CHARS = "23456789TJQKA"
    rank = RANK_CHARS.index(input[0].upper())+2
    suit = input[1].lower()
    return Card(rank,suit)




class Card: #card objects that can be created
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __eq__(self, other):#pasted this so that == that is used for the remove card will compare the values instead of whether its the same object
        return self.rank == other.rank and self.suit == other.suit

    def __hash__(self):
        return hash((self.rank, self.suit))

    def __repr__(self):
        return f"{self.rank}{self.suit}"

class Deck:#helps create 52 cards
    deck = Deck_Cards = []
    def __init__(self):
        self.deck = Deck_Cards = []
        for rank in range(2,15):
            for suit in "hdcs":
                card = Card(rank,suit)
                self.Deck_Cards.append(card)
    def shuffle(self):
        random.shuffle(self.Deck_Cards)
    #ok here i need a function that will be able to randomly deal cards
    def deal_card(self, num_deal):
        return [self.Deck_Cards.pop() for num in range(num_deal)]
            #now im looking to go back up and work through adding this to each player's hands
    def deal_to_hand(self, selected_card):
        self.Deck_Cards.remove(selected_card)
        return selected_card


simulation()








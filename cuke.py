"""The Game of Cucumber."""

# Cucumber application

#!/usr/bin/env python3

from datascience import Table


##########################################################
# Cards
#  - Cards are represented as a string '<cardval> <suit>'

card_nums = ["2","3", "4", "5", "6", "7", "8", "9", "10","Jack","Queen","King","Ace"]
card_suits = ["Clubs", "Diamonds", "Hearts", "Spades"]

def card_value(card):
    """ Return the value of a card, 2-14, Aces high.
    Cards are strings of the form "<num> <suit>".
    Strings not of this form should return zero

    >>> card_value('2 Clubs')
    2
    >>> card_value('Jack Spades')
    11
    >>> card_value('Ace Diamonds')
    14

    """
    # BEGIN Question 1
    if card is None:
        return 0
    return card_nums.index(card.split()[0])+2
    # END Question 1


##########################################################
# List utilities for hands and players

def remove_item(s, item):
    """Return a list with first occurence of item in sequence removed.

    >>> remove_item([2, 3, 'a', 3], 3)
    [2, 'a', 3]
    >>> remove_item([2, 3, 'a', 3], 2)
    [3, 'a', 3]
    >>> remove_item([2, 3, 'a', 4], 4)
    [2, 3, 'a']
    """

    assert item in s, "Attempt to remove non-existent item from sequence"
    # BEGIN Question 2
    flag = True
    new_list = []
    for i in range(len(s)):
        if(s[i]==item and flag):
            flag  = False
            continue
        new_list.append(s[i])
    return new_list
    # END Question 2

def rotate_list(s, n):
    """Return a list containing a sequence rotated left by n elements.

    >>> rotate_list([2, 3, 'a', 4], 0)
    [2, 3, 'a', 4]
    >>> rotate_list([2, 3, 'a', 4], 1)
    [3, 'a', 4, 2]
    >>> rotate_list([2, 3, 'a', 4], 7)
    [4, 2, 3, 'a']
    """
    
    # BEGIN Question 3
    return (s+s)[n%len(s):n%len(s)+len(s)]
    # END Question 3

##########################################################
# Hands are represented as a list of cards

def new_hand():
    return []

def highest_card(hand):
    """Return the highest value card in a hand.

    >>> highest_card(['Queen Spades', '7 Clubs', 'Ace Spades', '9 Clubs'])
    'Ace Spades'
    """

    assert hand, "Attempt to find highest card of empty hand."
    # BEGIN Question 4
    value_list = [card_value(i) for i in hand]
    
    if len(value_list)==1 or max(remove_item(value_list, max(value_list))) != max(value_list) :
        return hand[value_list.index(max(value_list))]
    else:
        hands = [card for card in hand if card_value(card) == max(value_list)]
        same_card = [card_suits.index(card.split()[1]) for card in hands]
        return hands[same_card.index(max(same_card))]

    # END Question 4

def lowest_card(hand):
    """Return the lowest value card in a hand.

    >>> lowest_card(['Queen Spades', '7 Clubs', 'Ace Spades', '9 Clubs'])
    '7 Clubs'
    """

    # BEGIN Question 4
    value_list = [card_value(i) for i in hand]
    if len(value_list)==1 or min(remove_item(value_list, min(value_list))) != min(value_list) :
        return hand[value_list.index(min(value_list))]
    else:
        hands = [card for card in hand if card_value(card) == min(value_list)]
        same_card = [card_suits.index(card.split()[1]) for card in hands]
        return hands[same_card.index(min(same_card))]


    # END Question 4


def playable(hand, value):
    """Return a list of cards in hand with value greater or equal to value

    >>> playable(['Queen Spades', '7 Clubs', 'Queen Clubs', '9 Clubs'], 7)
    ['Queen Spades', '7 Clubs', 'Queen Clubs', '9 Clubs']
    >>> playable(['Queen Spades', '7 Clubs', 'Queen Clubs', '9 Clubs'], 11)
    ['Queen Spades', 'Queen Clubs']
    >>> playable(['Queen Spades', '7 Clubs', 'Queen Clubs', '9 Clubs'], 13)
    []

    """
    # BEGIN Question 6
    "*** REPLACE THIS LINE ***"
    value_list = [card_value(i) for i in hand]
    return [hand[i] for i in range(len(hand)) if value_list[i] >= value] # replace this
    # END Question 6

def legal_play(card, hand, high_value):
    """Determine if card is a legal play for hand.

    >>> legal_play('7 Clubs', ['7 Clubs', '10 Clubs', '2 Hearts'], 7)
    True
    >>> legal_play('7 Clubs', ['7 Clubs', '10 Clubs', '2 Hearts'], 8)
    False
    >>> legal_play('2 Clubs', ['7 Clubs', '10 Clubs', '2 Hearts'], 8)
    False
    >>> legal_play('10 Clubs', ['7 Clubs', '10 Clubs', '2 Hearts'], 8)
    True
    >>> legal_play('3 Clubs', ['7 Clubs', '10 Clubs', '2 Hearts'], 8)
    False
    """
    # BEGIN
    "*** REPLACE THIS LINE ***"
    playable_list = playable(hand, high_value)
    if card in playable_list:
        return True
    if(len(playable_list)==0 and card in hand and card_value(card)==card_value(lowest_card(hand))):
        return True
    else:return False

    # END

def print_hands(players, hands):
    """Print the cards held by each player."""
    # You do not need to change this function
    for player, hand in zip(players, hands):
        print(player, "holds", hand)


##########################################################
# Deck of cards
#  - Decks are represented as a Table with one column 'Card'

def new_deck():
    """Return a deck of cards ordered by suit and value within suit.

    >>> new_deck().num_rows
    52
    >>> list(new_deck()["Card"][0:5])
    ['2 Clubs', '3 Clubs', '4 Clubs', '5 Clubs', '6 Clubs']
    >>> list(new_deck()["Card"][46:51])
    ['9 Spades', '10 Spades', 'Jack Spades', 'Queen Spades', 'King Spades']
    """

    # BEGIN Question 7
    return Table().with_column('Card',[i + " " + j for j in card_suits for i in card_nums] )
    # END Question 7

def shuffle_deck(deck):
    """Return a shuffled deck."""

    # You do not need to change this function
    # It uses Table methods that you have not seen yet
    return deck.sample(deck.num_rows,with_replacement = False)


##########################################################
# Deal from card deck to player's hands

def deal(deck, players, dealer, number_of_cards, shuffle=True):
    """Deal cards to hands associated with each of a list of players.

    deck: a deck of cards
    players: a list of player names
    dealer: index of the dealer in players
    number_of_cards: number of cards to deal to each player from the deck

    Emulate dealing of cards from the deck to each of the hands
    After shuffling the deck, deal the first card to the player to the left
      of the dealer by removing a card from the deck and adding it to the
      player's hand.  Continue until number_of_cards are dealt to each hand

    Return: list of dealt hands

    >>> deal(new_deck(), ["P1", "P2", "P3"],1,3,False)
    [['4 Clubs', '7 Clubs', '10 Clubs'], ['2 Clubs', '5 Clubs', '8 Clubs'], ['3 Clubs', '6 Clubs', '9 Clubs']]

    """
    # BEGIN Question 8
    "*** REPLACE THIS LINE ***"
    if shuffle:
        deck = shuffle_deck(deck)
    dealt_list = [[] for p in players]
    if(len(players)*number_of_cards > 52):
        print("Need more than 52 cards")
        return
    for i in range(len(players)*number_of_cards):
        dealt_list[dealer].append(list(deck["Card"][i:i+1])[0])
        dealer = (dealer+1)%len(players)
    return  dealt_list
    # END Question 8

##########################################################
# Board of play
#
#  Board is represented as a table of cards played in a tricks of the round.
#  Rows represent the tricks.
#  'lead' column is the index of the player who leads the trick
#  row is filled in with the cards played by each player as the trick progresses.
#  A player must play a card of value at least as high as the highest 
#  played so far in the round, of their lowest card if they cannot.

def new_board(players):
    """A board is a table containing a record of play in each round.

    >>> new_board(['player0', 'player1', 'player2', 'player3'])
    lead | player0 | player1 | player2 | player3
    """

    # BEGIN Question 9
    "*** REPLACE THIS LINE ***"
    
    return Table(["lead"]+players)  # replace this
    # END Question 9

def start_trick(board, lead):
    """Establish the leader in the next trick in a board. Mark all '*NOT PLAYED*'
    

    >>> start_trick(new_board(['player0', 'player1', 'player2', 'player3']),3)
    lead | player0      | player1      | player2      | player3
    3    | *NOT PLAYED* | *NOT PLAYED* | *NOT PLAYED* | *NOT PLAYED*
    """
    # BEGIN Question 10
    return board.append([lead]+["*NOT PLAYED*"]*(board.num_columns-1))
    # END Question 10

def play_card(board, player, card):
    """Update board with player playing card.

    >>> b = start_trick(new_board(['p0', 'p1']),0)
    >>> play_card(b, 'p0', '3 Clubs')
    >>> b
    lead | p0      | p1
    0    | 3 Clubs | *NOT PLAYED*
    """
    # BEGIN Question 11
    "*** REPLACE THIS LINE ***"
    if(board.column(player)[board.num_rows-1]=='*NOT PLAYED*'):
        play_list = remove_item(board.column(player),'*NOT PLAYED*')
        play_list.append(card)
        board.__setitem__(player,play_list)


    # END Question 11

def get_trick(board):
    """Return the index current trick for a board.

    >>> b = new_board(['p0', 'p1'])
    >>> start_trick(b, 1)
    lead | p0           | p1
    1    | *NOT PLAYED* | *NOT PLAYED*
    >>> get_trick(b)
    0
    >>> play_card(b, 'p1', '2 Clubs')
    >>> play_card(b, 'p0', '3 Clubs')
    >>> start_trick(b, 0)
    lead | p0           | p1
    1    | 3 Clubs      | 2 Clubs
    0    | *NOT PLAYED* | *NOT PLAYED*
    >>> get_trick(b)
    1
    >>> play_card(b, 'p0', '4 Clubs')
    >>> get_trick(b)
    1
    >>> b
    lead | p0      | p1
    1    | 3 Clubs | 2 Clubs
    0    | 4 Clubs | *NOT PLAYED*
    """
    # BEGIN Question 12
    return board.num_rows-1
    # END Question 12


def get_highest_in_trick(board):
    """Return the value of the highest card play in a trick.

    >>> b = new_board(['p0', 'p1'])
    >>> start_trick(b, 1)
    lead | p0           | p1
    1    | *NOT PLAYED* | *NOT PLAYED*
    >>> get_trick(b)
    0
    >>> play_card(b, 'p1', '2 Clubs')
    >>> get_highest_in_trick(b)
    2
    >>> play_card(b, 'p0', '3 Clubs')
    >>> get_highest_in_trick(b)
    3
    >>> start_trick(b, 0)
    lead | p0           | p1
    1    | 3 Clubs      | 2 Clubs
    0    | *NOT PLAYED* | *NOT PLAYED*
    >>> get_highest_in_trick(b)
    0
    >>> play_card(b, 'p0', '4 Clubs')
    >>> get_highest_in_trick(b)
    4
    """
    # BEGIN Question 13
    card_list = [i for i in board.row(get_trick(board)) if i != '*NOT PLAYED*' and str(i)==i]
    if len(card_list) == 0:
        return 0
    return card_value(highest_card(card_list))
    # END Question 13

##########################################################
# Strategy functions
#
# These are some simple strategy functions that can be passed in to
# the game play to assist in testing.
# The manual stategy uses input operations that you haven't seen yet
# You do not need to modify these routines

def play_first(board, player, hand):
    """Play the first playable card in hand."""

    # This is a terrible strategy to get you started
    playable_cards = playable(hand, get_highest_in_trick(board))
    if playable_cards:
        card = playable_cards[0] 
    else:
        card = lowest_card(hand)
    return card


def manual(board, player, hand):
    """Let a real person play the hand."""

    print(player, "current hand", hand)
    print("Current board")
    print(board)
    card = input("Card to play: ")
    while not legal_play(card, hand, get_highest_in_trick(board)):
        print("Sorry.  {0} is not a legal play.".format(card))
        if not (card in hand):
            print("Please enter a card in your hand.")
        else:
            print("Please play as high as previous or lowest in hand.")
        card = input("Card to play: ")
    return card

##########################################################
# Play the game

def play_trick(board, lead, players, hands, strategies):
    """Play a trick and return index of winning player.

    >>> players = ['P0', 'P1']
    >>> hands = deal(new_deck(), players, 0, 3, shuffle=False)
    >>> hands
    [['2 Clubs', '4 Clubs', '6 Clubs'], ['3 Clubs', '5 Clubs', '7 Clubs']]
    >>> board = new_board(players)
    >>> new_lead = play_trick(board, 1, players, hands, [play_first, play_first])
    >>> board
    lead | P0      | P1
    1    | 4 Clubs | 3 Clubs
    >>> hands
    [['2 Clubs', '6 Clubs'], ['5 Clubs', '7 Clubs']]
    >>> play_trick(board, new_lead, players, hands, [play_first, play_first])
    1
    >>> board
    lead | P0      | P1
    1    | 4 Clubs | 3 Clubs
    0    | 2 Clubs | 5 Clubs
    >>> hands
    [['6 Clubs'], ['7 Clubs']]

    """

    # BEGIN Question 14
    "*** REPLACE THIS LINE ***"
    new_lead = lead
    start_trick(board, lead)
    for i in range(len(players)):
        item = strategies[lead](board,players[lead],hands[lead])
        play_card(board, players[lead], item)
        hands[lead]  = remove_item(hands[lead],item)
        lead = (lead+1)%len(players)
    trick = [i for i in board.row(get_trick(board)) if str(i)==i]
    trick = rotate_list(trick,new_lead)
    def get_the_last_large_one(hand):
        value_list = [card_value(i) for i in hand]
        playhands = [card for card in hand if card_value(card) == max(value_list)]
        return playhands[len(playhands)-1]
    return (trick.index(get_the_last_large_one(trick))+new_lead)%len(players)
    # END Question 14

deck = new_deck()

def play_game(players, strategies, verbose=False, shuffle=True, num_cards=7, dealer=0, max_score=21):
    """
    Play a full game of tricks.

    players: list of player names
    strategies: list containing strategy function for each player

    verbose: print out things that happen in the game (default False)
    shuffle: set to False for testing
    num_cards: number of cards to deal, reduce for testing (default 7)
    dealer: player to deal the cards (default 0)
    max_score: termination point count (reduce for testing)

    returns: list of scores for players
    
    """
    # BEGIN Question 15
    "*** REPLACE THIS LINE ***"
    scores = [0]*len(players)
    lead = (dealer+1)%len(players)
    deck_list = deal(new_deck(), players, dealer, num_cards, shuffle)
    board = new_board(players)
    count = 0
    #record = [0]*len(players)
    while(max(scores)<max_score):
        while(count<num_cards):
            count += 1
            lead = play_trick(board, lead, players, deck_list, strategies)
            if verbose: print(board)
        trick = [i for i in board.row(get_trick(board))]
        highest_score = get_highest_in_trick(board)
        scores[lead] += highest_score*2
        card_list = [i for i in board.row(get_trick(board)) if str(i)==i]
        for k in range(len(card_list)):
            if card_value(card_list[k]) == highest_score:
                scores[k] -= highest_score
                if scores[k] <=0:
                    scores[k] = 0
        #change the scores
        if not verbose :print(board)
        print("Winner:",players[lead],"with",highest_card([i for i in board.row(get_trick(board)) if str(i)==i]))
        #record[lead] += 1
        print("Scores",scores)
        count = 0
        deck_list = deal(new_deck(), players, lead, num_cards, shuffle)
        board = new_board(players)
        #print(record)
    return scores
    # END Question 15

def test_game():
    #I have changed this function
    players = ["You", "Bot1", "Bot2", "Bot3"]
    strategies = [play_first, play_first, strategy,play_first]
    #Change different strategy
    dealer = deal(new_deck(), players, 0, 1, True)
    hands = [i[0] for i in dealer]
    dealer = hands.index(highest_card(hands))
    #decide the dealer by the value of the card
    
    return play_game(players, strategies, verbose=False, num_cards=7, max_score=15000, dealer=dealer)


##########################################################
# More advanced strategy functions
def fimp(board, player, hand):
    playable_cards = playable(hand, get_highest_in_trick(board))
    if playable_cards:
        card = lowest_card(playable_cards)
    else:
        card = lowest_card(hand)
    return card

def lead_second_highest_follow_low(board, player, hand):
    # BEGIN
    playable_cards = playable(hand, get_highest_in_trick(board))
    
    if [i for i in board.row(get_trick(board)) if str(i)==i and i != '*NOT PLAYED*']:
        if playable_cards and len(hand)>2:
            card = lowest_card(playable_cards)
        elif playable_cards and len(hand)==2:
            card = highest_card(playable_cards)
        else:
            card = lowest_card(hand)
    else:
        card_list = remove_item(hand,highest_card(hand))
        if card_list:
            card = highest_card(card_list)
        else:
            card = highest_card(hand)
    return card
    "*** REPLACE THIS LINE ***"
    # END

def strategy(board, player, hand):
    playable_cards = playable(hand, get_highest_in_trick(board))
    played_card = [i for i in board.row(get_trick(board)) if str(i)==i and i != '*NOT PLAYED*']
    card_values = [card_value(i) for i in hand]
    
    if playable_cards:
        #if sum(i<10 and i>5 for i in card_values)>3:
        #    card = highest_card(playable_cards)
        if len(playable_cards)>5:
            remove_highest = remove_item(playable_cards, highest_card(playable_cards))
            remove_second_highest = remove_item(remove_highest, highest_card(remove_highest))
            card = highest_card(remove_second_highest)
        else:
            if (card_value(highest_card(playable_cards)) < 10 or sum(i<10 for i in card_values)>4 ):
                card = highest_card(playable_cards)
            elif len(hand)>2:# just useful for num_card set over 4
                remove_lowest = remove_item(playable_cards, lowest_card(playable_cards))
                if remove_lowest:
                    if played_card:
                        card = lowest_card(remove_lowest)
                    else:
                        remove_highest = remove_item(remove_lowest, highest_card(remove_lowest))
                        if remove_highest :
                            card = highest_card(remove_highest)
                        else:
                            card = lowest_card(remove_lowest)
                else:
                    card = lowest_card(playable_cards)
            else:
                card = highest_card(playable_cards)
    else:
        card = lowest_card(hand)
    return card


def play(number_of_players=4, verbose=False):
    players = ["player"+str(i) for i in range(number_of_players)]
#    strategies = [manual for player in players]
    strategies = [play_first for player in players]
#    strategies = [lead_second_highest_follow_low for player in players]
    return play_game(players, strategies, verbose)

def main(verbose=False):
    number_of_players=4
    players = ["player"+str(i) for i in range(number_of_players)]
    strategies = [lead_second_highest_follow_low for player in players]
    strategies[0] = manual
    return play_game(players, strategies, verbose)

# if __name__ == '__main__':
#    main(True)





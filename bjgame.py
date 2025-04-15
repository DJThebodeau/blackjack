import os
import random
import time

suit_symbols = {
    'Hearts': '♥ ',
    'Diamonds': '♦',
    'Clubs': '♣',
    'Spades': '♠'
}
def create_deck():
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    royalty = ['J', 'Q', 'K']
    suits = ['Hearts', 'Spades', 'Clubs', 'Diamonds']
    deck = []
    for suit in suits:
        for rank in ranks:
            card = {'rank': rank, 'suit': suit}
            deck.append(card)
    random.shuffle(deck)
    return deck

def get_card_value(card_rank):
    if card_rank in ['J', 'Q', 'K']:
        return 10

    if card_rank in ['A']:
        return 11 
    return int(card_rank)

def deal_hand(deck):
    hand = []
    for _ in range(2):
        hand.append(deck.pop())
    return hand
    
def hit(deck):
    return deck.pop()
    
def hand_value(hand):
    total = 0
    ace_count = 0
        
    for card in hand:
        rank = card['rank']
        if rank == 'A':
            total += 11
            ace_count += 1
        elif rank in ['J', 'Q', 'K']:
            total += 10
        else:
            total += get_card_value(rank)
    
    while total > 21 and ace_count > 0:
        total -= 10
        ace_count -= 1
    
    return total
        
def display_hand(hand):
    for card in hand:
        symbol = suit_symbols[card['suit']]
        print(f"{card['rank']} of {symbol}")

def display_dealer_hand(hand, reveal=False):
    if reveal:
        for card in hand:
            symbol = suit_symbols[card['suit']]
            print(f"Dealer shows: {card['rank']} of {symbol}")
    else:
        symbol = suit_symbols[hand[0]['suit']]
        print(f"Dealer shows: {hand[0]['rank']} of {symbol}")
        print("Dealer's second card is hidden\n")

def player_turn(deck, hand):
    while True:
        display_hand(hand)
        hand_total = hand_value(hand)

        if hand_total > 21:
            print(f"You busted with a total of {hand_total}")
            break

        choice = input(f"Your total is {hand_total}. Would you like to hit or stand? ").lower()
        if choice == "hit":
            hand.append(hit(deck))
        elif choice == "stand":
            break
        else:
            print("Please type 'hit' or 'stand'.")
   
def dealer_turn(deck, hand):
    display_dealer_hand(hand, reveal=True)
    print(f"Dealer total is {hand_value(hand)}\n")
    time.sleep(1)

    while hand_value(hand) < 17:
        print("\nDealer hits...\n")
        time.sleep(1)

        card = (hit(deck))
        hand.append(card)
        
        symbol = suit_symbols[card['suit']]
        print(f"Dealer draws: {card['rank']} of {symbol}")
        print(f"Dealers total is {hand_value(hand)}\n")
        time.sleep(1)
                
def check_winner(player_hand, dealer_hand, bet):
    global player_balance
    player_total = hand_value(player_hand)
    dealer_total = hand_value(dealer_hand)
        
    if player_total > 21:
        print(f"Player Busted and lost ${bet}! Dealer wins.")
        player_balance -= bet
    elif dealer_total > 21:
        print(f"Dealer Busts! Player wins ${bet}.")
        player_balance += bet
    elif player_total > dealer_total:
        print(f"Player wins ${bet}!")
        player_balance += bet
    elif dealer_total > player_total:
        print(f"Dealer Wins! Player lost ${bet}!")
        player_balance -= bet
    else:
        print("Push. No money won or lost")

def start_game():
    global player_balance

    while True:
        try:
            bet = int(input(f"You have ${player_balance}. Enter your bet: "))
            if bet > player_balance:
                print("You cannot bet more than you have.")
                continue
            if bet <= 0:
                print("Bet must be greater than zero.")
                continue
            break
        except ValueError:
                print("Please enter a valid number.")
    deck = create_deck()
    player_hand = deal_hand(deck)
    dealer_hand = deal_hand(deck)

    display_dealer_hand(dealer_hand)
    player_turn(deck, player_hand)
    player_total = hand_value(player_hand)
    if player_total > 21:
            check_winner(player_hand, dealer_hand, bet)
            return
    dealer_turn(deck, dealer_hand)
    check_winner(player_hand, dealer_hand, bet)
    
player_balance = 100
player_wins = 0
dealer_wins = 0

while True:
    os.system('clear')

    print(f"Balance: ${player_balance}")
    print(f"Wins: Player {player_wins} - Dealer {dealer_wins}\n")

    start_game()  # or your main game function

    again = input("Play another round? (y/n): ").lower()
    if again != 'y':
        break


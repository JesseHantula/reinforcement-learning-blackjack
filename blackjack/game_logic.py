import random

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.name = f"{rank.lower()}_of_{suit.lower()}"

    def __repr__(self):
        return self.name

class BlackjackGame:
    def __init__(self):
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.high_cards = 0
        self.low_cards = 0
        self.aces = 0
        self.game_over = False

    def reset(self):
        self.player_hand = []
        self.dealer_hand = []
        self.game_over = False

    def create_deck(self):
        # We want to make a deck consisting of 6 sets of 52 cards
        # This is the standard amount used in casinos and online games
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        deck = [Card(rank, suit) for _ in range(6) for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def deal_card(self, hand):
        # We will use a new deck if the current deck is 5/6 empty
        # This will be done to somewhat mimic the behavior of a casino
        if len(self.deck) < 52:
            self.deck = self.create_deck()
            self.high_cards = 0
            self.low_cards = 0
            self.aces = 0
        if self.deck:
            card = self.deck.pop()
            hand.append(card)
            if card.rank in ['10', 'Jack', 'Queen', 'King']:
                self.high_cards += 1
            elif card.rank == 'Ace':
                self.aces += 1
            elif card.rank in ['2', '3', '4', '5']:
                self.low_cards += 1

    def calculate_score(self, hand):
        values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
        score = sum(values[card.rank] for card in hand)
        # Adjust for Aces
        aces = sum(1 for card in hand if card.rank == 'Ace')
        while score > 21 and aces:
            score -= 10
            aces -= 1
        return score

    def deal_player(self):
        for _ in range(2):
            self.deal_card(self.player_hand)

    def deal_dealer(self):
        for _ in range(2):
            self.deal_card(self.dealer_hand)

    def player_hit(self):
        self.deal_card(self.player_hand)
        player_score = self.calculate_score(self.player_hand)
        if player_score > 21:
            self.game_over = True
            return 'Player busts! You lose.'
        return ''
    
    def dealer_turn(self):
        dealer_score = self.calculate_score(self.dealer_hand)
        while dealer_score < 17:
            self.deal_card(self.dealer_hand)
            dealer_score = self.calculate_score(self.dealer_hand)
        player_score = self.calculate_score(self.player_hand)
        if dealer_score > 21:
            self.game_over = True
            return 'Dealer busts! You win.'
        if dealer_score > player_score:
            self.game_over = True
            return 'Dealer wins.'
        if dealer_score < player_score:
            self.game_over = True
            return 'You win.'
        self.game_over = True
        return 'It\'s a tie.'

    def get_game_state(self):
        return {
            'player_hand': [card.name for card in self.player_hand],
            'dealer_hand': [card.name for card in self.dealer_hand],
            'player_score': self.calculate_score(self.player_hand),
            'dealer_score': self.calculate_score(self.dealer_hand),
            'deck_size': len(self.deck),
            'high_cards': self.high_cards,
            'low_cards': self.low_cards,
            'aces': self.aces,
            'game_over': self.game_over
        }

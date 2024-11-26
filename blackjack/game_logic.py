import random

class BlackjackGame:
    def __init__(self):
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.game_over = False

    def create_deck(self):
        # We want to make a deck consisting of 6 sets of 52 cards
        # This is the standard amount used in casinos and online games
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = [{'rank': rank, 'suit': suit} for _ in range(6) for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def deal_card(self, hand):
        # We will use a new deck if the current deck is 5/6 empty
        # This will be done to somewhat mimic the behavior of a casino
        if len(self.deck) < 52:
            self.deck = self.create_deck()
        if self.deck:
            hand.append(self.deck.pop())

    def calculate_score(self, hand):
        values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
        score = sum(values[card['rank']] for card in hand)
        # Adjust for Aces
        aces = sum(1 for card in hand if card['rank'] == 'A')
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

    def get_game_state(self):
        return {
            'player_hand': self.player_hand,
            'dealer_hand': self.dealer_hand,
            'player_score': self.calculate_score(self.player_hand),
            'dealer_score': self.calculate_score(self.dealer_hand),
            'game_over': self.game_over
        }

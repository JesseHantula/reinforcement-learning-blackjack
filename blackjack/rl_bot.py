from flask import Flask, request, jsonify
import random
import joblib

app = Flask(__name__)

class RLAgent:
    def __init__(self):
        self.q_table = {}
        self.actions = ['hit', 'stand']
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.exploration_rate = 0.2

    def reset(self):
        self.q_table = {}

    def get_state_key(self, player_score, dealer_visible_card_rank):
        return f"{player_score}-{dealer_visible_card_rank}"

    def choose_action(self, state):
        if random.random() < self.exploration_rate:
            return random.choice(self.actions)
        return max(
            self.actions, 
            key=lambda action: self.q_table.get((state, action), 0)
        )

    def get_reward(self, game):
        if game.game_over:
            player_score = game.calculate_score(game.player_hand)
            dealer_score = game.calculate_score(game.dealer_hand)
            if player_score > 21:
                return -1
            elif dealer_score > 21 or player_score > dealer_score:
                return 1
            elif player_score < dealer_score:
                return -1
        return 0

    def update_q_value(self, state, action, reward, next_state):
        old_value = self.q_table.get((state, action), 0)
        future_rewards = max(
            [self.q_table.get((next_state, a), 0) for a in self.actions], 
            default=0
        )
        self.q_table[(state, action)] = old_value + self.learning_rate * (
            reward + self.discount_factor * future_rewards - old_value
        )

agent = RLAgent()
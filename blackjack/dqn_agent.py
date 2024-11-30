import numpy as np
import random
from collections import deque
import tensorflow as tf
from keras import models, layers, optimizers, Input

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95
        self.learning_rate = 0.001
        self.epsilon = 1.0
        self.epsilon_min = 0.1
        self.epsilon_decay = 0.995
        self.model = self.build_model()
        self.target_model = self.build_model()

    def reset(self):
        self.memory = deque(maxlen=2000)
        self.epsilon = 1.0

    def get_state(self, player_score, ace_in_hand, dealer_card, high_cards, low_cards, aces, deck_size):
        high_card_probability = (96 - high_cards) / deck_size # Probability of drawing a high card
        low_card_probability = (96 - low_cards) / deck_size # Probability of drawing a low card
        ace_probability = (24 - aces) / deck_size # Probability of drawing an ace
        ace = 1 if ace_in_hand else 0
        dealer_card_value = 0
        if dealer_card == 'Ace':
            dealer_card_value += 11
        elif dealer_card in ['Jack', 'Queen', 'King']:
            dealer_card_value += 10
        else:
            dealer_card_value += int(dealer_card)
        
        state = np.array([player_score, ace, dealer_card_value, high_card_probability, low_card_probability, ace_probability])
        return state.reshape(1, self.state_size)

    def build_model(self):
        model = models.Sequential([
            Input(shape=(self.state_size,)),
            layers.Dense(64, activation='relu'),
            layers.Dense(64, activation='relu'),
            layers.Dense(self.action_size, activation='linear')
        ])
        model.compile(optimizer=optimizers.Adam(learning_rate=self.learning_rate), loss='mse')
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])
    
    def get_reward(self, simulation):
        if simulation.calculate_score(simulation.player_hand) > 21:
            return -1
        elif simulation.calculate_score(simulation.player_hand) == simulation.calculate_score(simulation.dealer_hand):
            return 0
        elif simulation.calculate_score(simulation.player_hand) > simulation.calculate_score(simulation.dealer_hand):
            return 1
        else:
            return -1

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.max(self.target_model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())


agent = DQNAgent(state_size=6, action_size=2)

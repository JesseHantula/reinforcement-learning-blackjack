from flask import Flask, render_template, jsonify, request
from blackjack.game_logic import BlackjackGame
from blackjack.rl_bot import RLAgent

app = Flask(__name__)
game = BlackjackGame()
simulation = None
agent = RLAgent()

@app.route('/')
def home():
    global simulation
    simulation = BlackjackGame()
    return render_template('simulation.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    global simulation

    if request.json.get('new_game', False):
        simulation = BlackjackGame()
        agent.reset()

    num_simulations = request.json.get('num_simulations', 1)
    all_steps = []

    for _ in range(num_simulations):
        simulation.reset()
        simulation.deal_player()
        simulation.deal_dealer()

        steps = [{
            'player_hand': [card.name for card in simulation.player_hand],
            'dealer_hand': [card.name for card in simulation.dealer_hand],
            'player_score': simulation.calculate_score(simulation.player_hand),
            'dealer_score': None,
            'deck_size': len(simulation.deck),
            'high_cards': simulation.high_cards,
            'low_cards': simulation.low_cards,
            'aces': simulation.aces,
            'game_over': simulation.game_over,
            'bot_wins': simulation.bot_wins,
            'dealer_wins': simulation.dealer_wins,
            'draws': simulation.draws,
            'message': "Initial deal"
        }]

        state = agent.get_state_key(
            simulation.calculate_score(simulation.player_hand),
            simulation.dealer_hand[0].rank
        )

        while not simulation.game_over:
            action = agent.choose_action(state)

            if action == 'hit':
                message = simulation.player_hit()
            else:
                message = simulation.dealer_turn()

            steps.append({
                'player_hand': [card.name for card in simulation.player_hand],
                'dealer_hand': [card.name for card in simulation.dealer_hand],
                'player_score': simulation.calculate_score(simulation.player_hand),
                'dealer_score': simulation.calculate_score(simulation.dealer_hand) if simulation.game_over else None,
                'deck_size': len(simulation.deck),
                'high_cards': simulation.high_cards,
                'low_cards': simulation.low_cards,
                'aces': simulation.aces,
                'game_over': simulation.game_over,
                'bot_wins': simulation.bot_wins,
                'dealer_wins': simulation.dealer_wins,
                'draws': simulation.draws,
                'message': message
            })

            if not simulation.game_over:
                next_state = agent.get_state_key(
                    simulation.calculate_score(simulation.player_hand),
                    simulation.dealer_hand[0].rank
                )
                reward = agent.get_reward(simulation)
                agent.update_q_value(state, action, reward, next_state)
                state = next_state

        all_steps.extend(steps)

    return jsonify({
        'steps': all_steps
    })


if __name__ == '__main__':
    app.run(debug=True)
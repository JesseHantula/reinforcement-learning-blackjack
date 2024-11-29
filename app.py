from flask import Flask, render_template, jsonify, request
from blackjack.game_logic import BlackjackGame
from blackjack.rl_bot import RLAgent

app = Flask(__name__)
game = BlackjackGame()
simulation = None
agent = RLAgent()

@app.route('/')
def home():
    return render_template('blackjack.html')

@app.route('/test')
def test_bot():
    global simulation
    simulation = BlackjackGame()
    return render_template('simulation.html')

@app.route('/start', methods=['POST'])
def start_game():
    global game
    game = BlackjackGame()  # Reset the game
    game.deal_player()
    game.deal_dealer()
    return jsonify(game.get_game_state())

@app.route('/new_hand', methods=['POST'])
def new_hand():
    game.reset()
    game.deal_player()
    game.deal_dealer()
    return jsonify(game.get_game_state())

@app.route('/hit', methods=['POST'])
def hit():
    message = game.player_hit()
    if game.game_over:
        return jsonify({**game.get_game_state(), 'message': message, 'game_over': True})
    return jsonify({**game.get_game_state(), 'message': message, 'game_over': False})

@app.route('/stand', methods=['POST'])
def stand():
    message = game.dealer_turn()
    return jsonify({**game.get_game_state(), 'message': message})

@app.route('/simulate', methods=['POST'])
def simulate():
    global simulation

    num_simulations = request.json.get('num_simulations', 1)
    all_steps = []
    total_simulation_count = agent.simulation_count

    for _ in range(num_simulations):
        if not simulation:
            simulation = BlackjackGame()

        simulation.reset()
        simulation.deal_player()
        simulation.deal_dealer()

        state = agent.get_state_key(
            simulation.calculate_score(simulation.player_hand),
            simulation.dealer_hand[0].rank
        )
        steps = []

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

    agent.simulation_count += num_simulations

    return jsonify({
        'steps': all_steps,
        'simulation_count': agent.simulation_count,
    })


if __name__ == '__main__':
    app.run(debug=True)
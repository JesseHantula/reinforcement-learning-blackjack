from flask import Flask, render_template, jsonify, request
from blackjack.game_logic import BlackjackGame

app = Flask(__name__)
game = BlackjackGame()

@app.route('/')
def home():
    return render_template('blackjack.html')

@app.route('/start', methods=['POST'])
def start_game():
    global game
    game = BlackjackGame()  # Reset the game
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

if __name__ == '__main__':
    app.run(debug=True)
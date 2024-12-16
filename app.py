from flask import Flask, request, jsonify, session
from flask_cors import CORS
import mysql.connector
import random
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = 'supersecretkey'

# Connect to MySQL
conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='',
    database='cah_cards',
    charset='utf8mb4',
    collation='utf8mb4_unicode_ci'
)
cursor = conn.cursor(dictionary=True)

# Fetch cards from MySQL
def fetch_cards():
    cursor.execute("SELECT text FROM white_cards")
    white_cards = [row['text'] for row in cursor.fetchall()]
    cursor.execute("SELECT text FROM black_cards")
    black_cards = [row['text'] for row in cursor.fetchall()]
    return white_cards, black_cards

# Initialize game state
def init_game_state():
    white_cards, black_cards = fetch_cards()
    random.shuffle(white_cards)
    random.shuffle(black_cards)
    game_state = {
        'players': [{'name': 'Player 1', 'hand': [], 'score': 0},
                    {'name': 'Player 2', 'hand': [], 'score': 0},
                    {'name': 'Player 3', 'hand': [], 'score': 0}],
        'dealer_index': 0,
        'discard_pile': [],
        'black_card': None,
        'played_cards': [],
        'white_cards': white_cards,
        'black_cards': black_cards
    }
    deal_initial_cards(game_state)
    return game_state

# Deal initial cards
def deal_initial_cards(game_state):
    for player in game_state['players']:
        player['hand'] = [game_state['white_cards'].pop() for _ in range(7)]
    game_state['black_card'] = game_state['black_cards'].pop()

@app.route('/api/game-state', methods=['GET'])
def get_game_state():
    try:
        if 'game_state' not in session:
            session['game_state'] = init_game_state()
        response = jsonify(session['game_state'])
        logging.debug(f"Response: {response.get_data(as_text=True)}")
        return response
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/play-card', methods=['POST'])
def play_card():
    try:
        if 'game_state' not in session:
            return jsonify({'error': 'Game state not initialized'}), 400
        game_state = session['game_state']
        data = request.json
        player_index = data['player_index']
        card_index = data['card_index']
        card = game_state['players'][player_index]['hand'].pop(card_index)
        game_state['played_cards'].append({'player_index': player_index, 'card': card})
        session['game_state'] = game_state
        response = jsonify(game_state)
        logging.debug(f"Response: {response.get_data(as_text=True)}")
        return response
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/pick-winner', methods=['POST'])
def pick_winner():
    try:
        if 'game_state' not in session:
            return jsonify({'error': 'Game state not initialized'}), 400
        game_state = session['game_state']
        data = request.json
        winning_card_index = data['winning_card_index']
        winning_card = game_state['played_cards'][winning_card_index]
        winning_player_index = winning_card['player_index']
        game_state['players'][winning_player_index]['score'] += 1
        game_state['played_cards'] = []
        game_state['dealer_index'] = (game_state['dealer_index'] + 1) % len(game_state['players'])
        deal_initial_cards(game_state)
        session['game_state'] = game_state
        response = jsonify(game_state)
        logging.debug(f"Response: {response.get_data(as_text=True)}")
        return response
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import random
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS

# Configure logging
logging.basicConfig(level=logging.DEBUG)

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
    white_cards = cursor.fetchall()
    cursor.execute("SELECT text FROM black_cards")
    black_cards = cursor.fetchall()
    return white_cards, black_cards

# Initialize game state
def init_game_state():
    white_cards, black_cards = fetch_cards()
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
        player['hand'] = [random.choice(game_state['white_cards'])['text'] for _ in range(7)]
    game_state['black_card'] = random.choice(game_state['black_cards'])['text']

game_state = init_game_state()

@app.route('/api/game-state', methods=['GET'])
def get_game_state():
    try:
        response = jsonify(game_state)
        logging.debug(f"Response: {response.get_data(as_text=True)}")
        return response
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/next-round', methods=['POST'])
def next_round():
    try:
        global game_state
        game_state['dealer_index'] = (game_state['dealer_index'] + 1) % len(game_state['players'])
        deal_initial_cards(game_state)
        response = jsonify(game_state)
        logging.debug(f"Response: {response.get_data(as_text=True)}")
        return response
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
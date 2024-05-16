from flask import Flask, render_template, request, jsonify, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

medium_random = True

# this for the restart button, in order not to reset the scores
def init_game_restart():
    """Initialize a new game session with empty slots and starting player 'X'."""
    session['game'] = [''] * 9
    session['current_player'] = 'X'
    session['winner'] = None


# this for the back button, in order to reset the game and the scores
def init_game_back():
    """Initialize a new game session with empty slots, starting player 'X', and reset counters."""
    session['game'] = [''] * 9
    session['current_player'] = 'X'
    session['winner'] = None
    session['counter_X'] = 0  # Reset the X wins counter
    session['counter_O'] = 0  # Reset the O wins counter


def init_game():
    """Initialize a new game session with empty slots, starting player 'X', and reset counters."""
    session['game'] = [''] * 9
    session['current_player'] = 'X'
    session['winner'] = None
    session['counter_X'] = 0  # Reset the X wins counter
    session['counter_O'] = 0  # Reset the O wins counter
    session['difficulty'] = 'none'  # Optionally reset difficulty setting


@app.route("/")
def home():
    """Serve the main game page and initialize game state if not already present."""
    init_game()
    return render_template("index.html", game=session['game'], current_player=session['current_player'],
                           counter_X=session['counter_X'], counter_O=session['counter_O'])


@app.route("/move", methods=['POST'])
def move():
    """Process a player's move and update the game state."""
    idx = int(request.form['index'])
    numberOfPlayers = int(request.form['numberOfPlayers'])
    if session['game'][idx] == '' and session['winner'] is None:
        session['game'][idx] = session['current_player']
        session['winner'] = check_winner()
        if session['winner'] is None:
            if check_for_tie():  # Check for a tie
                session['winner'] = 'tie'
            # Switch players in case of two players and if no winner yet
        if session['winner'] is None:
            session['current_player'] = 'O' if session['current_player'] == 'X' else 'X'
    return jsonify(game=session['game'], current_player=session['current_player'], winner=session['winner'],
                   counter_X=session['counter_X'], counter_O=session['counter_O'])


@app.route("/computer-move", methods=["POST"])
def computer_move():
    """Handle the computer's move using Minimax algorithm/random algorithm according to the level."""
    global medium_random  # Declare that we intend to use the global variable
    best_move = None  # Initialize best_move to ensure it has a value even if no conditions are met
    # doing the moves according to the difficulty level
    if session['current_player'] == 'O' and session['winner'] is None:
        if session['difficulty'] == 'easy':
            best_move = place_random_o()
        elif session['difficulty'] == 'medium':
            medium_random = not medium_random
            best_move = medium_level(medium_random, session['game'])
        elif session['difficulty'] == 'hard':
            best_move = find_best_move(session['game'])
        if best_move is not None:
            session['game'][best_move] = 'O'
            session['winner'] = check_winner()
            if session['winner'] is None and check_for_tie():
                session['winner'] = 'tie'
            session['current_player'] = 'X'  # Switch back to player 'X' after computer's move
    return jsonify(game=session['game'], current_player=session['current_player'], winner=session['winner'],
                   counter_X=session['counter_X'], counter_O=session['counter_O'])


@app.route("/difficulty", methods=["POST"])
def difficultyLevel():
    data = request.get_json()  # Get the JSON data sent from the client
    session['difficulty'] = data['difficulty']  # Access the difficulty key from the JSON object
    return "Difficulty received", 200  # Return a simple string response and HTTP status code


# this function is for the medium level, it is a combination of the random algorithm and the minimax algorithm
def medium_level(medium_random, board):
    if medium_random == True:
        return find_best_move(board)
    else:
        return place_random_o()


def find_best_move(board):
    best_score = float('-inf')
    best_move = None
    for i in range(len(board)):
        if board[i] == '':
            board[i] = 'O'  # Computer's move
            score = minimax(board, 0, False)
            board[i] = ''  # Undo the move
            if score > best_score:
                best_score = score
                best_move = i
    return best_move


def minimax(board, depth, is_maximizing):
    winner = check_winner_minimax(board)
    if winner:
        return {'X': -1, 'O': 1, None: 0, 'tie': 0}[winner]

    if is_maximizing:
        best_score = float('-inf')
        for i in range(len(board)):
            if board[i] == '':
                board[i] = 'O'
                score = minimax(board, depth + 1, False)
                board[i] = ''
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(len(board)):
            if board[i] == '':
                board[i] = 'X'
                score = minimax(board, depth + 1, True)
                board[i] = ''
                best_score = min(score, best_score)
        return best_score


def check_winner_minimax(board):
    winning_lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for combo in winning_lines:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != '':
            return board[combo[0]]
    if '' not in board:
        return 'tie'
    return None


def check_winner():
    """Check for a winner and update counters."""
    winning_lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for a, b, c in winning_lines:
        if session['game'][a] == session['game'][b] == session['game'][c] != '':
            session['counter_X'] += 1 if session['game'][a] == 'X' else 0
            session['counter_O'] += 1 if session['game'][a] == 'O' else 0
            return session['game'][a]
    return None


def check_for_tie():
    """Check if the game is a tie."""
    return '' not in session['game'] and session['winner'] is None


# this is for the restart button, in order not to reset the scores
@app.route("/restart", methods=["POST"])
def restart():
    """Reset the game state but do not reset the counters."""
    init_game_restart()  # Only reinitialize the game board and current player
    return jsonify(game=session['game'], current_player=session['current_player'], winner=session['winner'],
                   counter_X=session['counter_X'], counter_O=session['counter_O'])


@app.route("/back", methods=["POST"])
def back():
    """Reset the game state and reset the counters."""
    init_game_back()  # Only reinitialize the game board and current player
    return jsonify(game=session['game'], current_player=session['current_player'], winner=session['winner'],
                   counter_X=session['counter_X'], counter_O=session['counter_O'])


def place_random_o():
    """Place 'O' in a random empty cell and return the index."""
    empty_indices = [i for i, x in enumerate(session['game']) if x == '']
    if empty_indices:
        random_index = random.choice(empty_indices)
        return random_index  # Return the index instead of modifying the game state
    return None  # Return None if no moves are possible


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
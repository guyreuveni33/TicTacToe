from flask import Flask, render_template, request, jsonify, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'


def init_game_restart():
    """Initialize a new game session with empty slots and starting player 'X'."""
    session['game'] = [''] * 9
    session['current_player'] = 'X'
    session['winner'] = None


def init_game():
    """Initialize a new game session with empty slots, starting player 'X', and reset counters."""
    session['game'] = [''] * 9
    session['current_player'] = 'X'
    session['winner'] = None
    session['counter_X'] = 0
    session['counter_O'] = 0


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
                print("bbbbb")
                session['winner'] = 'tie'
            # Switch players in case of two players and if no winner yet
        if session['winner'] is None:
            session['current_player'] = 'O' if session['current_player'] == 'X' else 'X'
    return jsonify(game=session['game'], current_player=session['current_player'], winner=session['winner'],
                   counter_X=session['counter_X'], counter_O=session['counter_O'])


@app.route("/computer-move", methods=["POST"])
def computer_move():
    """Handle the computer's move using Minimax algorithm."""
    if session['current_player'] == 'O' and session['winner'] is None:
        best_move = find_best_move(session['game'])
        if best_move is not None:
            session['game'][best_move] = 'O'
            session['winner'] = check_winner()
            if session['winner'] is None and check_for_tie():
                session['winner'] = 'tie'
            session['current_player'] = 'X'  # Switch back to player 'X' after computer's move
    return jsonify(game=session['game'], current_player=session['current_player'], winner=session['winner'],
                   counter_X=session['counter_X'], counter_O=session['counter_O'])


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

def place_random_o():
    """Place 'O' in a random empty cell."""
    empty_indices = [i for i, x in enumerate(session['game']) if x == '']
    if empty_indices:
        random_index = random.choice(empty_indices)
        session['game'][random_index] = 'O'
        return True
    return False


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


@app.route("/restart", methods=["POST"])
def restart():
    """Reset the game state but do not reset the counters."""
    init_game_restart()  # Only reinitialize the game board and current player
    return jsonify(game=session['game'], current_player=session['current_player'], winner=session['winner'],
                   counter_X=session['counter_X'], counter_O=session['counter_O'])


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify, session

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # This should be hidden in production!

# Initialize the game state
def init_game():
    """Initialize a new game session with empty slots and starting player 'X'."""
    session['game'] = [''] * 9  # Creates a list of 9 empty slots representing the Tic Tac Toe board
    session['current_player'] = 'X'  # Sets the starting player
    session['winner'] = None  # Initially, there is no winner

@app.route("/")
def home():
    """Serve the main game page and initialize game state if not already present."""
    if 'game' not in session:
        init_game()
    # Pass the game state and current player to the frontend
    return render_template("index.html", game=session['game'], current_player=session['current_player'])

@app.route("/move", methods=['POST'])
def move():
    """Process a player's move and update the game state."""
    idx = int(request.form['index'])  # Get the index of the move from the POST data
    if session['game'][idx] == '' and session['winner'] is None:  # Ensure the slot is empty and no winner yet
        session['game'][idx] = session['current_player']  # Mark the slot for the current player
        session['winner'] = check_winner()  # Check if this move wins the game
        # Toggle the player from 'X' to 'O', or 'O' to 'X'
        session['current_player'] = 'O' if session['current_player'] == 'X' else 'X'
    # Return the updated game state to the client
    return jsonify(game=session['game'], current_player=session['current_player'], winner=session['winner'])

"""Check if there is a winner based on predefined winning combinations."""
def check_winner():
    # Define winning combinations on the board
    winning_lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    # Check each winning line for a match
    for a, b, c in winning_lines:
        if session['game'][a] == session['game'][b] == session['game'][c] != '':
            return session['game'][a]  # Return the winning player ('X' or 'O')
    return None  # No winner found

@app.route("/restart", methods=["POST"])
def restart():
    """Reset the game state."""
    init_game()  # Reset the game session
    return jsonify(game=session['game'], current_player=session['current_player'], winner=session['winner'])

# Run the Flask app if this script is the main program
if __name__ == "__main__":
    app.run(debug=True)

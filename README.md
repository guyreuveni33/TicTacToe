# Tic Tac Toe Game

## Overview

This Tic Tac Toe game, was developed during a semester break after the test period, as part of a personal initiative to explore new technologies. The game features both single-player and multi-player modes, providing various levels of challenge against an AI or a human opponent.

### Technologies Used

- **Python & Flask**: Serve the game's backend logic.
- **HTML/CSS/JavaScript**: Facilitate the frontend interaction.
- **Docker**: Ensures consistent deployment across different environments.

### Game Interfaces

**Main Screen:**
- Options to play against the computer or another player.
- AI difficulty levels:
  - **Easy:** The AI performs random moves.
  - **Medium:** Combines random moves with the Minimax algorithm for a balanced challenge.
  - **Hard:** Employs the Minimax algorithm, designed to be unbeatable.

![image](https://github.com/guyreuveni33/TicTacToe/assets/116805344/485e9d38-0a0a-4035-9ba6-84a3c37a63e1)

**Game Board:**
- Displays scores and player turns, offering a user-friendly and interactive gaming experience.
  - **Restart Button:** Starts a new game while preserving the score tally.
  - **Back Button:** Returns to the main menu and resets scores for a new set of games. 

 ![image](https://github.com/guyreuveni33/TicTacToe/assets/116805344/ec2c945c-7a02-43c1-93c6-cb9c87a23dc8)

### Getting Started

To set up and run the game, follow these instructions:

1. Clone the repository:
   ```bash
   git clone https://github.com/guyreuveni33/TicTacToe.git
   ```
2. Navigate to the project directory:
   ```bash
   cd TicTacToe
   ```
3. Build the Docker image:
   ```bash
   docker build -t tic-tac-toe .
   ```
4. Run the Docker container, mapping port 80 of the container to port 5000 on your host:
   ```bash
   docker run -p 5000:80 tic-tac-toe
   ```
5. Access the game at `http://localhost:5000` in your web browser.

**Note:** The provided Docker commands facilitate running the game locally. Ensure Docker is properly installed and configured on your machine.

### How to Contribute

Contributions are welcome! If you're interested in improving the game, please fork the repository on GitHub, make your changes, and submit a pull request. Ensure your contributions are well-documented and include any necessary updates to tests.

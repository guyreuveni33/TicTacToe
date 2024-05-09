// Wait until the document is fully loaded to assign functionality
document.addEventListener("DOMContentLoaded", function () {

        const restartBtn = document.getElementById('restartBtn');
        const gameBoard = document.getElementById('gameboard');
        const backBtn = document.getElementById('backBtn');
        const xScore = document.getElementById('X_winning_counter');
        const oScore = document.getElementById('O_winning_counter');
        const playerText = document.getElementById('playerText');
        const welcomeText = document.getElementById('welcomeText');
        const difficultyHeader = document.getElementById('difficultyHeader');
        const difficultyButtons = document.querySelectorAll('.difficultyBtn'); // Ensure this matches your class name exactly
        const difficultyContainer = document.getElementById('difficultyContainer');
        const twoPlayersBtn = document.getElementById('twoPlayers');
        const onePlayerBtn = document.getElementById('onePlayer');
        let numberOfPlayers = 0 //this handle the how the server will respond for the user moves
        let difficulty = ""


        onePlayerBtn.addEventListener("click", function () {
            if (difficulty === "") {
                // Temporarily enlarge the header to draw attention
                difficultyHeader.style.fontSize = '20px';
                // Set a timeout to shrink it back to normal after 600 milliseconds
                setTimeout(() => {
                    difficultyHeader.style.fontSize = '16px';
                }, 500);
            } else {
                turnMenuOff()
                turnGameBoardOn()
                numberOfPlayers = 1;
            }
        });


        //Handle the number of players on the game
        twoPlayersBtn.addEventListener('click', function () {
            turnMenuOff()
            turnGameBoardOn()
            numberOfPlayers = 2
        });

        //this handle in modify the screen buttons to be hidden

        function turnGameBoardOn() {
            gameBoard.style.display = 'flex';
            restartBtn.style.display = 'flex';
            playerText.style.display = 'flex';
            backBtn.style.display = 'flex';
            xScore.style.display = 'flex';
            oScore.style.display = 'flex';
            document.getElementById('playerText').textContent = `Current Player: X`;

        }

        //this handle in modify the screen buttons to be hidden
        function turnMenuOff() {
            twoPlayersBtn.style.display = 'none';
            onePlayerBtn.style.display = 'none';
            welcomeText.style.display = 'none';
            difficultyContainer.style.display = 'none'; // Hide the difficulty buttons
            difficultyHeader.style.display = 'none';
            difficultyButtons.forEach(button => {
                button.style.display = 'none'
            });
        }

        function turnMenuOn() {
            difficultyContainer.style.display = 'flex'; // Show the difficulty buttons again
            onePlayerBtn.style.display = 'flex'
            twoPlayersBtn.style.display = 'flex'
            difficultyHeader.style.display = 'flex';
            difficultyButtons.forEach(button => {
                button.style.display = 'flex'
            });
        }

        //this handle the difficult buttons outer animation. geeksforgeeks.org
        const barOuter = document.querySelector(".bar-outer");
        let isBarOuterDisplayed = false;  // State to track if the bar-outer is displayed
        difficultyButtons.forEach((button, index) => {
            button.addEventListener("click", function () {
                if (!isBarOuterDisplayed) {
                    barOuter.style.display = "block";  // Show the bar-outer
                    isBarOuterDisplayed = true;  // Update the state
                }
                barOuter.className = "bar-outer";  // Reset class
                barOuter.classList.add(`pos${index + 1}`);  // Apply the right position class
                if (index + 1 > current) {
                    barOuter.classList.add("right");
                } else if (index + 1 < current) {
                    barOuter.classList.add("left");
                }
                current = index + 1;
            });
        });


        restartBtn.addEventListener('click', function () {
            console.log("Restarting game, making fetch call"); // To debug restart logic
            fetch("/restart", {method: 'POST'})
                .then(response => response.json())
                .then(data => {
                    updateGameState(data);
                });
        });

        function turnGameBoardOff() {
            gameBoard.style.display = 'none';
            backBtn.style.display = 'none'
            xScore.style.display = 'none'
            oScore.style.display = 'none'
            restartBtn.style.display = 'none'
        }

        backBtn.addEventListener('click', function () {
            turnMenuOn()
            turnGameBoardOff()
            fetch("/back", {method: 'POST'})
                .then(response => response.json())
                .then(data => {
                    data.game.forEach((value, idx) => {
                        document.getElementById(idx.toString()).textContent = value;
                    });
                });
            resetScores()
        })


        // Select all game cells
        const boxes = document.querySelectorAll(".box");
        // Add click event listener to each box
        let computerTurn = false
        boxes.forEach(box => {
            box.addEventListener('click', function () {
                    if (numberOfPlayers === 1) {
                        const index = this.id; // Get the ID of the clicked box
                        // Make a POST request to the server with the index of the clicked box
                        fetch("/move", {
                            method: 'POST',
                            body: new URLSearchParams({'index': index, 'numberOfPlayers': numberOfPlayers})
                        })
                            .then(response => response.json()) // Parse the JSON response
                            .then(data => updateGameState(data)); // Update the game state with the new data
                        setTimeout(() => {
                            fetch("/computer-move", {
                                method: 'POST'
                            })
                                .then(response => response.json()) // Parse the JSON response
                                .then(data => updateGameState(data)); // Update the game state with the new data
                        }, 500)
                    }
                    if (numberOfPlayers === 2) {
                        const index = this.id; // Get the ID of the clicked box
                        // Make a POST request to the server with the index of the clicked box
                        fetch("/move", {
                            method: 'POST',
                            body: new URLSearchParams({'index': index, 'numberOfPlayers': numberOfPlayers})
                        })
                            .then(response => response.json()) // Parse the JSON response
                            .then(data => updateGameState(data)); // Update the game state with the new data
                    }
                }
            )
            ;

        });

        // Function to update the game state on the client side
        function updateGameState(data) {
            // Update each box with the respective player's move
            data.game.forEach((value, idx) => {
                document.getElementById(idx.toString()).textContent = value;
            });
            // Introduce a slight delay before showing the winner message
            // This allows the last move to be displayed before the alert.
            setTimeout(() => {
                if (data.winner === 'tie') {
                    document.getElementById('playerText').textContent = `Draw! The board is full with no winners!`;
                    console.log("aaaa")
                } else if (data.winner && data.winner !== 'tie') {
                    console.log(data.winner, "acacacadcadca")
                    document.getElementById('playerText').textContent = `${data.winner} has won!`;
                    updateScores(data);    // Assuming updateScores is defined elsewhere and updates the score
                    //alert(`${data.winner} wins!`);  // Alert the user that there is a winner
                } else {
                    // Update the text content to show who the current player is if there's no winner yet
                    document.getElementById('playerText').textContent = `Current Player: ${data.current_player}`;
                }
            }, 300);  // Delay of 300 milliseconds
        }

        function updateScores(data) {
            // Ensure these elements exist and are updated correctly
            document.getElementById('X_winning_counter').textContent = `X Wins: ${data.counter_X}`;
            document.getElementById('O_winning_counter').textContent = `O Wins: ${data.counter_O}`;
        }

        function resetScores() {
            // Ensure these elements exist and are updated correctly
            document.getElementById('X_winning_counter').textContent = `X Wins: 0`;
            document.getElementById('O_winning_counter').textContent = `O Wins: 0`;
        }


        difficultyButtons.forEach(button => {
            button.addEventListener('click', function () {

                // Remove 'active' class from all difficulty buttons
                difficultyButtons.forEach(btn => btn.classList.remove('active'));
                difficulty = this.getAttribute('data-difficulty');
                console.log("Difficulty selected:", difficulty);


                fetch('/difficulty', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({difficulty: difficulty}) // Sending an object with a difficulty property
                })

                // Add 'active' class to the clicked difficulty button
                this.classList.add('active');
            });
        });
    }
)
;
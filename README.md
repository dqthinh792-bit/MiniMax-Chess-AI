
# Chess AI

A fully implemented interactive Chess AI implemented using the MiniMax algorithm and Alpha-beta pruning for optimization. Full-fledged UI makes for a pleasant user experience. 


## Demo


  ![Alt Text](https://media.giphy.com/media/hojJHfOF6Z8XvfHjl2/giphy.gif)
## Features

- **Game Modes (Chế độ chơi)**:
  - **Player vs AI (Chơi với máy)**: Challenge the MiniMax AI engine with customizable search depth, playing as either White or Black.
  - **Two-Player Mode (Chế độ 2 người chơi)**: Local pass-and-play multiplayer mode allowing two human players to compete on the same device without AI moves.
- **Draw & Stalemate Adjudication (Luật hòa cờ & Stalemate)**:
  - **Stalemate Detection (Hòa do bế tắc)**: Accurately identifies stalemate conditions (when a player to move has no legal moves and is not in check) and adjudicates the game as a Draw rather than declaring an incorrect winner.
  - **Full Draw Rules Support**: Detects and enforces official draw conditions including stalemate, insufficient material (không đủ quân chiếu hết), threefold repetition (lặp lại 3 lần), and the 50-move rule.
- **Move Validation & Assistance**:
  - Full legal move verification and invalid move prevention powered by [python-chess](https://pypi.org/project/python-chess/).
  - Visual move indicators (highlighted green dots for valid destination squares).
- **Interactive UI**: Sleek graphical chessboard, piece sprites, and menu screens powered by [pygame](https://www.pygame.org/).
- **Configurable AI Engine**:
  - MiniMax decision tree algorithm with Alpha-Beta pruning optimization.
  - Customizable search depth and evaluation heuristics (material balance and piece development tables).

## Game Modes & Rules

### 1. Two-Player Mode (Chế độ chơi 2 người)
In addition to playing against the AI, players can select a 2-Player PvP mode. Both players alternate turns on the same machine (Pass-and-Play), allowing friends to play together while benefiting from full graphical legal move validation.

### 2. Stalemate & Draw Rules (Luật hòa cờ Stalemate)
In standard chess, the game does not always end in a checkmate:
- **Stalemate (Hòa cờ bế tắc)**: Occurs when the player whose turn it is to move has no legal moves available and their king is NOT currently in check. The game immediately resolves as a draw (1/2 - 1/2) with an appropriate Game Over draw display.
- **Other Draw Conditions**: The engine checks for insufficient material, threefold repetition, and the 50-move rule to ensure standard FIDE chess rules are respected.

## Usage/Examples

You can instantly run the demo: 

- Download and unzip or clone this repository:
    ```
    git clone https://github.com/GerniVisser/Chess.git
    cd Chess
    ```
- Install requirements

    Install newest verion of pygame used to display a visual UI ([pygame's website](https://www.pygame.org/))
    . As well as the python-chess library to validate moves and board state ([python-chess's website](https://pypi.org/project/python-chess/))
    ```
    pip3 install -r requirements.txt 
    ```
- Run demo
    ```
    python3 main.py
    ```
  

  

## General

This project was the result of a research endeavour into simulating intelligent decision making in chess. In the field of Game Theory a common approach to compute the best sequence of moves to maximize the odds of winning is to use the Minimax algorithm to minimize the possible loss for a worst case (maximum loss) scenario.

### MiniMax

Minimax is a kind of backtracking algorithm that is used in decision making and game theory to find the optimal move for a player, assuming that your opponent also plays optimally. It is widely used in two player turn-based games such as Chess or Tic-Tac-Toe
In Minimax the two players are called maximizer and minimizer. The maximizer tries to get the highest score possible while the minimizer tries to do the opposite and get the lowest score possible.
Every board state has a value associated with it. In a given state if the maximizer has upper hand then, the score of the board will tend to be some positive value. If the minimizer has the upper hand in that board state then it will tend to be some negative value. The values of the board are calculated by some heuristics which are unique for every type of game.

![Alt Text](https://upload.wikimedia.org/wikipedia/commons/6/6f/Minimax.svg)

### Evauation function

The evaluation function is used to assign a numerical value to a board state so that different board states that is a result of different sequence of moves could be compared by the MiniMax algorithm 

#### Factors that are considered
- Material
- Piece development

### Alpha-beta pruning
This is an optimization algorithm that greatly reduces the number of board states that bahve to be evaluated by removing board states that are obviously undesireble

## Lessons Learned

The engine evaluates every possible move up to six moves into the future. All the board states after the six moves are analyzed to determine which one has the highest probability of winning. By utilizing the MiniMax algorithm, the engine can then calculate which moves to Allow generating and testing sound effects?
make. The assumption is that the opposing player would also be making the optimal moves to ensure his/her victory. I then added the Alpha-beta pruning algorithm that reduces the number of board states to evaluate by removing those that are obviously unfavorable.
Evaluating any given board state is done with the use of an evaluation function. There are many ways to implement such a function, so my goal was to find one that balanced performance with accuracy. Performance is improved by reducing the number of parameters to process while accuracy is improved by increasing it. I set a 10 second limit to the processing time and then went on to find the most efficient evaluation function that I could. The one I finally came up with allowed the engine to evaluate 6 moves ahead.

  



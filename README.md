# MiniMax Chess AI

Local desktop chess built with Python, Pygame and python-chess.

## Run
Install dependencies with pip install -r requirements.txt, then run python Main.py from the repository folder.

## Features
- Human vs AI and local two-player modes.
- Easy random, Medium capture/check-priority and Hard Minimax/alpha-beta AI.
- Optional 1+0, 3+2, 5+0 and 10+0 clocks with increment, or untimed play.
- Legal move indicators, selected-square, last-move and checked-king highlighting; click-to-move and drag-and-drop.
- SAN move history with Left/Right/Home/End position review.
- Captured-piece summary, evaluation hint and best-move hint.
- Save/load PGN with S/L to saved_game.pgn; board themes with T; restart with R.
- python-chess enforces legal moves, castling, en passant, promotion and draw rules.

## Controls
Mouse: select then destination; right click clears selection.
H: best-move hint. E: evaluate. Left/Right: review. Home/End: first/live position.
S/L: save/load PGN. T: theme. R: restart. Esc: setup menu.

## Architecture
Main.py manages the application loop, modes, clocks and PGN. Board.py renders the Pygame interface. MiniMax.py contains evaluation, alpha-beta search and difficulty selection. Evaluation.py keeps the earlier evaluator API compatible.

## Authentication
This is a local desktop app. The repository has no login flow, account service, authentication middleware, OAuth callback, API credential configuration, or token/session storage. Pygame provides the local UI and python-chess provides chess rules; neither authenticates users. The application sends no credentials or tokens to a backend. GitHub authentication used to access or edit the repository is separate from the chess app runtime and is not part of its request flow.

## Not included yet
Stockfish integration, sound effects, drag-and-drop, automated blunder/missed-opportunity classification, puzzle packs and opening-book study require additional modules/assets and are not part of this pass.

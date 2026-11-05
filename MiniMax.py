import chess
MATE_SCORE=100000

def evaluate_board(board):
    if board.is_checkmate(): return -MATE_SCORE if board.turn==chess.WHITE else MATE_SCORE
    if board.is_game_over(claim_draw=True): return 0
    values={chess.PAWN:100,chess.KNIGHT:320,chess.BISHOP:330,chess.ROOK:500,chess.QUEEN:900,chess.KING:0}
    score=0
    for sq,piece in board.piece_map().items():
        sign=1 if piece.color else -1
        score+=sign*values[piece.piece_type]
        f,r=chess.square_file(sq),chess.square_rank(sq)
        center=7-(abs(3.5-f)+abs(3.5-r))
        if piece.piece_type in (chess.KNIGHT,chess.BISHOP): score+=sign*int(center*5)
        elif piece.piece_type==chess.PAWN: score+=sign*(r if piece.color else 7-r)*7
    if board.is_check(): score+=-35 if board.turn else 35
    return score

def minimax(depth,maximizingPlayer,alpha,beta,board,firstMove=False):
    if depth<=0 or board.is_game_over(claim_draw=True): return evaluate_board(board)
    moves=list(board.legal_moves)
    moves.sort(key=lambda m:(board.is_capture(m),board.gives_check(m)),reverse=True)
    best_move=None
    if maximizingPlayer:
        best=-MATE_SCORE*2
        for move in moves:
            board.push(move); value=minimax(depth-1,False,alpha,beta,board); board.pop()
            if value>best: best,best_move=value,move
            alpha=max(alpha,best)
            if beta<=alpha: break
    else:
        best=MATE_SCORE*2
        for move in moves:
            board.push(move); value=minimax(depth-1,True,alpha,beta,board); board.pop()
            if value<best: best,best_move=value,move
            beta=min(beta,best)
            if beta<=alpha: break
    return best_move if firstMove else best

def choose_move(board,difficulty="Hard",depth=3):
    import random
    legal=list(board.legal_moves)
    if not legal: return None
    if difficulty.lower()=="easy": return random.choice(legal)
    if difficulty.lower()=="medium":
        def score(move):
            value=0
            if board.is_capture(move):
                victim=board.piece_at(move.to_square); attacker=board.piece_at(move.from_square)
                value+=(victim.piece_type if victim else chess.PAWN)*10-(attacker.piece_type if attacker else 0)
            if board.gives_check(move): value+=25
            board.push(move); value+=100000 if board.is_checkmate() else 0; board.pop()
            return value
        return max(legal,key=score)
    return minimax(depth,board.turn==chess.WHITE,-MATE_SCORE*2,MATE_SCORE*2,board,True)

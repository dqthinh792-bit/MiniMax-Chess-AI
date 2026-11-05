from MiniMax import evaluate_board

class Evalualtion:
    def __init__(self,board,color="W"):
        self.board=board; self.color=color
        self.lateGameWhite=False; self.lateGameBlack=False
    def materialComp(self):
        values={1:100,2:320,3:330,4:500,5:900}
        return sum((1 if p.color else -1)*values.get(p.piece_type,0) for p in self.board.piece_map().values())
    def development(self): return evaluate_board(self.board)-self.materialComp()
    def is_late_game(self):
        return sum(1 for p in self.board.piece_map().values() if p.piece_type in (2,3,4,5))<=6
    def checkmate(self):
        if not self.board.is_checkmate(): return 0
        return 50000 if self.board.turn else -50000
    def result(self):
        score=evaluate_board(self.board)
        return score if self.color=="W" else -score

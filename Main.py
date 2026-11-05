import time
import chess
import chess.pgn
import pygame as py
from Board import DisplayBoard
from MiniMax import choose_move,evaluate_board

MODES=["Player vs AI","Two Players"]
DIFFICULTIES=["Easy","Medium","Hard"]
TIMES=["Untimed","1+0","3+2","5+0","10+0"]
COLORS=["White","Black"]

def clock_setup(choice):
    if choice=="Untimed": return None,0
    m,i=choice.split("+"); return int(m)*60,int(i)

def fmt(seconds):
    if seconds is None: return "--:--"
    seconds=max(0,int(seconds)); return f"{seconds//60:02d}:{seconds%60:02d}"

def history_san(board):
    replay=board.root(); result=[]
    for move in board.move_stack: result.append(replay.san(move)); replay.push(move)
    return result

def captured(board):
    replay=board.root(); white=[]; black=[]
    for move in board.move_stack:
        victim=replay.piece_at(move.to_square)
        if replay.is_en_passant(move): victim=chess.Piece(chess.PAWN,not replay.turn)
        if victim: (white if replay.turn==chess.BLACK else black).append(victim.symbol().upper())
        replay.push(move)
    order={"Q":0,"R":1,"B":2,"N":3,"P":4}
    return "".join(sorted(white,key=lambda p:order.get(p,9))),"".join(sorted(black,key=lambda p:order.get(p,9)))

def main():
    board=chess.Board(); ui=DisplayBoard(board)
    mi,di,ti,ci=0,2,0,0
    mode,difficulty,time_choice,player_color=MODES[mi],DIFFICULTIES[di],TIMES[ti],COLORS[ci]
    initial,increment=clock_setup(time_choice)
    clocks={chess.WHITE:initial,chess.BLACK:initial}
    state="menu"; selected=None; legal=[]; last_move=None; hint=None; evaluation=None; status=""
    review=None; last_tick=time.monotonic(); running=True

    while running:
        if state=="menu":
            start_rect=ui.draw_menu(mode,difficulty,time_choice,player_color)
        else:
            shown=board
            if review is not None:
                shown=board.root()
                for move in board.move_stack[:review]: shown.push(move)
            clock_labels=(fmt(clocks[chess.WHITE]),fmt(clocks[chess.BLACK])) if initial is not None else None
            ui.draw(shown,selected if review is None else None,legal if review is None else (),last_move,
                    history_san(board),clock_labels,mode,difficulty,status,hint,evaluation,captured(board),review)

        now=time.monotonic()
        if state=="game" and review is None and initial is not None and not board.is_game_over():
            clocks[board.turn]-=now-last_tick
            if clocks[board.turn]<=0:
                clocks[board.turn]=0; state="over"
                status=("Black wins on time" if board.turn else "White wins on time")
            last_tick=now
        else: last_tick=now

        if state=="game" and mode=="Player vs AI" and board.turn!=(player_color=="White") and review is None and not board.is_game_over():
            ui.draw(board,selected,legal,last_move,history_san(board),
                    (fmt(clocks[chess.WHITE]),fmt(clocks[chess.BLACK])) if initial is not None else None,
                    mode,difficulty,"AI is thinking...",hint,evaluation,captured(board))
            move=choose_move(board,difficulty,{"Easy":1,"Medium":1,"Hard":3}[difficulty])
            if move:
                board.push(move); last_move=move
                if clocks[not board.turn] is not None: clocks[not board.turn]+=increment
            selected=None; legal=[]; review=None; last_tick=time.monotonic()

        for event in py.event.get():
            if event.type==py.QUIT: running=False
            elif event.type==py.KEYDOWN:
                if event.key==py.K_ESCAPE: state="menu"; review=None; selected=None
                elif state=="game":
                    if event.key==py.K_t: ui.theme_index=(ui.theme_index+1)%len(ui.THEMES)
                    elif event.key==py.K_h and review is None:
                        move=choose_move(board,"Hard",3); hint=board.san(move) if move else "No legal move"
                    elif event.key==py.K_e: evaluation=evaluate_board(board)
                    elif event.key==py.K_s:
                        game=chess.pgn.Game.from_board(board); game.headers["Event"]="MiniMax Chess AI"
                        with open("saved_game.pgn","w",encoding="utf-8") as f: f.write(str(game))
                        status="Saved to saved_game.pgn"
                    elif event.key==py.K_l:
                        try:
                            with open("saved_game.pgn",encoding="utf-8") as f: game=chess.pgn.read_game(f)
                            if game:
                                board=game.board()
                                for m in game.mainline_moves(): board.push(m)
                                last_move=board.peek() if board.move_stack else None
                                clocks={chess.WHITE:initial,chess.BLACK:initial}; review=None; status="PGN loaded"
                        except OSError: status="Cannot open saved_game.pgn"
                    elif event.key in (py.K_LEFT,py.K_RIGHT,py.K_HOME,py.K_END) and board.move_stack:
                        current=len(board.move_stack) if review is None else review
                        if event.key==py.K_LEFT: review=max(0,current-1)
                        elif event.key==py.K_RIGHT:
                            review=current+1
                            if review>=len(board.move_stack): review=None
                        elif event.key==py.K_HOME: review=0
                        else: review=None
                    elif event.key==py.K_r:
                        board.reset(); last_move=None; clocks={chess.WHITE:initial,chess.BLACK:initial}
                        selected=None; legal=[]; review=None; hint=None; evaluation=None; status="New game"
                    last_tick=time.monotonic()
            elif state=="menu" and event.type==py.MOUSEBUTTONDOWN and event.button==1:
                _,y=event.pos
                if 200<=y<=270: mi=(mi+1)%len(MODES); mode=MODES[mi]
                elif 270<y<=340: di=(di+1)%len(DIFFICULTIES); difficulty=DIFFICULTIES[di]
                elif 340<y<=410: ti=(ti+1)%len(TIMES); time_choice=TIMES[ti]
                elif 410<y<=480: ci=(ci+1)%len(COLORS); player_color=COLORS[ci]
                elif start_rect.collidepoint(event.pos):
                    board=chess.Board(); initial,increment=clock_setup(time_choice)
                    clocks={chess.WHITE:initial,chess.BLACK:initial}; last_move=None
                    selected=None; legal=[]; hint=None; evaluation=None; review=None; status=""
                    state="game"; last_tick=time.monotonic()
            elif state=="game" and event.type==py.MOUSEBUTTONDOWN and event.button==1:
                if review is not None: review=None
                square=ui.square_at(event.pos)
                if square is not None:
                    human_turn=(mode=="Two Players" or board.turn==(player_color=="White"))
                    if selected is None:
                        piece=board.piece_at(square)
                        if piece and piece.color==board.turn and human_turn:
                            selected=square; legal=[m for m in board.legal_moves if m.from_square==square]
                    else:
                        move=next((m for m in legal if m.to_square==square),None)
                        if move:
                            board.push(move); last_move=move
                            if clocks[not board.turn] is not None: clocks[not board.turn]+=increment
                            hint=None; evaluation=None; status=""
                            selected=None; legal=[]
                        else:
                            piece=board.piece_at(square)
                            if piece and piece.color==board.turn and human_turn:
                                selected=square; legal=[m for m in board.legal_moves if m.from_square==square]
                            else: selected=None; legal=[]
                else: selected=None; legal=[]
            elif state=="game" and event.type==py.MOUSEBUTTONDOWN and event.button==3:
                selected=None; legal=[]

        if state=="game" and board.is_game_over(claim_draw=True):
            outcome=board.outcome(claim_draw=True)
            status=board.result()+" — "+outcome.termination.name.replace("_"," ").title()
            state="over"
        if state=="over":
            ui.screen.fill((25,30,39))
            title=ui.large.render("GAME OVER",True,(245,245,245))
            ui.screen.blit(title,title.get_rect(center=(520,260)))
            label=ui.font.render(status,True,(245,220,140))
            ui.screen.blit(label,label.get_rect(center=(520,330)))
            prompt=ui.font.render("Press ENTER for menu or R for rematch",True,(225,225,225))
            ui.screen.blit(prompt,prompt.get_rect(center=(520,410))); py.display.flip()
            for event in py.event.get():
                if event.type==py.QUIT: running=False
                elif event.type==py.KEYDOWN and event.key in (py.K_RETURN,py.K_r): state="menu"; status=""
        ui.clock.tick(60)
    ui.close()

if __name__=="__main__": main()

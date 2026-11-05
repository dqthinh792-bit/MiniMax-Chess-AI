import pygame as py
import chess
from pathlib import Path

class DisplayBoard:
    WIDTH, HEIGHT = 1040, 760
    BOARD_X, BOARD_Y, SQ = 28, 62, 80
    THEMES = [((238,216,181),(126,87,58)),((232,235,239),(119,149,86)),((235,222,204),(105,125,145))]

    def __init__(self, board):
        py.init()
        self.screen=py.display.set_mode((self.WIDTH,self.HEIGHT))
        py.display.set_caption("MiniMax Chess AI")
        self.clock=py.time.Clock()
        self.font=py.font.SysFont("segoeui",20)
        self.small=py.font.SysFont("segoeui",15)
        self.large=py.font.SysFont("segoeui",34,bold=True)
        self.theme_index=0
        self.sprites={}
        root=Path(__file__).resolve().parent/"Image"
        for symbol in "pnbrqk":
            for color,suffix in ((chess.WHITE,"lt"),(chess.BLACK,"dt")):
                try:
                    img=py.image.load(str(root/("Chess_"+symbol+suffix+"60.png"))).convert_alpha()
                    self.sprites[(symbol,color)]=py.transform.smoothscale(img,(62,62))
                except (py.error,FileNotFoundError):
                    pass

    def square_at(self,pos):
        col=(pos[0]-self.BOARD_X)//self.SQ
        row=(pos[1]-self.BOARD_Y)//self.SQ
        return chess.square(col,7-row) if 0<=col<8 and 0<=row<8 else None

    def square_rect(self,sq):
        return py.Rect(self.BOARD_X+chess.square_file(sq)*self.SQ,
                       self.BOARD_Y+(7-chess.square_rank(sq))*self.SQ,self.SQ,self.SQ)

    def line(self,text,x,y,color=(225,228,234)):
        self.screen.blit(self.small.render(str(text),True,color),(x,y))

    def draw(self,board,selected=None,legal_moves=(),last_move=None,history=(),
             clocks=None,mode="Player vs AI",difficulty="Hard",status="",hint=None,
             evaluation=None,captured=None,history_index=None):
        self.screen.fill((25,30,39))
        light,dark=self.THEMES[self.theme_index]
        py.draw.rect(self.screen,(12,15,21),(self.BOARD_X-5,self.BOARD_Y-5,650,650),border_radius=8)
        targets={m.to_square for m in legal_moves}
        for sq in chess.SQUARES:
            rect=self.square_rect(sq)
            color=light if (chess.square_file(sq)+chess.square_rank(sq))%2==0 else dark
            py.draw.rect(self.screen,color,rect)
            if last_move and sq in (last_move.from_square,last_move.to_square):
                overlay=py.Surface((80,80),py.SRCALPHA); overlay.fill((255,220,0,75)); self.screen.blit(overlay,rect)
            if selected==sq: py.draw.rect(self.screen,(40,145,230),rect,4)
            if sq in targets:
                py.draw.circle(self.screen,(20,145,65),rect.center,32,5) if board.piece_at(sq) else py.draw.circle(self.screen,(20,125,60),rect.center,10)
        if board.is_check() and board.king(board.turn) is not None:
            py.draw.rect(self.screen,(210,45,45),self.square_rect(board.king(board.turn)),5)
        glyph={"K":"♔","Q":"♕","R":"♖","B":"♗","N":"♘","P":"♙","k":"♚","q":"♛","r":"♜","b":"♝","n":"♞","p":"♟"}
        for sq,piece in board.piece_map().items():
            rect=self.square_rect(sq); img=self.sprites.get((piece.symbol().lower(),piece.color))
            if img: self.screen.blit(img,img.get_rect(center=rect.center))
            else:
                label=self.large.render(glyph[piece.symbol()],True,(250,250,250) if piece.color else (20,20,20))
                self.screen.blit(label,label.get_rect(center=rect.center))
        for i in range(8):
            self.line(chess.FILE_NAMES[i],self.BOARD_X+i*80+36,706)
            self.line(8-i,8,self.BOARD_Y+i*80+32)
        x=710
        self.screen.blit(self.large.render("CHESS AI",True,(245,245,245)),(x,28))
        self.line("Mode: "+mode,x,82); self.line("AI: "+difficulty,x,111)
        self.line("White to move" if board.turn else "Black to move",x,140,(115,210,150))
        if clocks: self.line("White "+clocks[0]+"   Black "+clocks[1],x,170,(245,220,120))
        self.line("MOVE HISTORY",x,216,(120,190,245))
        start=max(0,len(history)-14)
        for idx,san in enumerate(history[start:],start):
            self.line((str(idx//2+1)+". " if idx%2==0 else "    ")+san,x,246+(idx-start)*23)
        self.line("CAPTURED",x,585,(120,190,245))
        if captured:
            self.line("White: "+captured[0],x,613); self.line("Black: "+captured[1],x,640)
        if evaluation is not None: self.line("Eval (White +): "+str(round(evaluation/100,2)),x,670)
        if hint: self.line("Hint: "+hint,x,697,(250,220,120))
        self.line(status or "H hint | ←/→ review | S save | L load | T theme",x,730,(190,195,205))
        py.display.flip()
        self.clock.tick(60)

    def draw_menu(self,mode,difficulty,time_control,player_color):
        self.screen.fill((25,30,39))
        title=self.large.render("MINIMAX CHESS AI",True,(245,245,245))
        self.screen.blit(title,title.get_rect(center=(520,105)))
        sub=self.font.render("Choose a game and start playing",True,(190,200,215))
        self.screen.blit(sub,sub.get_rect(center=(520,155)))
        for label,value,y in [("Mode",mode,230),("Difficulty",difficulty,300),("Clock",time_control,370),("Play as",player_color,440)]:
            self.screen.blit(self.font.render(label+":  "+value,True,(245,245,245)),(300,y))
            self.line("click to cycle",650,y+3,(150,160,175))
        rect=py.Rect(390,535,260,62); py.draw.rect(self.screen,(42,145,95),rect,border_radius=10)
        self.screen.blit(self.font.render("START GAME",True,(255,255,255)),self.font.render("START GAME",True,(255,255,255)).get_rect(center=rect.center))
        self.line("Modes: Player vs AI / Two Players     Difficulty: Easy / Medium / Hard",225,640)
        self.line("Clock: Untimed / 1+0 / 3+2 / 5+0 / 10+0",330,670)
        py.display.flip()
        return rect

    def close(self):
        py.quit()

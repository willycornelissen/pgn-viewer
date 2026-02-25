import sys
import os
import chess
import chess.pgn
import pygame

# Configurações de cores e tamanhos
SQUARE_SIZE = 80
BOARD_SIZE = SQUARE_SIZE * 8
WINDOW_SIZE = BOARD_SIZE
COLOR_LIGHT = (240, 217, 181)
COLOR_DARK = (181, 136, 99)
COLOR_HIGHLIGHT = (205, 210, 106)

class PGNViewer:
    def __init__(self, pgn_path):
        self.pgn_path = pgn_path
        self.game = self.load_game(pgn_path)
        self.moves = list(self.game.mainline_moves())
        self.current_move_idx = -1
        
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Chess PGN Viewer")
        
        self.piece_surfaces = self.load_or_generate_pieces()

    def load_game(self, path):
        try:
            with open(path) as pgn:
                game = chess.pgn.read_game(pgn)
                if game is None:
                    print("Erro: Arquivo PGN inválido.")
                    sys.exit(1)
                return game
        except Exception as e:
            print(f"Erro ao ler arquivo: {e}")
            sys.exit(1)

    def load_or_generate_pieces(self):
        surfaces = {}
        assets_dir = "assets"
        mapping = {
            'K': 'wK.png', 'Q': 'wQ.png', 'R': 'wR.png', 'B': 'wB.png', 'N': 'wN.png', 'P': 'wP.png',
            'k': 'bK.png', 'q': 'bQ.png', 'r': 'bR.png', 'b': 'bB.png', 'n': 'bN.png', 'p': 'bP.png'
        }
        
        for symbol, filename in mapping.items():
            path = os.path.join(assets_dir, filename)
            # Tenta carregar imagem real
            if os.path.exists(path):
                try:
                    img = pygame.image.load(path).convert_alpha()
                    surfaces[symbol] = pygame.transform.smoothscale(img, (SQUARE_SIZE, SQUARE_SIZE))
                    continue
                except:
                    print(f"Erro ao carregar {filename}, usando versão vetorial.")
            
            # Fallback Geométrico de Alta Qualidade
            surf = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            p_obj = chess.Piece.from_symbol(symbol)
            self.draw_vector_piece(surf, p_obj.piece_type, p_obj.color)
            surfaces[symbol] = surf
            
        return surfaces

    def draw_vector_piece(self, surf, p_type, color):
        fill = (255, 255, 255) if color == chess.WHITE else (45, 45, 45)
        line = (0, 0, 0) if color == chess.WHITE else (220, 220, 220)
        s = SQUARE_SIZE
        c = s // 2
        
        def poly(points):
            pygame.draw.polygon(surf, fill, points)
            pygame.draw.polygon(surf, line, points, 2)

        def circ(pos, radius, width=0):
            pygame.draw.circle(surf, fill if width==0 else line, pos, radius, width)
            if width == 0: pygame.draw.circle(surf, line, pos, radius, 2)

        if p_type == chess.PAWN:
            circ((c, s*0.35), s*0.15)
            poly([(s*0.3, s*0.85), (s*0.7, s*0.85), (s*0.6, s*0.5), (s*0.4, s*0.5)])
        elif p_type == chess.ROOK:
            poly([(s*0.25, s*0.85), (s*0.75, s*0.85), (s*0.75, s*0.3), (s*0.25, s*0.3)])
            poly([(s*0.2, s*0.3), (s*0.8, s*0.3), (s*0.8, s*0.15), (s*0.2, s*0.15)])
        elif p_type == chess.KNIGHT:
            poly([(s*0.3, s*0.85), (s*0.7, s*0.85), (s*0.8, s*0.4), (s*0.6, s*0.15), (s*0.35, s*0.2)])
        elif p_type == chess.BISHOP:
            circ((c, s*0.4), s*0.18)
            poly([(s*0.35, s*0.85), (s*0.65, s*0.85), (c, s*0.6)])
        elif p_type == chess.QUEEN:
            poly([(s*0.2, s*0.85), (s*0.8, s*0.85), (s*0.9, s*0.3), (c, s*0.5), (s*0.1, s*0.3)])
        elif p_type == chess.KING:
            poly([(s*0.25, s*0.85), (s*0.75, s*0.85), (s*0.7, s*0.35), (s*0.3, s*0.35)])
            pygame.draw.line(surf, line, (c, s*0.05), (c, s*0.3), 3)
            pygame.draw.line(surf, line, (s*0.35, s*0.15), (s*0.65, s*0.15), 3)

    def draw_board(self, board):
        last_move = self.moves[self.current_move_idx] if self.current_move_idx >= 0 else None
        for rank in range(8):
            for file in range(8):
                square = chess.square(file, 7 - rank)
                color = COLOR_LIGHT if (rank + file) % 2 == 0 else COLOR_DARK
                if last_move and (square == last_move.from_square or square == last_move.to_square):
                    color = COLOR_HIGHLIGHT
                pygame.draw.rect(self.screen, color, (file * SQUARE_SIZE, rank * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                piece = board.piece_at(square)
                if piece:
                    self.screen.blit(self.piece_surfaces[piece.symbol()], (file * SQUARE_SIZE, rank * SQUARE_SIZE))

    def run(self):
        clock = pygame.time.Clock()
        while True:
            board = self.game.board()
            for i in range(self.current_move_idx + 1):
                board.push(self.moves[i])
            self.draw_board(board)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and self.current_move_idx < len(self.moves)-1:
                        self.current_move_idx += 1
                    elif event.key == pygame.K_LEFT and self.current_move_idx >= 0:
                        self.current_move_idx -= 1
                    elif event.key == pygame.K_ESCAPE: return
            clock.tick(30)

if __name__ == "__main__":
    if len(sys.argv) < 2: 
        print("Uso: ./venv/bin/python pgn_viewer.py example.pgn")
        sys.exit(1)
    viewer = PGNViewer(sys.argv[1])
    print("Visualizador Pronto! (Priorizando imagens da pasta assets/)")
    viewer.run()

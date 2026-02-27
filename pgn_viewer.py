import sys
import os
import chess
import chess.pgn
import pygame

# Configurações de cores e tamanhos
SQUARE_SIZE = 80
BOARD_SIZE = SQUARE_SIZE * 8
TOP_BAR_HEIGHT = 50
BOTTOM_BAR_HEIGHT = 60
WINDOW_WIDTH = BOARD_SIZE
WINDOW_HEIGHT = BOARD_SIZE + TOP_BAR_HEIGHT + BOTTOM_BAR_HEIGHT

COLOR_LIGHT = (240, 217, 181)
COLOR_DARK = (181, 136, 99)
COLOR_HIGHLIGHT = (205, 210, 106)
COLOR_BAR = (45, 45, 45)
COLOR_TEXT = (240, 240, 240)
COLOR_INFO = (180, 180, 180)

# Cores para anotações
COLOR_GREEN = (34, 139, 34)
COLOR_RED = (178, 34, 34)
COLOR_YELLOW = (218, 165, 32)

def resource_path(relative_path):
    """ Obtém o caminho absoluto para o recurso, funciona para dev e para PyInstaller """
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class PGNViewer:
    def __init__(self, pgn_path):
        self.pgn_path = pgn_path
        self.game = self.load_game(pgn_path)
        
        # Guardamos os nós para acessar comentários e NAGs
        self.nodes = list(self.game.mainline())
        self.current_move_idx = -1
        
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Chess PGN Viewer")
        
        # Seleciona fontes de forma robusta
        font_name = pygame.font.match_font('arial', 'liberation-sans', 'sans-serif')
        self.font = pygame.font.Font(font_name, 22)
        self.small_font = pygame.font.Font(font_name, 16)
        self.bold_font = pygame.font.Font(font_name, 22)
        # Tenta aplicar negrito se a fonte permitir, caso contrário ignora
        try: self.bold_font.set_bold(True)
        except: pass
        
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
        mapping = {
            'K': 'wK.png', 'Q': 'wQ.png', 'R': 'wR.png', 'B': 'wB.png', 'N': 'wN.png', 'P': 'wP.png',
            'k': 'bK.png', 'q': 'bQ.png', 'r': 'bR.png', 'b': 'bB.png', 'n': 'bN.png', 'p': 'bP.png'
        }
        
        for symbol, filename in mapping.items():
            path = resource_path(os.path.join("assets", filename))
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
        last_move = self.nodes[self.current_move_idx].move if self.current_move_idx >= 0 else None
        for rank in range(8):
            for file in range(8):
                square = chess.square(file, 7 - rank)
                color = COLOR_LIGHT if (rank + file) % 2 == 0 else COLOR_DARK
                if last_move and (square == last_move.from_square or square == last_move.to_square):
                    color = COLOR_HIGHLIGHT
                
                # Ajusta a posição Y somando TOP_BAR_HEIGHT
                x = file * SQUARE_SIZE
                y = rank * SQUARE_SIZE + TOP_BAR_HEIGHT
                pygame.draw.rect(self.screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
                
                piece = board.piece_at(square)
                if piece:
                    self.screen.blit(self.piece_surfaces[piece.symbol()], (x, y))

    def draw_top_bar(self):
        # Fundo da barra superior
        bar_rect = pygame.Rect(0, 0, WINDOW_WIDTH, TOP_BAR_HEIGHT)
        pygame.draw.rect(self.screen, COLOR_BAR, bar_rect)
        
        headers = self.game.headers
        white = headers.get("White", "Brancas")
        black = headers.get("Black", "Pretas")
        event = headers.get("Event", "?")
        date = headers.get("Date", "????.??.??")
        
        # Renderiza Nomes dos Jogadores
        player_text = f"● {white} vs ● {black}"
        player_surf = self.bold_font.render(player_text, True, COLOR_TEXT)
        self.screen.blit(player_surf, (20, 10))
        
        # Renderiza Informações Extras (Evento e Data)
        info_text = f"{event} | {date}"
        info_surf = self.small_font.render(info_text, True, COLOR_INFO)
        self.screen.blit(info_surf, (20, TOP_BAR_HEIGHT - 20))

    def draw_bottom_bar(self):
        # Desenha o fundo da barra
        y_pos = BOARD_SIZE + TOP_BAR_HEIGHT
        bar_rect = pygame.Rect(0, y_pos, WINDOW_WIDTH, BOTTOM_BAR_HEIGHT)
        pygame.draw.rect(self.screen, COLOR_BAR, bar_rect)
        
        if self.current_move_idx < 0:
            return

        current_node = self.nodes[self.current_move_idx]
        
        # Mapeamento de NAGs para Símbolos e Cores
        # 1=!, 2=?, 3=!!, 4=??, 5=!?, 6=?!
        nag_map = {
            1: ("!", COLOR_GREEN),
            2: ("?", COLOR_RED),
            3: ("!!", COLOR_GREEN),
            4: ("??", COLOR_RED),
            5: ("!?", COLOR_YELLOW),
            6: ("?!", COLOR_YELLOW)
        }
        
        annotation = None
        for nag in current_node.nags:
            if nag in nag_map:
                annotation = nag_map[nag]
                break # Pega a primeira anotação encontrada

        x_offset = 20
        # Desenha Ícone de Anotação se existir
        if annotation:
            text, color = annotation
            # Desenha um círculo colorido
            circle_radius = 18
            circle_pos = (x_offset + circle_radius, y_pos + BOTTOM_BAR_HEIGHT // 2)
            pygame.draw.circle(self.screen, color, circle_pos, circle_radius)
            
            # Texto da anotação centralizado no círculo
            text_surf = self.bold_font.render(text, True, COLOR_TEXT)
            text_rect = text_surf.get_rect(center=circle_pos)
            self.screen.blit(text_surf, text_rect)
            x_offset += circle_radius * 2 + 15

        # Desenha Comentário
        comment = current_node.comment
        if comment:
            # Limita o tamanho do comentário para caber na tela
            max_width = WINDOW_WIDTH - x_offset - 20
            comment_surf = self.font.render(comment, True, COLOR_TEXT)
            
            # Truncar se for muito longo
            if comment_surf.get_width() > max_width:
                cropped_rect = pygame.Rect(0, 0, max_width, BOTTOM_BAR_HEIGHT)
                self.screen.blit(comment_surf, (x_offset, y_pos + (BOTTOM_BAR_HEIGHT - comment_surf.get_height()) // 2), cropped_rect)
            else:
                self.screen.blit(comment_surf, (x_offset, y_pos + (BOTTOM_BAR_HEIGHT - comment_surf.get_height()) // 2))

    def run(self):
        clock = pygame.time.Clock()
        while True:
            board = self.game.board()
            for i in range(self.current_move_idx + 1):
                board.push(self.nodes[i].move)
            
            self.draw_top_bar()
            self.draw_board(board)
            self.draw_bottom_bar()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and self.current_move_idx < len(self.nodes)-1:
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

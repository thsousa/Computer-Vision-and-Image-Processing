from .chess import *
from vpi.io import read_gray_image, display_image
import numpy as np

"""
    imagens com números ímpares: jogada de peça branca
    imagem 0.jpg é o tabuleiro inicial (é sempre o mesmo)
    dimensão da casa do tab = 60x60 pixels
    intensidades:
                   - casas escuras = 80
                   - casas claras = 180
                   - peça preta = 0
                   - peça branca = 255      
    
    Objeto Move:
        - piece_start: um objeto ChessSquare com a seguintes informações:
                        - string de identificação da peça movida;
                        - a posição inicial da peça movida (posição da peça movida na jogada anterior)

        - piece_stop, um objeto ChessSquare, com a seguintes informações:
                        - a string vazia, se a peça não capturou nenhuma peça adversária, ou 
                          identificação da peça capturada, caso contrário;
                        - a posição da peça depois da jogada conforme imagem sendo analisada.

        - image_filepath: o caminho do arquivo da imagem sendo analisada
    O objeto Move deve ser armazenado no objeto Game.
"""

def is_empty_chess_square(img, x0, xn, y0, yn):
    return(np.mean(img[x0:xn, y0:yn]) == 80 or np.mean(img[x0:xn, y0:yn]) == 180)

def fix_coordenate(x):
    return(np.floor(x/60)*60).astype(int)

def analyze_chess_game(image_directory):
    game = Game()
    chessboard = Chessboard()
    img = read_gray_image("images/chess/0.png")
    
    for i in range(1, 28, 1):
        filename = "images/chess/" + str(i) + ".png"
        img_actual = read_gray_image(filename)
        filename2 = "images/chess/" + str(i-1) + ".png"
        img_prev = read_gray_image(filename2)
        diff = img_actual - img_prev
        
        # procura as coordenas onde a diferença das imagens não é zero e corrige valor
        # para que coincida com as coordenadas de um ChessSquare
        x, y = diff.nonzero()
        x0, xn = fix_coordenate(x.min()), fix_coordenate(x.max() + 1)
        y0, yn = fix_coordenate(y.min()), fix_coordenate(y.max() + 1)

        #encontrar as duas casas alteradas e descobrir qual é a inicial através da média da cor do chessSquare
        # caso 1: mesma linha
        if x0 == xn:
            if is_empty_chess_square(img_actual, x0, x0 + 60, yn, yn + 60):
                tmp = y0
                y0 = yn
                yn = tmp
        else: 
            # caso 2: mesma coluna
            if y0 == yn:
                if is_empty_chess_square(img_actual, xn, xn + 60, y0, y0 + 60):
                    tmp = x0
                    x0 = xn
                    xn = tmp
            # caso 3: linhas e colunas diferentes (as coordenadas (x0, y0) e (xn, yn) definem um retângulo)
            else:
                x, y = diff[x0:x0 + 60,y0:yn + 60].nonzero()
                yt1 = y0 + set_coordenate(y.min())
                x, y = diff[xn:xn + 60,y0:yn + 60].nonzero()
                yt2 = y0 + set_coordenate(y.min())
                if(is_empty_chess_square(img_actual, xn, xn + 60, yt2, yt2 + 60)):
                    # casa que aparece na parte inferior está vazia é a inicial
                    tmp = x0
                    x0 = xn
                    xn = tmp
                    yn = yt1
                    y0 = yt2
                else:
                    y0 = yt1
                    yn = yt2
        # casting para acessar posições no tabuleiro
        xn = (xn/60).astype(int)
        yn = (yn/60).astype(int)
        x0 = (x0/60).astype(int)
        y0 = (y0/60).astype(int)
   
        name = chessboard.board[x0][y0].piece_name
        chessboard.set_piece("", x0, y0)            
        piece_start = ChessSquare(name, x0, y0)
        mov = chessboard.board[xn][yn].piece_name
        piece_stop = ChessSquare(mov, xn, yn)
        # atualiza peça no tabuleiro e salva a jogada
        chessboard.set_piece(name, xn, yn)
        game.add_move(Move(filename, piece_start,  piece_stop))
        
    return game


import numpy as np
import os

BlackPieces = ["RB1", "NB1", "BB1", "QB",  "KB",  "BB2", "NB2", "RB2", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PB7", "PB8"]
WhitePieces = ["PW1", "PW2", "PW3", "PW4", "PW5", "PW6", "PW7", "PW8", "RW1", "NW1", "BW1", "QW",  "KW",  "BW2", "NW2", "RW2"]

class ChessSquare:
    def __init__(self, piece_name, x, y):
        self.piece_name = piece_name
        self.x = x
        self.y = y

class Move:
    def __init__(self, image_filepath, piece_start,  piece_stop):
        self.image_filepath = image_filepath
        self.piece_start = piece_start
        self.piece_stop = piece_stop

class Game:
    def __init__(self):
        self.moves = []

    def add_move(self, move):
        self.moves.append(move)

class Chessboard:
    def __init__(self):
        self._init_board()

    def _init_board(self):
        self.board = []
        self.template = [["RB1", "NB1", "BB1", "QB",  "KB",  "BB2", "NB2", "RB2"],
             ["PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PB7", "PB8"],
             ["",    "",    "",    "",    "",    "",    "",     ""  ],
             ["",    "",    "",    "",    "",    "",    "",     ""  ],
             ["",    "",    "",    "",    "",    "",    "",     ""  ],
             ["",    "",    "",    "",    "",    "",    "",     ""  ],
             ["PW1", "PW2", "PW3", "PW4", "PW5", "PW6", "PW7", "PW8"],
             ["RW1", "NW1", "BW1", "QW",  "KW",  "BW2", "NW2", "RW2"]]

        for x in np.arange(8):
            self.board.append([])
            for y in np.arange(8) :
                self.board[x].append(ChessSquare(self.template[x][y],x,y))

    def set_piece(self, piece_name, x, y):
        self.board[x][y].piece_name = piece_name
        self.board[x][y].x = x
        self.board[x][y].y = y

    def print_board(self):
        for x in np.arange(8):
            for y in np.arange(8):
                if (self.board[x][y].piece_name in [""]):
                    print("   ", end=" ")
                else:
                    print(self.board[x][y].piece_name, end=" ")

            print()


    def get_flat_board(self):
        return [square for row in self.board for square in row]

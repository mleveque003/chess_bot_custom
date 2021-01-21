import chess


class Values:
    @staticmethod
    def get_piece_value(piece):
        piece_values = {
            chess.PAWN: 100,
            chess.ROOK: 500,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.QUEEN: 900,
            chess.KING: 20000,
            None: 0
        }
        return piece_values[piece]

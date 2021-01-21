import chess

from chess_bot_custom.values import Values


class Bot:
    """
    First bot working with minimax algorithm
    """
    def __init__(self, side=chess.BLACK, depth=4):
        self.depth = depth
        self.side = side

    def play(self, board):
        return self.minimax(self.side, self.depth, board)[1]


    def minimax(self, player, depth, board : chess.Board):
        if depth == 0 or board.is_game_over():
            return self.heuristic(board), None
        if player:
            value = -999999
            best_move = None
            for move in board.legal_moves:
                board.push(move)
                result = self.minimax(not player, depth-1, board)[0]
                board.pop()
                value = max(value, result)
                if value == result:
                    best_move = move
            return value, best_move
        else:
            value = 999999
            best_move = None
            for move in board.legal_moves:
                board.push(move)
                result = self.minimax(not player, depth-1, board)[0]
                board.pop()
                value = min(value, result)
                if value == result:
                    best_move = move
            return value, best_move

    def heuristic(self, board: chess.Board):
        i = 0
        evaluation = 0
        x = True
        try:
            x = bool(board.piece_at(i).color)
        except AttributeError as e:
            x = x
        while i < 63:
            i += 1
            evaluation = evaluation + (Values.get_piece_value(board.piece_type_at(i)) if x else
                                       -Values.get_piece_value(board.piece_type_at(i)))
        return evaluation

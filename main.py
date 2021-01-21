import chess
import chess.svg
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget
import argparse

from chess_bot_custom.bot import Bot

WIN_SIZE = 650
OFFSET = 10


class MainWindow(QWidget):
    """
    Create a surface for the chessboard.
    """

    def __init__(self, bot=None, side=chess.WHITE):
        """
        Initialize the chessboard.
        """
        super().__init__()

        self.setWindowTitle("Play Chess !")
        self.setGeometry(300, 300, WIN_SIZE + 2 * OFFSET, WIN_SIZE + 2 * OFFSET)

        self.widget_svg = QSvgWidget(parent=self)
        self.widget_svg.setGeometry(OFFSET, OFFSET, WIN_SIZE, WIN_SIZE)

        self.board_size = min(self.widget_svg.width(),
                              self.widget_svg.height())
        self.coordinates = True
        self.margin = 0.05 * self.board_size if self.coordinates else 0
        self.square_size = (self.board_size - 2 * self.margin) / 8.0
        self.piece_to_move = [None, None]
        self.bot = bot
        self.side = side

        self.board = chess.Board()
        self.drawBoard()

    @pyqtSlot(QWidget)
    def mousePressEvent(self, event):
        """
        Handle left mouse clicks and enable moving chess pieces by
        clicking on a chess piece and then the target square.

        Moves must be made according to the rules of chess because
        illegal moves are suppressed.
        """
        if event.x() <= self.board_size and event.y() <= self.board_size:
            if event.buttons() == Qt.LeftButton:
                if self.margin < event.x() < self.board_size - self.margin and \
                        self.margin < event.y() < self.board_size - self.margin:
                    file = int((event.x() - self.margin) / self.square_size)
                    rank = 7 - int((event.y() - self.margin) / self.square_size)
                    square = chess.square(file, rank)
                    piece = self.board.piece_at(square)
                    coordinates = "{}{}".format(chr(file + 97), str(rank + 1))
                    print(coordinates)
                    played = False
                    if self.piece_to_move[0] is not None:
                        move = chess.Move.from_uci("{}{}".format(self.piece_to_move[1], coordinates))
                        if move in self.board.legal_moves:
                            self.board.push(move)
                        piece = None
                        coordinates = None
                        played = True
                    else:
                        self.highlightSquare(square)
                    self.piece_to_move = [piece, coordinates]
                    self.drawBoard()
                    if self.board.turn is self.bot.side and self.bot is not None and played:
                        print("turn : {}".format(self.board.turn))
                        bot_move = self.bot.play(self.board)
                        self.board.push(bot_move)
                        self.drawBoard()
                        played = False
                    print(self.board.is_game_over())

    def drawBoard(self, board_svg=None):
        """
        Draw a chessboard with the starting position and then redraw
        it for every new move.
        """
        print(board_svg)
        if board_svg is None:
            board_svg = self.board._repr_svg_().encode("UTF-8")
        self.widget_svg.load(board_svg)

        

def commandParsing():
    parser = argparse.ArgumentParser(
        description='Chess game giving you your opponent\'s choice.')
    parser.add_argument('--mode', '-M',
                        dest='mode',
                        default='2p',
                        help='Define if you want to face a bot or play with 2 players. Args are : "2p", "minimax".')
    parser.add_argument('--side', '-S',
                        dest='side',
                        default='R',
                        help='Define if you want to be white (W), black (B) or random side (R)(default), only used '
                             'with a bot.')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = commandParsing()

    app = QApplication([])
    if args.side == "W":
        side = chess.WHITE
    elif args.side == "B":
        side = chess.BLACK
    else:
        import random
        side = chess.Color(bool(random.getrandbits(1)))

    bot = None
    if args.mode == "2p":
        bot = None
    elif args.mode == "minimax":
        bot = Bot(side=chess.BLACK)

    window = MainWindow(bot=bot, side=side)
    window.show()
    app.exec()

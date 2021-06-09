from CheckersReinforcementLearning.Board import Board
from CheckersReinforcementLearning.AI import Alpha_beta
from Chessboard import Chessboard
import cv2
from matplotlib import pyplot as plt
import numpy as np

chb = Chessboard.Chessboard()

img = cv2.imread("./img/checkers_scanner_pieces_2.jpg")

chb.detectGameState(img)

print(chb.pieceCoordinateInsidePos)
chb.prettyPrintBoard()


board = Board(chb.convertStateToAI())
# board.print_board()

print(chb.convertPositionToAI('c5'))

alpha_beta_ai = Alpha_beta(False, 6)
alpha_beta_ai.set_board(board)

print("Player Turn: ", board.player_turn)
# board.make_move([[2, 0], [3, 0]])
board.make_move([chb.convertPositionToAI('a3'), chb.convertPositionToAI('b4')])
print(chb.convertPositionFromAI([3, 1]))
chb.prettyPrintBoard(chb.convertStateFromAI(board.spots))
print(chb.convertPositionFromAI([5, 3]))
board.make_move([[5, 3], [4, 3]])
chb.prettyPrintBoard(chb.convertStateFromAI(board.spots))
board.make_move([[2, 1], [1, 0]])
chb.prettyPrintBoard(chb.convertStateFromAI(board.spots))
# board.print_board()
nextMove = alpha_beta_ai.get_next_move()
for nextM in nextMove:
    print(chb.convertPositionFromAI(nextM))
print("Player Turn: ", board.player_turn)
captured = board.make_move(nextMove)
for capture in captured:
    print("Captured: ", chb.convertPositionFromAI(capture))

chb.gameState = chb.convertStateFromAI(board.spots)
chb.prettyPrintBoard()


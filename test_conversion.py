from CheckersReinforcementLearning.Board import Board
from CheckersReinforcementLearning.AI import Alpha_beta
from Chessboard import Chessboard
import cv2
from matplotlib import pyplot as plt
import numpy as np

chb = Chessboard.Chessboard()

img = cv2.imread("./img/checkers_scanner_pieces_2.jpg")

gameState = chb.detectGameState(img)

chb.prettyPrintBoard()

board = Board(chb.convertStateToAI())
board.print_board()
print("================")

alpha_beta_ai = Alpha_beta(False, 6)
alpha_beta_ai.set_board(board)

print("Player Turn: ", board.player_turn)
board.make_move([[2, 0], [3, 0]])
chb.prettyPrintBoard(chb.convertStateFromAI(board.spots))
board.make_move([[5, 3], [4, 3]])
chb.prettyPrintBoard(chb.convertStateFromAI(board.spots))
board.make_move([[2, 1], [1, 0]])
chb.prettyPrintBoard(chb.convertStateFromAI(board.spots))
board.print_board()
print("================")
nextMove = alpha_beta_ai.get_next_move()
print(nextMove)
print("Player Turn: ", board.player_turn)
captured = board.make_move(nextMove)
print("Captured: ", captured)
print("================")

chb.gameState = chb.convertStateFromAI(board.spots)
chb.prettyPrintBoard()


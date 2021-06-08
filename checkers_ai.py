from CheckersReinforcementLearning.Board import Board
from CheckersReinforcementLearning.AI import Alpha_beta
from Chessboard import Chessboard
import cv2
from matplotlib import pyplot as plt
import numpy as np

chb = Chessboard.Chessboard()

img = cv2.imread("./img/checkers_scanner_pieces_2.jpg")

gameState = chb.detectGameState(img)

boardKeys = list(gameState.keys())
boardValues = list(gameState.values())

print(gameState)
listed = list(gameState.values())
print(listed)

reshaped = np.reshape(listed, (8, 4))
print(reshaped)
odd = reshaped[::2]
even = reshaped[1:8:2]
final = []
for i in range(4):
    final.append(odd[:, i])
    final.append(even[:, i])

print(final)

# Pretty print board
for i in range(0, len(boardKeys), 8):
    print(boardKeys[i][0].capitalize(), "[" + "] [".join(str(e) for e in boardValues[i:i + 8]).replace("0", " ") + "]")
print("# ", "   ".join(str(e) for e in range(1, 9)), )
old_spots = [[1, 4, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 2, 2], [2, 2, 2, 2],
             [2, 2, 2, 2]]

board = Board(old_spots=final)

print(board.spots)

board.print_board()
print("================")
# Make sure some Board methods don't alter the board
alpha_beta_ai = Alpha_beta(False, 6)
alpha_beta_ai.set_board(board)
print("Player Turn: ", board.player_turn)
board.make_move([[2, 0], [3, 0]])
board.make_move([[5, 3], [4, 3]])
board.make_move([[2, 1], [1, 0]])
board.print_board()
print("================")
nextMove = alpha_beta_ai.get_next_move()
print(nextMove)
print("Player Turn: ", board.player_turn)
captured = board.make_move(nextMove)
print("Captured: ", captured)
print("================")
print("Player Turn: ", board.player_turn)
board.make_move([[1, 2], [2, 2]])
board.print_board()
print("================")
nextMove = alpha_beta_ai.get_next_move()
print(nextMove)
print("Player Turn: ", board.player_turn)
captured = board.make_move(nextMove)
print("captured: ", captured)
board.print_board()
print("================")
alpha_beta_ai.get_next_move()
board.make_move([[2, 2], [3, 1]])
board.make_move([[1, 0], [2, 0]])
alpha_beta_ai.get_next_move()
board.make_move([[0, 1], [1, 0]])
board.make_move([[4, 1], [2, 2], [0, 1]])
alpha_beta_ai.get_next_move()
board.make_move([[5, 1], [4, 1]])
board.make_move([[3, 0], [5, 1]])
alpha_beta_ai.get_next_move()
print("==================")
# board.print_board()

# if board.spots == old_spots:
#     print("All tests passed.")
# else:
#     print("Test failed.")
#     print_test_results([board.spots], [old_spots])
#
import Chessboard
import cv2
from matplotlib import pyplot as plt
import numpy as np

chb = Chessboard.Chessboard()

img = cv2.imread("./img/checkers_scanner_pieces_2.jpg")

gameState = chb.detectGameState(img)

print(gameState)

boardKeys = list(gameState.keys())
boardValues = list(gameState.values())

# Pretty print board
for i in range(0, len(boardKeys), 8):
    print(boardKeys[i][0].capitalize(), "[" + "] [".join(str(e) for e in boardValues[i:i+8]) + "]")
print("# ", "   ".join(str(e) for e in range(1, 9)), )
from DobotAPI.Dobot import Dobot
from Chessboard.Chessboard import Chessboard
from CheckersReinforcementLearning.Board import Board
from CheckersReinforcementLearning.AI import Alpha_beta
from DobotCamera import DobotCamera
from DobotCheckers import DobotCheckers
import numpy as np
import time
import cv2
import helpers

dobot = Dobot(homeX=220, homeY=0, homeZ=-6.5)
zUpValue = None
zDownValue = None
releaseX = None
releaseY = None

dobotCam = DobotCamera(
    xDobRefPoint=150.75,
    yDobRefPoint=-64.8,
    xCamRefPoint=56,
    yCamRefPoint=51,
    xScaleFactor=0.68,
    yScaleFactor=0.645
)

chessboard = Chessboard()

dobotCheckers = DobotCheckers(
    chessboard,
    dobot,
    dobotCam,
    zDownValue,
    zUpValue,
    releaseX,
    releaseY
)

# img = helpers.captureBoard()
img = cv2.imread("./img/checkers_scanner_pieces_2.jpg")

chessboard.detectGameState(img)

chessboard.prettyPrintBoard()

AIBoard = Board(chessboard.convertStateToAI(), the_player_turn=False)

alphaBetaAI = Alpha_beta(False, 6)
alphaBetaAI.set_board(AIBoard)

# playerTurn = False
# while not AIBoard.is_game_over():
#     if not playerTurn:

# Get moves from AI
nextMove = alphaBetaAI.get_next_move()

captured = AIBoard.make_move(nextMove)

dobotCheckers.grab(nextMove[0])

dobotCheckers.release(nextMove[-1])


if len(captured) > 0:
    dobotCheckers.capture(captured)

dobot.moveHome()
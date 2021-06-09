from DobotAPI.Dobot import Dobot
from Chessboard.Chessboard import Chessboard
from CheckersReinforcementLearning.Board import Board
from CheckersReinforcementLearning.AI import Alpha_beta
from DobotCamera import DobotCamera
import numpy as np
import time
import cv2
import helpers


dobot = Dobot(homeX=220, homeY=0, homeZ=-6.5)

dobotCam = DobotCamera(
    xDobRefPoint=150.75,
    yDobRefPoint=-64.8,
    xCamRefPoint=56,
    yCamRefPoint=51,
    xScaleFactor=0.68,
    yScaleFactor=0.645
)

chessboard = Chessboard()

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

# Convert position from AI coordinates to Chessboard position (ex. 'a1')
fromPosition = chessboard.convertPositionFromAI(nextMove[0])

# Get piece image coordinates inside specified position
pieceCoordinates = chessboard.pieceCoordinateInsidePos[fromPosition]

# Convert piece image coordinates to dobot coordinates
dobotCoordinates = dobotCam.convertCameraToDobot(pieceCoordinates)

dobot.moveXY(dobotCoordinates[0], dobotCoordinates[1])
# TODO MoveDown and GrabPiece

# Make move
for i in range(1, len(nextMove)):
    toPosition = chessboard.convertPositionFromAI(nextMove[i])
    dobotCoordinates = dobotCam.convertCameraToDobot(chessboard.boardPositionsCenter[toPosition])
    dobot.moveXY(dobotCoordinates[0], dobotCoordinates[1])
# TODO MoveDown and ReleasePiece

# Remove captured pieces
for i in range(len(captured)):
    toRemovePosition = chessboard.convertPositionFromAI(captured[i])
    pieceCoordinates = chessboard.pieceCoordinateInsidePos[toRemovePosition]
    dobotCoordinates = dobotCam.convertCameraToDobot(pieceCoordinates)
    dobot.moveXY(dobotCoordinates[0], dobotCoordinates[1])
    # TODO MoveDown and GrabPiece
    # TODO GoUp and MovePiece outside the board
    # TODO ReleasePeace

# TODO GoHome (away from camera)

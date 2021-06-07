import cv2
import numpy as np


def getROIavgColor(frame, x, y, r):
    roi_values = frame[int(y - r / 2):int(y + r / 2), int(x - r / 2):int(x + r / 2)]
    avg = (np.mean(roi_values[:, :, 0]) + np.mean(roi_values[:, :, 1]) + np.mean(roi_values[:, :, 2])) / 3
    return avg


def detectBoardCorners(img):
    boardDimension = (7, 7)
    retval, corners = cv2.findChessboardCorners(img, boardDimension, 0, 0)
    if retval:
        print("Board detected!")
        return corners
    else:
        print("Board not detected!")
        return None


def pointInCircle(point, circle, radius):
    # ((pointX - circleX)**2 + (pointY - circleY)**2) < radius**2
    return ((point[0] - circle[0]) ** 2 + (point[1] - circle[1]) ** 2) < radius ** 2


class Chessboard:
    WHITE = 2
    BLACK = 1
    WHITE_KING = 3
    BLACK_KING = 4

    def __init__(self):
        # gameState is a dictionary with coordinates {"a1": "", ... "b2": ""}
        # or        [[0, 1, 0, 1, 0, 1, 0, 1],
        # 			[1, 0, 1, 0, 1, 0, 1, 0],
        # 			[0, 1, 0, 1, 0, 1, 0, 1],
        # 			[0, 0, 0, 0, 0, 0, 0, 0],
        # 			[0, 0, 0, 0, 0, 0, 0, 0],
        # 			[-1, 0, -1, 0, -1, 0, -1, 0],
        # 			[0, -1, 0, -1, 0, -1, 0, -1],
        # 			[-1, 0, -1, 0, -1, 0, -1, 0]]
        self.gameState = {}
        self.boardPositionsCenter = {}
        self.pieces = {
            "black": [],
            "white": []
        }
        self.initializeBoardPositions()

    def initializeBoardPositions(self):
        board = {}
        letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
        numbers = [1, 2, 3, 4, 5, 6, 7, 8]
        for letter in letters:
            for number in numbers:
                board[letter + str(number)] = 0
        self.boardPositionsCenter = board.copy()
        self.gameState = board.copy()

    def detectPieces(self, img):
        img = cv2.medianBlur(img, 5)

        height, width = img.shape[:2]
        maxRadius = int(0.1 * width)
        minRadius = int(0.02 * width)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(image=gray,
                                   method=cv2.HOUGH_GRADIENT,
                                   dp=1.5,
                                   minDist=maxRadius,
                                   param1=45,
                                   param2=40,
                                   minRadius=minRadius,
                                   maxRadius=maxRadius)

        self.pieces = {
            "black": [],
            "white": []
        }
        if circles is not None:
            circlesRound = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circlesRound:
                avg = getROIavgColor(img, x, y, r)
                if avg >= 140:
                    self.pieces["white"].append((x, y))
                else:
                    self.pieces["black"].append((x, y))
        else:
            print('No circles found')
        return self.pieces

    def getNextEmptyPos(self, skipPositions=0):
        boardKeys = list(self.boardPositionsCenter.keys())
        for i in range(len(boardKeys)):
            if (self.boardPositionsCenter[boardKeys[i]]) == 0:
                return boardKeys[i + skipPositions]

    def appendPosition(self, x, y, pos):
        self.boardPositionsCenter[pos] = [x, y]

    def detectBoard(self, img):
        corners = detectBoardCorners(img)
        for i in range(len(corners)):
            x, y = corners[i][0][0], corners[i][0][1]
            self.appendPosition(round(x - 22), round(y - 22), self.getNextEmptyPos())

            if ((i + 1) % 7) == 0:
                self.appendPosition(round(x + 22), round(y - 22), self.getNextEmptyPos())
            elif i >= 42:
                self.appendPosition(round(x - 22), round(y + 22), self.getNextEmptyPos(7))

            if i == 48:
                self.appendPosition(round(x - 22), round(y + 22), self.getNextEmptyPos())
                self.appendPosition(round(x + 22), round(y + 22), self.getNextEmptyPos())

    def detectGameState(self, img):
        self.detectBoard(img)
        self.detectPieces(img)
        boardKeys = list(self.boardPositionsCenter.keys())
        for boardKey in boardKeys:
            position = self.boardPositionsCenter[boardKey]
            for blackPiece in self.pieces["black"]:
                if pointInCircle(position, blackPiece, 6):
                    self.gameState[boardKey] = self.BLACK

            for whitePiece in self.pieces["white"]:
                if pointInCircle(position, whitePiece, 6):
                    self.gameState[boardKey] = self.WHITE

        return self.gameState

    def getPiecePositionOnBoard(self, x, y):
        boardKeys = list(self.boardPositionsCenter.keys())
        for boardKey in boardKeys:
            if pointInCircle(self.boardPositionsCenter[boardKey], (x, y), 6):
                return boardKey

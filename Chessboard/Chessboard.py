import cv2
import numpy as np
import matplotlib.pyplot as plt


def getROIavgColor(frame, x, y, r):
    roi_values = frame[int(y - r / 2):int(y + r / 2), int(x - r / 2):int(x + r / 2)]
    avg = (np.mean(roi_values[:, :, 0]) + np.mean(roi_values[:, :, 1]) + np.mean(roi_values[:, :, 2])) / 3
    return avg


def detectBoardCorners(img):
    boardDimension = (7, 7)
    plt.imshow(img)
    plt.show()
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
    WHITE_KING = 4
    BLACK_KING = 3
    EMPTY = 0

    def __init__(self):
        self.gameState = {}
        self.boardPositionsCenter = {}
        self.pieceCoordinateInsidePos = {}
        self.pieces = {
            "black": [],
            "white": []
        }
        self.initializeBoardPositions()

    def initializeBoardPositions(self):
        board = {}
        letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
        numbers = [1, 2, 3, 4, 5, 6, 7, 8]
        lastLetter = letters[0]
        i = 0
        for letter in letters:
            if letter != lastLetter:
                lastLetter = letter
                i = i + 1
            for number in numbers:
                if i % 2 == 0:
                    if (number % 2) == 0:
                        continue
                else:
                    if (number % 2) > 0:
                        continue
                board[letter + str(number)] = self.EMPTY
        self.boardPositionsCenter = board.copy()
        self.gameState = board.copy()
        self.pieceCoordinateInsidePos = board.copy()

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

        if circles is not None:
            circlesRound = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circlesRound:
                avg = getROIavgColor(img, x, y, r)
                if avg >= 130:
                    self.pieces["white"].append((x, y))
                else:
                    self.pieces["black"].append((x, y))
        else:
            print('No circles found')
        return self.pieces

    def getNextEmptyPos(self, skipPositions=0):
        boardKeys = list(self.boardPositionsCenter.keys())
        for i in range(len(boardKeys)):
            if (self.boardPositionsCenter[boardKeys[i]]) == self.EMPTY:
                return boardKeys[i + skipPositions]

    def appendPosition(self, x, y, pos):
        self.boardPositionsCenter[pos] = [x, y]

    def detectBoard(self, img):
        corners = detectBoardCorners(img)
        if corners is None:
            return False
        for i in range(len(corners)):
            x, y = corners[i][0][0], corners[i][0][1]
            if i % 2 == 0:
                self.appendPosition(round(x - 22), round(y - 22), self.getNextEmptyPos())
                if (i >= 42) & (i < 48):
                    self.appendPosition(round(x + 22), round(y + 22), self.getNextEmptyPos(3))
                if i == 48:
                    self.appendPosition(round(x + 22), round(y + 22), self.getNextEmptyPos())
            else:
                if (i + 1) % 7 == 0:
                    self.appendPosition(round(x + 22), round(y - 22), self.getNextEmptyPos())
        return True

    def detectGameState(self, img):
        boardDetected = self.detectBoard(img)
        if boardDetected is False:
            return False
        self.detectPieces(img)
        boardKeys = list(self.boardPositionsCenter.keys())
        for boardKey in boardKeys:
            position = self.boardPositionsCenter[boardKey]
            for blackPiece in self.pieces["black"]:
                if pointInCircle(position, blackPiece, 6):
                    self.gameState[boardKey] = self.BLACK
                    self.pieceCoordinateInsidePos[boardKey] = blackPiece
                    continue

            for whitePiece in self.pieces["white"]:
                if pointInCircle(position, whitePiece, 6):
                    self.gameState[boardKey] = self.WHITE
                    self.pieceCoordinateInsidePos[boardKey] = whitePiece
                    continue

        return self.gameState

    def getPiecePositionOnBoard(self, x, y):
        boardKeys = list(self.boardPositionsCenter.keys())
        for boardKey in boardKeys:
            if pointInCircle(self.boardPositionsCenter[boardKey], (x, y), 6):
                return boardKey

    def convertStateToAI(self, keys=False):
        if keys:
            boardValues = list(self.gameState.keys())
        else:
            boardValues = list(self.gameState.values())
        reshaped = np.reshape(boardValues, (8, 4))
        odd = reshaped[::2]
        even = reshaped[1:8:2]
        AIBoard = []
        for i in range(4):
            AIBoard.append(odd[:, i])
            AIBoard.append(even[:, i])
        return AIBoard

    def convertStateFromAI(self, AIBoard):
        odd = np.array(AIBoard[::2])
        even = np.array(AIBoard[1:8:2])
        final = []
        for i in range(4):
            final.append(odd[:, i])
            final.append(even[:, i])
        final = np.array(final).flatten()
        converted = self.gameState.copy()
        convertedKeys = list(converted.keys())
        for i in range(len(final)):
            converted[convertedKeys[i]] = final[i]
        return converted

    def convertPositionFromAI(self, position):
        boardKeys = list(self.gameState.keys())
        mapping = {1: 4, 3: 5, 5: 6, 7: 7}
        if position[0] % 2 == 0:
            pos = int(position[0] / 2)
        else:
            pos = mapping[position[0]]
        return boardKeys[pos + (position[1] * 8)]

    def convertPositionToAI(self, position):
        AIBoard = self.convertStateToAI(keys=True)
        AIBoard = np.array(AIBoard)
        return np.array(np.where(AIBoard == position)).flatten()

    def prettyPrintBoard(self, gameState=None):
        if gameState is None:
            gameState = self.gameState

        board = {}
        letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
        numbers = [1, 2, 3, 4, 5, 6, 7, 8]
        for letter in letters:
            for number in numbers:
                pos = letter + str(number)
                if pos in gameState:
                    board[pos] = gameState[pos]
                else:
                    board[pos] = self.EMPTY

        boardKeys = list(board.keys())
        boardValues = list(board.values())
        # print("=================================")
        for i in range(0, len(boardKeys), 8):
            print(boardKeys[i][0].capitalize(),
                  "[" + "] [".join(str(e) for e in boardValues[i:i + 8]).replace("0", " ") + "]")
        print("# ", "   ".join(str(e) for e in range(1, 9)))
        # print("=================================")



class DobotCheckers:
    def __init__(self, chessboard, dobot, dobotCamera, zDownValue, zUpValue, releaseX, releaseY):
        self.chessboard = chessboard
        self.dobot = dobot
        self.dobotCamera = dobotCamera
        self.zDownValue = zDownValue
        self.zUpValue = zUpValue
        self.releaseX = releaseX
        self.releaseY = releaseY

    def makeMove(self, position, suction):
        dobotCoordinates = self.convertPosToDobot(position)
        self.dobot.move(dobotCoordinates[0], dobotCoordinates[1])  # Move to specified coordinates
        self.dobot.move(self.dobot.x, self.dobot.y, self.zDownValue)  # MoveDown
        self.dobot.setSuction(suction)  # GrabPiece
        self.dobot.move(self.dobot.x, self.dobot.y, self.zUpValue)  # MoveUP

    def grab(self, position):
        self.makeMove(position, True)

    def release(self, position):
        self.makeMove(position, False)

    def capture(self, positions):
        for position in positions:
            self.makeMove(position, True)
            self.dobot.move(self.releaseX, self.releaseY)
            self.dobot.setSuction(False)

    def convertPosToDobot(self, position):
        # Convert position from AI coordinates to Chessboard position (ex. 'a1')
        fromPosition = self.chessboard.convertPositionFromAI(position)

        # Get piece image coordinates inside specified position
        pieceCoordinates = self.chessboard.pieceCoordinateInsidePos[fromPosition]

        # Convert piece image coordinates to dobot coordinates
        return self.dobotCamera.convertCameraToDobot(pieceCoordinates)

from DobotAPI import Dobot as Dbt
import time

zPiece = -38

xDobRefPoint = 150.75
yDobRefPoint = -64.8
xCamRefPoint = 56
yCamRefPoint = 51

xScaleFactor = 0.68
yScaleFactor = 0.645

releaseX = 64
releaseY = 142

xCamPiece = 370 - 71
yCamPiece = 257


xDobPiece = xDobRefPoint + ((xCamPiece - xCamRefPoint) * xScaleFactor)
yDobPiece = yDobRefPoint + ((yCamPiece - yCamRefPoint) * yScaleFactor)

dbt = Dbt.Dobot(220, 0, -6.5)
dbt.move(releaseX, releaseY)

# dbt.move(xDobPiece, yDobPiece)
# dbt.setSuction(True)
#
# time.sleep(1)
# dbt.setSuction(False)


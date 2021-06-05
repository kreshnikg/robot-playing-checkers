import Dobot as Dbt
import time

zPiece = -38

xDobRefPoint = 150.75
yDobRefPoint = -64.8
xCamRefPoint = 56
yCamRefPoint = 51

xScaleFactor = 0.68
yScaleFactor = 0.645

xCamPiece = 370 - 71
yCamPiece = 257

xDobPiece = xDobRefPoint + ((xCamPiece - xCamRefPoint) * xScaleFactor)
yDobPiece = yDobRefPoint + ((yCamPiece - yCamRefPoint) * yScaleFactor)

dbt = Dbt.Dobot(220, 0, -6.5)

dbt.moveXY(xDobPiece, yDobPiece)
dbt.toggleSuction()

time.sleep(1)
dbt.toggleSuction()


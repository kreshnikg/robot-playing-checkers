from DobotAPI.Dobot import Dobot
from Chessboard import Chessboard
import cv2
from matplotlib import pyplot as plt
import numpy as np


class DobotCamera:

    def __init__(self, xDobRefPoint, yDobRefPoint, xCamRefPoint,
                 yCamRefPoint, xScaleFactor, yScaleFactor, camWidth, camHeight):
        self.X_DOB_REF_POINT = xDobRefPoint
        self.Y_DOB_REF_POINT = yDobRefPoint
        self.X_CAM_REF_POINT = xCamRefPoint
        self.Y_CAM_REF_POINT = yCamRefPoint

        self.X_SCALE_FACTOR = xScaleFactor
        self.Y_SCALE_FACTOR = yScaleFactor

        self.CAM_WIDTH = camWidth
        self.CAM_HEIGHT = camHeight

    def convertCameraToDobot(self, point, camRefPoint, dobRefPoint):
        return (
                dobRefPoint[0] + ((point[0] - camRefPoint[0]) * self.X_SCALE_FACTOR),
                dobRefPoint[1] + ((point[1] - camRefPoint[1]) * self.Y_SCALE_FACTOR)
        )

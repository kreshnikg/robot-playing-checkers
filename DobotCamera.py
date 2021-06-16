

class DobotCamera:

    def __init__(self, xDobRefPoint, yDobRefPoint, xCamRefPoint,
                 yCamRefPoint, xScaleFactor, yScaleFactor):
        self.X_DOB_REF_POINT = xDobRefPoint
        self.Y_DOB_REF_POINT = yDobRefPoint

        self.X_CAM_REF_POINT = xCamRefPoint
        self.Y_CAM_REF_POINT = yCamRefPoint

        self.X_SCALE_FACTOR = xScaleFactor
        self.Y_SCALE_FACTOR = yScaleFactor

    def convertCameraToDobot(self, point):
        return (
                self.X_DOB_REF_POINT + ((370 - point[0] - self.X_CAM_REF_POINT) * self.X_SCALE_FACTOR),
                self.Y_DOB_REF_POINT + ((point[1] - self.Y_CAM_REF_POINT) * self.Y_SCALE_FACTOR)
        )

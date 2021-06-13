from DobotAPI import DobotDllType as dType

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError: "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"
}


class Dobot:
    def __init__(self, homeX, homeY, homeZ):
        self.api = dType.load()
        self.homeX = homeX
        self.homeY = homeY
        self.homeZ = homeZ
        self.x = None
        self.y = None
        self.z = None
        self.suctionEnabled = False
        self.connected = False
        self.dobotConnect()

    def __del__(self):
        self.dobotDisconnect()

    def dobotConnect(self):
        if self.connected:
            print("Dobot is already connected")
        else:
            state = dType.ConnectDobot(self.api, "", 115200)[0]
            print("Connect status:", CON_STR[state])
            if state == dType.DobotConnect.DobotConnect_NoError:
                dType.SetQueuedCmdClear(self.api)
                self.initParams()
                self.connected = True

    def initParams(self):
        dType.SetPTPJointParams(self.api, 200, 200, 200, 200, 200, 200, 200, 200, 0)
        dType.SetPTPCoordinateParams(self.api, 200, 200, 200, 200, 0)
        dType.SetPTPJumpParams(self.api, 10, 200, 0)
        dType.SetPTPCommonParams(self.api, 100, 100, 0)
        dType.SetHOMEParams(self.api, self.homeX, self.homeY, self.homeZ, 0, isQueued=0)
        currentPosition = self.getPosition()
        self.x = currentPosition[0]
        self.y = currentPosition[1]
        self.z = currentPosition[2]

    def dobotDisconnect(self):
        self.moveHome()
        dType.DisconnectDobot(self.api)

    def move(self, x, y, z=None):
        if z is None:
            z = self.z
        dType.SetPTPCmdEx(self.api, dType.PTPMode.PTPMOVLXYZMode, x, y, z, 0, isQueued=1)
        self.x = x
        self.y = y
        self.z = z

    def setSuction(self, enabled):
        status = 1 if enabled else 0
        dType.SetEndEffectorSuctionCup(self.api, status, status)
        self.suctionEnabled = enabled

    def getPosition(self):
        return dType.GetPose(self.api)

    def moveHome(self):
        dType.SetHOMECmdEx(self.api, 0)

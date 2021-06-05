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

    def dobotDisconnect(self):
        self.moveHome()
        dType.DisconnectDobot(self.api)

    def moveXY(self, x, y):
        dType.SetPTPCmdEx(self.api, dType.PTPMode.PTPMOVLXYZMode, x, y, self.homeZ, 0, isQueued=1)

    def toggleSuction(self):
        # TODO get suctionEnabled from API
        if self.suctionEnabled:
            dType.SetEndEffectorSuctionCup(self.api, 0, 0)
            self.suctionEnabled = False
        else:
            dType.SetEndEffectorSuctionCup(self.api, 1, 1)
            self.suctionEnabled = True

    def getPosition(self):
        return dType.GetPose(self.api)

    def moveHome(self):
        dType.SetHOMECmdEx(self.api, 0)
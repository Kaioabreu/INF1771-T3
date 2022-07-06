from Map.Position import Position
class Gamemap():   
    width = 34
    heigth = 59
    goldPos = []
    voidPos = []
    powerupPos = []
    blockedPos = []
    afePos = []
    UnsafePos = []
    
    def addPosition(self,type, Position):
        if type == "gold":
            self.goldPos.append(Position)
        elif type == "void":
            self.voidPos.append(Position)
        elif type == "block":
            self.blockedPos.append(Position)
        elif type == "powerup":
            self.powerupPos.append(Position)
    
    def getGoldPos(self):
        return self.goldPos

    def getVoidPos(self):
        return self.voidPos

    def getBlockedPos(self):
        return self.blockedPos
    
    def getPowerupPos(self):
        return self.powerupPos
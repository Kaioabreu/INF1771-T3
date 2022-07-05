class Gamemap():   
    width = 34
    heigth = 59
    goldPos = []
    voidPos = []
    blockedPos = []
    
    def addPosition(self,type, x, y):
        if type == "gold":
            self.goldPos.append((x,y))
        elif type == "void":
            self.voidPos.append((x,y))
        elif type == "block":
            self.blockedPos.append((x,y))
    
    def getGoldPos(self):
        return self.goldPos

    def getVoidPos(self):
        return self.voidPos

    def getBlockedPos(self):
        return self.blockedPos
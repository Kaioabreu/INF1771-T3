from platform import node
from Map.Position import Position

class Gamemap():   
    width = 34
    heigth = 59
    goldPos = []
    voidPos = []
    powerupPos = []
    blockedPos = []
    safePos = []
    unsafePos = []
    notVisit = []
    
    def addPosition(self,type, x,y):
        if type == "gold":
            self.goldPos.append((x,y))
        elif type == "unsafe":
            self.unsafePos.append((x,y))
        elif type == "block":
            self.blockedPos.append((x,y))
        elif type == "powerup":
            self.powerupPos.append((x,y))
    def __init__(self):
        for i in range(self.heigth):
            for j in range(self.width):
                self.notVisit.append((i,j))
        

    def getGoldPos(self):
        return self.goldPos

    def getVoidPos(self):
        return self.voidPos

    def getBlockedPos(self):
        return self.blockedPos
    
    def getPowerupPos(self):
        return self.powerupPos
    
    def getUnsafePos(self):
        return self.unsafePos
    def getNotVisit(self):
        return self.notVisit
#Seria bom ajustar essa função futuramente
    def nodeCost(self,x,y):
        if(self.isBadPos(x,y)):
            return 50
        return 1

    def getVizinhos(self,x,y,cost,xf,yf):
        ret = []

        ret.append(x-1,y,cost+self.nodeCost(x-1,y),self.manhattan(x-1,y,xf,yf))
        ret.append(x+1,y,cost+self.nodeCost(x+1,y),self.manhattan(x+1,y,xf,yf))
        ret.append(x,y+1,cost+self.nodeCost(x,y+1),self.manhattan(x,y+1,xf,yf))
        ret.append(x,y-1,cost+self.nodeCost(x,y-1),self.manhattan(x,y-1,xf,yf))

        return ret

    def isBadPos(self,x,y):
        return ((x,y) in self.getBlockedPos() or (x,y) in self.getUnsafePos())

    def manhattan(x1,y1,x2,y2):
        return abs(x1-x2)+abs(y1-y2)
    
    #A* funciona dando como parametro as coordenadas iniciais, e depois as coordenadas finais, os pesos e custos estão na funçao nodeCost(não deu tempo de fazer direito).

    def aStar(self,xi,yi,xf,yf):
        aberta=[]
        fechada=[]
        initialNode = Node(xi,yi,0,xf,yf)
        aberta.append(initialNode)
        current = initialNode
        while aberta:
            current = pegaMenor(aberta)
            if (current.x == xf and current.y == yf):
                return current.getPath()
            aberta.remove(current)
            fechada.append(current)
            vizinhos = current.getVizinhos()
            for nextNode in vizinhos:

                inFechada = False
                inAberta = False
                for i in fechada:
                    if(nextNode.x == i.x and nextNode.y == i.y):
                        inFechada = True
                if(not(inFechada)):
                    for i in aberta:
                        if(nextNode.x == i.x and nextNode.y == i.y):
                            inAberta = True
                            if(nextNode.f<i.f):
                                i.f=nextNode.f
                                nextNode.partner = current
                    if(inAberta==False):
                        aberta.append(nextNode)
                        nextNode.partner = current
        print("Caminho não encontrado")
        return None

def pegaMenor(lista):
    menor = lista[0]
    for i in lista[1:]:
        if menor.f > i.f:
            menor = i
    return menor
class Node:
    def __init__(self,x,y,g,xf,yf):
        self.x=x
        self.y=y
        self.xf = xf
        self.yf = yf
        self.h=self.manhattan(xf,yf)
        self.g=g
        self.f = self.g + self.h
        self.partner = None
        self.gamemap = Gamemap()
    
    def manhattan(self,xf,yf):
        return abs(self.x-xf)+abs(self.y-yf)
    
    def isValid(self,x,y):
        return(x>=0 and x<=self.gamemap.heigth and y>=0 and y<=self.gamemap.width) 

    def getVizinhos(self):

        ret = []
        if (self.isValid(self.x-1,self.y)):
            ret.append(Node(self.x-1,self.y,self.g+self.gamemap.nodeCost(self.x-1,self.y),self.xf,self.yf))
        if (self.isValid(self.x+1,self.y)):
            ret.append(Node(self.x+1,self.y,self.g+self.gamemap.nodeCost(self.x+1,self.y),self.xf,self.yf))
        if (self.isValid(self.x,self.y+1)):
            ret.append(Node(self.x,self.y+1,self.g+self.gamemap.nodeCost(self.x,self.y+1),self.xf,self.yf))
        if (self.isValid(self.x,self.y-1)):
            ret.append(Node(self.x,self.y-1,self.g+self.gamemap.nodeCost(self.x,self.y-1),self.xf,self.yf))
        return ret
    def getPath(self):
        temp=self
        pathList = list()
        while(temp.partner!=None):
            pathList.append(temp)
            temp=temp.partner
        return pathList[::-1]
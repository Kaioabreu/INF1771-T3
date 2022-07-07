﻿#!/usr/bin/env python

"""GameAI.py: INF1771 GameAI File - Where Decisions are made."""
#############################################################
#Copyright 2020 Augusto Baffa
#
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#############################################################
__author__      = "Augusto Baffa"
__copyright__   = "Copyright 2020, Rio de janeiro, Brazil"
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "abaffa@inf.puc-rio.br"
#############################################################

import random
from Map.Position import Position
from Gamemap import Gamemap, Node

# <summary>
# Game AI Example
# </summary>
class GameAI():

    player = Position()
    state = "ready"
    dir = "north"
    score = 0
    energy = 0
    status = []
    contEvent = 0
    proxEvento = []
    gamemap = Gamemap()
    tempBlock = []
    xObj = 0 
    yObj = 0
    #currentAction = "goldpath"

    # <summary>
    # Refresh player status
    # </summary>
    # <param name="x">player position x</param>
    # <param name="y">player position y</param>
    # <param name="dir">player direction</param>
    # <param name="state">player state</param>
    # <param name="score">player score</param>
    # <param name="energy">player energy</param>
    def SetStatus(self, x, y, dir, state, score, energy):
    
        self.player.x = x
        self.player.y = y
        self.dir = dir.lower()

        self.state = state
        self.score = score
        self.energy = energy


    # <summary>
    # Get list of observable adjacent positions
    # </summary>
    # <returns>List of observable adjacent positions</returns>
    def GetObservableAdjacentPositions(self):
        ret = []

        ret.append(Position(self.player.x - 1, self.player.y))
        ret.append(Position(self.player.x + 1, self.player.y))
        ret.append(Position(self.player.x, self.player.y - 1))
        ret.append(Position(self.player.x, self.player.y + 1))

        return ret


    # <summary>
    # Get list of all adjacent positions (including diagonal)
    # </summary>
    # <returns>List of all adjacent positions (including diagonal)</returns>
    def GetAllAdjacentPositions(self):
    
        ret = []

        ret.Add(Position(self.player.x - 1, self.player.y - 1))
        ret.Add(Position(self.player.x, self.player.y - 1))
        ret.Add(Position(self.player.x + 1, self.player.y - 1))

        ret.Add(Position(self.player.x - 1, self.player.y))
        ret.Add(Position(self.player.x + 1, self.player.y))

        ret.Add(Position(self.player.x - 1, self.player.y + 1))
        ret.Add(Position(self.player.x, self.player.y + 1))
        ret.Add(Position(self.player.x + 1, self.player.y + 1))

        return ret
    

    # <summary>
    # Get next forward position
    # </summary>
    # <returns>next forward position</returns>
    def NextPosition(self):
    
        ret = None
        
        if self.dir == "north":
            ret = Position(self.player.x, self.player.y - 1)
                
        elif self.dir == "east":
                ret = Position(self.player.x + 1, self.player.y)
                
        elif self.dir == "south":
                ret = Position(self.player.x, self.player.y + 1)
                
        elif self.dir == "west":
                ret = Position(self.player.x - 1, self.player.y)

        return ret
    

    # <summary>
    # Player position
    # </summary>
    # <returns>player position</returns>
    def GetPlayerPosition(self):
        return self.player


    # <summary>
    # Set player position
    # </summary>
    # <param name="x">x position</param>
    # <param name="y">y position</param>
    def SetPlayerPosition(self, x, y):
        self.player.x = x
        self.player.y = y

    

    # <summary>
    # Observations received
    # </summary>
    # <param name="o">list of observations</param>
    def GetObservations(self, o):

        #cmd = "";
        for s in o:
        
            if s == "blocked" or s == "steps" or s == "breeze" or s == "blueLight" or s =="redLight" or s[:6]=="enemy#":
                self.status.append(s)
                if s == "blueLight":
                    self.proxEvento.insert(0,"pegar")
                    if(not (self.player.x, self.player.y) in self.gamemap.getGoldPos()):
                        self.gamemap.addPosition("gold",self.player.x, self.player.y)
                        
                elif s == "redLight":
                    if(not (self.player.x, self.player.y) in self.gamemap.getPowerupPos()):
                        self.gamemap.addPosition("powerup", self.player.x, self.player.y)
                elif s == "breeze" or s == "flash":
                    self.proxEvento = []
                    coords = (self.xObj,self.yObj)
                    if (coords in self.gamemap.getGoldPos() or coords in self.gamemap.getPowerupPos()):
                        a = self.gamemap.aStar(self.player.x,self.player.y,self.xObj,self.yObj)
                        self.convertPathToCommands(a)
                elif s == "blocked":
                    self.GetObservationsClean()
                    if(not (self.NextPosition().x,self.NextPosition().y) in self.gamemap.getBlockedPos()):
                        self.gamemap.addPosition("block", self.NextPosition().x,self.NextPosition().y)
                        self.proxEvento = []
                        coords = (self.xObj,self.yObj)
                        if (coords in self.gamemap.getGoldPos() or coords in self.gamemap.getPowerupPos()):
                            a = self.gamemap.aStar(self.player.x,self.player.y,self.xObj,self.yObj)
                            self.convertPathToCommands(a)
                        #for i in self.gamemap.getBlockedPos():
                        #print(self.gamemap.getBlockedPos())

                elif s[:6] == "enemy#":
                    self.proxEvento.insert(0,"atacar")

    # <summary>
    # No observations received
    # </summary>
    def GetObservationsClean(self):
        self.status = []

    def isValidFoward(self):
        d = self.dir
        p = self.player
        if ((d == "north" and p.y == 0) or (d =="west" and p.x == 0) or (d == "east" and p.x == self.gamemap.heigth-1) or (d == "south" and p.y == self.gamemap.width-1) or self.gamemap.isBadPos(self.NextPosition().x,self.NextPosition().y)):
            return False
        return True

#Pode ser lapidada se tiver tempo sobrando(Achar exatamente onde está o buraco)
    def unsafePoints(self):
        p = self.player
        self.gamemap.addPosition("unsafe", p.x, p.y)
        if (self.dir == "north"):
            self.gamemap.addPosition("unsafe", p.x+1, p.y)
            self.gamemap.addPosition("unsafe", p.x-1, p.y)
            self.gamemap.addPosition("unsafe", p.x, p.y-1)
        elif (self.dir == "south"):
            self.gamemap.addPosition("unsafe", p.x+1, p.y)
            self.gamemap.addPosition("unsafe", p.x-1, p.y)
            self.gamemap.addPosition("unsafe", p.x, p.y+1)
        elif (self.dir == "west"):
            self.gamemap.addPosition("unsafe", p.x-1, p.y)
            self.gamemap.addPosition("unsafe", p.x, p.y-1)
            self.gamemap.addPosition("unsafe", p.x, p.y+1)
        elif (self.dir == "east"):
            self.gamemap.addPosition("unsafe", p.x+1, p.y)
            self.gamemap.addPosition("unsafe", p.x, p.y-1)
            self.gamemap.addPosition("unsafe", p.x, p.y+1)
        #print("Unsafe: ",self.gamemap.getUnsafePos())
    
    def convertPathToCommands(self, path):
        nextNode = Node(self.player.x, self.player.y, 0, 0, 0)
        Atualdir = self.dir
        while(path):
            AtualNode = nextNode
            nextNode = path.pop(0)
            if(nextNode.x>AtualNode.x):
                if(Atualdir=="south"):
                    self.proxEvento.append("virar_esquerda")
                elif(Atualdir=="north"):
                    self.proxEvento.append("virar_direita")
                elif(Atualdir=="west"):
                    self.proxEvento.append("virar_esquerda")
                    self.proxEvento.append("virar_esquerda")
                Atualdir = "east"
            elif(nextNode.x<AtualNode.x):
                if(Atualdir=="south"):
                    self.proxEvento.append("virar_direita")
                elif(Atualdir=="north"):
                    self.proxEvento.append("virar_esquerda")
                elif(Atualdir=="east"):
                    self.proxEvento.append("virar_esquerda")
                    self.proxEvento.append("virar_esquerda")
                Atualdir = "west"
            elif(nextNode.y<AtualNode.y):
                if(Atualdir=="west"):
                    self.proxEvento.append("virar_direita")
                elif(Atualdir=="east"):
                    self.proxEvento.append("virar_esquerda")
                elif(Atualdir=="south"):
                    self.proxEvento.append("virar_esquerda")
                    self.proxEvento.append("virar_esquerda")
                Atualdir = "north"
            elif(nextNode.y>AtualNode.y):
                if(Atualdir=="east"):
                    self.proxEvento.append("virar_direita")
                elif(Atualdir=="west"):
                    self.proxEvento.append("virar_esquerda")
                elif(Atualdir=="north"):
                    self.proxEvento.append("virar_esquerda")
                    self.proxEvento.append("virar_esquerda")
                Atualdir = "south"
            if(nextNode.x!=AtualNode.x or nextNode.y!=AtualNode.y):
                self.proxEvento.append("andar")

    
    def GetDecision(self):

        if(self.status!=[]):
            #print(self.status)
            pass
        #Se energia <30, ir para um powerup caso tenha algum anotado (A*)

        #Após achar 3 ouros aleatóriamente, começar a percorrer um mesmo caminho pegando esses 3 (A*)
        # toda vez que ele vira o cont é zerado
        if "breeze" in self.status:
            self.unsafePoints()
            self.proxEvento.append("andar_re")
            a = self.gamemap.aStar(self.player.x,self.player.y,10,10)
            self.convertPathToCommands(a)
            #print(self.proxEvento)
        elif (self.energy<=50 and self.gamemap.getPowerupPos()!=[]):
            self.xObj,self.yObj = self.gamemap.getNearNode(self.player.x,self.player.y,"powerup")
            a = self.gamemap.aStar(self.player.x,self.player.y,self.xObj,self.yObj)
            self.convertPathToCommands(a)                      
    
        elif "blocked" in self.status:
            if random.randint(0,1):
                self.proxEvento.append("virar_direita")
            else:
                self.proxEvento.append("virar_esquerda")

        # o melhor seria se sentisse uma breeze ir para um lugar seguro usando o A*

        elif self.contEvent >= 100:
            self.contEvent = 0
            if self.gamemap.goldPos != []:
                self.xObj,self.yObj = self.gamemap.getNearNode(self.player.x,self.player.y,"gold")
                a = self.gamemap.aStar(self.player.x,self.player.y,self.xObj,self.yObj )
                self.convertPathToCommands(a)
        
        else:

            self.xObj,self.yObj = self.gamemap.getNearNode(self.player.x,self.player.y,"notVisit")
            a = self.gamemap.aStar(self.player.x,self.player.y,self.xObj,self.yObj)
            self.convertPathToCommands(a)
        if self.proxEvento == []:
            self.proxEvento.append("")
            
        
        


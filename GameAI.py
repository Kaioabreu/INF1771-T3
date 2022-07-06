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
from Gamemap import Gamemap

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
        
            if s == "blocked" or s == "steps" or s == "breeze" or s =="flash" or s == "blueLight" or s =="redLight" or s[:6]=="enemy#":
                self.status.append(s)
                if s == "blueLight":
                    if(not self.player in self.gamemap.getGoldPos):
                        self.gamemap.addPosition("gold",self.player)
                elif s == "redLight":
                    if(not self.player in self.gamemap.getPowerupPos):
                        self.gamemap.addPosition("powerup", self.player)
                elif s == "blocked":
                    if(not self.NextPosition() in self.gamemap.getBlockedPos):
                        self.gamemap.addPosition("block", self.NextPosition())

    # <summary>
    # No observations received
    # </summary>
    def GetObservationsClean(self):
        self.status = []
        pass
    

    # <summary>
    # Get Decision
    # </summary>
    # <returns>command string to new decision</returns>

    def GetDecision(self):
        self.contEvent+=1 # toda vez que ele vira o cont é zerado
        if self.contEvent >= 10:
            self.contEvent = 0
            if random.randint(0,1):
                self.proxEvento.append("virar_direita")
            else: 
                self.proxEvento.append("virar_esquerda")
        print(self.status)
        if "blueLight" in self.status:
            self.GetObservationsClean()
            self.proxEvento.append("pegar_ouro")

        elif "redLight" in self.status and self.energy<30:
            self.GetObservationsClean()
            self.proxEvento.append("pegar_ouro")

        elif "enemy#1" in self.status or "enemy#2" in self.status or "enemy#3" in self.status:
            self.proxEvento.append("atacar")
        elif "enemy#4" in self.status or "enemy#5" in self.status or "enemy#6" in self.status:
            self.contEvent = 0
            self.proxEvento.append("virar_direita")
            self.proxEvento.append("andar")
        
    
        elif "blocked" in self.status:
            self.contEvent = 0
            self.GetObservationsClean()
            if random.randint(0,1):
                self.proxEvento.append("virar_direita")
            else:
                self.proxEvento.append("virar_esquerda")
        #O que fazer qunado tem flash ou breeze? Ele ta travando loucamente
        # o melhor seria se sentisse uma breeze ir para um lugar seguro usando o A*
        elif 'flash' in self.status:
            self.GetObservationsClean()
            self.proxEvento.append('andar')

        elif "breeze" in self.status:
            self.proxEvento.append("andar_re")
            self.proxEvento.append("virar_esquerda")
            
        self.proxEvento.append("andar")
        ## ALEATÓRIO
        


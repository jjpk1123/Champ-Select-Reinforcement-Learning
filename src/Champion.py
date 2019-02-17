import requests as req
import urllib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import copy
import League

#The Class 'Champion' is responsible for:
#1. Holding information about a single Champion
#2. Accessing this information

class Champion:


    #TODO: Refactor/rethink how a champion is put together
    #What are it's essential components? 
    #What can be done in League once, and then used for each Champion?
    #What *needs* to be done in this constructor?
    def __init__(self, championId, championgg, dataDragon, matchups):
        print(dataDragon)
        self.name = dataDragon['id']
        self.id = championId
        self.champInfo = getChampInfoById(championId, dataDragon)
        #TODO: Put below line in League, as it references many champions
        #self.matchups = getAllMatchupsById(championId, championgg, dataDragon)
        self.matchups = matchups

        # Roles in matchups that are not SYNERGY or ADCSUPPORT
        self.roles = [role for role in list(matchups.keys()) if role != 'SYNERGY' and role != 'ADCSUPPORT']

        # Image information
        # self.icon = mpimg.imread('http://ddragon.leagueoflegends.com/cdn/6.24.1/img/champion/' + self.dataDragon['image']['full'])

    def __repr__(self):
        return str(self.name) + ", " + str(self.id) + ": " + str(self.roles)

    def __eq__(self, other):
        return self.name == other.name

    #def showIcon(self):
    #    plt.imshow(img)
    #    plt.show()

    # Given a lane, gives the best match up aka the champ this champ has the highest win rate against/with.
    def getBestMatchup(self, lane):
        winrates = self.matchups[lane]
        bestWinrate = 0
        bestIndex = -1
        for i in range(len(winrates)):
            win = list(winrates[i].values())[0]
            # print(win)
            if win > bestWinrate:
                bestWinrate = win
                bestIndex = i
        return winrates[bestIndex]

    def getWorstMatchup(self, lane):
        winrates = self.matchups[lane]
        bestWinrate = 1
        bestIndex = -1
        for i in range(len(winrates)):
            win = list(winrates[i].values())[0]
            # print(win)
            if win < bestWinrate:
                bestWinrate = win
                bestIndex = i
        return winrates[bestIndex]

    def getWinrate(self, matchups):
        winrate = 0
        total = 0
        for role in matchups:
            for matchup in matchups[role]:
                winrate += list(matchup.values())[0]
                total += 1
        return winrate/total

    #TODO: Combine below method with above method
    #def getWinrate(self, matchups, role):
    #    roleMatchups = matchups[role]
    #    winrate = 0
    #    total = 0
    #    for matchup in roleMatchups:
    #        winrate += list(matchup.values())[0]
    #        total += 1
    #    if total == 0:
    #        return .5
    #    return winrate/total


#TODO: Organize this and like-methods into ChampionUtils.py ?

#Given a set of matchups, filter the set by how big the data size is, defaulting at limit=100.
def filterMatchups(matchups, limit=100):
    return [matchup for matchup in matchups if matchup['count'] >= limit]

#Given a name, and Data Dragon, returns the champion's id
def getChampIdByName(champName, dataDragon):
    return dataDragon['data'][champName]['key']

#Given an id number, and Data Dragon, returns all champion info
def getChampInfoById(champId, dataDragon):
    for key, value in dataDragon['data'].items():
        if int(value['key']) == int(champId):
            return value
    return None
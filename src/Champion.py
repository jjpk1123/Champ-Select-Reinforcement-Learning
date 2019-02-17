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
    # name, id, roles, matchups, 
    #What can be done in League once, and then used for each Champion?
    #What *needs* to be done in this constructor?
    def __init__(self, championgg, dataDragon, matchups):
        self.name = dataDragon['name']
        self.id = dataDragon['key']
        self.matchups = matchups
        self.roles = [role for role in list(matchups.keys()) if role != 'SYNERGY' and role != 'ADCSUPPORT']

        #TODO: Figure out this image stuff. Should this be handled here? 
        # Image information
        # self.icon = mpimg.imread('http://ddragon.leagueoflegends.com/cdn/6.24.1/img/champion/' + self.dataDragon['image']['full'])

    def __repr__(self):
        return str(self.name) + ", " + str(self.id) + ": " + str(self.roles)

    def __eq__(self, other):
        return self.name == other.name

    #def showIcon(self):
    #    plt.imshow(img)
    #    plt.show()

    #Return a formatted string of the matchups for human reading
    def getMatchups(self):
        result = ""
        for role in self.matchups:
            result += str(role) + "\n"
            for stats in self.matchups[role]:
                enemy = list(stats.keys())[0]
                winrate = list(stats.values())[0]
                result += "{"+str(enemy)+":"+"{:.{}f}".format(winrate, 2)+"}, "
            result += "\n"
        return result

    # Given a lane, gives the best match up aka the champ this champ has the highest win rate against/with.
    def getBestMatchup(self, role):
        winrates = self.matchups[role]
        bestWinrate = 0
        bestIndex = -1
        for i in range(len(winrates)):
            win = list(winrates[i].values())[0]
            # print(win)
            if win > bestWinrate:
                bestWinrate = win
                bestIndex = i
        return winrates[bestIndex]

    def getWorstMatchup(self, role):
        winrates = self.matchups[role]
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
    return dataDragon[champName]['key']

#Given an id number, and Data Dragon, returns all champion info
def getChampInfoById(champId, dataDragon):
    for key, value in dataDragon.items():
        if int(value['key']) == int(champId):
            return value
    return None
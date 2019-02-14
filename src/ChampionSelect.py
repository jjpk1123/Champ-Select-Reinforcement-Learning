import requests as req
import urllib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import copy
import League
import Champion

class ChampionSelect:

    def __init__(self):
        self.L = League.League()


    #def getValidChampMoves(self, league, comp1, comp2, bans=[]):
        #champList = self.L.getListOfChamps()

        # Get the remaining available roles:
    #    allRoles = ['TOP', 'JUNGLE', 'MIDDLE', 'DUO_CARRY', 'DUO_SUPPORT']
    #    takenRoles = list(comp1.keys())
    #    availableRoles = [x for x in allRoles if x not in takenRoles]

        # Get the remaining available champions:
    #    takenChamps = list(comp1.values()) + list(comp2.values()) + bans
    #    availableChamps = [x for x in champList if x not in takenChamps]
    #    return [{role: champ} for champ in availableChamps for role in champ.roles if role in availableRoles]

    #def getValidBanMoves(self, league, bans=[]):
    #    champList = self.L.getListOfChamps()

    #    # Get the remaining available champions:
    #    takenChamps = bans
    #    availableChamps = [x for x in champList if x.name not in takenChamps]
    #    return [champ for champ in availableChamps]
    #    # return [champ for champ in availableChamps for role in champ.roles if role in availableRoles] + ['None']

    # A move looks like: {'JUNGLE', Akali}
    #def makeChampMove(self, league, move, comp1, comp2, bans=[]):
        # Make sure the move is valid:
    #    if move not in self.getValidChampMoves(league, comp1, comp2, bans):
            # If it is an invalid move, return the ally composition unchanged.
    #        return comp1

        # Set up a new copy of the comp
    #    newComp = copy.deepcopy(comp1)

        # Make the move: Add the move to the comp
    #    newComp[list(move.keys())[0]] = list(move.values())[0]

        # Return the new comp!
    #    return newComp

    def calcWinChance(self, league, comp1, comp2):
        # Gather comp1,2 info into separate structures
        roles = list(comp1.keys())
        champs = list(comp1.values())
        #badRoles = list(comp2.keys())
        badChamps = list(comp2.values())

        winrate = 0
        for i, champ in enumerate(champs):
            matchups = champ.matchups[roles[i]]
            # print("Checking: " + champ.name + " " + roles[i])
            # print("Looking for: " + badChamps[i].name + " " + badRoles[i])
            found = False
            for matchup in matchups:
                # print(list(matchup.keys())[0])
                if list(matchup.keys())[0] == badChamps[i].name:
                    # print("match!")
                    # print(matchup)
                    found = True
                    winrate += list(matchup.values())[0]
                    break
            # No data on the matchup
            if not found:
                # print(champ)
                # print(matchups)
                winrate += Champion.Champion.getWinrate(champ.matchups, roles[i])
        return winrate / 5

    def winner(self, league, state):
        # Game is not finished yet
        if len(state['blue']) != 5 or len(state['red']) != 5:
            return False, False

        # Return True because game is over, then return whether blue team won or not
        return True, self.calcWinChance(league, state['blue'], state['red']) >= self.calcWinChance(league, state['red'], state['blue'])

    def printState(self, comp1, comp2, bans):
        # Print ban board
        banList = []
        for ban in bans:
            banList.append(ban.name)
        print("Bans: " + str(banList))

        # Print champ board
        roles1 = list(comp1.keys())
        champs1 = list(comp1.values())
        roles2 = list(comp2.keys())
        champs2 = list(comp2.values())
        print("----------------------")
        if len(roles1) == 5 and len(roles2) == 5:
            for i in range(5):
                print(roles1[i])
                print(champs1[i].name + " vs " + champs2[i].name)
                print()
        state = {'blue': comp1, 'red': comp2}
        if self.winner(self.L, state):
            print("Left team has " + "{0:.2f}".format(self.calcWinChance(self.L, comp1, comp2)) + " chance of a win.")
        else:
            print("Right team has " + "{0:.2f}".format(self.calcWinChance(self.L, comp2, comp1)) + " chance of a win.")
        print("----------------------")

import requests as req
import urllib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import copy

#TODO: Idea to simplify Champion memory size: Create a SimpleChampion class and have Champion extend SimpleChampion.
#TODO: SimpleChampion will then have less data. What data to trim? Not sure.


#The Champion.py class is responsible for all data related to a Champion. It holds the following data:

#name: The human-recognizable identifier for the Champion, such as "Aatrox" as shown above.
#id: The consistent identifier for grabbing a champion from Data Dragon or Champion.gg, such as '266'.
#winrate: The averaged winrate over all of the Champion's roles.
#roles: Any one champion can have any combination of the following entires of this list as their roles:
#
#    [TOP, JUNGLE, MIDDLE, DUO_CARRY, DUO_SUPPORT, SYNERGY, ADCSUPPORT].
#    TOP, JUNGLE, MIDDLE, DUO_CARRY, DUO_SUPPORT: describe what is known as a "lane assignment". In the community,
#       these are what people think of when they think of roles in a composition within League of Legends.
#       In this program, I will limit each team of 5 to one of each within this list. Can't make a team with 5
#       DUO_SUPPORT, for example.
#    SYNERGY: refers to two champions played on the same team, either playing in any role as long as it is not the same role.
#    ADCSUPPORT: refers to part of the DUO_SUPPORT/DUO_CARRY relationship, and can be thought of as BOTTOM SYNERGY since
#        DUO_SUPPORT and DUO_CARRY both play in the bottom lane.
#
#matchups: A list in the form -[ROLE: {ENEMY/ALLY: WINRATE WITH/AGAINST}, ...]
#This structure describes how Champion A relates to Champion B in terms of winrate. For every entry in the Champion's roles list, there is an entry in this list which goes more in depth. This could, for example, be used to find the winrate between Aatrox and Alistar, or the winrate when Aatrox and Alistar are on the same team.

#Use it in this way:
#   Champion(64, championgg, dd)
#The __repr__ will print this:
#   LeeSin, 64: ['TOP', 'JUNGLE', 'MIDDLE', 'DUO_CARRY', 'DUO_SUPPORT']

# Holds information about one champion
class Champion:

    def __init__(self, championId, championgg, dataDragon):
        self.dd = req.get("http://ddragon.leagueoflegends.com/cdn/8.24.1/data/en_US/champion.json").json() #TODO: Rename these variables
        self.dataDragon = self.getChampInfoById(championId, dataDragon)
        self.championgg = championgg  # TODO: Make League filter this field.

        # Matchups
        self.matchups = self.getAllMatchups(championId, championgg, dataDragon)

        # Roles in matchups that are not SYNERGY or ADCSUPPORT
        self.roles = [role for role in list(self.getAllMatchups(championId, championgg, dd).keys()) \
                      if role != 'SYNERGY' and role != 'ADCSUPPORT']

        # Any non-zero positive integer found in the Data Dragon champion data
        self.id = championId

        # Irelia, LeeSin, Aatrox...
        self.name = self.dataDragon['id']

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

    #Given an id number, and Data Dragon, returns all champion info
    def getChampInfoById(champId, dataDragon):
        for key, value in dataDragon['data'].items():
            if int(value['key']) == int(champId):
                return value
        return None

    #Given a set of matchups, filter the set by how big the data size is, defaulting at limit=100.
    def filterMatchups(self, matchups, limit=100):
        return [matchup for matchup in matchups if matchup['count'] >= limit]

    #[ROLE: {<ENEMY/ALLY Champion>: <Winrate AGAINST/WITH>}, ...}, ...]
    def getAllMatchups(self, champId, championgg, dataDragon, limit=10):
        #Every matchup
        champId = str(champId)
        matchups = req.get("http://api.champion.gg/v2/champions/"+champId+"/matchups?&limit=500&api_key="+api_key).json()

        #All champions: {64: 'LeeSin',...}
        allChamps = self.getAllChamps(championgg, dataDragon)

        #Filter the matchups, limiting it to only *limit* games as bottom threshold.
        #For example if limit=10, trim off all matchups with less than 10 games played.
        fm = self.filterMatchups(matchups, limit)
        all_roles = ['TOP', 'JUNGLE', 'MIDDLE', 'DUO_CARRY', 'DUO_SUPPORT', 'SYNERGY', 'ADCSUPPORT']
        all_matchups = {}

        #Iterate through each role type
        for role in all_roles:
            #Role_fm = role with filtered matchups. Looks at Lee Sin Jungle vs all(x) Jungle.
            role_fm = [x for i, x in enumerate(fm) if fm[i]['_id']['role'] == role]
            #print(role)
            #print(role_fm)

            #If there is at least one game...
            if role_fm:

                role_matchup = []
                for i, x in enumerate(role_fm):
                    #Figure out which champ_id is our champ, and which is the enemy, get the winrate AGAINST:
                    if int(x['_id']['champ2_id']) != int(champId):
                        enemyChamp = allChamps[x['_id']['champ2_id']]
                        enemyChampId = x['_id']['champ2_id']
                        winrate = role_fm[i]['champ1']['winrate']
                    else:
                        enemyChamp = allChamps[x['_id']['champ1_id']]
                        enemyChampId = x['_id']['champ1_id']
                        winrate = role_fm[i]['champ2']['winrate']
                    #Add this information to a dictionary
                    matchup = {}
                    matchup[enemyChamp] = winrate

                    #Add it to the collection of role_matchups
                    role_matchup.append(matchup)
                #Add this role_matchup to all matchups
                all_matchups[role] = role_matchup
        return all_matchups

    #Given champion.gg and Data Dragon champion data jsons, returns a dictionary of {id : champion name}
    def getAllChamps(self, championgg, datadragon):
        champs = {}

        #Iterate through all champions in championgg
        for i in range(len(championgg)):
            championggKey = championgg[i]['_id']['championId']

            #Iterate through all champions in datadragon
            for key, value in datadragon['data'].items():

                #If the champion id's match...
                if int(value['key']) == int(championggKey):
                    #... add it to the list, and go to next
                    champs[championggKey] = key
                    break
        return champs

    #Given a name, and Data Dragon, returns the champion's id
    def getChampId(self, champName, dataDragon):
        return self.dd['data'][champName]['key']

    def getWinrate(self, matchups):
        winrate = 0
        total = 0
        for role in matchups:
            for matchup in matchups[role]:
                winrate += list(matchup.values())[0]
                total += 1
        return winrate/total

    def getWinrate(self, matchups, role):
        roleMatchups = matchups[role]
        winrate = 0
        total = 0
        for matchup in roleMatchups:
            winrate += list(matchup.values())[0]
            total += 1
        if total == 0:
            return .5
        return winrate/total
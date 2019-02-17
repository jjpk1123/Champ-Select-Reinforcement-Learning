import requests as req
import urllib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import copy
import Champion
import Query

#The Class 'League' is responsible for:
#1. Holding a collection of all Champions
#2. Accessing this information

class League:
    # A constructor if you know nothing, or know patch and/or api_key
    def __init__(self, patch="9.3.1", api_key="e29bf7c5e411c43e2db51ceb2255e3d1"):
        #[{'_id': 
        #   {'championId': 412, 'role': 'DUO_SUPPORT'}, 
        # 'elo': 'PLATINUM,DIAMOND,MASTER,CHALLENGER', 
        # 'patch': '9.3', 
        # 'championId': 412, 
        # 'winRate': 0.5120458891013384, 
        # 'playRate': 0.1762162364524643, 
        # 'gamesPlayed': 54915, 
        # 'percentRolePlayed': 0.9281513031132745, 
        # 'banRate': 0.02094763892491463, 
        # 'role': 'DUO_SUPPORT'
        # } 
        # ,...]
        self.championgg = Query.getChampiongg(api_key)
        
        #{'type': 'champion', 
        # 'format': 'standAloneComplex', 
        # 'version': '9.3.1', 
        # 'data': {
        # 'Aatrox': 
        #   {'version': '9.3.1', 
        #   'id': 'Aatrox', 
        #   'key': '266',   
        #   'name': 'Aatrox', 
        #   'title': 'the Darkin Blade', 
        #   'blurb': 'Once honored defenders of Shurima against the Void, Aatrox and his brethren would eventually become an even greater threat to Runeterra, and were defeated only by cunning mortal sorcery. But after centuries of imprisonment, Aatrox was the first to find...', 
        #   'info': {'attack': 8, 'defense': 4, 'magic': 3, 'difficulty': 4}, 
        #   'image': {'full': 'Aatrox.png', 'sprite': 'champion0.png', 'group': 'champion', 'x': 0, 'y': 0, 'w': 48, 'h': 48}, 
        #   'tags': ['Fighter', 'Tank'], 
        #   'partype': 'Blood Well', 
        #   'stats': {'hp': 580, 'hpperlevel': 80, 'mp': 0, 'mpperlevel': 0, 'movespeed': 345, 'armor': 33, 'armorperlevel': 3.25, 'spellblock': 32.1, 'spellblockperlevel': 1.25, 'attackrange': 175, 'hpregen': 8, 'hpregenperlevel': 0.75, 'mpregen': 0, 'mpregenperlevel': 0, 'crit': 0, 'critperlevel': 0, 'attackdamage': 60, 'attackdamageperlevel': 5, 'attackspeedperlevel': 2.5, 'attackspeed': 0.651}
        # }, ...}
        #}
        self.dataDragon = Query.getDataDragon(patch)
        
        self.champions = [Champion.Champion(Champion.getChampIdByName(name, self.dataDragon), self.championgg, self.dataDragon) for name in self.dataDragon['data']]

    #def getChampsInRole(self, role):
    #    return [champ for champ in self.champions if role in champ.roles]

    #def getListOfChamps(self):
    #    return [champ for champ in self.champions]

    
    #Given champion.gg and Data Dragon champion data jsons, returns a dictionary of {id : champion name}
    def getAllChamps(self):
        champs = {}

        #Iterate through all champions in championgg
        for i in range(len(self.championgg)):
            championggKey = self.championgg[i]['_id']['championId']

            #Iterate through all champions in datadragon
            for key, value in self.dataDragon['data'].items():

                #If the champion id's match...
                if int(value['key']) == int(championggKey):
                    #... add it to the list, and go to next
                    champs[championggKey] = key
                    break
        return champs

    # #[ROLE: {<ENEMY/ALLY Champion>: <Winrate AGAINST/WITH>}, ...}, ...]
    # def getAllMatchups(self, champId, championgg, dataDragon, api_key="e29bf7c5e411c43e2db51ceb2255e3d1", limit=10):
    #     #Every matchup
    #     champId = str(champId)
    #     matchups = req.get("http://api.champion.gg/v2/champions/" + champId + "/matchups?&limit=500&api_key=" + api_key).json()

    #     #All champions: {64: 'LeeSin',...}
    #     allChamps = League.getAllChamps(championgg, dataDragon)

    #     #Filter the matchups, limiting it to only *limit* games as bottom threshold.
    #     #For example if limit=10, trim off all matchups with less than 10 games played.
    #     fm = self.filterMatchups(matchups, limit)
    #     all_roles = ['TOP', 'JUNGLE', 'MIDDLE', 'DUO_CARRY', 'DUO_SUPPORT', 'SYNERGY', 'ADCSUPPORT']
    #     all_matchups = {}

    #     #Iterate through each role type
    #     for role in all_roles:
    #         #Role_fm = role with filtered matchups. Looks at Lee Sin Jungle vs all(x) Jungle.
    #         role_fm = [x for i, x in enumerate(fm) if fm[i]['_id']['role'] == role]
    #         #print(role)
    #         #print(role_fm)

    #         #If there is at least one game...
    #         if role_fm:

    #             role_matchup = []
    #             for i, x in enumerate(role_fm):
    #                 #Figure out which champ_id is our champ, and which is the enemy, get the winrate AGAINST:
    #                 if int(x['_id']['champ2_id']) != int(champId):
    #                     enemyChamp = allChamps[x['_id']['champ2_id']]
    #                     #enemyChampId = x['_id']['champ2_id']
    #                     winrate = role_fm[i]['champ1']['winrate']
    #                 else:
    #                     enemyChamp = allChamps[x['_id']['champ1_id']]
    #                     #enemyChampId = x['_id']['champ1_id']
    #                     winrate = role_fm[i]['champ2']['winrate']
    #                 #Add this information to a dictionary
    #                 matchup = {}
    #                 matchup[enemyChamp] = winrate

    #                 #Add it to the collection of role_matchups
    #                 role_matchup.append(matchup)
    #             #Add this role_matchup to all matchups
    #             all_matchups[role] = role_matchup
    #     return all_matchups

    


import Champion
import Query

#The Class 'League' is responsible for:
#1. Holding a collection of all Champions
#2. Accessing this information

class League:
    # A constructor if you know nothing, or know patch and/or api_key
    def __init__(self, patch="9.3.1", api_key="e29bf7c5e411c43e2db51ceb2255e3d1"):
        #championgg looks like:
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
        
        #dataDragon looks like:
        #{'Aatrox': 
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
        # }
        #,...}
        self.dataDragon = Query.getDataDragon(patch)

        #champions looks like:
        # name = "Aatrox"
        # id = 266
        # roles = ['TOP', 'JUNGLE', 'MIDDLE']
        # matchups = ['TOP': 
        #   {Ornn:0.47}, {Illaoi:0.48}, {Kled:0.52}, ...}
        # ,...]
        self.champions = [Champion.Champion(self.championgg, self.dataDragon[name], self.getAllMatchups(self.dataDragon[name]['key'])) for name in self.dataDragon]

    # Returns a list of each champion given a role
    def getChampsInRole(self, role):
        return [champ for champ in self.champions if role in champ.roles]

    # Given champion.gg and Data Dragon champion data jsons, returns a dictionary of {id : champion name}
    def getAllChamps(self):
        allChampions = {}
        for champion in self.champions:
            allChampions[champion.id] = champion.name
        return allChampions

    #TODO: Refactor. This is WAY too big of a method, way too complex.
    # [ROLE: {<ENEMY/ALLY Champion>: <Winrate AGAINST/WITH>}, ...}, ...]
    def getAllMatchups(self, champId, limit = 10):
        #Every matchup
        champId = str(champId)
        matchups = Query.getMatchups(champId)

        #All champions: {64: 'LeeSin',...}
        allChamps = self.getAllChamps()

        #Filter the matchups, limiting it to only *limit* games as bottom threshold.
        #For example if limit=10, trim off all matchups with less than 10 games played.
        fm = Champion.filterMatchups(matchups, limit)
        all_roles = ['TOP', 'JUNGLE', 'MIDDLE', 'DUO_CARRY', 'DUO_SUPPORT', 'SYNERGY', 'ADCSUPPORT']
        all_matchups = {}

        #Iterate through each role type
        for role in all_roles:
            
            #Role_fm = role with filtered matchups. Looks at Lee Sin Jungle vs all(x) Jungle.
            role_fm = [x for i, x in enumerate(fm) if fm[i]['_id']['role'] == role]

            #If there is at least one game...
            if role_fm:

                role_matchup = []
                for i, x in enumerate(role_fm):
                    #Figure out which champ_id is our champ, and which is the enemy, get the winrate AGAINST:
                    if int(x['_id']['champ2_id']) != int(champId):
                        enemyChamp = allChamps[x['_id']['champ2_id']]
                        #enemyChampId = x['_id']['champ2_id']
                        winrate = role_fm[i]['champ1']['winrate']
                    else:
                        enemyChamp = allChamps[x['_id']['champ1_id']]
                        #enemyChampId = x['_id']['champ1_id']
                        winrate = role_fm[i]['champ2']['winrate']
                    #Add this information to a dictionary
                    matchup = {}
                    matchup[enemyChamp] = winrate

                    #Add it to the collection of role_matchups
                    role_matchup.append(matchup)
                #Add this role_matchup to all matchups
                all_matchups[role] = role_matchup
        return all_matchups
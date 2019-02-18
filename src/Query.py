import requests as req

#The Class 'Query' is responsible for:
#1. Making API calls to:
#   a. Champion.gg
#   b. DataDragon

def getChampiongg(api_key = "e29bf7c5e411c43e2db51ceb2255e3d1", limit = "500"):
    return req.get("http://api.champion.gg/v2/champions?&limit=" + limit + "&api_key=" + api_key).json()

def getMatchups(championId, api_key = "e29bf7c5e411c43e2db51ceb2255e3d1", limit="500"):
    return req.get("http://api.champion.gg/v2/champions/" + championId + "/matchups?&limit=" + limit + "&api_key=" + api_key).json()

def getDataDragon(patch):
    return req.get("http://ddragon.leagueoflegends.com/cdn/" + patch + "/data/en_US/champion.json").json()['data']

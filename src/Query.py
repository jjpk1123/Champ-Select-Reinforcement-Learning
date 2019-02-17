import urllib
import copy
import matplotlib
import requests as req
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys

#The Class 'Query' is responsible for:
#1. Making API calls to:
#   a. Champion.gg
#   b. DataDragon

def getChampiongg(api_key = "e29bf7c5e411c43e2db51ceb2255e3d1"):
    return req.get("http://api.champion.gg/v2/champions?&limit=500&api_key=" + api_key).json()

def getDataDragon(patch):
    return req.get("http://ddragon.leagueoflegends.com/cdn/" + patch + "/data/en_US/champion.json").json()['data']

def getMatchups(championId, api_key = "e29bf7c5e411c43e2db51ceb2255e3d1"):
    return req.get("http://api.champion.gg/v2/champions/" + championId + "/matchups?&limit=500&api_key=" + api_key).json()

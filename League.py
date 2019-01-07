import requests as req
import urllib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import copy
import Champion


# Creates a collection of every Champion.
# It accomplishes this by querying Data Dragon and Champion.gg for the requested patch, using the provided key.
class League:
    # A constructor if you know nothing, or know patch and/or api_key
    def __init__(self, patch="8.24.1", api_key="e29bf7c5e411c43e2db51ceb2255e3d1"):
        self.championgg = req.get("http://api.champion.gg/v2/champions?&limit=500&api_key=" + api_key).json()
        self.dd = req.get("http://ddragon.leagueoflegends.com/cdn/" + patch + "/data/en_US/champion.json").json()
        self.champions = [Champion(Champion.getChampId(name, self.dd), self.championgg, self.dd) for name in self.dd['data']]

    def getChampsInRole(self, role):
        return [champ for champ in self.champions if role in champ.roles]

    def getListOfChamps(self):
        return [champ for champ in self.champions]
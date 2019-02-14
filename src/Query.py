import urllib
import copy
import matplotlib
import requests as req
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys

###The Query.py class is responsible for interacting with the Data Dragon API and the Champion.gg API.


api_key = 'e29bf7c5e411c43e2db51ceb2255e3d1' #This will be used in many functions down the road, so I declare it now.
championgg = req.get("http://api.champion.gg/v2/champions?&limit=500&api_key="+api_key).json()
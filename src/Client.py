import os.path
import sys

import League

#TODO: Function to get current up-to-date patch so that Data Dragon and Champion.gg are synced for keys.
        #Example: Champion is added in patch 9.2 and Champion.gg says there are 143 champions, but Data Dragon for patch 8.24 says 142 champions. Key error.


#Preconditions: 
    # 1. A filename to store a new Q table
    # 2. A player name to associate with the Q table 
    #Post conditions:
    # 1. A file with a populated Q table, with a name such as "testQ.txt"
    # 2. A league file is written for future training or testing or playing!
def learn(name):
    print("learning...")
    #TODO: Once the learning system is figured out, a persistent data system will be figured out so as to reuse Q tables once theyre created.
    # 1. Q file
    #qFile = None
    #if os.path.isfile(str(sys.argv[2]) + "Q.txt"):
        #If file exists, inform user and exit
    #    print("Training already complete (Q file already exists), try the operation 'play'!")
    #    return
    #else: 
        # Open file, intention to write
    #    qFile = open(str(sys.argv[2]) + "Q.txt", "w")
    
    # 2. League file
    #leagueFile = None
    #league = None

    #Check if there is a league file
    #if os.path.isfile(str(sys.argv[2]) + "League.txt"):
        # Open it for reading
        #leagueFile = open(str(sys.argv[2]) + "League.txt", "r")
        #TODO: make a new League object with the existing leagueFile

        #For now, we will just make a new League using the API's
        #league = L.League()
    #else:
        # Open it for writing
        #leagueFile = open(str(sys.argv[2]) + "League.txt", "w")
        #Make new League object
            #TODO: Ask for parameters (patch, api_key). No input means set to default (patch="8.24.1", api_key="e29bf7c5e411c43e2db51ceb2255e3d1")
        #league = L.League() 
        #TODO: Save the file in <name>League.txt for future reference (such as in play ? )

    #Make a new league
    L = League.League()
    #print(L.champions[0])
    #print(L.champions[0].getMatchups())

    #Train a new player using this league
    #trainQ = Trainer.Trainer.trainQ()

    # TODO: Train!
    # trainQ = Trainer.Trainer.trainQ(<params>)
        # TODO: Ask for parameters, recommending certain ones (nRepetitions, learningRate, epsilonDecayFactor)
            # trainQ(self, nRepetitions, learningRate, epsilonDecayFactor, league, validChampMovesF, validBanMovesF, makeChampMoveF)
    # TODO: Write the Q table to a file! :)

    #print("writing a test file: " + str(qFile.name))
    #qFile.write(trainQ.toString OR trainQ.toJSON OR someting similar)

    #TODO: Ask if the user would like to immediately play?

def play(name):
    print("playing...")

if __name__== "__main__":
    #Argument check
    if (len(sys.argv) < 3):
        print("Usage: Client.py <operation> <name>\nExample: Client.py learn julien")
        sys.exit()

    #Learning
    if (sys.argv[1] == 'learn'):
        learn(sys.argv[2])
        
    #Playing
    elif (sys.argv[1] == 'play'):
        play(sys.argv[2])

    #Doing absolutely nothing :)
    else:
        print("just hanging out! :)")

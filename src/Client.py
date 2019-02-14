import os.path
import sys

import League as L


#Preconditions: 
    # 1. A filename to store a new Q table
    # 2. A player name to associate with the Q table 
    #Post conditions:
    # 1. A file with a populated Q table, with a name such as "testQ.txt"
    # 2. A league file is written for future training or testing or playing!
def learn(name):
    print("learning...")
    # 1. Q file
    qFile = None
    if os.path.isfile(str(sys.argv[2]) + "Q.txt"):
        #If file exists, inform user and exit
        print("Q file already exists, try the operation 'play'!")
        return
    else: 
        # Open file, intention to write
        qFile = open(str(sys.argv[2]) + "Q.txt", "w")

    # 2. League file
    leagueFile = None
    league = None
    if os.path.isfile(str(sys.argv[2]) + "League.txt"):
        # Open it for reading
        leagueFile = open(str(sys.argv[2]) + "League.txt", "r")
        #TODO: make a new League object with the existing leagueFile
        league = L.League() #TODO: Delete once above is fixed
    else:
        # Open it for writing
        leagueFile = open(str(sys.argv[2]) + "League.txt", "w")
        #Make new League object
            #TODO: Ask for parameters (patch, api_key). No input means set to default (patch="8.24.1", api_key="e29bf7c5e411c43e2db51ceb2255e3d1")
        league = L.League() #Default params
        #TODO: Save the file in <name>League.txt for future reference (such as in play ? )
        
    # TODO: Train!
    # trainQ = Trainer.Trainer.trainQ(<params>)
        # TODO: Ask for parameters, recommending certain ones (nRepetitions, learningRate, epsilonDecayFactor)
            # trainQ(self, nRepetitions, learningRate, epsilonDecayFactor, league, validChampMovesF, validBanMovesF, makeChampMoveF)
    # TODO: Write the Q table to a file! :)

    print("writing a test file: " + str(qFile.name))
    qFile.write("asdf") 
    #qFile.write(trainQ.toString OR trainQ.toJSON OR someting similar)

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

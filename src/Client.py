import os.path
import sys

import League as L

if __name__== "__main__":
    #Argument check
    if (len(sys.argv) < 3):
        print("Usage: Client.py <operation> <name>\nExample: Client.py learn julien")
        sys.exit()

    #Learning
    #Preconditions: 
    # 1. A filename to store a new Q table
    # 2. A player name to associate with the Q table 
    #Post conditions:
    # 1. A file with a populated Q table, with a name such as "testQ.txt"
    if (sys.argv[1] == 'learn'):
        print("learning...")

        # Open file, intention to write
        qFile = open(str(sys.argv[2]) + "Q.txt", "w")
        
        # Check for League file
        leagueFile = None
        if os.path.isfile(str(sys.argv[2]) + "League.txt"):
            # Open it for reading
            leagueFile = open(str(sys.argv[2]) + "League.txt", "r")
        else:
            # Open it for writing
            leagueFile = open(str(sys.argv[2]) + "League.txt", "w")
            #Make new League object
                #TODO: Ask for parameters (patch, api_key). No input means set to default (patch="8.24.1", api_key="e29bf7c5e411c43e2db51ceb2255e3d1")
            league = L.League()
            #TODO: Save the file as JSON in <name>League.txt
            



        # TODO: Train!
            # TODO: Ask for parameters, recommending certain ones (nRepetitions, learningRate, epsilonDecayFactor)
                # TODO: trainQ(self, nRepetitions, learningRate, epsilonDecayFactor, league, validChampMovesF, validBanMovesF, makeChampMoveF)
            # TODO: Run trainQ, which returns the Q table

        # TODO: Write the Q table to a file! :)
        print("writing a test file: " + str(qFile.name))
        qFile.write("asdf") 
        






    #Playing
    elif (sys.argv[1] == 'play'):
        print("playing...")

    #Doing absolutely nothing :)
    else:
        print("just hanging out! :)")

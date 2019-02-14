import sys

if __name__== "__main__":
    #Argument check
    if (len(sys.argv) < 3):
        print("Usage: Client.py <operation> <filename>\nExample: Client.py learn julien")
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
        filename = open(str(sys.argv[2]) + "Q.txt", "w")
        
        # Check for League file
            # If it exists, continue
            # Else, make a new one, continue
            
        # Train!
            # Ask for parameters, recommending certain ones (nRepetitions, learningRate, epsilonDecayFactor)
                # trainQ(self, nRepetitions, learningRate, epsilonDecayFactor, league, validChampMovesF, validBanMovesF, makeChampMoveF)
            # Run trainQ, which returns the Q table

        # Write the Q table to a file! :)
        print("writing a test file: " + str(filename.name))
        filename.write("asdf") 
        






    #Playing
    elif (sys.argv[1] == 'play'):
        print("playing...")

    #Doing absolutely nothing :)
    else:
        print("just hanging out! :)")
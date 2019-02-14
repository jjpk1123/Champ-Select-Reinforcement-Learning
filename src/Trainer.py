import requests as req
import urllib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import copy
import League
import Champion
import ChampionSelect

class Teacher:

    def __init__(self):
        x = 0 #Placeholder

    def stateMoveTuple(self, state, move):
        blue = state['blue']
        blueRoles = list(blue.keys())
        blueChampions = list(blue.values())
        # print("bluechamps: " + str(blueChampions))
        blueChampions = [champ.name for champ in blueChampions]

        red = state['red']
        redRoles = list(red.keys())
        redChampions = list(red.values())
        redChampions = [champ.name for champ in redChampions]

        blueTuple = tuple(blueRoles), tuple(blueChampions)
        redTuple = tuple(redRoles), tuple(redChampions)
        return blueTuple, redTuple

    def epsilonChampGreedy(self, epsilon, Q, league, comp1, comp2, bans=[]):
        validMoves = ChampionSelect.ChampionSelect.getValidChampMoves(league, comp1, comp2, bans)
        if np.random.uniform() < epsilon:
            # Random Move
            # print(" RANDOM NUMBER "+"\n" + str(np.random.choice(len(validMoves))))
            # print(" VALID MOVES "+"\n" + str(validMoves))
            return validMoves[np.random.choice(len(validMoves))]
        else:
            # Greedy Move
            state = {'blue': comp1, 'red': comp2} #TODO: Correct?
            Qs = np.array([Q.get(self.stateMoveTuple(state, move), 0) for move in validMoves])
            return validMoves[np.argmax(Qs)]

    def trainQ(self, nRepetitions, learningRate, epsilonDecayFactor, league, validChampMovesF, validBanMovesF, makeChampMoveF):
        rho = learningRate  # I left this assignment here because rho is more compact.
        epsilonDecayRate = epsilonDecayFactor  # Not sure why these are named differently, just reused assignment.
        epsilon = 1.0  # Start at 1 and decay
        graphics = False  # Graphics may be used eventually, leaving here just in case.
        showMoves = not graphics  # Similarly, I may use this functionality, so leaving here.

        outcomes = np.zeros(nRepetitions)
        epsilons = np.zeros(nRepetitions)
        Q = {}

        if graphics:
            fig = plt.figure(figsize=(10, 10))

        # Play a game each repetition.
        for repetitions in range(nRepetitions):
            print("Game: " + str(repetitions))
            epsilon *= epsilonDecayRate
            epsilons[repetitions] = epsilon
            step = 0

            # Ban phase
            # Grab empty bans
            bans = []
            banDone = False

            # Pick phase
            # Grab empty comp1, comp2, initialize turn start
            comp1 = {}
            comp2 = {}
            state = {'blue': comp1, 'red': comp2}
            turn = 1
            pickDone = False
            while not pickDone:
                step += 1
                # print(turn)
                # If blue/comp1 turn [1,4,5,8,9]
                if turn == 1 or turn == 4 or turn == 5 or turn == 8 or turn == 9:

                    # Make a move
                    move = self.epsilonChampGreedy(epsilon, Q, league, state['blue'], state['red'], bans)
                    newComp = ChampionSelect.makeChampMove(league, move, state['blue'], state['red'], bans=[]) #TODO: Need it to initialize a game of ChampionSelect and refer to the specific instance.
                    newState = copy.deepcopy(state)
                    newState['blue'] = newComp  # Update the blue comp
                    if self.stateMoveTuple(state, move) not in Q:
                        Q[self.stateMoveTuple(state, move)] = 0  # initial Q value for new state, move
                    turn += 1


                # If red/comp2 turn [2,3,6,7,10]
                elif turn == 2 or turn == 3 or turn == 6 or turn == 7 or turn == 10:

                    # Make a move
                    move = self.epsilonChampGreedy(epsilon, Q, league, state['red'], state['blue'], bans)
                    newComp = ChampionSelect.makeChampMove(league, move, state['red'], state['blue'], bans=[]) #TODO: Need it to initialize a game of ChampionSelect and refer to the specific instance.
                    newState = copy.deepcopy(state)
                    newState['red'] = newComp  # Update the bredlue comp
                    if stateMoveTuple(state, move) not in Q:
                        Q[stateMoveTuple(state, move)] = 0  # initial Q value for new state, move
                    turn += 1

                # print(stateMoveTuple(newState, move))

                # Is the game over?
                if ChampionSelect.winner(league, newState)[0]: #TODO: Need it to initialize a game of ChampionSelect and refer to the specific instance.
                    pickDone = True
                    outcomes[repetitions] = step
                    if ChampionSelect.winner(league, newState)[1]: #TODO: Need it to initialize a game of ChampionSelect and refer to the specific instance.
                        Q[self.stateMoveTuple(state, move)] = 1  # Reinforce 1 if blue is the winner.
                    else:
                        Q[self.stateMoveTuple(state, move)] = 0  # Reinforce 0 if red is the winner.

                if step > 1:
                    # print("step>1: " + str(stateMoveTuple(stateOld, moveOld)))
                    # print("Q[compMoveTuple(compOld, moveOld)]: " + str(Q[stateMoveTuple(stateOld, moveOld)]))
                    # print("Q[compMoveTuple(compNew, move)]: " + str(Q[stateMoveTuple(state, move)]))
                    # print("Q[compMoveTuple(compOld, moveOld)]: " + str(Q[stateMoveTuple(stateOld, moveOld)]))
                    Q[self.stateMoveTuple(stateOld, moveOld)] += rho * (
                    Q[self.stateMoveTuple(state, move)] - Q[self.stateMoveTuple(stateOld, moveOld)])

                stateOld, moveOld = state, move  # remember state and move to Q(state,move) can be updated after next steps
                state = newState

        # Returns Q and list or array of number of steps to reach goal for each repetition.
        return Q, outcomes

    def testQ(self, Q, league, validMovesF, makeMoveF, bans=[]):
        comp1 = {}
        comp2 = {}
        state = {'blue': comp1, 'red': comp2}
        path = [state]
        for turn in range(11):
            # If blue/comp1 turn [1,4,5,8,9]
            if turn + 1 == 1 or turn + 1 == 4 or turn + 1 == 5 or turn + 1 == 8 or turn + 1 == 9:

                # Make a move
                move = self.epsilonChampGreedy(0, Q, league, state['blue'], state['red'], bans)
                newComp = ChampionSelect.makeChampMove(league, move, state['blue'], state['red'], bans=[]) #TODO: Need it to initialize a game of ChampionSelect and refer to the specific instance.
                state['blue'] = newComp  # Update the blue comp


            # If red/comp2 turn [2,3,6,7,10]
            elif turn + 1 == 2 or turn + 1 == 3 or turn + 1 == 6 or turn + 1 == 7 or turn + 1 == 10:

                # Make a move
                move = self.epsilonChampGreedy(0, Q, league, state['red'], state['blue'], bans)
                newComp = ChampionSelect.makeChampMove(league, move, state['red'], state['blue'], bans=[]) #TODO: Need it to initialize a game of ChampionSelect and refer to the specific instance.
                state['red'] = newComp  # Update the red comp

            turn += 1
            if ChampionSelect.winner(league, state)[0]: #TODO: Need it to initialize a game of ChampionSelect and refer to the specific instance.
                # add to state to end of path
                return path

        return path
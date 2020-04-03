# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        (QUESTION 1)

        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()                             #(x,y) position of pacman
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()                        #position of ghost agent in hexideximal
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]  #how long until the ghosts arent scared anymore

        "*** YOUR CODE HERE ***"

        #get current score
        points = successorGameState.getScore()

        #check is this is sa win/lose state
        if successorGameState.isWin():
            return 1000000

        #calculate distance to nearest food
        listOfFood = newFood.asList()                                                #list of remaining food locations
        listOfDistFood = []

        for foodPos in listOfFood:
            distanceToFood = util.manhattanDistance(newPos, foodPos)
            listOfDistFood.append(distanceToFood)

        currentPos = currentGameState.getPacmanPosition()
        positionClosestFood = listOfFood[listOfDistFood.index(min(listOfDistFood))]

        #calculate distance to nearest ghost
        ghostDistList = []                                                           #list of distance to ghost
        for ghost in newGhostStates:
            ghostPos = ghost.getPosition()
            distanceToGhost = util.manhattanDistance(newPos, ghostPos)
            ghostDistList.append(distanceToGhost)

        #making sure that we are not too close to the ghost
        for ghostDist in ghostDistList:
            ghostNewPos = newGhostStates[ghostDistList.index(ghostDist)].getPosition()

            if util.manhattanDistance(newPos, ghostNewPos) == 1:
                return -10000000


        #reward pacman if he's moving towards the food
        if Directions.EAST == action:
            if currentPos[0] > positionClosestFood[0]:
                points -= 100
            else:
                points += 200

        if Directions.NORTH == action:
            if currentPos[1] > positionClosestFood[1]:
                points -= 100
            else:
                points += 200

        if Directions.WEST == action:
            if currentPos[0] < positionClosestFood[0]:
                points -= 100
            else:
                points += 200

        if Directions.SOUTH == action:
            if currentPos[1] < positionClosestFood[1]:
                points -= 100
            else:
                points += 200

        return points

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (QUESTION 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        #returned is best score and index of best move

        bestScore, indexBestMove = self.maxFunction(gameState, self.depth)
        bestMove = gameState.getLegalActions(0)[indexBestMove]
        return bestMove

    def maxFunction(self, gameState, depth):

        #check if state is win or lose
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState), None

        depth -= 1

        #get all actions
        actions = gameState.getLegalActions(0)
        scores = []

        #add all scores calculated from the list of actions
        for action in actions:
            score, movement = self.minFunction(gameState.generateSuccessor(0, action), 1, depth)
            scores.append(score)
        maxScore = max(scores)
        indexOfMax = scores.index(maxScore)

        #return highest score and its index
        return maxScore, indexOfMax

    def minFunction(self, gameState, agent, depth):

        #check if this is a win/lose state
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), None

        #calculate scores of all actions and decide min action
        actions = gameState.getLegalActions(agent)
        scores = []
        if agent != 0:
            for action in actions:
                score, movement = self.minFunction(gameState.generateSuccessor(agent, action), (agent+1) % gameState.getNumAgents(), depth)
                scores.append(score)
            minScore = min(scores)
            indexOfMin = scores.index(minScore)
            return minScore, indexOfMin
        else:
            return self.maxFunction(gameState, depth)




class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (QUESTION 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        bestValue, bestMove = self.maxFunction(gameState, self.depth, float('-Inf'), float('Inf'))
        return bestMove

    def maxFunction(self, gameState, depth, alpha, beta):

        #check if state is win or lose
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState), None

        depth -= 1
        maxEval = float('-Inf')


        #get all actions
        actions = gameState.getLegalActions(0)
        scores = []

        #add all scores calculated from the list of actions and find max
        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            score, movement = self.minFunction(successor, 1, depth, alpha, beta)
            maxEval = max(maxEval, score)
            scores.append(score)

            if maxEval > beta:
                return maxEval, movement

            alpha = max(maxEval, alpha)

        indexOfMax = scores.index(maxEval)

        return maxEval, actions[indexOfMax]

    def minFunction(self, gameState, agent, depth, alpha, beta):

        #check if state is win/lose
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), None

        minEval = float('Inf')

        actions = gameState.getLegalActions(agent)
        scores = []

        #if the agent is pacman, maximise, else minimise
        if agent != 0:
            for action in actions:
                successor = gameState.generateSuccessor((agent) % gameState.getNumAgents(), action)
                score, movement = self.minFunction(successor, (agent+1) % gameState.getNumAgents(), depth, alpha, beta)
                minEval = min(minEval, score)
                scores.append(score)

                if minEval < alpha:
                    return minEval, movement

                beta = min(minEval, beta)

            indexOfMin = scores.index(minEval)
            return minEval, actions[indexOfMin]
        else:
            return self.maxFunction(gameState, depth, alpha, beta)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (QUESTION 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        score, action = self.maxEval(gameState,self.depth)
        return action

    def maxEval(self, gameState, depth):

        # check if state is win or lose
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState),''

        # get all actions
        actions = gameState.getLegalActions(0)
        scores = []

        # add all scores calculated from the list of actions and find max
        for action in actions:
            nextAgent = 1 % gameState.getNumAgents()
            score = self.expectedVal(gameState.generateSuccessor(0, action), nextAgent , depth)
            scores.append(score)
        maxScore = max(scores)
        indexOfMaxScore = scores.index(maxScore)

        # return highest score and its action
        return maxScore, actions[indexOfMaxScore]

    def expectedVal(self, gameState, agent, depth):

        #check if agent is pacman or a ghost
        if agent == 0:
            return self.maxEval(gameState, depth-1)[0]
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        #calculate probability of actions
        actions = gameState.getLegalActions(agent)
        probability = 1.0 / len(actions)
        value = 0
        for action in actions:
           successor = gameState.generateSuccessor(agent, action)
           value += self.expectedVal(successor, (agent+1) % gameState.getNumAgents(), depth)*probability
        return value



def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (QUESTION 5).

      DESCRIPTION:

      1) I compute all the variables I'm going to need in the following functions and check for a terminating state
      2) I compute the distances to the ghosts and find their min, which would be the closest ghost to pacman
            (the one that exerts the greatest danger to him)
      3) I compute the distances to the food pellets and find their min, which would be the closest pellet to eat for pacman
      4) I weigh the worth of each variable:
            - current game score * 1 (we won't change this)
            - minimum distance to food * -2 (the further pacman goes from the food, the score decreases)
            - minimum distance to a ghost * -10 (the closer a ghost comes, the lower the score pacman gets)
            - amount of food left * -10 (the more food there is left, greater the penalty)
    """
    "*** YOUR CODE HERE ***"
    #all the variables we need
    currentScore = scoreEvaluationFunction(currentGameState)
    foodPos = (currentGameState.getFood()).asList()
    foodLeft = len(foodPos)
    pacmanPos = (currentGameState.getPacmanPosition())
    ghostStates = (currentGameState.getGhostStates())
    ghostPositions = (currentGameState.getGhostPositions())

    #check if state is win, if so return a lot of points
    if currentGameState.isWin():
        return 1000000

    #calculate ghost distances, find min
    ghostDistances = []
    for ghost in ghostPositions:
        distancetoGhost = util.manhattanDistance(pacmanPos, ghost)
        ghostDistances.append(distancetoGhost)

    minDistToGhost = min(ghostDistances)

    #calculate distances to food, find min
    foodDistances = []
    for food in foodPos:
        distanceToFood = util.manhattanDistance(pacmanPos, food)
        foodDistances.append(distanceToFood)

    minDistToFood = min(foodDistances)

    #weigh values of variables and return the weighted score
    score =  currentScore + (-10 * minDistToFood) + ( * minDistToGhost) + (-10 * foodLeft)
    return score

# Abbreviation
better = betterEvaluationFunction


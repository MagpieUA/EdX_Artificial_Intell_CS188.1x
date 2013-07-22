# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

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
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        minDist = 1000
        maxDist = 0
        "*** YOUR CODE HERE ***"
        food = newFood.asList()
        if food == []:
            minDist = -1000
            maxDist = 1000
        for dot in food:
            dist = abs(newPos[0] - dot[0]) + abs(newPos[1] - dot[1])
            if dist < minDist:
                minDist = dist
            if dist > maxDist:
                maxDist = dist
        ghostNewPos = newGhostStates[0].getPosition()
        distToGhost = abs(newPos[0]-ghostNewPos[0]) + abs(newPos[1]-ghostNewPos[1])
        if distToGhost > 4:
            value = 10*successorGameState.getScore()
        else:
            value = successorGameState.getScore() + distToGhost
        value = value - minDist
        return value
        

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
      Your minimax agent (question 2)
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
        legalMoves = gameState.getLegalActions(0)
        scores = []
        for action in legalMoves:
            newGameState = gameState.generateSuccessor(0, action)
            scores.append(self.minmaxValue(newGameState, 1, self.depth))
        bestScore = max(scores)        
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = bestIndices[0]
        return legalMoves[chosenIndex]

        
                  
    def minmaxValue(self, gameState, step, curDepth):
        if curDepth <= 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if step == 0:
            return self.maxValue(gameState, curDepth)
        if step >= 1:
            return self.minValue(gameState, step, curDepth)

    def maxValue(self, gameState, curDepth):
        v = -100000
        for action in gameState.getLegalActions(0):
            successorGameState = gameState.generateSuccessor(0, action)
            v = max(v, self.minmaxValue(successorGameState, 1, curDepth))
        return v

    def minValue(self, gameState, step, curDepth):
        v = +100000
        for action in gameState.getLegalActions(step):
            successorGameState = gameState.generateSuccessor(step, action)
            if step >= gameState.getNumAgents() - 1:
                v = min(v,self.minmaxValue(successorGameState, 0, curDepth - 1))
            else:
                v = min(v,self.minmaxValue(successorGameState, step + 1, curDepth))
        return v
        
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        legalMoves = gameState.getLegalActions(0)
        a = -100000
        #v = -100000
        scores = []
        for action in legalMoves:
            newGameState = gameState.generateSuccessor(0, action)
            curScore = self.minmaxValue(newGameState, 1, self.depth, a, +100000)
            scores.append(curScore)
            a = max(a,curScore)
        bestScore = max(scores)        
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = bestIndices[0]
        return legalMoves[chosenIndex]

        
                  
    def minmaxValue(self, gameState, step, curDepth, a, b):
        if curDepth <= 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if step == 0:
            return self.maxValue(gameState, curDepth, a, b)
        if step >= 1:
            return self.minValue(gameState, step, curDepth, a, b)

    def maxValue(self, gameState, curDepth, a, b):
        v = -100000
        for action in gameState.getLegalActions(0):
            successorGameState = gameState.generateSuccessor(0, action)
            v = max(v, self.minmaxValue(successorGameState, 1, curDepth, a, b))
            if v > b:
                return v
            a = max(a, v)
        return v

    def minValue(self, gameState, step, curDepth, a, b):
        v = +100000
        for action in gameState.getLegalActions(step):
            successorGameState = gameState.generateSuccessor(step, action)
            if step >= gameState.getNumAgents() - 1:
                v = min(v,self.minmaxValue(successorGameState, 0, curDepth - 1, a, b))
            else:
                v = min(v,self.minmaxValue(successorGameState, step + 1, curDepth, a, b))
            if v < a:
                return v
            b = min(b,v)
        return v
        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        legalMoves = gameState.getLegalActions(0)
        scores = []
        for action in legalMoves:
            newGameState = gameState.generateSuccessor(0, action)
            scores.append(self.expectimaxValue(newGameState, 1, self.depth))
        bestScore = max(scores)        
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = bestIndices[0]
        return legalMoves[chosenIndex]

        
                  
    def expectimaxValue(self, gameState, step, curDepth):
        if curDepth <= 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if step == 0:
            return self.maxValue(gameState, curDepth)
        if step >= 1:
            return self.expValue(gameState, step, curDepth)

    def maxValue(self, gameState, curDepth):
        v = -100000
        for action in gameState.getLegalActions(0):
            successorGameState = gameState.generateSuccessor(0, action)
            v = max(v, self.expectimaxValue(successorGameState, 1, curDepth))
        return v

    def expValue(self, gameState, step, curDepth):
        v = 0
        legalMoves = gameState.getLegalActions(step)
        for action in legalMoves:
            successorGameState = gameState.generateSuccessor(step, action)
            if step >= gameState.getNumAgents() - 1:
                p = 1.0/len(legalMoves)
                v += p * self.expectimaxValue(successorGameState, 0, curDepth - 1)
            else:
                p = 1.0/len(legalMoves)
                v += p * self.expectimaxValue(successorGameState, step + 1, curDepth)
        return v

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    currState = currentGameState
    score = currentGameState.getScore()
    minDist = 1000
    #successorGameState = currentGameState.generatePacmanSuccessor(action)
    pos = currentGameState.getPacmanPosition()
    foodGrid = currentGameState.getFood()
    food = foodGrid.asList()
    if food == []:
        minDist = -1000
    for dot in food:
        dist = abs(pos[0] - dot[0]) + abs(pos[1] - dot[1])
        if dist < minDist:
            minDist = dist
    ghostStates = currentGameState.getGhostStates()
    #newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    #######################
    
    ghostPos = ghostStates[0].getPosition()
    distToGhost = abs(pos[0]-ghostPos[0]) + abs(pos[1]-ghostPos[1])
    if distToGhost > 4:
        value = score - distToGhost
    else:
        value = score + distToGhost
    value = value - minDist
    return value

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


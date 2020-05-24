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
import random, util, math

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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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



        "*** YOUR CODE HERE ***"
        if successorGameState.isWin():
            isWin = 1
        else:
            isWin = 0
        if successorGameState.isLose():
            isLose = 1
        else:
            isLose = 0
        a = 1.5 
        b = 3
        c = 30
        d = 1.5
        e = 1000
        f = -1000

        if newFood.asList():
            minFoodDist = min([util.manhattanDistance(newPos, food) for food in newFood.asList()])
            succScore = successorGameState.getScore()

            total_sum = 0
            ghost_positions = successorGameState.getGhostPositions()
            for ghost in ghost_positions:
                total_sum += util.manhattanDistance(newPos, ghost)**(.5)
            ghostDistances = total_sum


            return (a * ghostDistances + b*succScore) / (d*minFoodDist + c*len(newFood.asList()) + 1) + e*isWin + f*isLose + 50
        else:
            minFoodDist = 0
        succScore = successorGameState.getScore()

        total_sum = 0
        ghost_positions = successorGameState.getGhostPositions()
        for ghost in ghost_positions:
            total_sum += util.manhattanDistance(newPos, ghost)**(.5)
        ghostDistances = total_sum


        return (a * ghostDistances + b*succScore) / (d*minFoodDist + c*len(newFood.asList()) + 1) + e*isWin + f*isLose + 50




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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return self.minimax(gameState, 0, 0)[1]

    def minimax(self, gameState, agent, depth):
        returnAction = None
        #returnScore = None
        if depth >= self.depth or gameState.isWin() or gameState.isLose():
             return (self.evaluationFunction(gameState), returnAction)
        if agent == gameState.getNumAgents() - 1:
            depth += 1
        if agent == 0:
            v = -math.inf
            successors = gameState.getLegalActions(agent)
            for action in successors:
                tempAgent = (agent + 1) % gameState.getNumAgents()
                possibleScore = self.minimax(gameState.generateSuccessor(agent, action), tempAgent, depth)[0]
                if possibleScore > v:
                    v = possibleScore
                    returnAction = action
            return (v, returnAction)
        else:
            #pacman depth
            v = math.inf
            successors = gameState.getLegalActions(agent)
            for action in successors:
                tempAgent = (agent + 1) % gameState.getNumAgents()
                possibleScore = self.minimax(gameState.generateSuccessor(agent, action), tempAgent, depth)[0]
                if possibleScore < v:
                    v = possibleScore
                    returnAction = action
                

        return (v, returnAction)
    
                    

        





class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.minimax(gameState, 0, 0, -math.inf, math.inf)[1]

    def minimax(self, gameState, agent, depth, a, b):
        returnAction = None
        #returnScore = None
        if depth >= self.depth or gameState.isWin() or gameState.isLose():
             return (self.evaluationFunction(gameState), returnAction)
        if agent == gameState.getNumAgents() - 1:
            depth += 1
        if agent == 0:
            v = -math.inf
            successors = gameState.getLegalActions(agent)
            for action in successors:
                tempAgent = (agent + 1) % gameState.getNumAgents()
                possibleScore = self.minimax(gameState.generateSuccessor(agent, action), tempAgent, depth, a, b)[0]
                if possibleScore > v:
                    v = possibleScore
                    returnAction = action
                if v > b:
                    break
                a = max(a, v)
            return (v, returnAction)
        else:
            #pacman depth
            v = math.inf
            successors = gameState.getLegalActions(agent)
            for action in successors:
                tempAgent = (agent + 1) % gameState.getNumAgents()
                possibleScore = self.minimax(gameState.generateSuccessor(agent, action), tempAgent, depth, a, b)[0]
                if possibleScore < v:
                    v = possibleScore
                    returnAction = action
                if v < a:
                    break
                b = min(b, v)
                

        return (v, returnAction)

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
        return self.minimax(gameState, 0, 0)[1]
    def minimax(self, gameState, agent, depth):
        returnAction = None
        #returnScore = None
        if depth >= self.depth or gameState.isWin() or gameState.isLose():
             return (self.evaluationFunction(gameState), returnAction)
        if agent == gameState.getNumAgents() - 1:
            depth += 1
        if agent == 0:
            v = -math.inf
            successors = gameState.getLegalActions(agent)
            for action in successors:
                tempAgent = (agent + 1) % gameState.getNumAgents()
                possibleScore = self.minimax(gameState.generateSuccessor(agent, action), tempAgent, depth)[0]
                if possibleScore > v:
                    v = possibleScore
                    returnAction = action
            return (v, returnAction)
        else:
            #pacman depth
            v = 0
            successors = gameState.getLegalActions(agent)
            for action in successors:
                tempAgent = (agent + 1) % gameState.getNumAgents()
                possibleScore = self.minimax(gameState.generateSuccessor(agent, action), tempAgent, depth)[0]
                v += possibleScore / len(successors)
                   

        return (v, returnAction)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    if currentGameState.isWin():
        isWin = 1
    else:
        isWin = 0
    if currentGameState.isLose():
        isLose = 1
    else:
        isLose = 0
    
    a = 1.5 
    b = 3
    c = 30
    d = 1.5
    e = 1000
    f = -1000
    if newFood.asList():
        minFoodDist = min([util.manhattanDistance(newPos, food) for food in newFood.asList()])
        succScore = currentGameState.getScore()


        return (a * 30 + b*succScore) / (d*minFoodDist + c*len(newFood.asList()) + 1) + e*isWin + f*isLose + 50
    else:
        minFoodDist = 0
    succScore = currentGameState.getScore()


    return (a * 30 + b*succScore) / (d*minFoodDist + c*len(newFood.asList()) + 1) + e*isWin + f*isLose + 50

# Abbreviation
better = betterEvaluationFunction

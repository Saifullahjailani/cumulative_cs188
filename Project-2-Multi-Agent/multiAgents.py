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


from hmac import new
from util import manhattanDistance
from game import Directions
import random
import util

from game import Agent
from pacman import GameState


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
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
        newPos = successorGameState.getPacmanPosition()  # tuple (x,y)
        newFood = successorGameState.getFood()  # weird format
        newFood = newFood.asList()  # list of tuples of each food pellet
        if len(newFood) == 0:  # theres no more food...reached goal state
            return 100
        # going to use distance to nearest food for heuristic, want to incentivize going to food
        distancesToFood = [
            1 / util.manhattanDistance(newPos, x) for x in newFood]
        bestFoodDist = max(distancesToFood)
        

        # also, did we eat pellet? want to incentivize this
        pelletEaten = 0  # assume no, so no points
        if(len(newFood) < len(currentGameState.getFood().asList())):  # this means we ate one
             pelletEaten = 1  # proportional to number of pellets left, maybe this will work?
        # now we need to avoid ghosts
        newGhostStates = successorGameState.getGhostStates()
        ghostPos = [s.getPosition()
                                  for s in successorGameState.getGhostStates()]
        distancesToGhosts = [util.manhattanDistance(
            newPos, x) for x in ghostPos]
        
        # so we want to stay far away from ghosts...give more points for min distance being larger
        worstGhostDist = min(distancesToGhosts)
        if worstGhostDist < 3:
            worstGhostDist = -1
        else: worstGhostDist = 1

        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]  # unused here

        "*** YOUR CODE HERE ***"
        
        return bestFoodDist + pelletEaten + worstGhostDist


def scoreEvaluationFunction(currentGameState: GameState):
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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    



    def getAction(self, gameState: GameState):
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
        Returns the totalScore number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        
        def minimaxHelper(gameState, index, depth):  # returns state with min score
            legalMoves = gameState.getLegalActions(index)
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            score = 100000  # arbitrary big number
            for action in legalMoves:
                if index < gameState.getNumAgents() - 1: #not on last ghost, keep going with recursion to iterate thru ghosts
                    next = index + 1
                    newScore = minimaxHelper(gameState.generateSuccessor(index, action), next, depth)
                    
                else:  # were on last ghost, need to change depth
                    if depth == self.depth: # we are at max depth
                        
                        newScore = self.evaluationFunction(gameState.generateSuccessor(index, action))
                    else:
                        newDepth = depth + 1
                        newScore = findBestAction(gameState.generateSuccessor(index, action), newDepth)
                if score > newScore:
                    score = newScore
            return score


        def findBestAction(gameState, depth):
            # legal moves for pacman, want to return one of these eventually (only if depth = 1 which is starting depth)
            legalMoves = gameState.getLegalActions(0)
            score = -100000  # arbitrary small number
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            nextAction = None
            for action in legalMoves:
                # this helper function recursively calls helper function
                newScore = minimaxHelper(gameState.generateSuccessor(0, action), 1, depth) # index 0 because we are only considering pacman
                if newScore > score:
                    score = newScore
                    nextAction = action
            if depth != 1:  # only want to return action if depth = 1
                return score
            else:
                return nextAction

        return findBestAction(gameState, 1)

   

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #this is very similar to findBestAction above
        #used on pacman moves (max nodes)
        def maxValue(gameState, depth, alpha, beta):
            score = -100000  # arbitrary small number
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            nextAction = None
            legalMoves = gameState.getLegalActions(0)  # 0 because always pacman for max
            for action in legalMoves:
                newScore = minValue(gameState.generateSuccessor(0, action), depth, alpha, beta, 1)
                if newScore > score:
                    score = newScore
                    nextAction = action
                if score > beta: # pseudocode from spec
                    return score
                alpha = max(score, alpha)

            if depth != 1:  # only want to return action if depth = 1
                return score
            else:
                return nextAction


        #used on ghost moves(min nodes)
        def minValue(gameState,depth,alpha,beta, index):
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            legalMoves = gameState.getLegalActions(index)
            score = 100000
            for action in legalMoves:
                #what number ghost are we on?
                if index < gameState.getNumAgents() - 1:
                #if this is true it means we can keep calling minValue on more ghosts
                    newScore = minValue(gameState.generateSuccessor(index, action), depth,alpha,beta, index + 1)

                else:  # were on last ghost, need to change depth
                    if depth == self.depth: # we are at max depth, so were done
                        
                        newScore = self.evaluationFunction(gameState.generateSuccessor(index, action))
                    else:
                        # not at max depth, start a new max node
                        newScore = maxValue(gameState.generateSuccessor(index, action), depth + 1, alpha, beta)
                if score > newScore:  #pseudocode from spec
                    score = newScore
                if score < alpha:
                    return score
                beta = min(beta, score)
            return score
        return maxValue(gameState, 1, -1000, 1000)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        #this is literally same function used for minimax
        def findBestAction(gameState, depth):
            # legal moves for pacman, want to return one of these eventually
            legalMoves = gameState.getLegalActions(0)
            score = -10000  # arbitrary small number
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            nextAction = None
            for action in legalMoves:
                # this helper function recursively calls helper function
                newScore = minimaxHelper(gameState.generateSuccessor(0, action), 1, depth) # index 0 because we are only considering pacman
                if newScore > score:
                    score = newScore
                    nextAction = action
            if depth != 1:  # only want to return action if depth = 1
                return score
            else:
                return nextAction

        #based off pseudocode from lecture
        def minimaxHelper(gameState, index, depth):  # returns score
            legalMoves = gameState.getLegalActions(index)
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            
            totalScore = 0
            for action in legalMoves:
                if index < gameState.getNumAgents() - 1: #not on last ghost, keep going with recursion to iterate thru ghosts
                    score = minimaxHelper(gameState.generateSuccessor(index, action), index + 1, depth)
                    totalScore = totalScore + score / len(legalMoves) # because uniform divide by len and add to total
                    
                else:  # rolling over, need to change depth if not at max
                    if depth == self.depth: # we are at max depth
                        
                        score = self.evaluationFunction(gameState.generateSuccessor(index, action))
                        totalScore = totalScore + score / len(legalMoves) 
                    else:
                        score = findBestAction(gameState.generateSuccessor(index, action), depth + 1)
                        totalScore = totalScore + score / len(legalMoves)
            
            return totalScore
        
        return findBestAction(gameState, 1)
def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: Things to consider (not neccessarily in order of significance)
    1.distance to nearest food want to incentivize going to food.  I actualy didnt use this at all!
        *just going to use manhattan distance, should be good heuristic
    2. also want to incentivize actually eating pellet, not just being close.  needs to outweigh closeness by a little
        *going to try giving points which are dependent on number of pellets.  that way we will have a base amount of points, 
    but if we eat pellet we will get more
    3.  need to avoid ghosts -- v important
        * i think i can use same logic as reflex agent just modified a little bit

    update: so i ended up not using anything besides just avoiding ghosts while incentivisng being near them so i can eat them.
    """
    "*** YOUR CODE HERE ***"
    if currentGameState.isWin():
        
        return 10000000
    pos = currentGameState.getPacmanPosition()  # tuple (x,y)
    food = currentGameState.getFood()  # weird format
    score = currentGameState.getScore()
    food = food.asList()# list of tuples of each food pellet
    

    #ok lets avoid ghosts
    ghostPos = [s.getPosition() for s in currentGameState.getGhostStates()]
    distancesToGhosts = [util.manhattanDistance(pos, x) for x in ghostPos]
        
    # so we want to stay close to ghosts but not too close
    worstGhostDist = min(distancesToGhosts)
    if worstGhostDist < 2: #i dont wanna be closer then 3 moves to ghost
        worstGhostDist = -1 #penalize this
    
    
    return   4 / worstGhostDist +  score    
    
    # by using 4 / worstGhostDist i am actualy incentivizing being near a ghost, which allows for more ghost eating. 
    # The ghost literally just chases me around lol


    

# Abbreviation
better = betterEvaluationFunction

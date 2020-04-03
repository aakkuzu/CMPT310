# search.py
# ---------
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

#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
"""
num_hours_i_spent_on_this_assignment = 9
"""
#
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
"""
Although the approach to AI in this class was not as abstract as I thought it would be,
I do enjoy the different algorithms we see in class and their applications and differences.

"""
#####################################################
#####################################################

"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Q1.1
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print ( problem.getStartState() )
    You will get (5,5)

    print (problem.isGoalState(problem.getStartState()) )
    You will get True

    print ( problem.getSuccessors(problem.getStartState()) )
    You will get [((x1,y1),'South',1),((x2,y2),'West',1)]
    """
    "*** YOUR CODE HERE ***"
    visited = []

    #recursive function for DFS
    def recursiveDFS(node):
        solution = []

        #append visited state
        visited.append(node)
        for theSuccessor, theDirection, theCost in problem.getSuccessors(node):

            #if the successor of state is in the visited list, skip
            if theSuccessor in visited:
                continue
            else:

                #check if this is a goal state
                if problem.isGoalState(theSuccessor) == True:
                    return [theDirection] + solution
                else:

                    #call function recursively on successor of state
                    #and then add their return statements to the list of actions
                    iterativeCall = recursiveDFS(theSuccessor)
                    if type(iterativeCall) == type(None):
                        continue
                    solution.extend(iterativeCall)

                    return [theDirection] + solution

        return None

    path = recursiveDFS(problem.getStartState())

    #making sure that the path is not NONE
    if type(path) == type(None):
        return []
    else:
        return path



    

def breadthFirstSearch(problem):
    """
    Q1.2
    Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    visited = []
    fringe = util.Queue()
    pathsDict = dict()

    #state is enqueued, marked visited
    fringe.push(problem.getStartState())
    pathsDict[problem.getStartState()] = []
    visited.append(problem.getStartState())

    #for each call of this function, make sure that
    #the fringe is not empty
    while fringe.isEmpty() != True:

        #assign path -> state in dictionary
        currentState = fringe.pop()
        currentPath = pathsDict[currentState]

        #check if this is a goal state
        if problem.isGoalState(currentState) == True:
            return pathsDict[currentState]

        for theSuccessor, theDirection, theCost in problem.getSuccessors(currentState):

            #check if we've revisited a state, if so, skip
            if theSuccessor in visited:
                continue

            else:
                #enqueue node, mark it as visited, assign the path
                #of successor to the successor state in dictionary
                fringe.push(theSuccessor)
                pathsDict[theSuccessor] = currentPath + [theDirection]
                visited.append(theSuccessor)

    #return path
    return []




def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """
    Q1.3
    Search the node that has the lowest combined cost and heuristic first."""
    """Call heuristic(s,problem) to get h(s) value."""
    "*** YOUR CODE HERE ***"

    visited = []
    fringe = util.PriorityQueue()
    pathsDict = dict()
    costsDict = dict()

    # state is enqueued, marked visited, cost is set to 0
    fringe.push(problem.getStartState(), heuristic(problem.getStartState(), problem))
    pathsDict[problem.getStartState()] = []
    costsDict[problem.getStartState()] = 0


    # for each call of this function
    while fringe.isEmpty() != True:

        currentState = fringe.pop()
        currentPath = pathsDict[currentState]
        currentCost = costsDict[currentState]

        #mark state as visited
        visited.append(currentState)

        #check if this is a goal state
        if problem.isGoalState(currentState) == True:
            return pathsDict[currentState]

        for theSuccessor, theDirection, theCost in problem.getSuccessors(currentState):
            # check if we've revisited a state, if so, skip
            costtoSuccessor = currentCost + theCost

            #calculate priority by adding heuristic and cost of
            #of movement to successor
            priority = heuristic(theSuccessor, problem) + costtoSuccessor

            #checking if this state is visited
            if theSuccessor in visited:
                continue

            #if it is in the fringe and is not expanded:
            elif theSuccessor in costsDict:
                if costtoSuccessor < costsDict[theSuccessor]:
                    fringe.update(theSuccessor, priority)
                    pathsDict[theSuccessor] = currentPath + [theDirection]
                    costsDict[theSuccessor] = costtoSuccessor

            #if it has had its cost calculated already (expanded)
            else:
                # enqueue node, mark it as visited
                fringe.update(theSuccessor, priority)
                pathsDict[theSuccessor] = currentPath + [theDirection]
                costsDict[theSuccessor] = costtoSuccessor

    #return path
    return []


def priorityQueueDepthFirstSearch(problem):
    """
    Q1.4a.
    Reimplement DFS using a priority queue.
    """
    "*** YOUR CODE HERE ***"

    #the algorithm is the same as the previous DFS,
    #priority calculation is by length of path
    #where longer is higher priority

    visited = []
    fringe = util.PriorityQueue()
    pathsDict = dict()
    costsDict = dict()

    # node is enqueued, marked visited
    fringe.push(problem.getStartState(), 0)
    pathsDict[problem.getStartState()] = []
    costsDict[problem.getStartState()] = 0


    # for each call of this function
    while fringe.isEmpty() != True:

        currentState = fringe.pop()
        currentPath = pathsDict[currentState]
        currentCost = costsDict[currentState]

        visited.append(currentState)

        if problem.isGoalState(currentState) == True:
            return pathsDict[currentState]

        for theSuccessor, theDirection, theCost in problem.getSuccessors(currentState):
            # check if we've revisited a state
            costtoSuccessor = currentCost + theCost
            priority = -len(currentPath + [theDirection])

            if theSuccessor in visited:
                continue


            elif theSuccessor in costsDict:
                if costtoSuccessor < costsDict[theSuccessor]:
                    fringe.update(theSuccessor, priority)
                    pathsDict[theSuccessor] = currentPath + [theDirection]
                    costsDict[theSuccessor] = costtoSuccessor

            else:
                # enqueue node, mark it as visited
                fringe.update(theSuccessor, priority)
                pathsDict[theSuccessor] = currentPath + [theDirection]
                costsDict[theSuccessor] = costtoSuccessor

    return []



def priorityQueueBreadthFirstSearch(problem):
    """
    Q1.4b.
    Reimplement BFS using a priority queue.
    """
    "*** YOUR CODE HERE ***"

    # the algorithm is the same as the previous DFS,
    # priority calculation is by length of path
    # where shorter is higher priority


    visited = []
    fringe = util.PriorityQueue()
    pathsDict = dict()
    costsDict = dict()

    # node is enqueued, marked visited
    fringe.push(problem.getStartState(), 0)
    pathsDict[problem.getStartState()] = []
    costsDict[problem.getStartState()] = 0


    # for each call of this function
    while fringe.isEmpty() != True:

        currentState = fringe.pop()
        currentPath = pathsDict[currentState]
        currentCost = costsDict[currentState]

        visited.append(currentState)

        if problem.isGoalState(currentState) == True:
            return pathsDict[currentState]

        for theSuccessor, theDirection, theCost in problem.getSuccessors(currentState):
            # check if we've revisited a state
            costtoSuccessor = currentCost + theCost
            priority = len(currentPath + [theDirection])

            if theSuccessor in visited:
                continue


            elif theSuccessor in costsDict:
                if costtoSuccessor < costsDict[theSuccessor]:
                    fringe.update(theSuccessor, priority)
                    pathsDict[theSuccessor] = currentPath + [theDirection]
                    costsDict[theSuccessor] = costtoSuccessor

            else:
                # enqueue node, mark it as visited
                fringe.update(theSuccessor, priority)
                pathsDict[theSuccessor] = currentPath + [theDirection]
                costsDict[theSuccessor] = costtoSuccessor

    return []

#####################################################
#####################################################
# Discuss the results of comparing the priority-queue
# based implementations of BFS and DFS with your original
# implementations.

"""
For the DFS and DFS2 implementations, in the outputs there 
were less nodes expanded, which provided efficiency.
For the BFS and BFS2 implementations, I found no difference 
in their output.
"""

#####################################################
#####################################################



# Abbreviations (please DO NOT change these.)
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
bfs2 = priorityQueueBreadthFirstSearch
dfs2 = priorityQueueDepthFirstSearch

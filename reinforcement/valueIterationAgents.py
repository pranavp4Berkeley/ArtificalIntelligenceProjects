# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        maxSoFar = -999999
        total = 0
        for k in range(self.iterations):
            temp_dict = self.values.copy() # temp should be k+1 and self.values should be kth. 
            for state in self.mdp.getStates():
                if self.mdp.isTerminal(state):
                    continue
                for action in self.mdp.getPossibleActions(state): 
                    for nextPair in self.mdp.getTransitionStatesAndProbs(state, action): #(nextState, prob)
                        total += nextPair[1] * (self.mdp.getReward(state, action, nextPair[0]) + self.discount * self.values[nextPair[0]])
                    if total > maxSoFar:
                        maxSoFar = total
                    total = 0
                temp_dict[state] = maxSoFar
                maxSoFar = -999999
                total = 0   
            self.values = temp_dict.copy()

            #have not considered edge case listed in spec


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        total = 0
        for nextPair in self.mdp.getTransitionStatesAndProbs(state, action): #(nextState, prob)
            total += nextPair[1] * (self.mdp.getReward(state, action, nextPair[0]) + self.discount * self.values[nextPair[0]])
        return total



    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        maxSoFar = -9999
        bestAction = None
        total = 0
        if len(self.mdp.getPossibleActions(state)) == 0:
            return None
        for action in self.mdp.getPossibleActions(state):
            total = self.computeQValueFromValues(state, action)
            if total > maxSoFar:
                maxSoFar = total
                bestAction = action
        return bestAction

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        maxSoFar = -999999
        total = 0
        for k in range(self.iterations):
            temp_dict = self.values.copy() # temp should be k+1 and self.values should be kth. 
            state = self.mdp.getStates()[k % len(self.mdp.getStates())]
            if self.mdp.isTerminal(state):
                continue
            for action in self.mdp.getPossibleActions(state): 
                for nextPair in self.mdp.getTransitionStatesAndProbs(state, action): #(nextState, prob)
                    total += nextPair[1] * (self.mdp.getReward(state, action, nextPair[0]) + self.discount * self.values[nextPair[0]])
                if total > maxSoFar:
                    maxSoFar = total
                total = 0
            temp_dict[state] = maxSoFar
            maxSoFar = -999999
            total = 0   
            self.values = temp_dict.copy()

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        #first finding predecessors:

        predecessors = {}
        for state in self.mdp.getStates():
            for action in self.mdp.getPossibleActions(state):
                for nextPair in self.mdp.getTransitionStatesAndProbs(state, action): #(nextState, prob)
                    if nextPair[1] > 0:
                        if nextPair[0] in predecessors:
                            predecessors[nextPair[0]].add(state)
                        else:
                            predecessors[nextPair[0]] = set()
                            predecessors[nextPair[0]].add(state)

        #now the alg

        pq = util.PriorityQueue()
        for state in self.mdp.getStates():
            if not self.mdp.isTerminal(state):
                maxQValue = -999999
                temp = 0 
                for action in self.mdp.getPossibleActions(state):
                    temp = self.computeQValueFromValues(state, action)
                    if temp > maxQValue:
                        maxQValue = temp
                diff = abs(self.values[state] - maxQValue)
                pq.push(state, -diff)

        for iteration in range(self.iterations):
            if pq.isEmpty():
                return 
            state = pq.pop()
            if self.mdp.isTerminal(state):
                continue
            temp_dict = self.values.copy()
            total = 0
            maxSoFar = -99999
            for action in self.mdp.getPossibleActions(state): 
                for nextPair in self.mdp.getTransitionStatesAndProbs(state, action): #(nextState, prob)
                    total += nextPair[1] * (self.mdp.getReward(state, action, nextPair[0]) + self.discount * self.values[nextPair[0]])
                if total > maxSoFar:
                    maxSoFar = total
                total = 0
            temp_dict[state] = maxSoFar
            maxSoFar = -999999
            total = 0   
            self.values = temp_dict.copy()
            for p in predecessors[state]:
                maxQValue = -999999
                temp = 0 
                for action in self.mdp.getPossibleActions(p):
                    temp = self.computeQValueFromValues(p, action)
                    if temp > maxQValue:
                        maxQValue = temp
                diff = abs(self.values[p] - maxQValue)
                if diff > self.theta:
                    pq.update(p, -diff)





                    
                    








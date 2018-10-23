# -*- coding: utf-8 -*-
"""

ROBOT LOCALIZATION ASSIGNMENT

"""


import numpy as np


class HMM():
    """

    This class represents a Hidden Markov Model (HMM), consisting of 
    eight random variables, with the following structure:
    
                    (X1)---(X2)---(X3)---(X4)
                      |      |      |      |
                      |      |      |      |
                    (O1)   (O2)   (O3)   (O4)
                  
    """

    def __init__(self, start, trans, emit):
        """

        This function initiallzes an instance of the HMM class.  
        
        """

        # store the length of the Markov chain
        self.length = 4

        # -------------------------------------------------------------------------
        # YOUR CODE GOES HERE
        #
        self._table = {}
        self._start = start
        self._trans = trans
        self._emit = emit
        
        # construct joint probability table for each non-zero location random variable
        for key0 in start:
            for key1 in trans[key0]:
                for key2 in trans[key1]:
                    for key3 in trans[key2]:
                        val = start[key0] * trans[key0][key1] * \
                        trans[key1][key2] * trans[key2][key3]
                        
                        if val > 0:
                            self._table[(key0, key1, key2, key3)] = val

        #
        # END OF YOUR CODE
        # -------------------------------------------------------------------------    


    def get_cell(self, key):
        """

        This function consults the data structure that represents the HMM and
        returns the value in a particular cell in the joint probability table.
                                                
        Input
        -----
    
        - key: A tuple of locations on the Tic-Tac-Toe board.
                        
        Output
        -----
    
        - val: The probability of that sequence of locations.
        
        """

        val = 0

        # -------------------------------------------------------------------------
        # YOUR CODE GOES HERE
        #
        if key in self._table:
            val = self._table[key]

        #
        # END OF YOUR CODE
        # -------------------------------------------------------------------------    
            
        return val

    def get_emit(self, coord, observation):
        """

        This function consults the data structure that represents the HMM and
        returns the emission probability.
                                                
        Input
        -----
    
        - coord: A tuple of locations on the Tic-Tac-Toe board.
        
        - observation: A tuple of locations on the Tic-Tac-Toe board.
                        
        Output
        -----
    
        - val: The probability of that sequence of locations.
        
        """

        val = 0

        # -------------------------------------------------------------------------
        # YOUR CODE GOES HERE
        #
        if observation in self._emit[coord]:
            val = self._emit[coord][observation]

        #
        # END OF YOUR CODE
        # -------------------------------------------------------------------------    
            
        return val

    def update(self, observations):
        """

        This function updates the data structure that represents the HMM based 
        on the evidence that is observed.
                    
        Input
        -----
    
        - observations: A list of observations.  The first item in the list is 
                        the evidence o1 that is observed at the first time step,
                        the second item in the list is the evidence o2 that is 
                        observed at the second time step, etc.

        """

        # -------------------------------------------------------------------------
        # YOUR CODE GOES HERE
        #
        
        # iterate through each value in the joint probability table
        for each in self._table:
            val = self._table[each]
            
            # only update the probability if there is an observation
            for i in range(self.length):
                if observations[i] != None:
                    val *= self.get_emit(each[i], observations[i])

            if val > 0:
                    self._table[each] = val
        
        # zero out any combinations if they do not align with observations
        for key in self._table:
            if ((observations[0] not in self._emit[key[0]]) and observations[0] != None) or \
            ((observations[1] not in self._emit[key[1]]) and observations[1] != None) or \
            ((observations[2] not in self._emit[key[2]]) and observations[2] != None) or \
            ((observations[3] not in self._emit[key[3]]) and observations[3] != None):
                self._table[key] = 0
            
        self.normalize()
        
        #
        # END OF YOUR CODE
        # -------------------------------------------------------------------------    


    def marginalize(self, axis):
        """

        This function consults the data structure that represents the HMM and
        returns the current probability distribution for one of the 
        random variables in the Markov chain.
                                        
        Input
        -----
    
        - axis: The random variable to be marginalized: 1 for X1, 2 for X2, 
                3 for X3, or 4 for X4
                        
        """

        dist = {}

        # -------------------------------------------------------------------------
        # YOUR CODE GOES HERE
        #
        
        # iterate through all of the cells in the joint probability table
        for key in self._table:

            # get the value in this cell
            val = self.get_cell(key)

            # figure out which key for the marginal distribution is associated with this cell
            key_dist = key[axis - 1]

            # if there is no entry in the marginal distribution for this key, create it
            if key_dist not in dist:
                dist[key_dist] = 0

            # add the value of this cell to the appropriate cell in the marginal distribution
            dist[key_dist] += val

        #
        # END OF YOUR CODE
        # -------------------------------------------------------------------------    

        return dist
        
    def marginalize2(self, axis1, axis2):
        """

        This function consults the data structure that represents the HMM and
        returns the current probability distribution for two of the 
        random variables in the Markov chain.
                                        
        Input
        -----
    
        - axis1: The random variable to be marginalized: 1 for X1, 2 for X2, 
                3 for X3, or 4 for X4
                
        - axis2: The random variable to be marginalized: 1 for X1, 2 for X2, 
                3 for X3, or 4 for X4
                        
        """

        dist = {}

        # -------------------------------------------------------------------------
        # YOUR CODE GOES HERE
        #
        
        # iterate through all of the cells in the joint probability table
        for key in self._table:

            # get the value in this cell
            val = self.get_cell(key)

            # figure out which key for the marginal distribution is associated with this cell
            key_dist = (key[axis1 - 1], key[axis2 - 1])

            # if there is no entry in the marginal distribution for this key, create it
            if key_dist not in dist:
                dist[key_dist] = 0

            # add the value of this cell to the appropriate cell in the marginal distribution
            dist[key_dist] += val

        #
        # END OF YOUR CODE
        # -------------------------------------------------------------------------    

        return dist
    
    def MAP(self, axis):
        """

        This function consults the data structure that represents the HMM and
        returns the most likely value for one of the random variables in the 
        Markov chain.
                                               
        Input
        -----
    
        - axis: The random variable: 1 for X1, 2 for X2, 3 for X3, or 4 for X4

        Output
        -----
    
        - best_loc: A location on the Tic-Tac-Toe board.
                        
        """

        best_loc = None

        # -------------------------------------------------------------------------
        # YOUR CODE GOES HERE
        #
        
        margin = self.marginalize(axis)
        maximum = 0
        
        for key in margin:
            if margin[key] > maximum:
                maximum = margin[key]
                best_loc = key

        #
        # END OF YOUR CODE
        # -------------------------------------------------------------------------    
    
        return best_loc
        

    def MAP_sequence(self):
        """

        This function consults the data structure that represents the HMM and
        returns the most likely sequence of values for the random variables
        in the Markov chain.
                                                        
        Output
        -----
    
        - best_seq: A tuple of locations on the Tic-Tac-Toe board.
                                
        """
        
        best_seq = (None, None, None, None)
    
        # -------------------------------------------------------------------------
        # YOUR CODE GOES HERE
        #
        
        maximum = 0
        
        for key in self._table:
            if self._table[key] > maximum:
                maximum = self._table[key]
                best_seq = key[0:4]

        #
        # END OF YOUR CODE
        # -------------------------------------------------------------------------    

        return best_seq


    def entropy(self, axis):
        """

        This function consults the data structure that represents the HMM and
        returns the entropy of one of the random variables in the Markov chain.
                                        
        Input
        -----
    
        - axis: The random variable: 1 for X1, 2 for X2, 3 for X3, or 4 for X4
                        
        Output
        -----
    
        - val_ent: The entropy of the random variable.

        """

        val_ent = 0

        # -------------------------------------------------------------------------
        # YOUR CODE GOES HERE
        #
        
        margin = self.marginalize(axis)
        
        for key in margin:
            if margin[key] > 0 :
                val_ent += margin[key] * np.log2(1 / margin[key])

        #
        # END OF YOUR CODE
        # -------------------------------------------------------------------------    

        return val_ent
    
    def entropy2(self, axis1, axis2):
        """

        This function consults the data structure that represents the HMM and
        returns the entropy of the intersection of two of the random variables in the Markov chain.
                                        
        Input
        -----
    
        - axis1: The random variable: 1 for X1, 2 for X2, 3 for X3, or 4 for X4

        - axis2: The random variable: 1 for X1, 2 for X2, 3 for X3, or 4 for X4                        
        Output
        -----
    
        - val_ent: The entropy of the random variable.

        """

        val_ent = 0

        # -------------------------------------------------------------------------
        # YOUR CODE GOES HERE
        #
        
        margin = self.marginalize2(axis1, axis2)
        
        for key in margin:
            if margin[key] > 0 :
                val_ent += margin[key] * np.log2(1 / margin[key])

        #
        # END OF YOUR CODE
        # -------------------------------------------------------------------------    

        return val_ent


    def mutual_information(self, axis1, axis2):
        """

        This function consults the data structure that represents the HMM and
        returns the mutual infomration between two of the random variables 
        in the Markov chain.
                                                            
        Input
        -----
    
        - axis1: The first random variable: 1 for X1, 2 for X2, 3 for X3, 
                    or 4 for X4
                        
        - axis2: The second random variable to be marginalized: 1 for X1, 
                2 for X2, 3 for X3, or 4 for X4
                        
        Output
        -----
    
        - val_mi: The mutual information between the two random variables.
        
        """

        val_mi = 0

        # -------------------------------------------------------------------------
        # YOUR CODE GOES HERE
        #
        
        val_mi = self.entropy(axis1) + self.entropy(axis2) - self.entropy2(axis1, axis2)
        
        #
        # END OF YOUR CODE
        # -------------------------------------------------------------------------    

        return val_mi
    
    
    def total(self):
    
        tot = 0
    
        for key in self._table:
            tot += self.get_cell(key)

        return tot


    def normalize(self):
    
        tot = self.total()

        for key in self._table:
            self._table[key] = self.get_cell(key) / tot


def main():
    # HMM for the Tic-Tac-Toe version of Robot Localization

    # START PROBABILITIES (priors for the possible locations at the first time step)
    robot_start = {(0, 0): 0.1, (0, 1): 0.1, (0, 2): 0.1, (1, 0): 0.1, (1, 1): 0.2, 
                   (1, 2): 0.1, (2, 0): 0.1, (2, 1): 0.1, (2, 2): 0.1}        

    # TRANSITION PROBABILITIES (only UP, RIGHT, STAY have positive probability)
    robot_trans = {(0, 0): {(0, 1): 0.45, (2, 0): 0.45, (0, 0): 0.1}, 
                   (0, 1): {(0, 1): 0.1, (2, 1): 0.45, (0, 2): 0.45}, 
                   (0, 2): {(2, 2): 0.45, (0, 0): 0.45, (0, 2): 0.1}, 
                   (1, 0): {(0, 0): 0.45, (1, 0): 0.1, (1, 1): 0.45}, 
                   (1, 1): {(1, 2): 0.45, (1, 1): 0.1, (0, 1): 0.45},
                   (1, 2): {(1, 2): 0.1, (1, 0): 0.45, (0, 2): 0.45}, 
                   (2, 0): {(2, 0): 0.1, (1, 0): 0.45, (2, 1): 0.45}, 
                   (2, 1): {(1, 1): 0.45, (2, 1): 0.1, (2, 2): 0.45}, 
                   (2, 2): {(2, 0): 0.45, (1, 2): 0.45, (2, 2): 0.1}} 

    # EMISSION PROBABILITIES 
    robot_emit = {(0, 0): {(0, 1): 0.15, (2, 0): 0.15, (1, 0): 0.15, (0, 0): 0.4, (0, 2): 0.15}, 
                  (0, 1): {(0, 1): 0.4, (0, 0): 0.15, (0, 2): 0.15, (2, 1): 0.15, (1, 1): 0.15}, 
                  (0, 2): {(1, 2): 0.15, (0, 1): 0.15, (0, 0): 0.15, (0, 2): 0.4, (2, 2): 0.15}, 
                  (1, 0): {(1, 2): 0.15, (2, 0): 0.15, (1, 0): 0.4, (0, 0): 0.15, (1, 1): 0.15}, 
                  (1, 1): {(1, 2): 0.15, (0, 1): 0.15, (1, 0): 0.15, (1, 1): 0.4, (2, 1): 0.15},
                  (1, 2): {(1, 2): 0.4, (1, 1): 0.15, (1, 0): 0.15, (0, 2): 0.15, (2, 2): 0.15}, 
                  (2, 0): {(2, 0): 0.4, (1, 0): 0.15, (0, 0): 0.15, (2, 1): 0.15, (2, 2): 0.15}, 
                  (2, 1): {(0, 1): 0.15, (2, 0): 0.15, (1, 1): 0.15, (2, 1): 0.4, (2, 2): 0.15}, 
                  (2, 2): {(1, 2): 0.15, (2, 0): 0.15, (0, 2): 0.15, (2, 1): 0.15, (2, 2): 0.4}} 
    
                
    robot = HMM(robot_start, robot_trans, robot_emit)

    # Some of the Questions from Part 1

    print("")
    print("PART 1")

    # Question 2
    print("Entropy of X1:")
    print("My Answer = ", robot.entropy(1))

    # Question 3
    print("Entropy of X4:")
    print("My Answer = ", robot.entropy(4))

    # Question 5
    print("Mutual Information between X1 and X2:")
    print("My Answer = ", robot.mutual_information(1, 2))

    # Question 6
    print("Mutual Information between X1 and X4:")
    print("My Answer = ", robot.mutual_information(1, 4))


    # The Questions from Part 2

    print("")
    print("PART 2")

    # TEST DATA - list of Observations at the four time steps
    robot_obs = [(1, 0), (0, 2), (2, 2), (0, 2)]
    #expected_MAPs = ((1, 1), (0, 1), (0, 2), (2, 2))
    #expected_MAP_sequence = ((1, 2), (0, 2), (2, 2), (1, 2))

    # REAL DATA - list of Observations for Part 2 of Final Project
    #robot_obs = [(1, 0), (2, 1), (2, 0), (1, 1)]

    robot.update(robot_obs)

    # Question 1
    for cnt in range(1, robot.length + 1):
        print("MAP estimate for X", cnt, ":")
        print("My Answer =       ", robot.MAP(cnt))

    # Question 2
    print("MAP sequence:")
    print("My Answer =       ", robot.MAP_sequence())


    # The Questions from Part 3 (Do Over)

    print("")
    print("PART 3")

    # have to reinitialize since starting over with new data
    robot = HMM(robot_start, robot_trans, robot_emit)
    
    # TEST DATA - list of Observations at the four time steps, with one missing
    robot_obs = [(1, 0), (0, 2), None, (0, 2)]
    #expected_MAPs = ((1, 1), (0, 1), (0, 2), (0, 2))
    #expected_MAP_sequence = ((1, 0), (0, 0), (0, 1), (0, 2))

    # REAL DATA - list of Observations for Part 3 of Final Project
    #robot_obs = [(1, 0), (2, 1), None, (1, 1)]

    robot.update(robot_obs)    

    # Question 1
    for cnt in range(1, robot.length + 1):
        print("MAP estimate for X", cnt, ":")
        print("My Answer =       ", robot.MAP(cnt))

    # Question 2
    print("MAP sequence:")
    print("My Answer =       ", robot.MAP_sequence())


if __name__ == '__main__':
    main()


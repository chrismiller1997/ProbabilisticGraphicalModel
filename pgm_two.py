# -*- coding: utf-8 -*-
"""

PGM TWO ASSIGNMENT (aka CONDITIONALIZE WITH CLASSES ASSIGNMENT)

"""

class PGM2():
    """

    This class represents a probabilistic graphical model (PGM), consisting of 
    two random variables, with the following structure:
    
                    (N0)
                     | 
                     |   
                    (N1)
                  
    """

    def __init__(self, node_0, edge_0_1):
        """

        This function initiallzes an instance of the PGM2 class.  It takes as 
        input one node potentiol (for node N0) and one edge potential (for the edge
        from N0 to N1).  And it initializes a data structure that represents the PGM.  
        The data structure that you use, and how you use it, is up to you.  My 
        recommendation is to pick a data structure that allows you to represent the 
        joint probability table for the PGM.
        
        Input
        -----
    
        - node_0: A prior probability distribution represented as a Python dictionary; 
                node_0[h] gives the (unconditional) probability that h is the value
                of N0.

        - edge_0_1: A set of conditional probability distributions represented as 
                a Python dictionary of dictionaries; edge_0_1[h][e] gives the 
                (conditional) probability that e is value of N1 given that
                h is the value of N0 (i.e., edge_0_1[h][e] equals P(N1 = e | N0 = h).

        """

        # -------------------------------------------------------------------------
        # YOUR CODE GOES HERE
        #
        #self._joint = edge_0_1
        self._table = {}
        
        # calculate the intersection of h and e using the simple product rule
        for h in node_0:
            for e in edge_0_1[h]:
                self._table[(h, e)] = node_0[h] * edge_0_1[h][e]
                
        #
        # END OF YOUR CODE
        # -------------------------------------------------------------------------    


    def get_cell(self, key):
        """

        This function returns the value in a particular cell of the joint 
        probability table for the PGM.
                                
        Input
        -----
    
        - key: A tuple of possible values of the two random variables in the 
                PGM.  For instance, ('POX', 'NOSPOTS').
                
        Output
        -----
    
        - val: The value in the cell of the joint probability table indicated by 
                key.  val is set to 0 if there is no such cell.
                
        """

        val = 0

        # -------------------------------------------------------------------------
        # YOUR CODE GOES HERE
        #
        
        #h = key[0]
        #e = key[1]

        val = self._table[(key[0], key[1])]

            
        #
        # END OF YOUR CODE
        # -------------------------------------------------------------------------    

        return val


    def update(self, observed, axis):
        """

        This function updates the data structure that represents the PGM based 
        on the evidence e that is observed.
                
        Input
        -----
    
        - observed: The evidence e that is observed.

        - axis: The random variable from which e was observed: 0 or 1
        
        Note that we have to send axis because two different random variables
        could have some of the same possible values.
                        
        """

        # -------------------------------------------------------------------------
        # YOUR CODE GOES HERE
        #
        total = 0
        
        # zero out irrelevant data and calculate total for observed sample
        for each in self._table:
            if (axis == 1 and each[1] != observed) or (axis == 0 and each[0] != observed):
                self._table[each] = 0
            else:
                total += self._table[each]
        
        # normalize the revelant data
        for each in self._table:
            if (axis == 1 and each[1] == observed) or (axis == 0 and each[0] == observed):
                self._table[each] = self._table[each] / total

        #
        # END OF YOUR CODE
        # -------------------------------------------------------------------------    


    def marginalize(self, axis):
        """

        This function consults the data structure that represents the PGM and
        returns the current probability distribution for one of the two 
        random variables.
                        
        Input
        -----
    
        - axis: The random variable to be marginalized: 0 or 1
        
        Output
        -----
    
        - dist: If x is the value of axis, dist is the current probability 
                distribution for random variable Nx represented as a Python
                dictionary.
                
        """
           
        dist = {}

        # -------------------------------------------------------------------------
        # YOUR CODE GOES HERE
        #
        
        # get relevant data based on the given random variable
        for i in self._table:
            if axis == 0:
                if i[0] in dist:
                    dist[i[0]] += self._table[i]
                else:
                    dist[i[0]] = self._table[i]
            else:
                if i[1] in dist:
                    dist[i[1]] += self._table[i]
                else:
                    dist[i[1]] = self._table[i]


        #
        # END OF YOUR CODE
        # -------------------------------------------------------------------------    

        return dist


def conditionalize(prior, conditional, observed):
    """

    This function takes an agent's prior probability distribution and (using the
    agent's likelihoods) conditionalizes on an observed datum to produce a 
    posterior probability distribution.

    Note: This function impletements the Master Method.

    Input
    -----

    - prior: A prior probability distribution represented as a Python dictionary; 
            prior[e] gives the (unconditional) probability that e is the outcome.

    - conditional: A set of conditional probability distributions represented as 
            a Python dictionary of dictionaries; conditional[h][e] gives the 
            (conditional) probability that e is the evidence that is observed given 
            that hypothesis h is true (i.e., conditional[h][e] equals P(e | h).

    - observed: The evidence e that is observed.

    Output
    -----

    - posterior: A posterior probability distribution represented as a Python dictionary.

    """

    # construct joint probability table (Step 1 of Master Method)
    joint = PGM2(prior, conditional)
    #print(joint.get_cell(('POX', 'NOSPOTS')))

    # update joint probability table after observing value of N1 (Steps 2 and 3 of Master Method)
    joint.update(observed, 1)

    # marginalize to get probability distribution for N0 (Step 4 of Master Method)
    posterior = joint.marginalize(0)

    return posterior


def main():

    # Chicken Pox inference

    chicken_pox_prior = {'NOPOX': 0.9, 'POX': 0.1}
    chicken_pox_spots_conditional = {'NOPOX': {'NOSPOTS': 0.999, 'SPOTS': 0.001}, 'POX': {'NOSPOTS': 0.2, 'SPOTS': 0.8}}

    print("The doctor's prior regarding chicken pox is ", chicken_pox_prior) 

    print("Suppose that the patient has spots.")
    chicken_pox_posterior = conditionalize(chicken_pox_prior, chicken_pox_spots_conditional, 'SPOTS')

    print("My Answer:")
    print("The doctor's posterior regarding chicken pox is ", chicken_pox_posterior) 

    print("Expected Answer:")
    print("The doctor's posterior regarding chicken pox is ", {'NOPOX': 0.011, 'POX': 0.989}) 
    print("")

    # Firefly inference

    firefly_prior = {'Good': 1/3, 'Bad': 1/3, 'Ugly': 1/3}
    firefly_flash_conditional = {'Good': {'YELLOW': 1, 'WHITE': 0}, 'Bad': {'YELLOW': 1, 'WHITE': 0}, 'Ugly': {'YELLOW': 0, 'WHITE': 1}}

    print("The male firefly's prior is ", firefly_prior) 

    print("Suppose that he sees a Yellow flash.")
    firefly_posterior = conditionalize(firefly_prior, firefly_flash_conditional, 'YELLOW')

    print("My Answer:")
    print("The male firefly's posterior is ", firefly_posterior) 

    print("Expected Answer:")
    print("The male firefly's posterior is ", {'Good': 0.500, 'Bad': 0.500, 'Ugly': 0.000}) 
    print("")
    
if __name__ == '__main__':
    main()


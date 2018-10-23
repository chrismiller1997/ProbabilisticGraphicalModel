# -*- coding: utf-8 -*-
"""

PROBABILISTIC GRAPHICAL MODEL with THREE NODES ASSIGNMENT

"""

class PGM3():
    """

    This class represents a probabilistic graphical model (PGM), consisting of 
    three random variables, with the following structure:
    
                    (N0)
                    /  \
                   /    \
                 (N1)   (N2)
                  
    """

    def __init__(self, node_0, edge_0_1, edge_0_2):
        """

        This function initiallzes an instance of the PGM3 class.  It takes as 
        input one node potentiol (for node N0) and two edge potentials (for the two
        edges).  And it initializes a data structure that represents the PGM.  
        The data structure that you use, and how you use it, is up to you.  My 
        recommendation is to pick a data structure that allows you to represent the 
        joint probability table for the PGM.
        
        Input
        -----
    
        - node_0: A prior probability distribution represented as a Python dictionary; 
                node0[h] gives the (unconditional) probability that h is the value
                of N0.

        - edge_0_1: A set of conditional probability distributions represented as 
                a Python dictionary of dictionaries; edge1[h][e] gives the 
                (conditional) probability that e is value of N1 given that
                h is the value of N1 (i.e., node1[h][e] equals P(N1 = e | N0 = h).

        - edge_0_2: Just like edge1 except that it is the edge potential for the edge
                connecting N0 and N2 rather than for the edge connecting N0 and N1.
                
        """

        # -------------------------------------------------------------------------
        # YOUR CODE GOES HERE
        #
        self._table = {}
        
        for h in node_0:
            for e1 in edge_0_1[h]:
                for e2 in edge_0_2[h]:
                    #print((h, e1, e2))
                    self._table[(h, e1, e2)] = node_0[h] * edge_0_1[h][e1] * edge_0_2[h][e2]
                    #print(self._table[(h, e1, e2)])


        #
        # END OF YOUR CODE
        # -------------------------------------------------------------------------    


    def get_cell(self, key):
        """

        This function returns the value in a particular cell of the joint 
        probability table for the PGM.
                                
        Input
        -----
    
        - key: A tuple of possible values of the three random variables in the 
                PGM.  For instance, ('POX', 'NOSPOTS', 'FEVER').
                
        Output
        -----
    
        - val: The value in the cell of the joint probability table indicated by 
                key.  val is set to 0 if there is no such cell.
                
        """

        val = 0

        # -------------------------------------------------------------------------
        # YOUR CODE GOES HERE
        #
        val = self._table[(key[0], key[1], key[2])]

            
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

        - axis: The random variable from which e was observed: 0, 1, or 2
        
        Note that we have to send axis because two different random variables
        could have some of the same possible values.
                        
        """

        # -------------------------------------------------------------------------
        # YOUR CODE GOES HERE
        #
        total = 0
        
        # zero out irrelevant data and calculate total for observed sample
        for each in self._table:
            if (axis == 1 and each[1] != observed) or (axis == 0 and each[0] != observed) or (axis == 2 and each[2] != observed):
                self._table[each] = 0
            else:
                total += self._table[each]
                
        # normalize the revelant data
        for each in self._table:
            if (axis == 1 and each[1] == observed) or (axis == 0 and each[0] == observed) or (axis == 2 and each[2] == observed):
                self._table[each] = self._table[each] / total


        #
        # END OF YOUR CODE
        # -------------------------------------------------------------------------    

    def marginalize(self, axis):
        """

        This function consults the data structure that represents the PGM and
        returns the current probability distribution for one of the three 
        random variables.
                        
        Input
        -----
    
        - axis: The random variable to be marginalized: 0, 1, or 2
        
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
            elif axis == 1:
                if i[1] in dist:
                    dist[i[1]] += self._table[i]
                else:
                    dist[i[1]] = self._table[i]
            else:
                if i[2] in dist:
                    dist[i[2]] += self._table[i]
                else:
                    dist[i[2]] = self._table[i]


        #
        # END OF YOUR CODE
        # -------------------------------------------------------------------------    

        return dist

        
def main():

    # the priors and the likelihoods for the Chicken Pox example
    chicken_pox_prior = {'NOPOX': 0.9, 'POX': 0.1}
    chicken_pox_spots_conditional = {'NOPOX': {'NOSPOTS': 0.999, 'SPOTS': 0.001}, 'POX': {'NOSPOTS': 0.2, 'SPOTS': 0.8}}
    chicken_pox_fever_conditional = {'NOPOX': {'NOFEVER': 0.95, 'FEVER': 0.05}, 'POX': {'NOFEVER': 0.4, 'FEVER': 0.6}}

    # in the Chicken Pox example, infer Pox from Spots and Fever
    print("")
    print("Example #1: Inferring Pox from Spots and Fever ...")
    print("")

    # create a joint probability table (Step 1 of the Master Method)
    chicken_pox = PGM3(chicken_pox_prior, chicken_pox_spots_conditional, chicken_pox_fever_conditional)
    
    print("My Answer:")
    print("The doctor's prior regarding chicken pox is ", chicken_pox.marginalize(0)) 
    print("Expected Answer:")
    print("The doctor's prior regarding chicken pox is ", {'NOPOX': 0.9, 'POX': 0.1}) 
    print("")
    
    # update the joint probability table based on the evidenece (Steps 2 and 3 of the Master Method)
    print("Suppose that the patient has spots.")
    chicken_pox.update('SPOTS', 1)
    print("Suppose that the patient has fever as well.")
    chicken_pox.update('FEVER', 2)
    print("")

    # marginalize to find the probability of the variable of interest (Step 4 of the Master Method)
    print("My Answer:")
    print("The doctor's posterior regarding chicken pox is ", chicken_pox.marginalize(0)) 
    print("Expected Answer:")
    print("The doctor's posterior regarding chicken pox is ", {'NOPOX': 0.001, 'POX': 0.999}) 
    print("")


    # in the Chicken Pox example, infer Fever from Spots
    print("")
    print("Example #2: Inferring Fever from Spots ...")
    print("")

    # create a joint probability table (Step 1 of the Master Method)
    chicken_pox = PGM3(chicken_pox_prior, chicken_pox_spots_conditional, chicken_pox_fever_conditional)
    
    print("My Answer:")
    print("The doctor's prior regarding fever is ", chicken_pox.marginalize(2)) 
    print("Expected Answer:")
    print("The doctor's prior regarding fever is ", {'NOFEVER': 0.895, 'FEVER': 0.105}) 
    print("")
    
    # update the joint probability table based on the evidenece (Steps 2 and 3 of the Master Method)
    print("Suppose that the patient has spots.")
    chicken_pox.update('SPOTS', 1)
    print("")

    # marginalize to find the probability of the variable of interest (Step 4 of the Master Method)
    print("My Answer:")
    print("The doctor's posterior regarding fever is ", chicken_pox.marginalize(2)) 
    print("Expected Answer:")
    print("The doctor's posterior regarding fever is ", {'NOFEVER': 0.406, 'FEVER': 0.594}) 
    print("")


    temp3_prior = {'HOT': 0.4, 'JUST_RIGHT': 0.2, 'COLD': 0.4}
    temp3_sales_conditional = {'HOT': {'HIGH': 0.6, 'MEDIUM': 0.2, 'LOW': 0.2}, 'JUST_RIGHT': {'HIGH': 0.3, 'MEDIUM': 0.4, 'LOW': 0.3}, 'COLD': {'HIGH': 0.2, 'MEDIUM': 0.3, 'LOW': 0.5}}
    temp3_crime_conditional = {'HOT': {'HIGH': 0.4, 'MEDIUM': 0.3, 'LOW': 0.3}, 'JUST_RIGHT': {'HIGH': 0.2, 'MEDIUM': 0.6, 'LOW': 0.2}, 'COLD': {'HIGH': 0.1, 'MEDIUM': 0.2, 'LOW': 0.7}}

    # in an expanded version the Ice Cream example, infer Ice Cream Sales from Crime
    print("")
    print("Example #3: Inferring Ice Cream Sales from Crime ...")
    print("")

    # create a joint probability table (Step 1 of the Master Method)
    temp3 = PGM3(temp3_prior, temp3_sales_conditional, temp3_crime_conditional)
    
    print("My Answer:")
    print("The city manager's prior regarding ice cream sales is ", temp3.marginalize(1)) 
    print("Expected Answer:")
    print("The city manager's prior regarding ice cream sales is ", {'HIGH': 0.38, 'MEDIUM': 0.28, 'LOW': 0.34}) 
    print("")
    
    # update the joint probability table based on the evidenece (Steps 2 and 3 of the Master Method)
    print("Suppose that crime is high.")
    temp3.update('HIGH', 2)
    print("")

    # marginalize to find the probability of the variable of interest (Step 4 of the Master Method)
    print("My Answer:")
    print("The city manager's posterior regarding ice cream sales is ", temp3.marginalize(1)) 
    print("Expected Answer:")
    print("The city manager's posterior regarding ice cream sales is ", {'HIGH': 0.483, 'MEDIUM': 0.250, 'LOW': 0.267}) 
    print("")


    print("")
    print("Extra Example #1: The original Ice Cream example from the Quiz ...")
    print("")

    temp_prior = {'HOT': 0.5, 'COLD': 0.5}
    temp_sales_conditional = {'HOT': {'HIGH': 0.8, 'LOW': 0.2}, 'COLD': {'HIGH': 0.2, 'LOW': 0.8}}
    temp_crime_conditional = {'HOT': {'HIGH': 0.6, 'LOW': 0.4}, 'COLD': {'HIGH': 0.1, 'LOW': 0.9}}

    temp = PGM3(temp_prior, temp_sales_conditional, temp_crime_conditional)

    print("Priors for the three variables:")
    print(temp.marginalize(0))
    print(temp.marginalize(1))
    print(temp.marginalize(2))
    print("")

    print("Suppose that crime is high.")
    temp.update('HIGH', 2)
    print("")

    print("Posteriors for the three variables:")
    print(temp.marginalize(0))
    print(temp.marginalize(1))
    print(temp.marginalize(2))
    print("")

    print("")
    print("Extra Example #2: The Wealth-Car-Heart example from the Lecture ...")
    print("")

    wealth_prior = {'POOR': 0.75, 'RICH': 0.25}
    wealth_car_conditional = {'POOR': {'CHEAP': 0.95, 'PRICEY': 0.05}, 'RICH': {'CHEAP': 0.2, 'PRICEY': 0.8}}
    wealth_heart_conditional = {'POOR': {'UNHEALTHY': 0.5, 'HEALTHY': 0.5}, 'RICH': {'UNHEALTHY': 0.3, 'HEALTHY': 0.7}}

    wealth = PGM3(wealth_prior, wealth_car_conditional, wealth_heart_conditional)

    print("Priors for the three variables:")
    print(wealth.marginalize(0))
    print(wealth.marginalize(1))
    print(wealth.marginalize(2))
    print("")

    print("Suppose that Tim has a pricy car.")
    wealth.update('PRICEY', 1)
    print("")

    print("Posteriors for the three variables:")
    print(wealth.marginalize(0))
    print(wealth.marginalize(1))
    print(wealth.marginalize(2))
    print("")

if __name__ == '__main__':
    main()
        


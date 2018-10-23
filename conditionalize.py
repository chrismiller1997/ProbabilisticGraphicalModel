2# -*- coding: utf-8 -*-
"""

CONDITIONALIZE ASSIGNMENT

"""


def conditionalize(prior, conditional, observed):
    """

    This function takes an agent's prior probability distribution and (using the
    agent's likelihoods) conditionalizes on an observed datum to produce a 
    posterior probability distribution.

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

    posterior = {}
    

    # -------------------------------------------------------------------------
    # YOUR CODE GOES HERE
    #
    probE = 0
    
    # Calculating the probability of the observation using the Law of Total Probability
    for h in prior:
        probE += prior[h] * conditional[h][observed]
    
    # Calculating the conditional probability using Bayes' Theorem
    for h in prior:
        posterior[h] = conditional[h][observed] * prior[h] / probE

    #
    # END OF YOUR CODE
    # -------------------------------------------------------------------------    

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


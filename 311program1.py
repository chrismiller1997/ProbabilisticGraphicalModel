"""

Name:   Chris Miller
Date:   01/25/2018
Class:  ISTA 311

"""

# routine/function that returns H or T given a coin probability dictionary 
def coin_flip(coin):
    import random
    
    hRange = [0, coin['heads']] # probability of H range endpoints
    tRange = [coin['heads'], coin['heads'] + coin['tails']] # same for T
    
    # random number from 0 to 1
    randVal = random.uniform(0, coin['heads'] + coin['tails'])
    
    # random number to outcome: 0 < H <= 0.4 < T <= 1
    if randVal > hRange[0] and randVal <= hRange[1]:
        return 'H'
    elif randVal > tRange[0] and randVal <= tRange[1]:
        return 'T'
    else:
        return 'Error'
    
# function that counts the number of H in a row from a sequence of H or T
def count_heads(sequence, numH):
    count = 0
    target = 'H' * numH
    
    # count each time the sequence includes the target
    for trial in range(len(sequence) - numH + 1):
        if sequence[trial:trial + numH] == target:
            count += 1
            
    return count
    
# creates coin dictionary, 'flips' coin 1000 times, analyzes data, plots data
def main():
    import matplotlib.pyplot as plt
    
    numFlips = 1000
    
    # create dictionary
    biasedCoin = {'heads': 0.4, 'tails': 0.6}
    
    # loop routine 1000 times
    result = ''
    
    for each in range(numFlips):
        result += coin_flip(biasedCoin) # appends result of the coin flip
    
    # analyze data (count sequences found)
    countH = count_heads(result, 1)
    countHH = count_heads(result, 2)
    countHHH = count_heads(result, 3)
    countHHHH = count_heads(result, 5)
    
    # plot results
    plt.bar(1, countH, label='# of H = ' + str(countH))
    plt.bar(2, countHH, label='# of HH = ' + str(countHH))
    plt.bar(3, countHHH, label='# of HHH = ' + str(countHHH))
    plt.bar(4, countHHHH, label='# of HHHHH = ' + str(countHHHH))
            
    plt.axis([0, 5, 0, numFlips])
    plt.ylabel('Count')
    plt.xlabel('# of H in a Row')
    plt.title('Results of 1000 flips')
    plt.legend()
    plt.show()
    
main()

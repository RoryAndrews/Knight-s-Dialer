# A logarithmic solution to the Knight's Dialer problem mentioned here:
# https://medium.com/@alexgolec/google-interview-questions-deconstructed-the-knights-dialer-f780d516f029

import numpy as np
import sys
from timeit import default_timer as timer

# Uses a fibonacci sequence approach to compute matrices that "add" up towards 
# the final matrix. Each row and column reprents the count of all sequences
# that start on that row's number and end with that columns number.
# Adding up a row gives the total possible sequences.
def count_sequences(start_position, num_hops):
    sequence_count = initial_sequence()
    last_hops = 0
    current_hops = 1
    hopslist = [1, 2] # Will contain fibonacci numbers, represents the number of hops at the same index of sequence_count

    while hopslist[current_hops] < num_hops:
        newhops = hopslist[current_hops] + hopslist[last_hops]
        if newhops > num_hops:
            last_hops = last_hops - 1 # Goes down list until small enough to add without going over.
        else:
            hopslist.append(newhops)
            sequence_count.append(develop_sequence(sequence_count[current_hops], sequence_count[last_hops]))
            last_hops = last_hops + 1
            current_hops = current_hops + 1

    return np.sum(sequence_count[current_hops][start_position])

# Initializes first two matrices where N = 1 and N = 2
def initial_sequence():
    sequence_count = list()
    sequence_ends = np.zeros((10,10), dtype='object')
    # Each row contains the count of possible ending numbers produced if starting from the number equal to the row.
    sequence_ends[0][4] = 1 # 0 can lead to both 4 and 6
    sequence_ends[0][6] = 1
    sequence_ends[1][8] = 1 # 1 can lead to both 8 and 6
    sequence_ends[1][6] = 1
    sequence_ends[2][7] = 1
    sequence_ends[2][9] = 1
    sequence_ends[3][4] = 1
    sequence_ends[3][8] = 1
    sequence_ends[4][3] = 1
    sequence_ends[4][9] = 1
    sequence_ends[4][0] = 1
    sequence_ends[6][0] = 1
    sequence_ends[6][7] = 1
    sequence_ends[6][1] = 1
    sequence_ends[7][6] = 1
    sequence_ends[7][2] = 1
    sequence_ends[8][1] = 1
    sequence_ends[8][3] = 1
    sequence_ends[9][2] = 1
    sequence_ends[9][4] = 1
    sequence_count.append(sequence_ends)
    sequence_count.append(develop_sequence(sequence_ends, sequence_ends)) # Calculates what ending numbers would result for 1 + 1 hops
    return sequence_count

#Takes two matrices which have been calculated for N and M hops and produces a matrix for N + M hops
def develop_sequence(basis, extension, dimensions = 10):
    new_sequence = np.zeros_like(basis)

    for row in range(dimensions):
        for col in range(dimensions):
            new_sequence[row] += basis[row][col] * extension[col]

    return new_sequence






############################################################
# Code below from 
# https://medium.com/@alexgolec/google-interview-questions-deconstructed-the-knights-dialer-f780d516f029
# https://gist.github.com/alexgolec/50d120cac9c419dfecfe077d040ff5a5#file-dynamic_programming-py
NEIGHBORS_MAP = {
    1: (6, 8),
    2: (7, 9),
    3: (4, 8),
    4: (3, 9, 0),
    5: tuple(),  # 5 has no neighbors
    6: (1, 7, 0),
    7: (2, 6),
    8: (1, 3),
    9: (2, 4),
    0: (4, 6),
}
def neighbors(position):
    return NEIGHBORS_MAP[position]

def count_sequences_linear(start_position, num_hops):
    prior_case = [1] * 10                                     
    current_case = [0] * 10                                   
    current_num_hops = 1                                      
                                                              
    while current_num_hops <= num_hops:                       
        current_case = [0] * 10                               
        current_num_hops += 1                                 
                                                              
        for position in range(0, 10):                         
            for neighbor in neighbors(position):              
                current_case[position] += prior_case[neighbor]
        prior_case = current_case                             
                                                              
    return current_case[start_position]
############################################################



if __name__ == '__main__':
    hops = 10
    start_num = 1
    if len(sys.argv) >= 3:
        start_num = int(sys.argv[1])
        hops = int(sys.argv[2])

    print("Logarithmic solution:")
    start = timer()
    print(count_sequences(start_num, hops))
    end = timer()
    print("Time: {:f}".format(end - start))

    print("Article's linear solution:")
    start = timer()
    print(count_sequences_linear(start_num, hops))
    end = timer()
    print("Time: {:f}".format(end - start))
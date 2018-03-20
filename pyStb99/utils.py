'''
Created on 20 mars 2018

@author: christophemorisset
'''

import numpy as np

def fill_from_file(N, open_file, dtype = np.float64):
    """
    Read N elements from an already open file and put them to a numpy array.
    The elements don't need to be in rectangular form, e.g. the following 10 elements can be read:
    1 2 3 4
    2 3 4 5
    2 4
    """
    i = 0
    res = np.zeros(N, dtype = dtype)
    for line in iter(open_file):
        tab = line.split()
        for elem in tab:
            res[i] = dtype(elem)
            i += 1
            if i >= N:
                return(res)
    return(res)

def write_cols(tab, N, open_file):
    """
    Write an array into an already open file, using N columns
    """
    for i, elem in enumerate(tab):
        open_file.write('{0} '.format(elem))
        if i%N == (N-1):
            open_file.write('\n')

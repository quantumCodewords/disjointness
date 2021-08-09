import numpy as np

import stabilizer
import operator_utils as util

class Paulis(object):
    '''
    Object representing pauli operators for a stabilizer code
    '''
    def __init__(self, *args, **kwargs):
        '''
        Initialize a Pauli group.  There are two ways to do so.
        :param stabilizer: A stabilizer object.  If this is passed in, the pauli group
        will represent all of the logical pauli operators of the stabilizer
        :param file: A file representing a set of pauli operators.  Should be in the 
        same format as Stabilizer generator
        '''
        stabilizer = kwargs.get("stabilizer", None)
        if stabilizer != None:
            self.pauli_operators = stabilizer.get_logical_paulis()
        
        file = kwargs.get("file", "")
        if file != "":
            pauli_matrix = np.loadtxt(file)
            self.pauli_operators = [pauli_matrix[i, :] for i in range(pauli_matrix.shape[0])]
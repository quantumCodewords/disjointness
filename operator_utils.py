import numpy as np

'''
A collection of useful functions used throughout the package
'''

def to_binary(number: int, width: int):
    temp_number = number
    output_array = np.zeros(width)
    idx = 0
    while(temp_number > 0):
        if(temp_number % 2 != 0):
            output_array[idx] = 1
        idx += 1
        temp_number = temp_number//2
    return output_array

def commutes(A, B):
    '''
    Assumes that A and B are proper pauli operators and have the same size
    :param A: The binary symplectic form of a pauli operator
    :param B: The binary symplectic form of a pauli operator
    :returns True if the operators corresponding to A and B commute 
    '''
    #Assert: len(A) == len(B)
    num_qubits = len(A)//2
    x_A = A[:num_qubits]
    z_A = A[num_qubits:]
    x_B = B[:num_qubits]
    z_B = B[num_qubits:]

    cumulative_phase = np.prod(np.power(-1, np.logical_and(x_A, z_B))) * np.prod(np.power(-1, np.logical_and(x_B,z_A))) 
    if(cumulative_phase == 1):
        return True
    return False

def into_weight(s):
    output_len = len(s)//2
    x = s[:output_len]
    z = s[output_len:]
    return np.logical_or(x, z)

def commutes_with_all(bin_symp, op: np.ndarray):
    for i in range(bin_symp.shape[0]):
        if(not commutes(bin_symp[i, :].astype(int), op)):
            return False
    return True

def not_in(pauli_set, pauli):
    for p in pauli_set:
        if (p == pauli).all():
            return False
    return True

def iterate_operator(bin_symplectic):
    idx = 0
    while(bin_symplectic[idx] == 1):
        bin_symplectic[idx] = 0
        idx = idx + 1
    bin_symplectic[idx] = 1
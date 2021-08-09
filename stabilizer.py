import numpy as np
import operator_utils as util

class StabilizerCode(object):
    def __init__(self, *args, **kwargs):
        '''
        Create a StabilizerCode Object from the binary symplectic form
        of a stabilizer code.  For now I assume that the code is a valid code

        :param file: The name of a text file that represents a 2D array of bits
        :param matrix: 
        '''
        file = kwargs.get("file", "")
        if file != "":
            self.bin_symplectic_form = np.loadtxt(file)
            return
        self.bin_symplectic_form = kwargs.get("matrix", np.zeros((0, 0)))

    def num_qubits(self):
        '''
        Returns the number of qubits represented by the stabilizer code (n)
        '''
        return int(self.bin_symplectic_form.shape[1]/2)

    def num_generators(self):
        '''
        Returns the number of generators of the stabilizer code (r)
        '''
        return self.bin_symplectic_form.shape[0]

    def compute_stabilizer_element(self, element: int):
        '''
        Returns the stabilizer element represented by the index given
        :param element: The index of the stabilizer element, less than 2^r
        '''
        binary_array = util.to_binary(element, self.num_generators())
        non_mod = np.matmul(binary_array, self.bin_symplectic_form)
        final_action = np.mod(non_mod, 2)
        return final_action

    def get_representatives(self, pauli):
        '''
        Returns all representatives of a given logical pauli
        :param pauli: numpy array representing a pauli operator
        '''
        reps = []
        for i in range(0, 2**self.num_generators()):
            generator = self.compute_stabilizer_element(i)
            reps.append(np.logical_xor(pauli, generator).astype(int))
        return reps

    def get_logical_paulis(self):
        '''
        Returns all of the logical paulis of the stabilizer code
        '''
        found_paulis = []
        current_operator = np.zeros(self.num_qubits() * 2, dtype=int)
        found_operators = self.get_representatives(current_operator)
        current_operator[0] = 1

        num_logical_qubits = self.num_qubits() - self.num_generators() + 1

        while((current_operator == 0).any()):
            if(util.commutes_with_all(self.bin_symplectic_form, current_operator) and
               util.not_in(found_operators, current_operator)):
                found_paulis.append(current_operator.copy())
                if(len(found_paulis) == (4**(num_logical_qubits) - 1)):
                    return found_paulis
                found_operators += self.get_representatives(current_operator)
            util.iterate_operator(current_operator)
        return found_paulis


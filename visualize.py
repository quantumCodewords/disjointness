def display_bin_form(pauli):
    num_qubits = len(pauli)//2
    output_string = ""
    for i in range(num_qubits):
        if(pauli[i] == 1 and pauli[i + num_qubits] == 1):
            output_string += "Y"
        if(pauli[i] == 1 and pauli[i + num_qubits] == 0):
            output_string += "X"
        if(pauli[i] == 0 and pauli[i + num_qubits] == 1):
            output_string += "Z"
        if(pauli[i] == 0 and pauli[i + num_qubits] == 0):
            output_string += "I"
    return output_string


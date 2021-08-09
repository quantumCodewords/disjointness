from pulp import LpProblem, lpSum, LpVariable, lpDot, LpMaximize, PULP_CBC_CMD, value
import re
import numpy as np

import stabilizer
import pauli
import operator_utils as util
import visualize

def extract_index(name):
    regex = r"Include_Set_([0-9]*)"
    m = re.search(regex, name)
    return int(m.group(1))

def disjointness_LP(sets):
    if(len(sets) == 0):
        return
    prob = LpProblem("Disjointness Problem", LpMaximize)
    variables = []
    for i in range(len(sets)):
        variables.append(LpVariable("Include Set " + str(i), 0, 1))

    #objective
    prob += lpSum([1 * variables[i] for i in range(len(sets))])

    #constraints
    for j in range(len(sets[0])):
        #for every qubit, make the sum of actions less than 1
        prob += lpDot([sets[i][j] for i in range(len(sets))], [variables[i] for i in range(len(sets))]) <= 1

    prob.writeLP("Disjointness.lp")

    prob.solve(solver = PULP_CBC_CMD(msg=0))

    representatives  = []
    values = []

    for v in prob.variables():
        i = extract_index(v.name)
        if(v.varValue != 0.0):
            representatives.append(i)
            values.append(v.varValue)

    return value(prob.objective), representatives, values

def compute_disjointness(code: stabilizer.StabilizerCode, paulis: pauli.Paulis, verbose: bool):
    disjointnesses = []
    best_disjointness = code.num_qubits()
    for representative in paulis.pauli_operators:
        reps = code.get_representatives(representative)
        weights = list(map(util.into_weight, reps))
        disjointness, representatives, values = disjointness_LP(weights)
        min_weight = 100
        best_index = 0
        for i in range(len(reps)):
            if sum(weights[i]) < min_weight:
                min_weight = sum(weights[i])
                best_index = i
        print("Disjointness: ", disjointness)
        print("MinWeight Operator: ", reps[best_index])
        if verbose:
            print("Logical Pauli: ", visualize.display_bin_form(representative))
            for i in range(len(representatives)):
                rep = np.logical_xor(representative, code.compute_stabilizer_element(representatives[i]))
                print("Take Representative " + visualize.display_bin_form(rep.astype(int)) + " with weight " + str(values[i]))
        disjointnesses.append(disjointness)
        if disjointness < best_disjointness:
            best_disjointness = disjointness
    return disjointnesses, best_disjointness

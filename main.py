import argparse

import stabilizer
import pauli
import disjointness as calc

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute the Disjointness of a Stabilizer and Paulis")
    parser.add_argument("--stabilizer", help="File to stabilizer generators")
    parser.add_argument("--paulis", nargs='?', help="File to logical paulis")
    parser.add_argument("--verbose", action='store_true')

    args = parser.parse_args()
    verbose = args.verbose

    code = stabilizer.StabilizerCode(file = args.stabilizer)
    if args.paulis != None:
        paulis = pauli.Paulis(file=args.paulis)
    else:   
        paulis = pauli.Paulis(stabilizer = code)
    disjointnesses, disjointness = calc.compute_disjointness(code, paulis, verbose)
    print("Best Disjointness: ", disjointness)

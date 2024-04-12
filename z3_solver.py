import json
from z3 import *

def solve_formula(input_file, output_file):
    # Load the JSON data from the input file
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Extract the formula and variables from the JSON
    formula_code = data['formula']
    variables = data['variables']

    # Declare Boolean variables
    bool_vars = {var: Bool(var) for var in variables}

    # Add Z3 functions to the dictionary
    bool_vars.update({'Or': Or, 'And': And, 'Not': Not, 'Implies':Implies, 'XOR':Xor})

    # Execute the formula code
    local_vars = {}
    exec(formula_code, bool_vars, local_vars)
    formula = local_vars['formula']

    # Create a solver and add the formula
    s = Solver()
    s.add(formula)

    # Find all possible solutions
    solutions = {}
    i = 1
    print(formula)
    while s.check() == sat:
        model = s.model()
        solution = {str(v): str(model[v]) for v in model}
        solutions[f'Solution{i}'] = solution
        i += 1
        
        # Add a constraint to exclude the current solution
        s.add(Or([v() != model[v] for v in model]))

    # Write the solutions to the output file
    with open(output_file, 'w') as f:
        json.dump(solutions, f, indent=2)
    
    print(f"Solutions have been generated to {output_file}")

# Example usage:
# solve_formula('input.json', 'output.json')

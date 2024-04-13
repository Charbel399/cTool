import json
import os
import copy

def store_true_variables(data):
    true_variables = {}
    for solution, variables in data.items():
        true_variables[solution] = [var for var, value in variables.items() if value == "True"]
    return true_variables

def store_may_elements(data):
    states = {}
    transitions = {}
    for variable, value in data['may_elements'].items():
        for state, transition in value.items():
            if variable not in states:
                states[variable] = []
            states[variable].append(state)

            if variable not in transitions:
                transitions[variable] = []
            transitions[variable].append(transition['transitions'])
    return states, transitions

def generate_concretization(initial_state_file, solutions_file, may_elements, output_dir):
    # Load the JSON data from the files
    with open(initial_state_file, 'r') as f:
        initial_state_data = json.load(f)
    with open(solutions_file, 'r') as f:
        solutions_data = json.load(f)
    with open(may_elements, 'r') as f:
        may_elements_data = json.load(f)

    # Get the true variables for each solution
    true_variables = store_true_variables(solutions_data)

    # Get the states and transitions for each variable
    states, transitions = store_may_elements(may_elements_data)

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Add the new states and transitions to the initial state for each solution
    for solution, variables in true_variables.items():
        updated_state_data = copy.deepcopy(initial_state_data)
        updated_state_data.pop("formula", None)
        updated_state_data.pop("variables", None)
        for variable in variables:
            if variable in states and variable in transitions:
                for state, transition in zip(states[variable], transitions[variable]):
                        if state not in initial_state_data['states']:
                            updated_state_data['states'][state] = {'transitions': transition}
                        else:
                            updated_state_data['states'][state]['transitions'].update(transition)

        # Write the updated state data to a new JSON file in the specified output directory
        with open(os.path.join(output_dir, f'{solution}.json'), 'w') as f:
            json.dump(updated_state_data, f, indent=2)

    print(f"JSON files have been written to the '{output_dir}' directory.")

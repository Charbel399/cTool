import os
import json

def generate_concretization(first_json_path, second_json_path, output_directory):
    # Load the JSON files
    with open(first_json_path, 'r') as f1, open(second_json_path, 'r') as f2:
        first_json = json.load(f1)
        second_json = json.load(f2)

    # Iterate through each solution in the first JSON file
    for solution_key, solution_value in first_json.items():
        # Create a copy of the second JSON
        updated_json = second_json.copy()

        # Iterate through each variable in the solution
        for variable, value in solution_value.items():
            # Check if the value is True
            if value == "True":
                # Check if the variable exists in may_elements of the second JSON
                if variable in updated_json["may_elements"]:
                    # Get the transitions for the variable
                    transitions = updated_json["may_elements"][variable]

                    # Iterate through the transitions and add them to the states
                    for transition_name, transition_value in transitions.items():
                        # Get the target state for the transition
                        target_state = transition_value.get("transitions", {}).get("target_state", transition_name)
                        
                        # Check if the target state exists in the states of the second JSON
                        if target_state in updated_json["states"]:
                            # Update existing state with transitions from may_elements
                            updated_json["states"].setdefault(target_state, {}).setdefault("transitions", {}).update(transition_value["transitions"])
                        else:
                            # Add the state and transitions if it doesn't exist
                            updated_json["states"][target_state] = transition_value

                else:
                    print(f"Warning: {variable} not found in may_elements.")

        # Remove formula, variables, and may_elements
        updated_json.pop("formula", None)
        updated_json.pop("variables", None)
        updated_json.pop("may_elements", None)

        # Create directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)

        # Write the updated JSON to a separate file for each solution
        output_file = os.path.join(output_directory, f"{solution_key}.json")
        with open(output_file, 'w') as outfile:
            json.dump(updated_json, outfile, indent=4)
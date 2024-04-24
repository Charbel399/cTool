import json
import shutil
import os

def find_satisfied_design_decisions(Uncertain_Task_Json, Goal_Model, output_json_path):
    # Load JSON data
    with open(Uncertain_Task_Json) as f1, open(Goal_Model) as f2:
        json1 = json.load(f1)
        json2 = json.load(f2)
    
    satisfied_design_decisions = []
    
    # Extract design decisions from JSON 1
    design_decisions = [task["Design Decisions"] for task in json1["Uncertain_Tasks"]]
    
    # Flatten the list of design decisions
    design_decisions = [decision for sublist in design_decisions for decision in sublist]
    
    # Extract tasks with a value of "Satisfied" from JSON 2
    satisfied_tasks = [task["name"] for task in json2["Model"]["Goal_Model"]["Task"] if task["value"] == "Satisfied"]
    
    # Check which design decisions match the satisfied tasks
    for decision in design_decisions:
        if decision in satisfied_tasks:
            satisfied_design_decisions.append(decision)
    
    # Create the output JSON
    output_json = {"Satisfied_Design_Decisions": satisfied_design_decisions}
    
    # Write the output JSON to file
    with open(output_json_path, "w") as outfile:
        json.dump(output_json, outfile, indent=4)


def print_files_for_folders(json_file_path, folder_path, output_folder):
    # Load JSON data
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Initialize a set to hold files present in all folders
    common_files = None

    # Iterate over the elements in the JSON array
    for element in data['Satisfied_Design_Decisions']:
        folder_name = element.replace(" ", " ")  # Replace spaces with underscores
        folder_path_with_name = os.path.join(folder_path, folder_name)

        # Check if the folder exists
        if os.path.exists(folder_path_with_name) and os.path.isdir(folder_path_with_name):
            # List files in the folder
            files = os.listdir(folder_path_with_name)

            # If it's the first folder, initialize the common_files set
            if common_files is None:
                common_files = set(files)
            else:
                # Update the common_files set to contain only files present in both sets
                common_files &= set(files)

    # Print common files present in all folders
    if common_files:
        print("Common solutions found:")
        for file in common_files:
            print(f"- {file}")

        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Copy common files to the output folder
        for file in common_files:
            for element in data['Satisfied_Design_Decisions']:
                folder_name = element.replace(" ", " ")  # Replace spaces with underscores
                folder_path_with_name = os.path.join(folder_path, folder_name)
                src_file_path = os.path.join(folder_path_with_name, file)
                dst_file_path = os.path.join(output_folder, file)
                shutil.copy(src_file_path, dst_file_path)
        print(f"Common solutions copied to '{output_folder}'.")
    else:
        print("No common solutions found.")


def multiple_stakeholders_decision(json_file_paths, folder_path, output_folder):
    output_data = {"Stakeholder Design Solutions": {}}  # Initialize output dictionary
    i = 1
    # Iterate over the JSON files
    for json_file_path in json_file_paths:
        # Load JSON data
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        # Initialize a set to hold files present in all folders
        common_files = None

        # Iterate over the elements in the JSON array
        for element in data['Satisfied_Design_Decisions']:
            folder_name = element.replace(" ", " ")  # Replace spaces with underscores
            folder_path_with_name = os.path.join(folder_path, folder_name)

            # Check if the folder exists
            if os.path.exists(folder_path_with_name) and os.path.isdir(folder_path_with_name):
                # List files in the folder
                files = os.listdir(folder_path_with_name)

                # If it's the first folder, initialize the common_files set
                if common_files is None:
                    common_files = set(files)
                else:
                    # Update the common_files set to contain only files present in both sets
                    common_files &= set(files)

        # Collect common files present in all folders for this JSON file
        if common_files:
            # Remove ".json" extension from file names
            common_files = [os.path.splitext(file)[0] for file in common_files]
            output_data["Stakeholder Design Solutions"][f"Stakeholder {i}"] = common_files
        else:
            output_data["Stakeholder Design Solutions"][f"No common solutions found for {json_file_path}"] = []

        i += 1

    # Write output data to JSON file (optional)
    output_file_path = os.path.join(output_folder, "Multiple_Stakeholder_Decisions.json")
    with open(output_file_path, "w") as output_file:
        json.dump(output_data, output_file, indent=4)
    print(f"Multiple stakeholders design decisions successfully generated and can be found at '{output_file_path}'")
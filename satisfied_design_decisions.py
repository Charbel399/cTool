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
            print(f"Files in folder '{folder_name}':")
            # List files in the folder
            files = os.listdir(folder_path_with_name)

            # If it's the first folder, initialize the common_files set
            if common_files is None:
                common_files = set(files)
            else:
                # Update the common_files set to contain only files present in both sets
                common_files &= set(files)

            for file in files:
                print(f"- {file}")
            print()  # Add a newline after listing files for each folder
        else:
            print(f"Folder '{folder_name}' does not exist.")

    # Print common files present in all folders
    if common_files:
        print("Common files present in all folders:")
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
        print(f"Common files copied to '{output_folder}'.")
    else:
        print("No common files found in all folders.")
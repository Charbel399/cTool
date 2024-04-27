import os
import json
import shutil
import csv

def sort_solutions(json_file_path, mapping_csv_path, output_folder):
    # Load JSON data
    with open(json_file_path, 'r') as json_file:
        solutions_data = json.load(json_file)
    
    # Read mapping from CSV
    mapping = {}
    with open(mapping_csv_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip header
        for row in csv_reader:
            decision, may_element, value = row
            if decision not in mapping:
                mapping[decision] = []
            mapping[decision].append((may_element, value == 'True'))

    # Create folders if they don't exist
    for decision in mapping.keys():
        folder_name = decision.replace('/', '_')  # Replace forward slashes with underscores
        folder_path = os.path.join(output_folder, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    
    # Copy solutions into folders
    for solution_name, solution_data in solutions_data.items():
        for decision, conditions in mapping.items():
            all_conditions_met = all(solution_data.get(may_element) == str(value) for may_element, value in conditions)
            if all_conditions_met:
                folder_name = decision.replace('/', '_')  # Replace forward slashes with underscores
                destination_folder = os.path.join(output_folder, folder_name)
                source_file = os.path.join(output_folder, f"{solution_name}.json")
                destination_file = os.path.join(destination_folder, f"{solution_name}.json")
                shutil.copy(source_file, destination_file)
    
    # Delete original files
    for solution_name in solutions_data.keys():
        original_file = os.path.join(output_folder, f"{solution_name}.json")
        if os.path.exists(original_file):
            os.remove(original_file)
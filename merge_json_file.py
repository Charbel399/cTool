import os
import json

def merge_json_files(json1_path, json2_path, merged_output_path):
        # Read the content of the first JSON file
        with open(json1_path, 'r') as file:
            json1_data = json.load(file)

        # Read the content of the second JSON file
        with open(json2_path, 'r') as file:
            json2_data = json.load(file)

        # Merge the content of both JSON files
        merged_data = {}
        merged_data['Uncertainty'] = json1_data
        merged_data['Model'] = json2_data

        # Write the merged content into a new JSON file
        with open(merged_output_path, 'w') as file:
            json.dump(merged_data, file, indent=4)

        print("Goal Model successfully generated and has been saved to:", merged_output_path)

        # Delete the original JSON files
        os.remove(json1_path)
        os.remove(json2_path)
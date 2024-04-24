import xml.etree.ElementTree as ET
import json

def Uncertainty_tasks(file_path, output_file):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Extract the targets of all BeliefLinks
    belief_link_targets = [connection.attrib.get('target') for connection in root.iter('connections') if 'grl:BeliefLink' in connection.attrib.values()]

    # Find the intElements with matching refs and return their names and ids
    tasks_info = [{"name": intElement.attrib.get('name'), "id": intElement.attrib.get('id')} for intElement in root.iter('intElements') if intElement.attrib.get('refs') in belief_link_targets]

    # Extract links and organize them by destination (uncertain task)
    links = [{"id": link.attrib.get('id'), "dest": link.attrib.get('dest'), "src": link.attrib.get('src')} for link in root.iter('links')]

    # Create a dictionary to store subtasks grouped by uncertain task IDs
    subtasks_dict = {}
    for task in tasks_info:
        task_id = task["id"]
        subtasks_dict[task_id] = []

    # Populate the subtasks dictionary with linked tasks
    for link in links:
        dest_id = link["dest"]
        src_id = link["src"]
        if dest_id in subtasks_dict:
            subtasks_dict[dest_id].append(src_id)

    # Create a dictionary for structured output
    tasks_dict = {"Uncertain_Tasks": []}
    for task in tasks_info:
        task_id = task["id"]
        task_name = task["name"]
        subtask_names = [intElement.attrib.get('name') for intElement in root.iter('intElements') if intElement.attrib.get('id') in subtasks_dict.get(task_id, [])]
        tasks_dict["Uncertain_Tasks"].append({"Uncertain Task": task_name, "Design Decisions": subtask_names})

    # Write the results to a JSON file
    with open(output_file, 'w') as f:
        json.dump(tasks_dict, f, indent=4)  # Use indent to format the output


def extract_uncertainty(json_file_path, output_file_path):
    with open(json_file_path, 'r') as file:
        json_data = json.load(file)
        uncertainty_data = json_data.get("Uncertainty")
        if uncertainty_data:
            with open(output_file_path, 'w') as output_file:
                json.dump(uncertainty_data, output_file, indent=4)

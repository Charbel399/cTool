import xml.etree.ElementTree as ET
import json

def Uncertainty_tasks(file_path, output_file):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Extract the targets of all BeliefLinks
    belief_link_targets = [connection.attrib.get('target') for connection in root.iter('connections') if 'grl:BeliefLink' in connection.attrib.values()]

    # Find the intElements with matching refs and return their names
    tasks_names = [intElement.attrib.get('name') for intElement in root.iter('intElements') if intElement.attrib.get('refs') in belief_link_targets]

    # Create a dictionary for structured output
    tasks_dict = {"Uncertain_Tasks": tasks_names}

    # Write the results to a JSON file
    with open(output_file, 'w') as f:
        json.dump(tasks_dict, f, indent=4)  # Use indent to format the output

    print(f"Results have been written to {output_file}")

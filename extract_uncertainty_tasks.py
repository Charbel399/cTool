import xml.etree.ElementTree as ET

def extract_uncertainty_tasks(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Extract the targets of all BeliefLinks
    belief_link_targets = [connection.attrib.get('target') for connection in root.iter('connections') if 'grl:BeliefLink' in connection.attrib.values()]

    # Find the intElements with matching refs and return their names
    tasks_names = [intElement.attrib.get('name') for intElement in root.iter('intElements') if intElement.attrib.get('refs') in belief_link_targets]

    return tasks_names

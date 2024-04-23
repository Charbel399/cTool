import xml.etree.ElementTree as ET
import json
import extract_uncertainty_tasks

def xmi_2_json(file_path, output_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Get the namespaces
    namespaces = {'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
    
    data = {
        "Goal_Model": {},
        "links": {}
    }

    id_to_name = {}  # Create a dictionary to map id to name
    id_to_description = {}  # Create a dictionary to map id to description

    for element in root.findall('.//intElements'):
        value = element.find(".//metadata[@name='_qualEval']").attrib.get('value')
        if value == "None":
            value = "Not Satisfied"
        item = {
            "name": element.attrib.get('name', ''),
            "type": element.attrib.get('type', 'Softgoal') or 'Softgoal',
            "value": value
        }
        
        # Group intElements by type
        if item["type"] not in data["Goal_Model"]:
            data["Goal_Model"][item["type"]] = []
        data["Goal_Model"][item["type"]].append(item)

        # Add the id and name to the id_to_name dictionary
        id_to_name[element.attrib.get('id')] = element.attrib.get('name')

        # Add the id and description to the id_to_description dictionary
        id_to_description[element.attrib.get('id')] = element.attrib.get('description')

    for link in root.findall('.//links'):
        link_attrib = link.attrib.get('{'+namespaces['xsi']+'}type')
        link_type = ''  # Define link_type as an empty string
        if link_attrib is not None:
            link_type = link_attrib.split(":")[-1]
        src_id = link.attrib.get('src', '')  # Get the source id directly
        dest_id = link.attrib.get('dest', '')  # Get the destination id directly
        src_name = id_to_name.get(src_id, '')  # Get source name using id
        dest_name = id_to_name.get(dest_id, '')  # Get destination name using id
        item = {
            "source": src_name,
            "destination": dest_name,
        }

        # Include "contribution value" only for Contribution links
        if link_type == "Contribution":
            value = link.attrib.get('quantitativeContribution', '25')  # Set to 25 if empty
            item["contribution value"] = value

        # Group links by type
        if link_type not in data["links"]:
            data["links"][link_type] = []
        data["links"][link_type].append(item)
        

    # Add BeliefLink to the links section
    for node in root.findall('.//nodes'):
        node_type = node.attrib.get('{'+namespaces['xsi']+'}type')
        if node_type == "grl:Belief":
            src_description = node.attrib.get('description', '')  # Retrieve description
            src_id = node.attrib.get('id', '')  # Get the source id directly
            # Look for connections with this source id
            for connection in root.findall('.//connections'):
                connection_type = connection.attrib.get('{'+namespaces['xsi']+'}type')
                if connection_type == "grl:BeliefLink":
                    src = connection.attrib.get('source', '')
                    dest = connection.attrib.get('target', '')
                    if src == src_id:
                        # Find the name of the destination
                        dest_name = None
                        for int_element in root.findall('.//intElements'):
                                refs = int_element.attrib.get('refs')
                                for int_element_ref in refs.split():
                                    if int_element_ref == dest:
                                        dest_name = int_element.attrib.get('name')
                                        break
                                if dest_name:
                                    break
                        item = {
                            "source": src_description,
                            "destination": dest_name if dest_name else dest,  # Use name if found, else use id
                        }
                        # Group BeliefLink by type
                        if 'BeliefLink' not in data["links"]:
                            data["links"]['BeliefLink'] = []
                        data["links"]['BeliefLink'].append(item)


    save_json(data, output_path)


def save_json(data, output_path):
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f'XMI file successfully converted to JSON and can be found in {output_path}')


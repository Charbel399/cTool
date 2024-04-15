import xml.etree.ElementTree as ET
import json

def xmi_2_json(file_path, output_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Get the namespaces
    namespaces = {'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
    
    data = {
        "intElements": {},
        "links": {}
    }

    id_to_name = {}  # Create a dictionary to map id to name

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
        if item["type"] not in data["intElements"]:
            data["intElements"][item["type"]] = []
        data["intElements"][item["type"]].append(item)

        # Add the id and name to the id_to_name dictionary
        id_to_name[element.attrib.get('id')] = element.attrib.get('name')

    for link in root.findall('.//links'):
        link_attrib = link.attrib.get('{'+namespaces['xsi']+'}type')
        link_type = ''  # Define link_type as an empty string
        if link_attrib is not None:
            link_type = link_attrib.split(":")[-1]
        src = id_to_name.get(link.attrib.get('src'), '')  # Replace src with its name
        dest = id_to_name.get(link.attrib.get('dest'), '')  # Replace dest with its name
        item = {
            "source": src,
            "destination": dest,
        }

        # Include "contribution value" only for Contribution links
        if link_type == "Contribution":
            value = link.attrib.get('quantitativeContribution', '25')  # Set to 25 if empty
            item["contribution value"] = value

        # Group links by type
        if link_type not in data["links"]:
            data["links"][link_type] = []
        data["links"][link_type].append(item)

    save_json(data, output_path)


  


def save_json(data, output_path):
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f'XMI file successfully converted to JSON and can be found in {output_path}')
import json
import os 
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY

def merge_json_files(json_file_paths, output_file_path):
    # Initialize an empty dictionary to store JSON data
    merged_data = {}

    # Loop through each file path
    for file_path in json_file_paths:
        # Check if the file exists
        if file_path.endswith('.json') and os.path.exists(file_path):
            try:
                # Open the file and load JSON data
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    # Use the filename without extension as a key in the merged_data dictionary
                    filename = os.path.splitext(os.path.basename(file_path))[0]
                    merged_data[filename] = data
            except Exception as e:
                print(f"Error loading JSON file '{file_path}': {e}")
        else:
            print(f"File '{file_path}' is not a valid JSON file.")

    # If no valid files were selected, return None
    if not merged_data:
        print("No valid JSON files selected for merging.")
        return None

    # Ensure the directory of the output file path exists
    output_directory = os.path.dirname(output_file_path)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Write the merged JSON data to the specified output file path
    if not output_file_path.endswith('.json'):
        output_file_path += '.json'

    try:
        with open(output_file_path, 'w') as file:
            json.dump(merged_data, file, indent=4)
    except Exception as e:
        print(f"Error: {e}")

def generate_pdf(content, output_filename):
    doc = SimpleDocTemplate(output_filename, pagesize=letter)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    flowables = []

    for line in content:
        if line.strip():
            p = Paragraph(line.strip(), styles['Justify'])
            flowables.append(p)
            flowables.append(Spacer(1, 12))  # Add space between paragraphs

    doc.build(flowables)

def analyze_stakeholder(stakeholder, solution, design_decision, output_filename):
    with open(solution, 'r') as file:
        solutions = json.load(file)

    with open(design_decision, 'r') as file1:
        design_decisions = json.load(file1)

    content = []

    for other_stakeholder in solutions["Stakeholder Design Solutions"]:
        if other_stakeholder != stakeholder:
            content.append('<para align=center spaceb=20><b>Analysis between {} and {}:</b></para>'.format(stakeholder, other_stakeholder))
            
            # Solutions
            stakeholder_solutions = solutions["Stakeholder Design Solutions"][stakeholder]
            other_solutions = solutions["Stakeholder Design Solutions"][other_stakeholder]
            differing_solutions = list(set(stakeholder_solutions) ^ set(other_solutions))
            common_solutions = list(set(stakeholder_solutions) & set(other_solutions))

            content.append('<para align=left spaceb=20><b>Solutions in common:</b><br/>{}</para>'.format(', '.join(common_solutions)))
            if differing_solutions:
                content.append('<para align=left spaceb=20><b>Solutions that differ:</b><br/>{}</para>'.format(', '.join(differing_solutions)))

            # Decisions
            decisions = design_decisions[stakeholder]["Satisfied_Design_Decisions"]
            other_decisions = design_decisions[other_stakeholder]["Satisfied_Design_Decisions"]
            differing_decisions = list(set(decisions) ^ set(other_decisions))
            same_decisions = list(set(decisions) & set(other_decisions))

            content.append('<para align=left spaceb=20><b>Decisions in common:</b><br/>{}</para>'.format(', '.join(same_decisions)))
            if differing_decisions:
                content.append('<para align=left spaceb=20><b>Decisions that differ:</b><br/>{}</para>'.format(', '.join(differing_decisions)))

            # Conflicting Solutions
            conflicting_solutions = list(set(stakeholder_solutions) & set(other_solutions))
            for solution in conflicting_solutions:
                if differing_solutions:
                    content.append('<para align=left spaceb=20><b>Solution {} is a conflict between {} and {}.</b><br/><b>Decisions causing the conflict:</b><br/>{}</para>'.format(', '.join(differing_solutions), stakeholder, other_stakeholder, ', '.join(differing_decisions)))
                else:
                    content.append('<para align=left spaceb=20><b>There are no conflicts between {} and {}.</b></para>'.format(stakeholder, other_stakeholder))

            content.append('<para spaceb=20></para>')

    generate_pdf(content, output_filename + "/report.pdf")
import json
import os 
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

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
        print(f"JSON files successfully merged and saved to '{output_file_path}'.")
    except Exception as e:
        print(f"Error saving merged JSON file: {e}")

def generate_pdf(content, output_filename):
    doc = SimpleDocTemplate(output_filename, pagesize=letter)

    styles = getSampleStyleSheet()
    style_normal = styles["Normal"]
    style_heading = styles["Heading1"]

    flowables = []

    for line in content.split('\n'):
        if line.strip():
            p = Paragraph(line.strip(), style_normal)
            flowables.append(p)
            flowables.append(Spacer(1, 12))  # Add space between paragraphs

    doc.build(flowables)

def analyze_stakeholder(stakeholder, solution, design_decision, output_filename):
    with open(solution, 'r') as file:
        solutions = json.load(file)

    with open(design_decision, 'r') as file1:
        design_decisions = json.load(file1)

    content = []

    decisions = design_decisions[stakeholder]["Satisfied_Design_Decisions"]
    content.append(f"<b>Decisions made by {stakeholder}:</b><br/>{decisions}<br/><br/>")

    stakeholder_solutions = solutions["Stakeholder Design Solutions"][stakeholder]
    content.append(f"<b>Solutions for {stakeholder}:</b><br/>{stakeholder_solutions}<br/><br/>")

    for other_stakeholder in solutions["Stakeholder Design Solutions"]:
        if other_stakeholder != stakeholder:
            other_solutions = solutions["Stakeholder Design Solutions"][other_stakeholder]
            differing_solutions = list(set(stakeholder_solutions) ^ set(other_solutions))
            content.append(f"<b>Solutions that differ between {stakeholder} and {other_stakeholder}:</b><br/>{differing_solutions}<br/><br/>")

            other_decisions = design_decisions[other_stakeholder]["Satisfied_Design_Decisions"]
            differing_decisions = list(set(decisions) ^ set(other_decisions))
            content.append(f"<b>Decisions that differ between {stakeholder} and {other_stakeholder}:</b><br/>{differing_decisions}<br/><br/>")

            conflicting_solutions = list(set(stakeholder_solutions) & set(other_solutions))
            for solution in conflicting_solutions:
                content.append(f"<b>Solution {solution} is a conflict between {stakeholder} and {other_stakeholder}.</b><br/>")
                content.append(f"<b>Decisions causing the conflict:</b><br/>{decisions}<br/><br/>")

    generate_pdf("\n".join(content), output_filename + "/report.pdf")
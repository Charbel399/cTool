import extract_uncertainty_tasks
import satisfied_design_decisions
import concretization_generation
import z3_solver
import xmi2json
import filter
import json
import os 

#Input Files
Goal_Model = "C:\\Users\\ashle\\OneDrive\\Desktop\\cTool\\inputs\\TorrentTO.xmi" #path xmi file
z3_diagram_file = "C:\\Users\\ashle\OneDrive\\Desktop\\cTool\\inputs\\Initial_State.json" #path of diagram and z3 formula file
mapping_csv = "C:\\Users\\ashle\OneDrive\\Desktop\\cTool\\inputs\\goals2mayelements.csv"


#Output Files
xmi_2_json_output_file = "C:\\Users\\ashle\\OneDrive\\Desktop\\cTool\\outputs\\Goal_Model2.json" #output of where you want your converted xmi file to be stored
z3_solutions_output = "C:\\Users\\ashle\\OneDrive\\Desktop\\cTool\\outputs\\Concretizations.json" #path of output for solutions for z3 solver
uncertain_tasks_output = "C:\\Users\\ashle\\OneDrive\\Desktop\\cTool\\outputs\\uncertain_tasks.json" #path for output of uncertain tasks
output_diagram_solutions = "C:\\Users\\ashle\\OneDrive\\Desktop\\cTool\\outputs\\solution_diagram" #path of the folder where solutions should be outputed
merged_output_file = "C:\\Users\\ashle\\OneDrive\\Desktop\\cTool\\outputs\\Goal_Model.json"
Goal_Model_Design_Decision_Output = "C:\\Users\\ashle\\OneDrive\\Desktop\\cTool\\outputs\\Goal_Model_Satisfied_Design_Decision.json"
satisfied_design_decisions_folder = "C:\\Users\\ashle\\OneDrive\\Desktop\\cTool\\outputs\\solution_diagram\\Satisfied_Design_Decision"

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

    print("Merged output saved to:", merged_output_path)

    # Delete the original JSON files
    os.remove(json1_path)
    os.remove(json2_path)

def main():
    
    xmi2json.xmi_2_json(Goal_Model,xmi_2_json_output_file)
    extract_uncertainty_tasks.Uncertainty_tasks(Goal_Model,uncertain_tasks_output)
    merge_json_files(uncertain_tasks_output,xmi_2_json_output_file,merged_output_file)
    extract_uncertainty_tasks.extract_uncertainty(merged_output_file,uncertain_tasks_output)
    satisfied_design_decisions.find_satisfied_design_decisions(uncertain_tasks_output,merged_output_file,Goal_Model_Design_Decision_Output)
    z3_solver.solve_formula(z3_diagram_file,z3_solutions_output)
    concretization_generation.generate_concretization(z3_diagram_file,z3_solutions_output,z3_diagram_file,output_diagram_solutions)
    filter.sort_solutions(z3_solutions_output,mapping_csv,output_diagram_solutions)
    satisfied_design_decisions.print_files_for_folders(Goal_Model_Design_Decision_Output,output_diagram_solutions,satisfied_design_decisions_folder)
    
if __name__ == "__main__":
    main()
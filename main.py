import extract_uncertainty_tasks
import concretization_generation
import z3_solver
import xmi2json
import filter

#Input Files
Goal_Model = "C:\\Users\\ashle\\OneDrive\\Desktop\\cTool\\inputs\\TorrentTO.xmi" #path xmi file
z3_diagram_file = "C:\\Users\\ashle\OneDrive\\Desktop\\cTool\\inputs\\Initial_State.json" #path of diagram and z3 formula file
may_elements = "C:\\Users\\ashle\OneDrive\\Desktop\\cTool\\inputs\\may_elements.json" #path of the file where may_elements are they can also be in the initial z3_diagram_file
mapping_csv = "C:\\Users\\ashle\OneDrive\\Desktop\\cTool\\inputs\\goals2mayelements.csv"


#Output Files
xmi_2_json_output_file = "C:\\Users\\ashle\\OneDrive\\Desktop\\cTool\\outputs\\xmi_2_json.json" #output of where you want your converted xmi file to be stored
z3_solutions_output = "C:\\Users\\ashle\\OneDrive\\Desktop\\cTool\\outputs\\solutions.json" #path of output for solutions for z3 solver
uncertain_tasks_output = "C:\\Users\\ashle\\OneDrive\\Desktop\\cTool\\outputs\\uncertain_tasks.json" #path for output of uncertain tasks
output_diagram_solutions = "C:\\Users\\ashle\\OneDrive\\Desktop\\cTool\\outputs\\solution_diagram" #path of the folder where solutions should be outputed

def main():
    extract_uncertainty_tasks.Uncertainty_tasks(Goal_Model,uncertain_tasks_output)
    z3_solver.solve_formula(z3_diagram_file,z3_solutions_output)
    concretization_generation.generate_concretization(z3_diagram_file,z3_solutions_output,may_elements,output_diagram_solutions)
    xmi2json.xmi_2_json(Goal_Model,xmi_2_json_output_file)
    filter.sort_solutions(z3_solutions_output,mapping_csv,output_diagram_solutions)

if __name__ == "__main__":
    main()
import extract_uncertainty_tasks
import concretization_generation
import z3_solver
import json

#Data Files
xmi_file = "C:\\Users\\ashle\\OneDrive\\Desktop\\cTool\\inputs\\TorrentTO.xmi" #path xmi file
z3_diagram_file = "C:\\Users\\ashle\OneDrive\\Desktop\\cTool\\inputs\\Initial_State.json" #path of diagram and z3 formula file
z3_solutions_output = "C:\\Users\\ashle\\OneDrive\\Desktop\\cTool\\outputs\\solutions.json" #path of output for solutions for z3 solver
uncertain_tasks_output = "C:\\Users\\ashle\\OneDrive\\Desktop\\cTool\\outputs\\uncertain_tasks.json" #path for output of uncertain tasks
output_diagram_solutions = "C:\\Users\\ashle\\OneDrive\\Desktop\\cTool\\outputs\\solution_diagram"
may_elements = "C:\\Users\\ashle\OneDrive\\Desktop\\cTool\\inputs\\may_elements.json"





def main():
    extract_uncertainty_tasks.Uncertainty_tasks(xmi_file,uncertain_tasks_output)
    z3_solver.solve_formula(z3_diagram_file,z3_solutions_output)
    #concretization_generation.generate_concretization(z3_solutions_output,z3_diagram_file,output_diagram_solutions)
    #concretization_generation.update_states(z3_solutions_output,z3_diagram_file,output_diagram_solutions)
    concretization_generation.generate_concretization(z3_diagram_file,z3_solutions_output,may_elements,output_diagram_solutions)

if __name__ == "__main__":
    main()
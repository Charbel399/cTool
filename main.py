import extract_uncertainty_tasks
import z3_solver

#Data Files
xmi_file = "C:\\Users\\ashle\\OneDrive\\Desktop\\cTool\\inputs\\TorrentTO.xmi" #path xmi file
z3_diagram_file = "C:\\Users\\ashle\OneDrive\\Desktop\\cTool\\inputs\\Initial_State.json" #path of diagram and z3 formula file
z3_solutions_output = "C:\\Users\\ashle\\OneDrive\\Desktop\\cTool\\outputs\\solutions.json" #path of output for solutions for z3 solver






def main():
    z3_solver.solve_formula(z3_diagram_file,z3_solutions_output)

if __name__ == "__main__":
    main()
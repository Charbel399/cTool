import extract_uncertainty_tasks
import tkinter as tk
from tkinter import filedialog
import satisfied_design_decisions
import concretization_generation
import z3_solver
import xmi2json
import filter
import os 
import merge_json_file
import sys
import shutil


class SimpleUI:
    def __init__(self, master):
        self.master = master
        master.title("cTool")

        self.output_field = tk.Text(master, height=30, width=100)
        self.output_field.grid(row=0, column=0, padx=10, pady=10)

        self.button_convert = tk.Button(master, text="Convert XMI to JSON or select already made Goal Model", command=self.convert_and_more)
        self.button_convert.grid(row=1, column=0, padx=10, pady=10)

        self.button_extract_tasks = tk.Button(master, text="Extract Tasks with Uncertainty", command=self.extract_tasks_with_uncertainty)
        self.button_extract_tasks.grid(row=2, column=0, padx=10, pady=10)

        self.button_satisfied_design_decisions = tk.Button(master, text="Satisfied Design Decisions", command=self.satisfied_design_decisions)
        self.button_satisfied_design_decisions.grid(row=3, column=0, padx=10, pady=10)

        self.button_solve_formula = tk.Button(master, text="Solve Formula", command=self.solve_formula)
        self.button_solve_formula.grid(row=4, column=0, padx=10, pady=10)

        self.button_generate_concretization = tk.Button(master, text="Generate Concretization", command=self.generate_concretization)
        self.button_generate_concretization.grid(row=5, column=0, padx=10, pady=10)

        self.button_sort_tasks = tk.Button(master, text="Sort by Tasks", command=self.sort_by_tasks)
        self.button_sort_tasks.grid(row=6, column=0, padx=10, pady=10)

        self.button_select_tasks_decisions = tk.Button(master, text="Select Tasks Design Decisions", command=self.select_tasks_decisions)
        self.button_select_tasks_decisions.grid(row=7, column=0, padx=10, pady=10)

        # Redirect standard output to a variable
        self.stdout = sys.stdout
        sys.stdout = self

    def write(self, text):
        # Write text to the output field
        self.output_field.insert(tk.END, text)


    def convert_and_more(self):

        
        goal_model_file = filedialog.askopenfilename(title="Select Goal Model File", filetypes=[("XMI files", "*.xmi"), ("JSON files", "*.json")])
        global output_folder 
        output_folder= filedialog.askdirectory(title="Select output folder")
        if not output_folder:
            self.output_field.insert(tk.END, "No output folder selected.\n")
            return

        if goal_model_file.lower().endswith('.xmi'):
            if not goal_model_file:
                self.output_field.insert(tk.END, "No file selected.\n")
                return
            
            # Convert XMI to JSON
            xmi_output_file = os.path.join(output_folder, "Goal_Model2.json")
            try:
                xmi2json.xmi_2_json(goal_model_file, xmi_output_file)
            except Exception as e:
                self.output_field.insert(tk.END, f"Error converting XMI to JSON: {str(e)}\n")
                return

            # Extract Uncertainty Tasks
            uncertain_tasks_output = os.path.join(output_folder, "uncertain_tasks.json")
            try:
                extract_uncertainty_tasks.Uncertainty_tasks(goal_model_file, uncertain_tasks_output)
            except Exception as e:
                self.output_field.insert(tk.END, f"Error extracting uncertainty tasks: {str(e)}\n")
                return

            # Merge JSON files
            merged_output_file = os.path.join(output_folder, "Goal_Model.json")
            try:
                merge_json_file.merge_json_files(uncertain_tasks_output, xmi_output_file, merged_output_file)
                self.output_field.insert(tk.END, "\n")
            except Exception as e:
                self.output_field.insert(tk.END, f"Error merging JSON files: {str(e)}\n")
        elif goal_model_file.lower().endswith('.json'):
            # Just copy the JSON file to output folder with desired name
            try:
                shutil.copy2(goal_model_file, os.path.join(output_folder, "Goal_Model.json"))
                self.output_field.insert(tk.END, "JSON file copied successfully.\n")
            except Exception as e:
                self.output_field.insert(tk.END, f"{str(e)}\n")
                return

    def extract_tasks_with_uncertainty(self):

        merged_output_file = os.path.join(output_folder, "Goal_Model.json")
        uncertain_tasks_output = os.path.join(output_folder, "uncertain_tasks.json")

        try:
            extract_uncertainty_tasks.extract_uncertainty(merged_output_file, uncertain_tasks_output)
            self.output_field.insert(tk.END, "Tasks with uncertainty extracted successfully.\n")
        except Exception as e:
            self.output_field.insert(tk.END, f"Error extracting tasks with uncertainty: {str(e)}\n")

    def satisfied_design_decisions(self):

        uncertain_tasks_output = os.path.join(output_folder, "uncertain_tasks.json")
        merged_output_file = os.path.join(output_folder, "Goal_Model.json")
        goal_model_design_decision_output = os.path.join(output_folder, "Goal_Model_Satisfied_Design_Decision.json")

        try:
            satisfied_design_decisions.find_satisfied_design_decisions(uncertain_tasks_output, merged_output_file, goal_model_design_decision_output)
            self.output_field.insert(tk.END, "Satisfied design decisions extracted successfully.\n")
        except Exception as e:
            self.output_field.insert(tk.END, f"Error extracting satisfied design decisions: {str(e)}\n")

    def solve_formula(self):
        global z3_diagram_file 
        z3_diagram_file = filedialog.askopenfilename(title="Select Z3 Diagram JSON file", filetypes=[("JSON files", "*.json")])
        if not z3_diagram_file:
            self.output_field.insert(tk.END, "No file selected.\n")
            return

        global z3_solutions_output 
        z3_solutions_output = os.path.join(output_folder, "Concretizations.json")

        try:
            z3_solver.solve_formula(z3_diagram_file, z3_solutions_output)
            self.output_field.insert(tk.END, "Formula solved successfully.\n")
        except Exception as e:
            self.output_field.insert(tk.END, f"Error solving formula: {str(e)}\n")

    def generate_concretization(self):

        global output_diagram_solutions_folder 
        output_diagram_solutions_folder = os.path.join(output_folder, "solution_diagram")
        if not os.path.exists(output_diagram_solutions_folder):
            os.makedirs(output_diagram_solutions_folder)

        try:
            concretization_generation.generate_concretization(z3_diagram_file, z3_solutions_output, z3_diagram_file, output_diagram_solutions_folder)
            self.output_field.insert(tk.END, "Concretization generated successfully.\n")
        except Exception as e:
            self.output_field.insert(tk.END, f"Error generating concretization: {str(e)}\n")

    def sort_by_tasks(self):

        # Ask user to select mapping CSV file
        global mapping_csv_file 
        mapping_csv_file = filedialog.askopenfilename(title="Select Mapping CSV file", filetypes=[("CSV files", "*.csv")])
        if not mapping_csv_file:
            self.output_field.insert(tk.END, "No mapping CSV file selected.\n")
            return

        try:
            # Call filter.sort_solutions with the selected parameters
            filter.sort_solutions(z3_solutions_output, mapping_csv_file, output_diagram_solutions_folder)
            self.output_field.insert(tk.END, "Solutions sorted by tasks successfully.\n")
        except Exception as e:
            self.output_field.insert(tk.END, f"Error sorting solutions: {str(e)}\n")

    def select_tasks_decisions(self):
        goal_model_design_decision_output = filedialog.askopenfilename(title="Select Design Decisions", filetypes=[("JSON files", "*.json")])
        if not goal_model_design_decision_output:
            self.output_field.insert(tk.END, "No file selected.\n")
            return
        # Create the folder if it doesn't exist
        global satisfied_design_decisions_folder 
        satisfied_design_decisions_folder = os.path.join(output_folder, "Selected_Tasks_Solutions")
        if not os.path.exists(satisfied_design_decisions_folder):
            os.makedirs(satisfied_design_decisions_folder)

        try:
            # Call satisfied_design_decisions.print_files_for_folders with the provided parameters
            satisfied_design_decisions.print_files_for_folders(goal_model_design_decision_output, output_diagram_solutions_folder, satisfied_design_decisions_folder)
            self.output_field.insert(tk.END, "Tasks Design Decisions selected successfully.\n")
        except Exception as e:
            self.output_field.insert(tk.END, f"Error selecting tasks design decisions: {str(e)}\n")

def main():
    
    root = tk.Tk()
    app = SimpleUI(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()
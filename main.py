import extract_uncertainty_tasks
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import satisfied_design_decisions
import concretization_generation
import z3_solver
import xmi2json
import filter
import os 
import merge_json_file
import sys
import shutil
import Analysis
import traceback

def copy_files(source_folder, destination_folder):
    # Create destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Iterate through files in the source folder
    for filename in os.listdir(source_folder):
        source_file = os.path.join(source_folder, filename)
        # Check if it's a file
        if os.path.isfile(source_file):
            destination_file = os.path.join(destination_folder, filename)
            # Copy the file to the destination folder
            shutil.copy2(source_file, destination_file)

class SimpleUI:
    def __init__(self, master):
        self.master = master
        master.title("cTool")

        # Text field on the left
        self.output_field = tk.Text(master, height=30, width=50)  # Reduced width
        self.output_field.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Frame to contain buttons on the right
        self.button_frame = tk.Frame(master)
        self.button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Help Menu
        self.menu_bar = tk.Menu(master)
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="Help", command=self.show_help1)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        master.config(menu=self.menu_bar)

        # Buttons in the button frame
        self.button_convert = tk.Button(self.button_frame, text="1. Import Goal Model", command=self.convert_and_more, compound=tk.LEFT)
        self.button_convert.pack(fill="x", padx=10, pady=5)
        self.button_convert.bind("<Button-3>", lambda event: self.show_help("This button is used to import the goal model it can be an already made goal model or a jucmnav xmi file. If it's the xmi file it will then be converted to json"))

        self.button_extract_tasks = tk.Button(self.button_frame, text="2. Extract Tasks With Uncertainty", command=self.extract_tasks_with_uncertainty, compound=tk.LEFT)
        self.button_extract_tasks.pack(fill="x", padx=10, pady=5)
        self.button_extract_tasks.bind("<Button-3>", lambda event: self.show_help("Also known as design decisions, this button is used to extract the tasks with uncertainty from the goal model. The tasks with uncertainty are defined by having beliefs attached to them in the goal model."))

        self.button_satisfied_design_decisions = tk.Button(self.button_frame, text="3. Detect Imported Decisions Scenario", command=self.satisfied_design_decisions, compound=tk.LEFT)
        self.button_satisfied_design_decisions.pack(fill="x", padx=10, pady=5)
        self.button_satisfied_design_decisions.bind("<Button-3>", lambda event: self.show_help("This button helps extracting design decisions that are satisfied according to the goal model"))

        self.button_solve_formula = tk.Button(self.button_frame, text="4. Import Partial Design Model", command=self.solve_formula, compound=tk.LEFT)
        self.button_solve_formula.pack(fill="x", padx=10, pady=5)
        self.button_solve_formula.bind("<Button-3>", lambda event: self.show_help("This button is used to import the initial partial model where all may elements are set to false it also imports the may formula from the same file as well as the may elements and their addition to the partial model"))

        self.button_generate_concretization = tk.Button(self.button_frame, text="5.Generate all concretizations", command=self.generate_concretization, compound=tk.LEFT)
        self.button_generate_concretization.pack(fill="x", padx=10, pady=5)
        self.button_generate_concretization.bind("<Button-3>", lambda event: self.show_help("This button generates all concretizations of the partial model based on the may formula and the may elements."))

        self.button_sort_tasks = tk.Button(self.button_frame, text="6. Sort concretizations by design decisions", command=self.sort_by_tasks, compound=tk.LEFT)
        self.button_sort_tasks.pack(fill="x", padx=10, pady=5)
        self.button_sort_tasks.bind("<Button-3>", lambda event: self.show_help("This button sorts each solution by design decisions based on the mapping of the may elements to design decisions provided by the user."))

        self.button_multiple_stakeholders_decision = tk.Button(self.button_frame, text="7. Import Decision Scenarios", command=self.multiple_stakeholders_decision, compound=tk.LEFT)
        self.button_multiple_stakeholders_decision.pack(fill="x", padx=10, pady=5)
        self.button_multiple_stakeholders_decision.bind("<Button-3>", lambda event: self.show_help("This button generate the concretization that satisfies the design decisions selected by the user. Select 1 file for a single stakeholder or select multiple files for multiples stakeholders!"))

        self.button_analysis = tk.Button(self.button_frame, text="8. Analyse", command=self.Analysis_of_files, compound=tk.LEFT)
        self.button_analysis.pack(fill="x", padx=10, pady=5)
        self.button_analysis.bind("<Button-3>", lambda event: self.show_help("This button produces a report a pdf format for better understanding and assessment of the situation."))

        # Configure grid weights to make text field expandable
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        # Redirect standard output to a variable
        self.stdout = sys.stdout
        sys.stdout = self

    def write(self, text):
        self.output_field.insert("end", text)
        self.output_field.see("end")
        self.stdout.write(text)
    
    def show_help(self, message):
        messagebox.showinfo("Help", message)

    def show_help1(self):
        messagebox.showinfo("Help", "Right-click each button for help.")
    


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
            self.output_field.insert(tk.END, "Tasks with uncertainty Generated and can be found in {}\n".format(uncertain_tasks_output))
        except Exception as e:
            self.output_field.insert(tk.END, f"Error extracting tasks with uncertainty: {str(e)}\n")

    def satisfied_design_decisions(self):

        uncertain_tasks_output = os.path.join(output_folder, "uncertain_tasks.json")
        merged_output_file = os.path.join(output_folder, "Goal_Model.json")
        goal_model_design_decision_output = os.path.join(output_folder, "Imported_Decision_Scenario.json")

        try:
            satisfied_design_decisions.find_satisfied_design_decisions(uncertain_tasks_output, merged_output_file, goal_model_design_decision_output)
            self.output_field.insert(tk.END, "Decision scenario generated successfully and can be found in {}\n".format(goal_model_design_decision_output))
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
            self.output_field.insert(tk.END, "Solutions generated successfully.\n")
        except Exception as e:
            self.output_field.insert(tk.END, f"Error generating solutions: {str(e)}\n")

    def generate_concretization(self):

        global output_diagram_solutions_folder 
        output_diagram_solutions_folder = os.path.join(output_folder, "generated_concretizations")
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
        output_diagram_solutions_folder2 = output_diagram_solutions_folder + "\decision_sorted_concretizations"
        if not mapping_csv_file:
            self.output_field.insert(tk.END, "No mapping CSV file selected.\n")
            return

        try:
            copy_files(output_diagram_solutions_folder,output_diagram_solutions_folder2)
            # Call filter.sort_solutions with the selected parameters
            filter.sort_solutions(z3_solutions_output, mapping_csv_file, output_diagram_solutions_folder2)
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
            satisfied_design_decisions.print_files_for_folders(goal_model_design_decision_output, output_diagram_solutions_folder + "\decision_sorted_concretizations", satisfied_design_decisions_folder)
            self.output_field.insert(tk.END, "Tasks Design Decisions selected successfully.\n")
        except Exception as e:
            self.output_field.insert(tk.END, f"Error selecting tasks design decisions: {str(e)}\n")
        
    def multiple_stakeholders_decision(self):
        # Ask user to select JSON files
        global json_file_paths1 
        json_file_paths1 = filedialog.askopenfilenames(title="Select JSON Files",filetypes=[("JSON files", "*.json")])
        if not json_file_paths1:
            self.output_field.insert(tk.END, "No file selected.\n")
            return
        try:
            # Call the function to perform the desired operation
            satisfied_design_decisions.multiple_stakeholders_decision(json_file_paths1, output_diagram_solutions_folder + "\decision_sorted_concretizations", output_folder)
        except Exception as e:
             self.output_field.insert(tk.END, f"Error generating multiple stakeholders design decisions: {str(e)}\n")
        
    def Analysis_of_files(self):

        try:
            Analysis.merge_json_files(json_file_paths1, output_folder + "/Stakeholder_Choices.json")
            Analysis.analyze_stakeholder("Stakeholder1", output_folder + "/Stakeholders_report.json", output_folder + "/Stakeholder_Choices.json", output_folder)
            os.remove(output_folder + "/Stakeholder_Choices.json")
            Analysis.generate_pdf_from_json(output_folder + "/report.json", output_folder + "/report.pdf")
            self.output_field.insert(tk.END, "Analysis PDF Generated and can be found in {}/report.pdf\n".format(output_folder))
        except Exception as e:
            error_message = f"Error generating Analysis: {str(e)}\n"
            detailed_error_message = traceback.format_exc()
            self.output_field.insert(tk.END, error_message)
            self.output_field.insert(tk.END, detailed_error_message)



def main():
    
    root = tk.Tk()
    app = SimpleUI(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()
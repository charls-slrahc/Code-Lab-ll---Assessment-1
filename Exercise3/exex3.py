import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

class StudentManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("800x600")
        
        # Apply blueish color theme
        self.root.configure(bg='#e6f2ff')
        
        # Data storage
        self.students = []
        self.filename = "studentMarks.txt"
        
        # Load data
        self.load_data()
        
        # Create GUI
        self.create_gui()
    
    def load_data(self):
        """Load student data from file"""
        try:
            if not os.path.exists(self.filename):
                # Create sample data if file doesn't exist
                self.create_sample_data()
            
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                
            # First line is number of students
            if lines:
                num_students = int(lines[0].strip())
                
            # Process student data
            self.students = []
            for line in lines[1:1+num_students]:
                data = line.strip().split(',')
                if len(data) >= 6:
                    student = {
                        'code': int(data[0]),
                        'name': data[1],
                        'coursework1': int(data[2]),
                        'coursework2': int(data[3]),
                        'coursework3': int(data[4]),
                        'exam': int(data[5])
                    }
                    self.students.append(student)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
            self.students = []
    
    def load_jokes(self):
        """Load marks from studentMarks file"""
   
        with open('studentMarks.txt', 'r', encoding='utf-8') as file:
                jokes = [line.strip() for line in file if line.strip()]
        return jokes
    
    def save_data(self):
        """Save student data to file"""
        try:
            with open(self.filename, 'w') as file:
                file.write(f"{len(self.students)}\n")
                for student in self.students:
                    file.write(f"{student['code']},{student['name']},{student['coursework1']},{student['coursework2']},{student['coursework3']},{student['exam']}\n")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
            return False
    
    def calculate_percentage(self, student):
        """Calculate overall percentage"""
        total_coursework = student['coursework1'] + student['coursework2'] + student['coursework3']
        total_marks = total_coursework + student['exam']  # Max 60 coursework + 100 exam = 160
        percentage = (total_marks / 160) * 100
        return round(percentage, 2)
    
    def calculate_grade(self, percentage):
        """Calculate grade based on percentage"""
        if percentage >= 70:
            return 'A'
        elif percentage >= 60:
            return 'B'
        elif percentage >= 50:
            return 'C'
        elif percentage >= 40:
            return 'D'
        else:
            return 'F'
    
    def create_gui(self):
        """Create the main GUI"""
        # Configure styles for blueish theme
        style = ttk.Style()
        style.configure('Blue.TFrame', background='#e6f2ff')
        style.configure('Blue.TLabel', background='#e6f2ff', foreground='#003366', font=('Arial', 10))
        style.configure('Title.TLabel', background='#e6f2ff', foreground='#003366', font=('Arial', 16, 'bold'))
        style.configure('Blue.TButton', background='#4da6ff', foreground='#003366', font=('Arial', 10))
        style.map('Blue.TButton', background=[('active', '#3399ff'), ('pressed', '#0073e6')])
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10", style='Blue.TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Student Manager", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Menu buttons
        buttons = [
            ("1. View All Student Records", self.view_all_students),
            ("2. View Individual Student Record", self.view_individual_student),
            ("3. Show Student with Highest Mark", self.show_highest_student),
            ("4. Show Student with Lowest Mark", self.show_lowest_student),
            ("5. Sort Student Records", self.sort_students),
            ("6. Add Student Record", self.add_student),
            ("7. Delete Student Record", self.delete_student),
            ("8. Update Student Record", self.update_student)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(main_frame, text=text, command=command, width=30, style='Blue.TButton')
            btn.grid(row=i+1, column=0, pady=5, padx=10, sticky=tk.W)
        
        # Results area with blueish background
        self.results_text = tk.Text(main_frame, width=70, height=25, wrap=tk.WORD, 
                                   bg='#f0f8ff', fg='#003366', font=('Arial', 10),
                                   selectbackground='#cce5ff', selectforeground='#003366')
        self.results_text.grid(row=1, column=1, rowspan=8, padx=10, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for results
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        scrollbar.grid(row=1, column=2, rowspan=8, sticky=(tk.N, tk.S))
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(8, weight=1)
    
    def display_results(self, text):
        """Display results in the text widget"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, text)
    
    def format_student_output(self, student):
        """Format individual student output"""
        percentage = self.calculate_percentage(student)
        grade = self.calculate_grade(percentage)
        total_coursework = student['coursework1'] + student['coursework2'] + student['coursework3']
        
        output = f"Student Name: {student['name']}\n"
        output += f"Student Number: {student['code']}\n"
        output += f"Total Coursework: {total_coursework}/60\n"
        output += f"Exam Mark: {student['exam']}/100\n"
        output += f"Overall Percentage: {percentage}%\n"
        output += f"Grade: {grade}\n"
        output += "-" * 50 + "\n"
        
        return output
    
    def view_all_students(self):
        """Menu item 1: View all student records"""
        if not self.students:
            self.display_results("No student records found.")
            return
        
        output = "ALL STUDENT RECORDS\n"
        output += "=" * 50 + "\n\n"
        
        total_percentage = 0
        
        for student in self.students:
            output += self.format_student_output(student)
            total_percentage += self.calculate_percentage(student)
        
        # Summary
        avg_percentage = total_percentage / len(self.students)
        output += f"\nSUMMARY:\n"
        output += f"Number of students: {len(self.students)}\n"
        output += f"Average percentage: {avg_percentage:.2f}%\n"
        
        self.display_results(output)
    
    def view_individual_student(self):
        """Menu item 2: View individual student record"""
        if not self.students:
            messagebox.showwarning("Warning", "No student records available.")
            return
        
        # Create selection dialog with blueish theme
        selection_window = tk.Toplevel(self.root)
        selection_window.title("Select Student")
        selection_window.geometry("300x200")
        selection_window.configure(bg='#e6f2ff')
        
        ttk.Label(selection_window, text="Select Student:", style='Blue.TLabel').pack(pady=10)
        
        # Create combobox with student names and codes
        student_list = [f"{s['code']} - {s['name']}" for s in self.students]
        combo_var = tk.StringVar()
        student_combo = ttk.Combobox(selection_window, textvariable=combo_var, values=student_list, state="readonly")
        student_combo.pack(pady=10)
        
        def show_selected():
            selected_index = student_combo.current()
            if selected_index >= 0:
                student = self.students[selected_index]
                output = "INDIVIDUAL STUDENT RECORD\n"
                output += "=" * 50 + "\n\n"
                output += self.format_student_output(student)
                self.display_results(output)
                selection_window.destroy()
        
        ttk.Button(selection_window, text="Show Record", command=show_selected, style='Blue.TButton').pack(pady=10)
    
    def show_highest_student(self):
        """Menu item 3: Show student with highest overall mark"""
        if not self.students:
            messagebox.showwarning("Warning", "No student records available.")
            return
        
        highest_student = max(self.students, key=lambda x: self.calculate_percentage(x))
        
        output = "STUDENT WITH HIGHEST MARK\n"
        output += "=" * 50 + "\n\n"
        output += self.format_student_output(highest_student)
        
        self.display_results(output)
    
    def show_lowest_student(self):
        """Menu item 4: Show student with lowest overall mark"""
        if not self.students:
            messagebox.showwarning("Warning", "No student records available.")
            return
        
        lowest_student = min(self.students, key=lambda x: self.calculate_percentage(x))
        
        output = "STUDENT WITH LOWEST MARK\n"
        output += "=" * 50 + "\n\n"
        output += self.format_student_output(lowest_student)
        
        self.display_results(output)
    
    def sort_students(self):
        """Menu item 5: Sort student records"""
        if not self.students:
            messagebox.showwarning("Warning", "No student records available.")
            return
        
        # Create sort selection dialog with blueish theme
        sort_window = tk.Toplevel(self.root)
        sort_window.title("Sort Students")
        sort_window.geometry("250x150")
        sort_window.configure(bg='#e6f2ff')
        
        ttk.Label(sort_window, text="Sort by:", style='Blue.TLabel').pack(pady=10)
        
        sort_var = tk.StringVar(value="percentage")
        
        ttk.Radiobutton(sort_window, text="Percentage (Descending)", 
                       variable=sort_var, value="percentage", style='Blue.TLabel').pack(anchor=tk.W)
        ttk.Radiobutton(sort_window, text="Name (Ascending)", 
                       variable=sort_var, value="name", style='Blue.TLabel').pack(anchor=tk.W)
        ttk.Radiobutton(sort_window, text="Student Code (Ascending)", 
                       variable=sort_var, value="code", style='Blue.TLabel').pack(anchor=tk.W)
        
        def perform_sort():
            if sort_var.get() == "percentage":
                sorted_students = sorted(self.students, key=lambda x: self.calculate_percentage(x), reverse=True)
            elif sort_var.get() == "name":
                sorted_students = sorted(self.students, key=lambda x: x['name'])
            else:  # code
                sorted_students = sorted(self.students, key=lambda x: x['code'])
            
            output = f"SORTED STUDENT RECORDS ({sort_var.get().upper()})\n"
            output += "=" * 50 + "\n\n"
            
            total_percentage = 0
            for student in sorted_students:
                output += self.format_student_output(student)
                total_percentage += self.calculate_percentage(student)
            
            # Summary
            avg_percentage = total_percentage / len(sorted_students)
            output += f"\nSUMMARY:\n"
            output += f"Number of students: {len(sorted_students)}\n"
            output += f"Average percentage: {avg_percentage:.2f}%\n"
            
            self.display_results(output)
            sort_window.destroy()
        
        ttk.Button(sort_window, text="Sort", command=perform_sort, style='Blue.TButton').pack(pady=10)
    
    def add_student(self):
        """Menu item 6: Add a student record"""
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Student")
        add_window.geometry("300x350")
        add_window.configure(bg='#e6f2ff')
        
        # Form fields
        ttk.Label(add_window, text="Student Code:", style='Blue.TLabel').pack(pady=5)
        code_entry = ttk.Entry(add_window)
        code_entry.pack(pady=5)
        
        ttk.Label(add_window, text="Student Name:", style='Blue.TLabel').pack(pady=5)
        name_entry = ttk.Entry(add_window)
        name_entry.pack(pady=5)
        
        ttk.Label(add_window, text="Coursework 1 (0-20):", style='Blue.TLabel').pack(pady=5)
        cw1_entry = ttk.Entry(add_window)
        cw1_entry.pack(pady=5)
        
        ttk.Label(add_window, text="Coursework 2 (0-20):", style='Blue.TLabel').pack(pady=5)
        cw2_entry = ttk.Entry(add_window)
        cw2_entry.pack(pady=5)
        
        ttk.Label(add_window, text="Coursework 3 (0-20):", style='Blue.TLabel').pack(pady=5)
        cw3_entry = ttk.Entry(add_window)
        cw3_entry.pack(pady=5)
        
        ttk.Label(add_window, text="Exam Mark (0-100):", style='Blue.TLabel').pack(pady=5)
        exam_entry = ttk.Entry(add_window)
        exam_entry.pack(pady=5)
        
        def save_student():
            try:
                # Validate inputs
                code = int(code_entry.get())
                name = name_entry.get().strip()
                cw1 = int(cw1_entry.get())
                cw2 = int(cw2_entry.get())
                cw3 = int(cw3_entry.get())
                exam = int(exam_entry.get())
                
                if not (1000 <= code <= 9999):
                    messagebox.showerror("Error", "Student code must be between 1000 and 9999")
                    return
                
                if not name:
                    messagebox.showerror("Error", "Student name is required")
                    return
                
                if not (0 <= cw1 <= 20) or not (0 <= cw2 <= 20) or not (0 <= cw3 <= 20):
                    messagebox.showerror("Error", "Coursework marks must be between 0 and 20")
                    return
                
                if not (0 <= exam <= 100):
                    messagebox.showerror("Error", "Exam mark must be between 0 and 100")
                    return
                
                # Check if code already exists
                if any(s['code'] == code for s in self.students):
                    messagebox.showerror("Error", "Student code already exists")
                    return
                
                # Add new student
                new_student = {
                    'code': code,
                    'name': name,
                    'coursework1': cw1,
                    'coursework2': cw2,
                    'coursework3': cw3,
                    'exam': exam
                }
                
                self.students.append(new_student)
                
                if self.save_data():
                    messagebox.showinfo("Success", "Student added successfully!")
                    add_window.destroy()
                    self.view_all_students()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for all marks")
        
        ttk.Button(add_window, text="Save", command=save_student, style='Blue.TButton').pack(pady=10)
    
    def delete_student(self):
        """Menu item 7: Delete a student record"""
        if not self.students:
            messagebox.showwarning("Warning", "No student records available.")
            return
        
        # Create selection dialog with blueish theme
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete Student")
        delete_window.geometry("300x200")
        delete_window.configure(bg='#e6f2ff')
        
        ttk.Label(delete_window, text="Select Student to Delete:", style='Blue.TLabel').pack(pady=10)
        
        student_list = [f"{s['code']} - {s['name']}" for s in self.students]
        combo_var = tk.StringVar()
        student_combo = ttk.Combobox(delete_window, textvariable=combo_var, values=student_list, state="readonly")
        student_combo.pack(pady=10)
        
        def delete_selected():
            selected_index = student_combo.current()
            if selected_index >= 0:
                student = self.students[selected_index]
                if messagebox.askyesno("Confirm", f"Delete {student['name']} ({student['code']})?"):
                    del self.students[selected_index]
                    if self.save_data():
                        messagebox.showinfo("Success", "Student deleted successfully!")
                        delete_window.destroy()
                        self.view_all_students()
        
        ttk.Button(delete_window, text="Delete", command=delete_selected, style='Blue.TButton').pack(pady=10)
    
    def update_student(self):
        """Menu item 8: Update a student record"""
        if not self.students:
            messagebox.showwarning("Warning", "No student records available.")
            return
        
        # Create selection dialog with blueish theme
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Student")
        update_window.geometry("300x200")
        update_window.configure(bg='#e6f2ff')
        
        ttk.Label(update_window, text="Select Student to Update:", style='Blue.TLabel').pack(pady=10)
        
        student_list = [f"{s['code']} - {s['name']}" for s in self.students]
        combo_var = tk.StringVar()
        student_combo = ttk.Combobox(update_window, textvariable=combo_var, values=student_list, state="readonly")
        student_combo.pack(pady=10)
        
        def update_selected():
            selected_index = student_combo.current()
            if selected_index >= 0:
                student = self.students[selected_index]
                update_window.destroy()
                self.show_update_form(student, selected_index)
        
        ttk.Button(update_window, text="Update", command=update_selected, style='Blue.TButton').pack(pady=10)
    
    def show_update_form(self, student, index):
        """Show form to update student details"""
        update_form = tk.Toplevel(self.root)
        update_form.title(f"Update {student['name']}")
        update_form.geometry("300x350")
        update_form.configure(bg='#e6f2ff')
        
        # Form fields with current values
        ttk.Label(update_form, text="Student Name:", style='Blue.TLabel').pack(pady=5)
        name_entry = ttk.Entry(update_form)
        name_entry.insert(0, student['name'])
        name_entry.pack(pady=5)
        
        ttk.Label(update_form, text="Coursework 1 (0-20):", style='Blue.TLabel').pack(pady=5)
        cw1_entry = ttk.Entry(update_form)
        cw1_entry.insert(0, str(student['coursework1']))
        cw1_entry.pack(pady=5)
        
        ttk.Label(update_form, text="Coursework 2 (0-20):", style='Blue.TLabel').pack(pady=5)
        cw2_entry = ttk.Entry(update_form)
        cw2_entry.insert(0, str(student['coursework2']))
        cw2_entry.pack(pady=5)
        
        ttk.Label(update_form, text="Coursework 3 (0-20):", style='Blue.TLabel').pack(pady=5)
        cw3_entry = ttk.Entry(update_form)
        cw3_entry.insert(0, str(student['coursework3']))
        cw3_entry.pack(pady=5)
        
        ttk.Label(update_form, text="Exam Mark (0-100):", style='Blue.TLabel').pack(pady=5)
        exam_entry = ttk.Entry(update_form)
        exam_entry.insert(0, str(student['exam']))
        exam_entry.pack(pady=5)
        
        def save_update():
            try:
                name = name_entry.get().strip()
                cw1 = int(cw1_entry.get())
                cw2 = int(cw2_entry.get())
                cw3 = int(cw3_entry.get())
                exam = int(exam_entry.get())
                
                if not name:
                    messagebox.showerror("Error", "Student name is required")
                    return
                
                if not (0 <= cw1 <= 20) or not (0 <= cw2 <= 20) or not (0 <= cw3 <= 20):
                    messagebox.showerror("Error", "Coursework marks must be between 0 and 20")
                    return
                
                if not (0 <= exam <= 100):
                    messagebox.showerror("Error", "Exam mark must be between 0 and 100")
                    return
                
                # Update student
                self.students[index]['name'] = name
                self.students[index]['coursework1'] = cw1
                self.students[index]['coursework2'] = cw2
                self.students[index]['coursework3'] = cw3
                self.students[index]['exam'] = exam
                
                if self.save_data():
                    messagebox.showinfo("Success", "Student updated successfully!")
                    update_form.destroy()
                    self.view_all_students()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for all marks")
        
        ttk.Button(update_form, text="Save Changes", command=save_update, style='Blue.TButton').pack(pady=10)

def main():
    root = tk.Tk()
    app = StudentManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
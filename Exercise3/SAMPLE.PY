import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

class StudentManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("800x600")
        
        # Blueish color scheme
        self.bg_color = "#f0f8ff"  # Alice Blue
        self.accent_color = "#1e90ff"  # Dodger Blue
        self.button_color = "#4169e1"  # Royal Blue
        self.highlight_color = "#87ceeb"  # Sky Blue
        self.text_color = "#2c3e50"  # Dark Blue-Gray
        self.success_color = "#228b22"  # Forest Green
        self.warning_color = "#ff8c00"  # Dark Orange
        self.error_color = "#dc143c"  # Crimson
        
        self.root.configure(bg=self.bg_color)
        
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
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.bg_color, padx=15, pady=15)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="🎓 Student Manager", 
            font=("Arial", 18, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Menu buttons
        buttons = [
            ("📋 View All Student Records", self.view_all_students),
            ("👤 View Individual Student", self.view_individual_student),
            ("🏆 Student with Highest Mark", self.show_highest_student),
            ("📉 Student with Lowest Mark", self.show_lowest_student),
            ("🔄 Sort Student Records", self.sort_students),
            ("➕ Add Student Record", self.add_student),
            ("🗑️ Delete Student Record", self.delete_student),
            ("✏️ Update Student Record", self.update_student)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = tk.Button(
                main_frame, 
                text=text, 
                command=command, 
                width=25,
                height=2,
                font=("Arial", 10, "bold"),
                bg=self.button_color,
                fg="white",
                activebackground=self.highlight_color,
                activeforeground="white",
                relief="raised",
                bd=2
            )
            btn.grid(row=i+1, column=0, pady=6, padx=10, sticky=tk.W)
        
        # Results area frame
        results_frame = tk.Frame(main_frame, bg="white", relief="sunken", bd=2)
        results_frame.grid(row=1, column=1, rowspan=8, padx=10, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Results text widget
        self.results_text = tk.Text(
            results_frame, 
            width=70, 
            height=25, 
            wrap=tk.WORD,
            bg="#fafafa",
            fg=self.text_color,
            font=("Consolas", 10),
            relief="flat",
            padx=10,
            pady=10
        )
        self.results_text.pack(fill='both', expand=True)
        
        # Scrollbar for results
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
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
        output += "─" * 50 + "\n"
        
        return output
    
    def view_all_students(self):
        """Menu item 1: View all student records"""
        if not self.students:
            self.display_results("No student records found.")
            return
        
        output = "🎓 ALL STUDENT RECORDS\n"
        output += "=" * 50 + "\n\n"
        
        total_percentage = 0
        
        for student in self.students:
            output += self.format_student_output(student)
            total_percentage += self.calculate_percentage(student)
        
        # Summary
        avg_percentage = total_percentage / len(self.students)
        output += f"\n📊 SUMMARY:\n"
        output += f"Number of students: {len(self.students)}\n"
        output += f"Average percentage: {avg_percentage:.2f}%\n"
        
        self.display_results(output)
    
    def view_individual_student(self):
        """Menu item 2: View individual student record"""
        if not self.students:
            messagebox.showwarning("Warning", "No student records available.")
            return
        
        # Create selection dialog
        selection_window = tk.Toplevel(self.root)
        selection_window.title("Select Student")
        selection_window.geometry("350x250")
        selection_window.configure(bg=self.bg_color)
        selection_window.resizable(False, False)
        
        tk.Label(
            selection_window, 
            text="👤 Select Student:", 
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        ).pack(pady=15)
        
        # Create combobox with student names and codes
        student_list = [f"{s['code']} - {s['name']}" for s in self.students]
        combo_var = tk.StringVar()
        student_combo = ttk.Combobox(selection_window, textvariable=combo_var, values=student_list, state="readonly")
        student_combo.pack(pady=15)
        
        def show_selected():
            selected_index = student_combo.current()
            if selected_index >= 0:
                student = self.students[selected_index]
                output = "👤 INDIVIDUAL STUDENT RECORD\n"
                output += "=" * 50 + "\n\n"
                output += self.format_student_output(student)
                self.display_results(output)
                selection_window.destroy()
        
        tk.Button(
            selection_window, 
            text="Show Record", 
            command=show_selected,
            bg=self.button_color,
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            height=1
        ).pack(pady=10)
    
    def show_highest_student(self):
        """Menu item 3: Show student with highest overall mark"""
        if not self.students:
            messagebox.showwarning("Warning", "No student records available.")
            return
        
        highest_student = max(self.students, key=lambda x: self.calculate_percentage(x))
        
        output = "🏆 STUDENT WITH HIGHEST MARK\n"
        output += "=" * 50 + "\n\n"
        output += self.format_student_output(highest_student)
        
        self.display_results(output)
    
    def show_lowest_student(self):
        """Menu item 4: Show student with lowest overall mark"""
        if not self.students:
            messagebox.showwarning("Warning", "No student records available.")
            return
        
        lowest_student = min(self.students, key=lambda x: self.calculate_percentage(x))
        
        output = "📉 STUDENT WITH LOWEST MARK\n"
        output += "=" * 50 + "\n\n"
        output += self.format_student_output(lowest_student)
        
        self.display_results(output)
    
    def sort_students(self):
        """Menu item 5: Sort student records"""
        if not self.students:
            messagebox.showwarning("Warning", "No student records available.")
            return
        
        # Create sort selection dialog
        sort_window = tk.Toplevel(self.root)
        sort_window.title("Sort Students")
        sort_window.geometry("300x200")
        sort_window.configure(bg=self.bg_color)
        sort_window.resizable(False, False)
        
        tk.Label(
            sort_window, 
            text="🔄 Sort by:", 
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        ).pack(pady=15)
        
        sort_var = tk.StringVar(value="percentage")
        
        tk.Radiobutton(
            sort_window, 
            text="📊 Percentage (Descending)", 
            variable=sort_var, 
            value="percentage",
            bg=self.bg_color,
            fg=self.text_color,
            font=("Arial", 10)
        ).pack(anchor=tk.W, pady=5)
        
        tk.Radiobutton(
            sort_window, 
            text="👤 Name (Ascending)", 
            variable=sort_var, 
            value="name",
            bg=self.bg_color,
            fg=self.text_color,
            font=("Arial", 10)
        ).pack(anchor=tk.W, pady=5)
        
        tk.Radiobutton(
            sort_window, 
            text="🔢 Student Code (Ascending)", 
            variable=sort_var, 
            value="code",
            bg=self.bg_color,
            fg=self.text_color,
            font=("Arial", 10)
        ).pack(anchor=tk.W, pady=5)
        
        def perform_sort():
            if sort_var.get() == "percentage":
                sorted_students = sorted(self.students, key=lambda x: self.calculate_percentage(x), reverse=True)
            elif sort_var.get() == "name":
                sorted_students = sorted(self.students, key=lambda x: x['name'])
            else:  # code
                sorted_students = sorted(self.students, key=lambda x: x['code'])
            
            output = f"🔄 SORTED STUDENT RECORDS ({sort_var.get().upper()})\n"
            output += "=" * 50 + "\n\n"
            
            total_percentage = 0
            for student in sorted_students:
                output += self.format_student_output(student)
                total_percentage += self.calculate_percentage(student)
            
            # Summary
            avg_percentage = total_percentage / len(sorted_students)
            output += f"\n📊 SUMMARY:\n"
            output += f"Number of students: {len(sorted_students)}\n"
            output += f"Average percentage: {avg_percentage:.2f}%\n"
            
            self.display_results(output)
            sort_window.destroy()
        
        tk.Button(
            sort_window, 
            text="Sort", 
            command=perform_sort,
            bg=self.button_color,
            fg="white",
            font=("Arial", 10, "bold"),
            width=10
        ).pack(pady=15)
    
    def add_student(self):
        """Menu item 6: Add a student record"""
        add_window = tk.Toplevel(self.root)
        add_window.title("➕ Add Student")
        add_window.geometry("350x400")
        add_window.configure(bg=self.bg_color)
        add_window.resizable(False, False)
        
        # Form fields
        labels = [
            "🔢 Student Code:",
            "👤 Student Name:",
            "📝 Coursework 1 (0-20):",
            "📝 Coursework 2 (0-20):",
            "📝 Coursework 3 (0-20):",
            "📊 Exam Mark (0-100):"
        ]
        
        entries = []
        for i, label_text in enumerate(labels):
            tk.Label(
                add_window, 
                text=label_text,
                bg=self.bg_color,
                fg=self.text_color,
                font=("Arial", 10)
            ).pack(pady=8)
            entry = tk.Entry(add_window, font=("Arial", 10), width=25)
            entry.pack(pady=5)
            entries.append(entry)
        
        code_entry, name_entry, cw1_entry, cw2_entry, cw3_entry, exam_entry = entries
        
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
                    messagebox.showinfo("Success", "✅ Student added successfully!")
                    add_window.destroy()
                    self.view_all_students()
                
            except ValueError:
                messagebox.showerror("Error", "❌ Please enter valid numbers for all marks")
        
        tk.Button(
            add_window, 
            text="💾 Save Student", 
            command=save_student,
            bg=self.success_color,
            fg="white",
            font=("Arial", 10, "bold"),
            width=15
        ).pack(pady=15)
    
    def delete_student(self):
        """Menu item 7: Delete a student record"""
        if not self.students:
            messagebox.showwarning("Warning", "No student records available.")
            return
        
        # Create selection dialog
        delete_window = tk.Toplevel(self.root)
        delete_window.title("🗑️ Delete Student")
        delete_window.geometry("350x200")
        delete_window.configure(bg=self.bg_color)
        delete_window.resizable(False, False)
        
        tk.Label(
            delete_window, 
            text="❌ Select Student to Delete:", 
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        ).pack(pady=15)
        
        student_list = [f"{s['code']} - {s['name']}" for s in self.students]
        combo_var = tk.StringVar()
        student_combo = ttk.Combobox(delete_window, textvariable=combo_var, values=student_list, state="readonly")
        student_combo.pack(pady=15)
        
        def delete_selected():
            selected_index = student_combo.current()
            if selected_index >= 0:
                student = self.students[selected_index]
                if messagebox.askyesno("Confirm", f"Delete {student['name']} ({student['code']})?"):
                    del self.students[selected_index]
                    if self.save_data():
                        messagebox.showinfo("Success", "✅ Student deleted successfully!")
                        delete_window.destroy()
                        self.view_all_students()
        
        tk.Button(
            delete_window, 
            text="🗑️ Delete", 
            command=delete_selected,
            bg=self.error_color,
            fg="white",
            font=("Arial", 10, "bold"),
            width=12
        ).pack(pady=10)
    
    def update_student(self):
        """Menu item 8: Update a student record"""
        if not self.students:
            messagebox.showwarning("Warning", "No student records available.")
            return
        
        # Create selection dialog
        update_window = tk.Toplevel(self.root)
        update_window.title("✏️ Update Student")
        update_window.geometry("350x200")
        update_window.configure(bg=self.bg_color)
        update_window.resizable(False, False)
        
        tk.Label(
            update_window, 
            text="✏️ Select Student to Update:", 
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        ).pack(pady=15)
        
        student_list = [f"{s['code']} - {s['name']}" for s in self.students]
        combo_var = tk.StringVar()
        student_combo = ttk.Combobox(update_window, textvariable=combo_var, values=student_list, state="readonly")
        student_combo.pack(pady=15)
        
        def update_selected():
            selected_index = student_combo.current()
            if selected_index >= 0:
                student = self.students[selected_index]
                update_window.destroy()
                self.show_update_form(student, selected_index)
        
        tk.Button(
            update_window, 
            text="✏️ Update", 
            command=update_selected,
            bg=self.warning_color,
            fg="white",
            font=("Arial", 10, "bold"),
            width=12
        ).pack(pady=10)
    
    def show_update_form(self, student, index):
        """Show form to update student details"""
        update_form = tk.Toplevel(self.root)
        update_form.title(f"✏️ Update {student['name']}")
        update_form.geometry("350x400")
        update_form.configure(bg=self.bg_color)
        update_form.resizable(False, False)
        
        # Form fields with current values
        labels = [
            "👤 Student Name:",
            "📝 Coursework 1 (0-20):",
            "📝 Coursework 2 (0-20):",
            "📝 Coursework 3 (0-20):",
            "📊 Exam Mark (0-100):"
        ]
        
        entries = []
        for i, label_text in enumerate(labels):
            tk.Label(
                update_form, 
                text=label_text,
                bg=self.bg_color,
                fg=self.text_color,
                font=("Arial", 10)
            ).pack(pady=8)
            entry = tk.Entry(update_form, font=("Arial", 10), width=25)
            entry.pack(pady=5)
            entries.append(entry)
        
        name_entry, cw1_entry, cw2_entry, cw3_entry, exam_entry = entries
        
        # Pre-fill current values
        name_entry.insert(0, student['name'])
        cw1_entry.insert(0, str(student['coursework1']))
        cw2_entry.insert(0, str(student['coursework2']))
        cw3_entry.insert(0, str(student['coursework3']))
        exam_entry.insert(0, str(student['exam']))
        
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
                    messagebox.showinfo("Success", "✅ Student updated successfully!")
                    update_form.destroy()
                    self.view_all_students()
                
            except ValueError:
                messagebox.showerror("Error", "❌ Please enter valid numbers for all marks")
        
        tk.Button(
            update_form, 
            text="💾 Save Changes", 
            command=save_update,
            bg=self.success_color,
            fg="white",
            font=("Arial", 10, "bold"),
            width=15
        ).pack(pady=15)

def main():
    root = tk.Tk()
    app = StudentManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
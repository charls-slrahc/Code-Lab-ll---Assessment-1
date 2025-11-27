import tkinter as tk
import random
from PIL import Image, ImageTk
import os

class ArithmeticQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Arithmetic Quiz")
        self.WIDTH, self.HEIGHT = 900, 600
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.root.resizable(False, False)
        
        # Colors
        self.bg_color = "#f0f8ff"
        self.paper_color = "#ffffff"
        self.button_color = "#4CAF50"
        self.accent_color = "#2196F3"
        
        # Quiz variables
        self.difficulty = None
        self.score = 0
        self.current_question = 0
        self.total_questions = 10
        
        self.setup_gui()
        self.show_welcome()

    def setup_gui(self):
        self.root.configure(bg=self.bg_color)
        self.create_paper_card()
        self.create_frames()
        self.create_widgets()

    def create_paper_card(self):
        self.paper_shadow = tk.Frame(self.root, bg='#b0bec5')
        self.paper_shadow.place(relx=0.5, rely=0.5, anchor='center', width=608, height=458)

        self.paper_frame = tk.Frame(self.root, bg=self.paper_color, bd=2, relief='ridge')
        self.paper_frame.place(relx=0.5, rely=0.5, anchor='center', width=600, height=450)

    def create_frames(self):
        self.welcome_frame = tk.Frame(self.root, bg=self.bg_color)
        self.menu_frame = tk.Frame(self.paper_frame, bg=self.paper_color)
        self.quiz_frame = tk.Frame(self.paper_frame, bg=self.paper_color)
        self.results_frame = tk.Frame(self.paper_frame, bg=self.paper_color)

    def create_widgets(self):
        # Welcome widgets
        try:
            base_dir = os.path.dirname(__file__)
            image_path = os.path.join(base_dir, 'Exercise1WelcomePage.png')
            if not os.path.exists(image_path):
                image_path = os.path.join(base_dir, '..', 'Exercise1WelcomePage.png')
            if os.path.exists(image_path):
                img = Image.open(image_path)
                img = img.resize((self.WIDTH, self.HEIGHT), Image.LANCZOS)
                self.welcome_img = ImageTk.PhotoImage(img)
                self.welcome_bg = tk.Label(self.welcome_frame, image=self.welcome_img)
                self.welcome_bg.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception:
            tk.Label(self.welcome_frame, text='Welcome to Arithmetic Quiz!', 
                    font=('Arial', 28, 'bold'), bg=self.bg_color, fg=self.accent_color).pack(pady=40)
        
        self.start_btn = self.create_button(self.welcome_frame, 'START QUIZ', self.show_difficulty_menu,
                                          font=('Arial', 16, 'bold'), bg=self.accent_color)
        self.start_btn.place(relx=0.5, rely=0.75, anchor='center')

        # Menu widgets
        tk.Label(self.menu_frame, text="SELECT DIFFICULTY", font=("Arial", 20, "bold"), 
                bg=self.paper_color, fg=self.accent_color).pack(pady=30)
        
        self.easy_btn = self.create_button(self.menu_frame, "EASY", lambda: self.start_quiz("easy"),
                                         bg="#4CAF50", font=("Arial", 16, "bold"))
        self.moderate_btn = self.create_button(self.menu_frame, "MODERATE", lambda: self.start_quiz("moderate"),
                                             bg="#FF9800", font=("Arial", 16, "bold"))
        self.advanced_btn = self.create_button(self.menu_frame, "ADVANCED", lambda: self.start_quiz("advanced"),
                                             bg="#F44336", font=("Arial", 16, "bold"))
        
        self.easy_btn.pack(pady=15)
        self.moderate_btn.pack(pady=15)
        self.advanced_btn.pack(pady=15)

        # Quiz widgets
        header_frame = tk.Frame(self.quiz_frame, bg=self.paper_color)
        header_frame.pack(pady=10)
        
        self.score_label = tk.Label(header_frame, text="Score: 0", font=("Arial", 16, "bold"), bg=self.paper_color)
        self.question_label = tk.Label(header_frame, text="Question: 1/10", font=("Arial", 16, "bold"), bg=self.paper_color)
        self.score_label.pack(side='left', padx=20)
        self.question_label.pack(side='right', padx=20)
        
        self.problem_label = tk.Label(self.quiz_frame, text="", font=("Arial", 32, "bold"), bg=self.paper_color)
        self.problem_label.pack(expand=True, pady=30)
        
        self.answer_entry = tk.Entry(self.quiz_frame, font=("Arial", 20), width=8, justify='center')
        self.answer_entry.pack(pady=10)
        
        self.submit_btn = self.create_button(self.quiz_frame, "SUBMIT", self.check_answer)
        self.submit_btn.pack(pady=10)
        
        self.feedback_label = tk.Label(self.quiz_frame, text="", font=("Arial", 14), bg=self.paper_color)
        self.feedback_label.pack(pady=10)

        # Results widgets
        tk.Label(self.results_frame, text="QUIZ COMPLETED!", font=("Arial", 24, "bold"), 
                bg=self.paper_color, fg=self.accent_color).pack(pady=30)
        
        self.final_score_label = tk.Label(self.results_frame, text="", font=("Arial", 20), bg=self.paper_color)
        self.grade_label = tk.Label(self.results_frame, text="", font=("Arial", 22, "bold"), bg=self.paper_color)
        self.final_score_label.pack(pady=15)
        self.grade_label.pack(pady=15)
        
        buttons_frame = tk.Frame(self.results_frame, bg=self.paper_color)
        buttons_frame.pack(pady=30)
        
        self.play_again_btn = self.create_button(buttons_frame, "PLAY AGAIN", self.restart_quiz)
        self.quit_btn = self.create_button(buttons_frame, "QUIT", self.root.quit, bg="#f44336")
        self.play_again_btn.pack(side='left', padx=10)
        self.quit_btn.pack(side='right', padx=10)

    def create_button(self, parent, text, command, **kwargs):
        btn = tk.Button(parent, text=text, command=command, 
                       font=kwargs.get('font', ("Arial", 14, "bold")),
                       bg=kwargs.get('bg', self.button_color),
                       fg='white', width=12, height=1)
        return btn

    def show_welcome(self):
        self.hide_all_frames()
        self.welcome_frame.pack(expand=True, fill='both')

    def show_difficulty_menu(self):
        self.hide_all_frames()
        self.menu_frame.pack(expand=True, fill='both')

    def start_quiz(self, difficulty):
        self.difficulty = difficulty
        self.score = 0
        self.current_question = 0
        self.hide_all_frames()
        self.quiz_frame.pack(expand=True, fill='both')
        self.next_question()

    def next_question(self):
        if self.current_question >= self.total_questions:
            self.show_results()
            return
        
        self.current_question += 1
        self.feedback_label.config(text="")
        self.answer_entry.delete(0, tk.END)
        
        self.score_label.config(text=f"Score: {self.score}")
        self.question_label.config(text=f"Question: {self.current_question}/{self.total_questions}")
        
        self.num1 = self.generate_number()
        self.num2 = self.generate_number()
        operation = random.choice(['+', '-'])
        
        if operation == '-' and self.num1 < self.num2:
            self.num1, self.num2 = self.num2, self.num1
        
        self.correct_answer = self.num1 + self.num2 if operation == '+' else self.num1 - self.num2
        self.problem_label.config(text=f"{self.num1} {operation} {self.num2} = ?")
        self.answer_entry.focus()

    def generate_number(self):
        if self.difficulty == "easy":
            return random.randint(1, 9)
        elif self.difficulty == "moderate":
            return random.randint(10, 99)
        else:
            return random.randint(1000, 9999)

    def check_answer(self):
        try:
            user_answer = int(self.answer_entry.get())
            
            if user_answer == self.correct_answer:
                self.score += 10
                self.feedback_label.config(text="Correct! +10 points", fg="green")
                self.root.after(1000, self.next_question)
            else:
                self.feedback_label.config(text=f"Wrong! Answer: {self.correct_answer}", fg="red")
                self.root.after(1500, self.next_question)
                
        except ValueError:
            self.feedback_label.config(text="Please enter a number", fg="orange")

    def show_results(self):
        self.hide_all_frames()
        self.results_frame.pack(expand=True, fill='both')
        
        percentage = (self.score / 100) * 100
        grade = self.calculate_grade(percentage)
        
        self.final_score_label.config(text=f"Final Score: {self.score}/100")
        self.grade_label.config(text=f"Grade: {grade}")

    def calculate_grade(self, percentage):
        if percentage >= 90: return "A+"
        elif percentage >= 80: return "A"
        elif percentage >= 70: return "B"
        elif percentage >= 60: return "C"
        elif percentage >= 50: return "D"
        else: return "F"

    def hide_all_frames(self):
        for frame in [self.welcome_frame, self.menu_frame, self.quiz_frame, self.results_frame]:
            frame.pack_forget()

    def restart_quiz(self):
        self.show_difficulty_menu()

def main():
    root = tk.Tk()
    app = ArithmeticQuiz(root)
    root.mainloop()

if __name__ == "__main__":
    main()
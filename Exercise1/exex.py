import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk
import os

class ArithmeticQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Arithmetic Quiz")
        # Set a fixed, more manageable window size and make it non-resizable
        self.WIDTH, self.HEIGHT = 900, 600
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.root.resizable(False, False)
        
        # Quiz variables
        self.difficulty = None
        self.score = 0
        self.current_question = 0
        self.total_questions = 10
        self.attempts = 0
        self.current_operation = None
        self.num1 = None
        self.num2 = None
        self.correct_answer = None
        
        # Colors
        self.bg_color = "#f0f8ff"  # Light blue background
        self.paper_color = "#ffffff"
        self.button_color = "#4CAF50"
        self.button_hover_color = "#45a049"
        self.accent_color = "#2196F3"
        self.text_color = "#2c3e50"
        
        self.root.configure(bg=self.bg_color)
        # Setup only the centered paper card
        self.create_paper_card()
        self.create_widgets()
        # Start with a welcome screen with an image and Start button
        self.show_welcome()

    def create_paper_card(self, width=600, height=450):
        """Create a centered paper-like card where all app frames live."""
        # Save sizes for layout use
        self.PAPER_WIDTH = width
        self.PAPER_HEIGHT = height
        # create a subtle shadow behind the paper
        self.paper_shadow = tk.Frame(self.root, bg='#b0bec5')
        self.paper_shadow.place(relx=0.5, rely=0.5, anchor='center', width=width+8, height=height+8)

        # draw the paper itself
        self.paper_frame = tk.Frame(self.root, bg=self.paper_color, bd=2, relief='ridge')
        self.paper_frame.place(relx=0.5, rely=0.5, anchor='center', width=width, height=height)

    def create_hover_button(self, parent, text, command, **kwargs):
        """Create a button with hover effect"""
        btn = tk.Button(parent, text=text, command=command, **kwargs)
        
        def on_enter(e):
            btn.configure(bg=self.button_hover_color)
        def on_leave(e):
            btn.configure(bg=self.button_color)
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    def show_welcome(self):
        """Display a welcome screen using `Exercise1WelcomePage.png` and a Start button."""
        # Hide other frames
        self.hide_all_frames()

        # Welcome frame
        self.welcome_frame = tk.Frame(self.root, bg=self.bg_color)
        self.welcome_frame.pack(expand=True, fill='both')

        # Try loading the image from this folder
        try:
            base_dir = os.path.dirname(__file__)
            image_path = os.path.join(base_dir, 'Exercise1WelcomePage.png')
            if not os.path.exists(image_path):
                # try repo root
                image_path = os.path.join(base_dir, '..', 'Exercise1WelcomePage.png')
            if os.path.exists(image_path):
                img = Image.open(image_path)
                # Resize to fill the window size for a perfect fit
                img = img.resize((self.WIDTH, self.HEIGHT), Image.LANCZOS)
                self.welcome_img = ImageTk.PhotoImage(img)
                bg_label = tk.Label(self.welcome_frame, image=self.welcome_img)
                bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            else:
                raise FileNotFoundError(image_path)
        except Exception:
            # If we can't load the image, show a simple title
            title_label = tk.Label(self.welcome_frame, text='Welcome to Arithmetic Quiz!', 
                                 font=('Comic Sans MS', 28, 'bold'), bg=self.bg_color, fg=self.accent_color)
            title_label.pack(pady=40)
            
            subtitle_label = tk.Label(self.welcome_frame, text='Test Your Math Skills!', 
                                    font=('Comic Sans MS', 18), bg=self.bg_color, fg=self.text_color)
            subtitle_label.pack(pady=10)

        # Place a Start button centered on the welcome screen
        start_btn = self.create_hover_button(
            self.welcome_frame, 
            'START QUIZ', 
            self.on_start_clicked,
            font=('Arial', 16, 'bold'), 
            bg=self.accent_color, 
            fg='white', 
            width=15,
            height=2,
            relief='raised',
            bd=3
        )
        start_btn.place(relx=0.5, rely=0.75, anchor='center')

    def on_start_clicked(self):
        # Remove welcome and show difficulty menu
        if hasattr(self, 'welcome_frame'):
            self.welcome_frame.pack_forget()
        self.show_difficulty_menu()
    
    def create_widgets(self):
        # Main frames live inside the paper frame
        self.menu_frame = tk.Frame(self.paper_frame, bg=self.paper_color)
        self.quiz_frame = tk.Frame(self.paper_frame, bg=self.paper_color)
        self.results_frame = tk.Frame(self.paper_frame, bg=self.paper_color)
        
        # Menu frame widgets
        self.menu_label = tk.Label(self.menu_frame, text="SELECT DIFFICULTY", 
                                  font=("Arial", 20, "bold"), bg=self.paper_color, fg=self.accent_color)
        
        # Difficulty buttons with larger fonts and better styling
        button_style = {
            'font': ("Arial", 16, "bold"),
            'width': 12,
            'height': 2,
            'relief': 'raised',
            'bd': 3
        }
        
        self.easy_btn = self.create_hover_button(self.menu_frame, text="🎯 EASY", 
                                               command=lambda: self.set_difficulty("easy"),
                                               bg="#4CAF50", fg="white", **button_style)
        
        self.moderate_btn = self.create_hover_button(self.menu_frame, text="🎲 MODERATE", 
                                                   command=lambda: self.set_difficulty("moderate"),
                                                   bg="#FF9800", fg="white", **button_style)
        
        self.advanced_btn = self.create_hover_button(self.menu_frame, text="🚀 ADVANCED", 
                                                   command=lambda: self.set_difficulty("advanced"),
                                                   bg="#F44336", fg="white", **button_style)
        
        # Quiz frame widgets
        self.quiz_header_frame = tk.Frame(self.quiz_frame, bg=self.paper_color)
        
        self.score_label = tk.Label(self.quiz_header_frame, text="Score: 0", 
                                   font=("Arial", 16, "bold"), bg=self.paper_color, fg=self.text_color)
        
        self.question_label = tk.Label(self.quiz_header_frame, text="Question: 1/10", 
                                      font=("Arial", 16, "bold"), bg=self.paper_color, fg=self.accent_color)
        
        self.problem_frame = tk.Frame(self.quiz_frame, bg=self.paper_color)
        self.problem_label = tk.Label(self.problem_frame, text="", 
                                     font=("Arial", 32, "bold"), bg=self.paper_color, fg=self.text_color)
        
        self.answer_frame = tk.Frame(self.quiz_frame, bg=self.paper_color)
        self.answer_entry = tk.Entry(self.answer_frame, font=("Arial", 20), width=8, justify='center',
                                   relief='solid', bd=2)
        
        self.submit_btn = self.create_hover_button(self.answer_frame, text="SUBMIT", 
                                                 command=self.check_answer, 
                                                 bg=self.button_color, fg="white",
                                                 font=("Arial", 14, "bold"), width=10, height=1)
        
        self.feedback_label = tk.Label(self.quiz_frame, text="", font=("Arial", 14),
                                      bg=self.paper_color, fg="red")
        
        # Results frame widgets
        self.results_label = tk.Label(self.results_frame, text="🎉 QUIZ COMPLETED!", 
                                     font=("Arial", 24, "bold"), bg=self.paper_color, fg=self.accent_color)
        
        self.final_score_label = tk.Label(self.results_frame, text="", font=("Arial", 20),
                                         bg=self.paper_color, fg=self.text_color)
        
        self.grade_label = tk.Label(self.results_frame, text="", font=("Arial", 22, "bold"),
                                   bg=self.paper_color, fg=self.accent_color)
        
        self.results_buttons_frame = tk.Frame(self.results_frame, bg=self.paper_color)
        
        self.play_again_btn = self.create_hover_button(self.results_buttons_frame, text="PLAY AGAIN", 
                                                     command=self.restart_quiz, 
                                                     bg=self.button_color, fg="white",
                                                     font=("Arial", 14, "bold"), width=12, height=1)
        
        self.quit_btn = self.create_hover_button(self.results_buttons_frame, text="QUIT", 
                                               command=self.root.quit, 
                                               bg="#f44336", fg="white",
                                               font=("Arial", 14, "bold"), width=12, height=1)
    
    def show_difficulty_menu(self):
        self.hide_all_frames()
        self.menu_frame.pack(expand=True, fill='both')
        
        self.menu_label.pack(pady=30)
        self.easy_btn.pack(pady=15)
        self.moderate_btn.pack(pady=15)
        self.advanced_btn.pack(pady=15)
    
    def hide_all_frames(self):
        self.menu_frame.pack_forget()
        self.quiz_frame.pack_forget()
        self.results_frame.pack_forget()
    
    def set_difficulty(self, level):
        self.difficulty = level
        self.start_quiz()
    
    def start_quiz(self):
        self.score = 0
        self.current_question = 0
        self.hide_all_frames()
        self.quiz_frame.pack(expand=True, fill='both')
        
        # Pack quiz widgets in organized layout
        self.quiz_header_frame.pack(pady=10)
        self.score_label.pack(side='left', padx=20)
        self.question_label.pack(side='right', padx=20)
        
        self.problem_frame.pack(expand=True, pady=30)
        self.problem_label.pack()
        
        self.answer_frame.pack(pady=20)
        self.answer_entry.pack(pady=10)
        self.submit_btn.pack(pady=10)
        
        self.feedback_label.pack(pady=10)
        
        self.next_question()
    
    def next_question(self):
        if self.current_question >= self.total_questions:
            self.show_results()
            return
        
        self.current_question += 1
        self.attempts = 0
        self.feedback_label.config(text="")
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus()
        
        # Update labels
        self.score_label.config(text=f"Score: {self.score}")
        self.question_label.config(text=f"Question: {self.current_question}/{self.total_questions}")
        
        # Generate new problem
        self.num1 = self.randomInt()
        self.num2 = self.randomInt()
        self.current_operation = self.decideOperation()
        
        # Ensure subtraction doesn't give negative results for better user experience
        if self.current_operation == '-' and self.num1 < self.num2:
            self.num1, self.num2 = self.num2, self.num1
        
        self.correct_answer = self.num1 + self.num2 if self.current_operation == '+' else self.num1 - self.num2
        
        self.displayProblem()
    
    def randomInt(self):
        """Generate random numbers based on difficulty level"""
        if self.difficulty == "easy":
            return random.randint(1, 9)
        elif self.difficulty == "moderate":
            return random.randint(10, 99)
        else:  # advanced
            return random.randint(1000, 9999)
    
    def decideOperation(self):
        """Randomly decide between addition and subtraction"""
        return random.choice(['+', '-'])
    
    def displayProblem(self):
        """Display the arithmetic problem"""
        problem_text = f"{self.num1} {self.current_operation} {self.num2} = ?"
        self.problem_label.config(text=problem_text)
    
    def check_answer(self):
        """Check if the user's answer is correct"""
        try:
            user_answer = int(self.answer_entry.get())
            self.attempts += 1
            
            if self.isCorrect(user_answer):
                if self.attempts == 1:
                    self.score += 10
                    self.feedback_label.config(text="✅ Correct! +10 points", fg="green")
                else:
                    self.score += 5
                    self.feedback_label.config(text="✅ Correct! +5 points", fg="green")
                
                self.root.after(1000, self.next_question)  # Wait 1 second before next question
            else:
                if self.attempts == 1:
                    self.feedback_label.config(text="❌ Incorrect! Try again.", fg="red")
                    self.answer_entry.delete(0, tk.END)
                else:
                    self.feedback_label.config(text=f"❌ Wrong! Correct answer: {self.correct_answer}", fg="red")
                    self.root.after(1500, self.next_question)  # Wait 1.5 seconds before next question
        except ValueError:
            self.feedback_label.config(text="⚠️ Please enter a valid number!", fg="orange")
    
    def isCorrect(self, user_answer):
        """Check if the user's answer matches the correct answer"""
        return user_answer == self.correct_answer
    
    def show_results(self):
        """Display final results and grade"""
        self.hide_all_frames()
        self.results_frame.pack(expand=True, fill='both')
        
        percentage = (self.score / 100) * 100
        grade = self.calculate_grade(percentage)
        
        self.final_score_label.config(text=f"Final Score: {self.score}/100")
        self.grade_label.config(text=f"Grade: {grade}")
        
        self.results_label.pack(pady=30)
        self.final_score_label.pack(pady=15)
        self.grade_label.pack(pady=15)
        
        self.results_buttons_frame.pack(pady=30)
        self.play_again_btn.pack(side='left', padx=10)
        self.quit_btn.pack(side='right', padx=10)
    
    def calculate_grade(self, percentage):
        """Calculate grade based on percentage"""
        if percentage >= 90:
            return "A+ 🎊"
        elif percentage >= 80:
            return "A 🎉"
        elif percentage >= 70:
            return "B 👍"
        elif percentage >= 60:
            return "C 👌"
        elif percentage >= 50:
            return "D 🤔"
        else:
            return "F 😞"
    
    def restart_quiz(self):
        """Restart the quiz by showing difficulty menu again"""
        self.show_difficulty_menu()

def main():
    root = tk.Tk()
    app = ArithmeticQuiz(root)
    root.mainloop()

if __name__ == "__main__":
    main()
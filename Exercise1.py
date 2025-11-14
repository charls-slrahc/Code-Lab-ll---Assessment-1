import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk
import os

class MathQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Quiz")
        self.difficulty = None
        self.score = 0
        self.question_num = 0
        self.attempt = 1
        self.current_problem = None
        self.bg_image = None
        self.content_frame = None

        # Setup background image (looks for 'mathquiz-bg.jpg' next to this file)
        self.setup_background()

        # Show welcome screen first; user clicks Start to choose difficulty
        self.displayWelcome()

    def setup_background(self):
        WIDTH, HEIGHT = 700, 500
        try:
            image_path = os.path.join(os.path.dirname(__file__), 'Exe1bg.jpg')
            self.root.geometry(f"{WIDTH}x{HEIGHT}")
            if os.path.exists(image_path):
                img = Image.open(image_path)
                img = img.resize((WIDTH, HEIGHT), Image.LANCZOS)
                self.bg_image = ImageTk.PhotoImage(img)
                bg_label = tk.Label(self.root, image=self.bg_image)
                bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            # else: window is already set to default size
        except Exception as e:
            print('Could not load background image:', e)
            self.root.geometry(f'{WIDTH}x{HEIGHT}')

    def _ensure_content_frame(self, width=420, height=320):
        """Create (if needed) and clear a centered white content frame."""
        if self.content_frame is None:
            self.content_frame = tk.Frame(self.root, bg='white', bd=2, relief='ridge')
            # place centered on the root window
            self.content_frame.place(relx=0.5, rely=0.5, anchor='center', width=width, height=height)
        else:
            for w in self.content_frame.winfo_children():
                w.destroy()

    def displayWelcome(self):
        # Use the centered content frame for welcome content
        self._ensure_content_frame()
        tk.Label(self.content_frame, text="Welcome to Math Quiz", font=("Comic Sans MS", 28, "bold"), bg='white').pack(pady=(0,10))
        tk.Label(self.content_frame, text="Test your skills with 10 fun questions.", font=("Comic Sans MS", 14), bg='white').pack(pady=(0,20))
        tk.Button(self.content_frame, text="Start", font=("Comic Sans MS", 16, "bold"), width=14, command=self.displayMenu).pack()

    def displayMenu(self):
        # Use centered content frame and populate difficulty choices
        self._ensure_content_frame()
        tk.Label(self.content_frame, text="DIFFICULTY LEVEL", font=("Comic Sans MS", 22, "bold"), bg='white').pack(pady=10)
        tk.Button(self.content_frame, text="1. Easy", command=lambda: self.setDifficulty('easy'), width=22, font=("Comic Sans MS", 14, "bold")).pack(pady=6)
        tk.Button(self.content_frame, text="2. Moderate", command=lambda: self.setDifficulty('moderate'), width=22, font=("Comic Sans MS", 14, "bold")).pack(pady=6)
        tk.Button(self.content_frame, text="3. Advanced", command=lambda: self.setDifficulty('advanced'), width=22, font=("Comic Sans MS", 14, "bold")).pack(pady=6)

    def setDifficulty(self, diff):
        self.difficulty = diff
        self.startQuiz()

    def startQuiz(self):
        self.score = 0
        self.question_num = 0
        self.nextQuestion()

    def nextQuestion(self):
        if self.question_num >= 10:
            self.displayResults()
            return
        self.question_num += 1
        self.attempt = 1
        num1, num2 = self.randomInt(self.difficulty)
        op = self.decideOperation()
        self.current_problem = (num1, op, num2)
        self.displayProblem()

    def randomInt(self, difficulty):
        if difficulty == 'easy':
            min_val = 0
            max_val = 9
        elif difficulty == 'moderate':
            min_val = 10
            max_val = 99
        elif difficulty == 'advanced':
            min_val = 1000
            max_val = 9999
        return random.randint(min_val, max_val), random.randint(min_val, max_val)

    def decideOperation(self):
        return random.choice(['+', '-'])

    def displayProblem(self):
        # Use centered content frame for the question
        self._ensure_content_frame()
        num1, op, num2 = self.current_problem
        tk.Label(self.content_frame, text=f"Question {self.question_num}: {num1} {op} {num2} =", font=("Comic Sans MS", 20, "bold"), bg='white').pack(pady=10)
        self.answer_entry = tk.Entry(self.content_frame, font=("Comic Sans MS", 18), justify='center')
        self.answer_entry.pack(pady=8)
        tk.Button(self.content_frame, text="Submit", command=self.isCorrect, width=14, font=("Comic Sans MS", 14, "bold")).pack(pady=10)

    def isCorrect(self):
        try:
            user_answer = int(self.answer_entry.get())
            num1, op, num2 = self.current_problem
            if op == '+':
                correct = num1 + num2
            else:
                correct = num1 - num2
            if user_answer == correct:
                if self.attempt == 1:
                    self.score += 10
                else:
                    self.score += 5
                messagebox.showinfo("Correct!", "Well done!")
                self.nextQuestion()
            else:
                if self.attempt == 1:
                    self.attempt = 2
                    messagebox.showerror("Wrong", "Try again!")
                    self.displayProblem()  # Redisplay the problem
                else:
                    messagebox.showerror("Wrong", f"Sorry, the correct answer is {correct}")
                    self.nextQuestion()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number")

    def displayResults(self):
        # Use centered content frame for results
        self._ensure_content_frame()
        rank = self.getRank()
        tk.Label(self.content_frame, text=f"Your score: {self.score}/100", font=("Comic Sans MS", 20, "bold"), bg='white').pack(pady=10)
        tk.Label(self.content_frame, text=f"Rank: {rank}", font=("Comic Sans MS", 20, "bold"), bg='white').pack(pady=10)
        tk.Button(self.content_frame, text="Play Again", command=self.displayMenu, width=14, font=("Comic Sans MS", 14, "bold")).pack(pady=6)
        tk.Button(self.content_frame, text="Quit", command=self.root.quit, width=14, font=("Comic Sans MS", 14, "bold")).pack(pady=6)

    def getRank(self):
        if self.score > 90:
            return "A+"
        elif self.score > 80:
            return "A"
        elif self.score > 70:
            return "B"
        elif self.score > 60:
            return "C"
        else:
            return "D"

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = MathQuiz(root)
    root.mainloop()
import tkinter as tk
from tkinter import messagebox
import random

class JokeTellingAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa - Joke Teller")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        
        # Load jokes from file
        self.jokes = self.load_jokes()
        self.current_joke = None
        self.current_setup = ""
        self.current_punchline = ""
        
        # Colors and styling
        self.bg_color = "#232f3e"  # Alexa blue-ish dark
        self.button_color = "#ff9900"  # Amazon orange
        self.text_color = "white"
        self.setup_color = "#00a8e1"  # Light blue for setup
        self.punchline_color = "#ff9900"  # Orange for punchline
        
        self.root.configure(bg=self.bg_color)
        
        # Create and place widgets
        self.create_widgets()
        
    def load_jokes(self):
        """Load jokes from the randomJokes.txt file"""
        try:
            with open('randomJokes.txt', 'r', encoding='utf-8') as file:
                jokes = [line.strip() for line in file if line.strip()]
            return jokes
        except FileNotFoundError:
            # Fallback jokes if file not found
            return [
                "Why did the chicken cross the road?To get to the other side.",
                "What happens if you boil a clown?You get a laughing stock.",
                "Why don't scientists trust atoms?Because they make up everything.",
                "What do you call a fake noodle?An impasta.",
                "Why did the scarecrow win an award?Because he was outstanding in his field.",
                "What do you call a bear with no teeth?A gummy bear.",
                "Why don't eggs tell jokes?They'd crack each other up.",
                "What do you call a sleeping bull?A bulldozer.",
                "Why did the math book look so sad?Because it had too many problems.",
                "What do you call a fish wearing a crown?A king fish."
            ]
    
    def create_widgets(self):
        """Create and arrange all GUI widgets"""
        # Main title
        self.title_label = tk.Label(
            self.root, 
            text="Alexa Joke Teller", 
            font=("Arial", 24, "bold"),  # Increased font size
            bg=self.bg_color, 
            fg=self.text_color
        )
        self.title_label.pack(pady=20)
        
        # Subtitle
        self.subtitle_label = tk.Label(
            self.root,
            text="Your personal joke-telling assistant",
            font=("Arial", 14),  # Increased font size
            bg=self.bg_color,
            fg=self.text_color
        )
        self.subtitle_label.pack(pady=5)
        
        # Joke display frame
        self.joke_frame = tk.Frame(self.root, bg=self.bg_color)
        self.joke_frame.pack(pady=30, padx=20, fill='both', expand=True)
        
        # Setup label
        self.setup_label = tk.Label(
            self.joke_frame,
            text="Click 'Tell me a Joke' to hear a joke!",
            font=("Arial", 16, "bold"),  # Increased font size
            bg=self.bg_color,
            fg=self.setup_color,
            wraplength=500,
            justify='center'
        )
        self.setup_label.pack(pady=10)
        
        # Punchline label
        self.punchline_label = tk.Label(
            self.joke_frame,
            text="",
            font=("Arial", 14, "italic"),  # Increased font size
            bg=self.bg_color,
            fg=self.punchline_color,
            wraplength=500,
            justify='center'
        )
        self.punchline_label.pack(pady=10)
        
        # Button frame
        self.button_frame = tk.Frame(self.root, bg=self.bg_color)
        self.button_frame.pack(pady=20)
        
        # Button style - all buttons same size
        button_style = {
            'font': ("Arial", 13, "bold"),  # Increased font size
            'width': 16,  # Same width for all buttons
            'height': 2,   # Same height for all buttons
            'bd': 2,
            'relief': 'raised'
        }
        
        # Tell Joke button
        self.tell_joke_btn = tk.Button(
            self.button_frame,
            text="Alexa tell me a Joke",
            command=self.tell_joke,
            bg=self.button_color,
            fg="white",
            **button_style
        )
        self.tell_joke_btn.grid(row=0, column=0, padx=8, pady=8)
        
        # Show Punchline button
        self.punchline_btn = tk.Button(
            self.button_frame,
            text="Show Punchline",
            command=self.show_punchline,
            bg="#32a852",
            fg="white",
            state='disabled',
            **button_style
        )
        self.punchline_btn.grid(row=0, column=1, padx=8, pady=8)
        
        # Next Joke button
        self.next_joke_btn = tk.Button(
            self.button_frame,
            text="Next Joke",
            command=self.next_joke,
            bg="#007bff",
            fg="white",
            state='disabled',
            **button_style
        )
        self.next_joke_btn.grid(row=1, column=0, padx=8, pady=8)
        
        # Quit button
        self.quit_btn = tk.Button(
            self.button_frame,
            text="Quit",
            command=self.quit_app,
            bg="#dc3545",
            fg="white",
            **button_style
        )
        self.quit_btn.grid(row=1, column=1, padx=8, pady=8)
        
        # Status label
        self.status_label = tk.Label(
            self.root,
            text=f"Loaded {len(self.jokes)} jokes",
            font=("Arial", 12),  # Increased font size
            bg=self.bg_color,
            fg=self.text_color
        )
        self.status_label.pack(pady=10)
    
    def tell_joke(self):
        """Tell a random joke - show only the setup"""
        if not self.jokes:
            messagebox.showerror("Error", "No jokes available!")
            return
        
        # Select random joke
        self.current_joke = random.choice(self.jokes)
        
        # Split joke into setup and punchline
        if '?' in self.current_joke:
            parts = self.current_joke.split('?', 1)
            self.current_setup = parts[0] + "?"
            self.current_punchline = parts[1] if len(parts) > 1 else ""
        else:
            # Fallback if no question mark found
            self.current_setup = self.current_joke
            self.current_punchline = "(Punchline not available)"
        
        # Update display
        self.setup_label.config(text=self.current_setup)
        self.punchline_label.config(text="")
        
        # Enable/disable buttons
        self.punchline_btn.config(state='normal')
        self.next_joke_btn.config(state='normal')
        self.tell_joke_btn.config(state='disabled')
        
        # Update status
        self.status_label.config(text="Joke ready! Click 'Show Punchline' for the funny part!")
    
    def show_punchline(self):
        """Display the punchline of the current joke"""
        if self.current_punchline:
            self.punchline_label.config(text=self.current_punchline)
            self.punchline_btn.config(state='disabled')
            self.status_label.config(text="Hope that made you smile! Try another joke?")
        else:
            messagebox.showinfo("Info", "No punchline available for this joke.")
    
    def next_joke(self):
        """Get the next random joke"""
        # Reset display
        self.setup_label.config(text="Getting another joke...")
        self.punchline_label.config(text="")
        
        # Enable tell joke button and disable others
        self.tell_joke_btn.config(state='normal')
        self.punchline_btn.config(state='disabled')
        self.next_joke_btn.config(state='disabled')
        
        # Update status
        self.status_label.config(text="Ready for another joke!")
        
        # After a brief delay, show the prompt
        self.root.after(500, lambda: self.setup_label.config(text="Click 'Alexa tell me a Joke' for another joke!"))
    
    def quit_app(self):
        """Quit the application with confirmation"""
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.root.quit()

def main():
    root = tk.Tk()
    app = JokeTellingAssistant(root)
    root.mainloop()

if __name__ == "__main__":
    main()
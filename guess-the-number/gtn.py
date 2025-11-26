import tkinter as tk
from tkinter import ttk
import random
window = tk.Tk()
window.title("Guess the number")
window.geometry("450x800")
window.config(bg="#2C3E50")
window.minsize(500,500)
window.resizable(True, True)

# Create a Notebook (tab container)
notebook = ttk.Notebook(window)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# Create two frames - one for each tab
settings_tab = tk.Frame(notebook, bg="#2C3E50")
game_tab = tk.Frame(notebook, bg="#2C3E50")

# Add frames as tabs
notebook.add(settings_tab, text="⚙️ Settings")
notebook.add(game_tab, text="🎮 Game")

# Initialize game variables
secret_number = 0
current_input = ""
attempts = 0
max_attempts = 10  # Default max attempts
min_range = 1  # Default minimum number
max_range = 100  # Default maximum number
game_over = False
game_started = False  # Track if game has started

# Settings Frame - for configuring the game
settings_frame = tk.Frame(settings_tab, bg="#2C3E50")
settings_frame.pack(pady=20, padx=20, fill=tk.X)

# Title for settings
settings_title = tk.Label(settings_frame, text="Game Settings", 
                         font=("Arial", 14, "bold"), bg="#2C3E50", fg="white")
settings_title.pack()

# Range settings (min and max)
range_frame = tk.Frame(settings_frame, bg="#2C3E50")
range_frame.pack(pady=10)

min_label = tk.Label(range_frame, text="Min:", font=("Arial", 11),
                    bg="#2C3E50", fg="white")
min_label.pack(side=tk.LEFT, padx=5)

min_entry = tk.Entry(range_frame, width=5, font=("Arial", 11))
min_entry.insert(0, "1")  # Default value
min_entry.pack(side=tk.LEFT, padx=5)

max_label = tk.Label(range_frame, text="Max:", font=("Arial", 11),
                    bg="#2C3E50", fg="white")
max_label.pack(side=tk.LEFT, padx=5)

max_entry = tk.Entry(range_frame, width=5, font=("Arial", 11))
max_entry.insert(0, "100")  # Default value
max_entry.pack(side=tk.LEFT, padx=5)

# Max attempts setting
attempts_frame = tk.Frame(settings_frame, bg="#2C3E50")
attempts_frame.pack(pady=5)

attempts_setting_label = tk.Label(attempts_frame, text="Max Attempts:", 
                                 font=("Arial", 11), bg="#2C3E50", fg="white")
attempts_setting_label.pack(side=tk.LEFT, padx=5)

attempts_entry = tk.Entry(attempts_frame, width=5, font=("Arial", 11))
attempts_entry.insert(0, "10")  # Default value
attempts_entry.pack(side=tk.LEFT, padx=5)

# Feedback label for settings errors
settings_feedback = tk.Label(settings_tab, text="", font=("Arial", 11),
                            bg="#2C3E50", fg="orange")
settings_feedback.pack(pady=10)

# Function to start the game with settings
def start_game():
    global secret_number, min_range, max_range, max_attempts, attempts, game_started, game_over
    
    try:
        # Get values from entries and convert to integers
        min_range = int(min_entry.get())
        max_range = int(max_entry.get())
        max_attempts = int(attempts_entry.get())
        
        # Validate the settings
        if min_range >= max_range:
            settings_feedback.config(text="Min must be less than Max!", fg="orange")
            return
        
        if max_attempts < 1:
            settings_feedback.config(text="Max attempts must be at least 1!", fg="orange")
            return
        
        # Generate secret number within the range
        secret_number = random.randint(min_range, max_range)

        # Reset game variables
        attempts = 0
        game_over = False
        game_started = True
        
        # Update labels
        result_label.config(text=f"Guess a number between {min_range}-{max_range}", fg="white")
        attempts_label.config(text=f"Attempts: 0/{max_attempts}")

        # Clear any previous feedback
        settings_feedback.config(text="")
        
        # Disable settings (can't change mid-game)
        min_entry.config(state=tk.DISABLED)
        max_entry.config(state=tk.DISABLED)
        attempts_entry.config(state=tk.DISABLED)
        start_button.config(state=tk.DISABLED, bg="#95A5A6")
        
        # Switch to game tab!
        # notebook.select(1) switches to tab at index 1 (Game tab)
        notebook.select(1)

    except ValueError:
        # If entries contain non-numbers
        settings_feedback.config(text="Please enter valid numbers!", fg="orange")

# Start Game button
start_button = tk.Button(settings_frame, text="Start Game", 
                        command=start_game,
                        font=("Arial", 12, "bold"),
                        bg="#9B59B6",
                        fg="white",
                        width=12,
                        activebackground="#8E44AD")
start_button.pack(pady=10)

# Display label
display_label = tk.Label(game_tab, text="", font=("Arial", 24, "bold"),
                        bg="#34495E", fg="white", height=2)
display_label.pack(pady=20, padx=20, fill=tk.X)

# Result label
result_label = tk.Label(game_tab, text="Configure settings and click Start Game", 
                       font=("Arial", 12), bg="#2C3E50", fg="white")
result_label.pack(pady=10)

# Attempts label
attempts_label = tk.Label(game_tab, text="Attempts: 0/10", 
                         font=("Arial", 11), bg="#2C3E50", fg="#BDC3C7")
attempts_label.pack(pady=5)

def button_click(number):
    global current_input

    # Don't allow input if game hasn't started or is over
    if not game_started or game_over:
        return
    
    # Limit input length based on max_range digits
    max_digits = len(str(max_range))
    if len(current_input) >= max_digits:
        return
    
    current_input += str(number)
    display_label.config(text=current_input)

# Function to clear the current input
def clear_input():
    global current_input
    current_input = ""  # Reset to empty string
    display_label.config(text="")  # Clear the display
    #result_label.config(text="Guess a number between 1-100")  # Reset result message

# Function to check the guess when Enter is pressed
def check_guess():
    global current_input, attempts, game_over

    # Don't allow checking if game hasn't started or is over
    if not game_started or game_over:
        return
    
    # Check if user actually entered something
    if current_input == "":
        result_label.config(text="Please enter a number!", fg="orange")
        return
    
    # Convert the input string to an integer
    guess = int(current_input)
    
    # Validate guess is in range
    if guess < min_range or guess > max_range:
        result_label.config(text=f"Please enter a number between {min_range}-{max_range}!", fg="orange")
        current_input = ""
        display_label.config(text="")
        return
    
    # Increment attempts
    attempts += 1
    attempts_label.config(text=f"Attempts: {attempts}/{max_attempts}")
    
    # Check if guess is too low, too high, or correct
    if guess < secret_number:
        result_label.config(text=f"{guess} is too low! Try again.", fg="#E74C3C")
    elif guess > secret_number:
        result_label.config(text=f"{guess} is too high! Try again.", fg="#E74C3C")
    else:
       # Correct guess!
        game_over = True
        result_label.config(text=f"🎉 Correct! You guessed it in {attempts} attempts!", fg="#2ECC71")
        play_again_button.pack(pady=10)

    # Check if out of attempts
    if attempts >= max_attempts and not game_over:
        game_over = True
        result_label.config(text=f"😞 Game Over! The number was {secret_number}", fg="#E74C3C")
        play_again_button.pack(pady=10)
    
    # Clear the input for next guess
    current_input = ""
    display_label.config(text="")

def reset_game():
    global secret_number, current_input, attempts, game_over, game_started
    
    # Reset variables
    current_input = ""
    attempts = 0
    game_over = False
    game_started = False
    
    # Reset labels
    display_label.config(text="")
    result_label.config(text="Configure settings and click Start Game", fg="white")
    attempts_label.config(text="Attempts: 0/10")
    
    # Re-enable settings
    min_entry.config(state=tk.NORMAL)
    max_entry.config(state=tk.NORMAL)
    attempts_entry.config(state=tk.NORMAL)
    start_button.config(state=tk.NORMAL, bg="#9B59B6")

    # Hide play again button
    play_again_button.pack_forget()

    # Switch back to settings tab
    notebook.select(0)
    
number_frame= tk.Frame(game_tab,bg="#1681ED")
number_frame.pack(pady=20)

button_style ={
    "font": ("Arial", 18, "bold"),
    "bg": "#3498DB",
    "fg": "white",
    "width": 5,
    "height": 2,
    "activebackground": "#2980B9"
}

for i in range(9):
    row = i // 3
    col = i % 3
    number = i + 1

    btn = tk.Button(number_frame, text=str(number), command=lambda n=number: button_click(n),**button_style)

    btn.grid(row=row, column=col, padx=5, pady= 5)

btn_0 = tk.Button(number_frame,text="0", command=lambda: button_click(0),**button_style)
btn_0.grid(row=3, column=1, padx=5, pady=5)

# Clear button (bottom left)
btn_clear = tk.Button(number_frame, text="C", 
                     command=clear_input,
                     font=("Arial", 18, "bold"),
                     bg="#E74C3C",  # Red color
                     fg="white",
                     width=5,
                     height=2,
                     activebackground="#C0392B")
btn_clear.grid(row=3, column=0, padx=5, pady=5)

# Enter button (bottom right)
btn_enter = tk.Button(number_frame, text="↵", 
                     command=check_guess,
                     font=("Arial", 18, "bold"),
                     bg="#2ECC71",  # Green color
                     fg="white",
                     width=5,
                     height=2,
                     activebackground="#27AE60")
btn_enter.grid(row=3, column=2, padx=5, pady=5)

# Play Again button (hidden initially)
play_again_button = tk.Button(game_tab, text="Play Again", 
                             command=reset_game,
                             font=("Arial", 14, "bold"),
                             bg="#F39C12",
                             fg="white",
                             width=15,
                             height=1,
                             activebackground="#E67E22")




window.mainloop()

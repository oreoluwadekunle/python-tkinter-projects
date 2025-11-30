import tkinter as tk
from tkinter import ttk
import random
import time
import pygame
import json
import os

pygame.init()
# Sound setup
sound_name=r"C:\Users\USER\Desktop\MyProjects\python-tkinter-projects\guess-the-number\stand_up.mp3"
BGM2 = r"C:\Users\USER\Desktop\MyProjects\python-tkinter-projects\guess-the-number\BGM2.mp3"
BGM1 = r"C:\Users\USER\Desktop\MyProjects\python-tkinter-projects\guess-the-number\BGM1.mp3"

# Define your playlist and current song index
PLAYLIST = [BGM1, BGM2]
current_track_index = 0

# Define a custom event ID
# This event will be triggered by Pygame when a track finishes.
MUSIC_END_EVENT = pygame.USEREVENT + 1

# Initialize pygame mixer for sound
pygame.mixer.init()
pygame.mixer.music.set_endevent(MUSIC_END_EVENT)


try:
    # Load the music file (must be done with mixer.music.load)
    pygame.mixer.music.load(PLAYLIST[current_track_index])
    
    # Play the music. The -1 means it will loop indefinitely.
    # The 0.0 means start playing immediately.
    pygame.mixer.music.play(0) 
    
    # Optional: Set volume (0.0 to 1.0)
    pygame.mixer.music.set_volume(0.5) 
    
    print(f"✓ Background music started.")

except pygame.error as e:
    print(f"⚠ Could not load background music: {e}")
    
# Load the sound file (change filename if yours is different)
try:
    win_sound = pygame.mixer.Sound(sound_name)  # Change to your filename
    sound_loaded = True
except:
    sound_loaded = False
    print("Sound file not found - game will work without sound")


window = tk.Tk()
window.title("Guess the number")
window.geometry("450x800")
window.config(bg="#2C3E50")
window.minsize(500,500)
window.resizable(True, True)


# Create a Notebook (tab container)
notebook = ttk.Notebook(window)
notebook.pack(fill="both", expand=True, padx=10, pady=5)

# Create two frames - one for each tab
settings_tab = tk.Frame(notebook, bg="#2C3E50")
game_tab = tk.Frame(notebook, bg="#2C3E50")
leaderboard_tab = tk.Frame(notebook, bg="#2C3E50")

# Add frames as tabs
notebook.add(settings_tab, text="⚙️ Settings")
notebook.add(game_tab, text="🎮 Game")
notebook.add(leaderboard_tab, text="🏆 Leaderboard")

# Initialize game variables
secret_number = 0
current_input = ""
attempts = 0
max_attempts = 10  # Default max attempts
min_range = 1  # Default minimum number
max_range = 100  # Default maximum number
game_over = False
game_started = False  # Track if game has started
hints_used = 0 # Track number of hints used
guess_history=[]
guessed_after_hint = True  # Track if player guessed after last hint
start_time = 0  # Track when game started
score = 0  # Player's score
Global_elapsed_time = 0

# Separate leaderboards for each difficulty
leaderboards = {
    "Easy": [],
    "Medium": [],
    "Hard": [],
    "Custom": []
}

# File to save leaderboard
LEADERBOARD_FILE = "leaderboard.json"

#
def play_next_track():
    global current_track_index
    
    # Calculate the index of the next song, wrapping around the playlist
    current_track_index = (current_track_index + 1) % len(PLAYLIST)
    
    # Get the file name
    next_track = PLAYLIST[current_track_index]
    
    try:
        # Load the next track
        pygame.mixer.music.load(next_track)
        
        # Start playing (0 means play once)
        pygame.mixer.music.play(0) 
        
        print(f"Now playing: {next_track}")
    except pygame.error as e:
        print(f"Error loading {next_track}: {e}")

def check_pygame_events(window):
    # Process all events in the Pygame queue
    for event in pygame.event.get():
        
        # Check if the event is the one we defined (song ended)
        if event.type == MUSIC_END_EVENT:
            play_next_track()
            
    # Schedule this function to run again after a small delay (e.g., 100ms)
    window.after(100, check_pygame_events, window)

window.after(100, check_pygame_events, window)
    
# Load leaderboards from file
def load_leaderboards():
    global leaderboards
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, 'r') as f:
                leaderboards = json.load(f)
            # Ensure all difficulty keys exist
            for difficulty in ["Easy", "Medium", "Hard", "Custom"]:
                if difficulty not in leaderboards:
                    leaderboards[difficulty] = []
            print(f"✓ Loaded leaderboards")
        except:
            leaderboards = {"Easy": [], "Medium": [], "Hard": [], "Custom": []}
            print("⚠ Could not load leaderboards, starting fresh")
    else:
        leaderboards = {"Easy": [], "Medium": [], "Hard": [], "Custom": []}
        print("ℹ No leaderboard file found, starting fresh")
        save_leaderboards()

# Save leaderboard to file
def save_leaderboards():
    try:
        # Write leaderboard to JSON file
        with open(LEADERBOARD_FILE, 'w') as f:
            json.dump(leaderboards, f, indent=2)
        print("✓ Leaderboards saved")
    except:
        print("⚠ Could not save leaderboards")

# Add score to appropriate leaderboard
def add_to_leaderboard(player_name, score, time_taken, difficulty):
    entry = {
        "name": player_name,
        "score": score,
        "time": time_taken
    }
    
    # Add to the appropriate difficulty leaderboard
    leaderboards[difficulty].append(entry)
    
    # Sort by score (highest first)
    leaderboards[difficulty].sort(key=lambda x: x["score"], reverse=True)
    
    # Keep only top 10 for this difficulty
    leaderboards[difficulty] = leaderboards[difficulty][:9]
    
    save_leaderboards()
    update_leaderboard_display()

# Update leaderboard display based on selected difficulty
def update_leaderboard_display():
    # Get selected difficulty from dropdown
    selected_difficulty = difficulty_var.get()
    
    # Clear existing content
    for widget in leaderboard_content_frame.winfo_children():
        widget.destroy()
    
    # Get leaderboard for selected difficulty
    current_leaderboard = leaderboards[selected_difficulty]
    
    if not current_leaderboard:
        no_scores = tk.Label(leaderboard_content_frame, 
                            text=f"No {selected_difficulty} scores yet!\nBe the first to set a record!",
                            font=("Arial", 14), bg="#2C3E50", fg="#7F8C8D",
                            justify=tk.CENTER)
        no_scores.pack(pady=50)
    else:
        for i, entry in enumerate(current_leaderboard, 1):
            entry_frame = tk.Frame(leaderboard_content_frame, bg="#34495E", 
                                  relief=tk.RAISED, bd=2)
            entry_frame.pack(pady=2, padx=10, fill=tk.X)

            # Rank with medals
            if i == 1:
                rank = "🥇"
            elif i == 2:
                rank = "🥈"
            elif i == 3:
                rank = "🥉"
            else:
                rank = f"{i}."
            
            rank_label = tk.Label(entry_frame, text=rank, font=("Arial", 16, "bold"),
                                 bg="#34495E", fg="white", width=3)
            rank_label.pack(side=tk.LEFT, padx=5)
            
            info_frame = tk.Frame(entry_frame, bg="#34495E")
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=3)
            
            name_label = tk.Label(info_frame, text=entry["name"], 
                                 font=("Arial", 12, "bold"),
                                 bg="#34495E", fg="white", anchor="w")
            name_label.pack(anchor="w")

            details = f"Score: {entry['score']} | Time: {entry['time']}s"
            details_label = tk.Label(info_frame, text=details,
                                   font=("Arial", 9), bg="#34495E", fg="#BDC3C7",
                                   anchor="w")
            details_label.pack(anchor="w")

load_leaderboards()

# Title for settings
settings_title = tk.Label(settings_tab, text="Game Settings", 
                         font=("Arial", 14, "bold"), bg="#2C3E50", fg="white")
settings_title.pack()

# Difficulty Presets Frame
difficulty_frame = tk.Frame(settings_tab, bg="#2C3E50")
difficulty_frame.pack(pady=15)

difficulty_title = tk.Label(difficulty_frame, text="Quick Presets:", 
                           font=("Arial", 12, "bold"), bg="#2C3E50", fg="white")
difficulty_title.pack(pady=5)

# ==================== LEADERBOARD TAB ====================

leaderboard_header = tk.Frame(leaderboard_tab, bg="#2C3E50")
leaderboard_header.pack(pady=20, fill=tk.X)

leaderboard_title = tk.Label(leaderboard_header, text="🏆 High Scores", 
                            font=("Arial", 20, "bold"), bg="#2C3E50", fg="#F39C12")
leaderboard_title.pack()

# Difficulty selector frame
selector_frame = tk.Frame(leaderboard_header, bg="#2C3E50")
selector_frame.pack(pady=10)

difficulty_label = tk.Label(selector_frame, text="Difficulty:", 
                           font=("Arial", 12), bg="#2C3E50", fg="white")
difficulty_label.pack(side=tk.LEFT, padx=5)

# Dropdown for difficulty selection
difficulty_var = tk.StringVar(value="Medium")  # Default to Medium

# Create styled dropdown
difficulty_dropdown = ttk.Combobox(selector_frame, textvariable=difficulty_var,
                                  values=["Easy", "Medium", "Hard", "Custom"],
                                  state="readonly", width=12, font=("Arial", 11))
difficulty_dropdown.pack(side=tk.LEFT, padx=5)

# Update display when dropdown changes
difficulty_dropdown.bind("<<ComboboxSelected>>", lambda e: update_leaderboard_display())

# Scrollable frame for leaderboard entries
leaderboard_canvas = tk.Canvas(leaderboard_tab, bg="#2C3E50", highlightthickness=0)
leaderboard_scrollbar = tk.Scrollbar(leaderboard_tab, orient="vertical", 
                                    command=leaderboard_canvas.yview)
leaderboard_content_frame = tk.Frame(leaderboard_canvas, bg="#2C3E50")

leaderboard_content_frame.bind(
    "<Configure>",
    lambda e: leaderboard_canvas.configure(scrollregion=leaderboard_canvas.bbox("all"))
)

leaderboard_canvas.create_window((0, 0), window=leaderboard_content_frame, anchor="nw")
leaderboard_canvas.configure(yscrollcommand=leaderboard_scrollbar.set)

leaderboard_canvas.pack(side="left", fill="both", expand=True, padx=10)
leaderboard_scrollbar.pack(side="right", fill="y")

# Clear leaderboard button (clears selected difficulty only)
def clear_leaderboard():
    selected_difficulty = difficulty_var.get()
    
    confirm_window = tk.Toplevel(window)
    confirm_window.title("Confirm")
    confirm_window.geometry("300x120")
    confirm_window.config(bg="#E74C3C")
    confirm_window.grab_set()
    
    confirm_label = tk.Label(confirm_window, 
                            text=f"Clear all {selected_difficulty} scores?\nThis cannot be undone!",
                            font=("Arial", 11, "bold"), bg="#E74C3C", fg="white",
                            justify=tk.CENTER)
    confirm_label.pack(pady=15)

    def do_clear():
        leaderboards[selected_difficulty] = []
        save_leaderboards()
        update_leaderboard_display()
        confirm_window.destroy()
    
    button_frame = tk.Frame(confirm_window, bg="#E74C3C")
    button_frame.pack(pady=10)
    
    yes_btn = tk.Button(button_frame, text="Yes, Clear", command=do_clear,
                       font=("Arial", 10, "bold"), bg="#C0392B", fg="white",
                       width=10)
    yes_btn.pack(side=tk.LEFT, padx=5)
    
    no_btn = tk.Button(button_frame, text="Cancel", command=confirm_window.destroy,
                      font=("Arial", 10), bg="#95A5A6", fg="white",
                      width=10)
    no_btn.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(leaderboard_tab, text="Clear Selected Difficulty", 
                        command=clear_leaderboard,
                        font=("Arial", 10), bg="#E74C3C", fg="white",
                        activebackground="#C0392B")
#clear_button.pack(pady=10)

# Initial display
update_leaderboard_display()

# Function to set difficulty preset
def set_difficulty(level):
    # Clear any previous feedback
    settings_feedback.config(text="")
    
    if level == "easy":
        min_entry.delete(0, tk.END)  # Clear current value
        min_entry.insert(0, "1")
        max_entry.delete(0, tk.END)
        max_entry.insert(0, "50")
        attempts_entry.delete(0, tk.END)
        attempts_entry.insert(0, "15")
        settings_feedback.config(text="✓ Easy mode selected!", fg="#2ECC71")
    elif level == "medium":
        min_entry.delete(0, tk.END)
        min_entry.insert(0, "1")
        max_entry.delete(0, tk.END)
        max_entry.insert(0, "100")
        attempts_entry.delete(0, tk.END)
        attempts_entry.insert(0, "10")
        settings_feedback.config(text="✓ Medium mode selected!", fg="#F39C12")
    elif level == "hard":
        min_entry.delete(0, tk.END)
        min_entry.insert(0, "1")
        max_entry.delete(0, tk.END)
        max_entry.insert(0, "500")
        attempts_entry.delete(0, tk.END)
        attempts_entry.insert(0, "12")
        settings_feedback.config(text="✓ Hard mode selected!", fg="#E74C3C")

#Difficulty buttons container
preset_buttons = tk.Frame(difficulty_frame, bg="#2C3E50")
preset_buttons.pack(pady=5)

# Easy button
easy_btn = tk.Button(preset_buttons, text="🟢 Easy\n(1-50, 15 tries)", 
                    command=lambda: set_difficulty("easy"),
                    font=("Arial", 10, "bold"),
                    bg="#2ECC71", fg="white",
                    width=12, height=3,
                    activebackground="#27AE60")
easy_btn.pack(side=tk.LEFT, padx=5)

# Medium button
medium_btn = tk.Button(preset_buttons, text="🟡 Medium\n(1-100, 10 tries)", 
                      command=lambda: set_difficulty("medium"),
                      font=("Arial", 10, "bold"),
                      bg="#F39C12", fg="white",
                      width=12, height=3,
                      activebackground="#E67E22")
medium_btn.pack(side=tk.LEFT, padx=5)

# Hard button
hard_btn = tk.Button(preset_buttons, text="🔴 Hard\n(1-500, 12 tries)", 
                    command=lambda: set_difficulty("hard"),
                    font=("Arial", 10, "bold"),
                    bg="#E74C3C", fg="white",
                    width=12, height=3,
                    activebackground="#C0392B")
hard_btn.pack(side=tk.LEFT, padx=5)

# Divider
divider = tk.Label(settings_tab, text="─── OR Custom Settings ───", 
                  font=("Arial", 10), bg="#2C3E50", fg="#7F8C8D")
divider.pack(pady=10)

# Range settings (min and max)
range_frame = tk.Frame(settings_tab, bg="#2C3E50")
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
attempts_frame = tk.Frame(settings_tab, bg="#2C3E50")
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

# ==================== GAME TAB ====================

# Create main container with 3 columns
main_game_container = tk.Frame(game_tab, bg="#2C3E50")
main_game_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Left frame - for play again button
left_frame = tk.Frame(main_game_container, bg="#2C3E50", width=150)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
left_frame.pack_propagate(False)  # Prevents frame from shrinking

# Center frame - main game area
center_frame = tk.Frame(main_game_container, bg="#2C3E50")
center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

# Right frame - for hint display
right_frame = tk.Frame(main_game_container, bg="#2C3E50", width=200)
right_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
right_frame.pack_propagate(False)  # Prevents frame from shrinking

# Display label
display_label = tk.Label(center_frame, text="", font=("Arial", 24, "bold"),
                        bg="#34495E", fg="white", height=2)
display_label.pack(pady=20, padx=20, fill=tk.X)

# Result label
result_label = tk.Label(center_frame, text="Configure settings and click Start Game", 
                       font=("Arial", 12), bg="#2C3E50", fg="white")
result_label.pack(pady=10)

# Info frame for attempts, hints, timer, score
info_frame = tk.Frame(center_frame, bg="#2C3E50")
info_frame.pack(pady=5)

attempts_label = tk.Label(info_frame, text="Attempts: 0/10 | Hints: 0", 
                         font=("Arial", 10), bg="#2C3E50", fg="#BDC3C7")
attempts_label.pack()

timer_label = tk.Label(info_frame, text="Time: 0s", 
                      font=("Arial", 10), bg="#2C3E50", fg="#3498DB")
timer_label.pack()

score_label = tk.Label(info_frame, text="Score: 0", 
                      font=("Arial", 11, "bold"), bg="#2C3E50", fg="#F39C12")
score_label.pack()

# Hint label (hidden by default)
hint_label = tk.Label(right_frame, text="", 
                     font=("Arial", 10), bg="#EC4710", fg="white",
                      padx=10, pady=10,relief=tk.RAISED,wraplength=180, bd=2)
# Function to start the game with settings
def start_game():
    global secret_number, min_range, max_range, max_attempts, attempts, game_started, game_over,start_time, hints_used, guess_history, guessed_after_hint, score
    
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
        hints_used = 0
        guess_history=[]
        guessed_after_hint = True  # Can use first hint without guessing
        start_time = time.time()  # Record start time
        score = 0

        # Update labels
        result_label.config(text=f"Guess a number between {min_range}-{max_range}", fg="white")
        attempts_label.config(text=f"Attempts: 0/{max_attempts} | Hints: 0")
        timer_label.config(text="Time: 0s")
        score_label.config(text="Score: 0")
        display_label.config(text="", bg="#34495E")
        hint_label.pack_forget()  # Hide hint label

        # Clear any previous feedback
        settings_feedback.config(text="")
        
        # Disable settings (can't change mid-game)
        min_entry.config(state=tk.DISABLED)
        max_entry.config(state=tk.DISABLED)
        attempts_entry.config(state=tk.DISABLED)
        start_button.config(state=tk.DISABLED, bg="#95A5A6")

        # Disable difficulty preset buttons during game
        easy_btn.config(state=tk.DISABLED)
        medium_btn.config(state=tk.DISABLED)
        hard_btn.config(state=tk.DISABLED)
        
        # Switch to game tab!
        # notebook.select(1) switches to tab at index 1 (Game tab)
        notebook.select(1)
        update_timer()  # Start the timer

    except ValueError:
        # If entries contain non-numbers
        settings_feedback.config(text="Please enter valid numbers!", fg="orange")

# Start Game button
start_button = tk.Button(settings_tab, text="Start Game", 
                        command=start_game,
                        font=("Arial", 12, "bold"),
                        bg="#9B59B6",
                        fg="white",
                        width=12,
                        activebackground="#8E44AD")
start_button.pack(pady=10)


def update_timer():
    # This function updates the timer every second
    if game_started and not game_over:
        elapsed = int(time.time() - start_time)  # Calculate elapsed seconds
        timer_label.config(text=f"Time: {elapsed}s")
        # Call this function again after 1000ms (1 second)
        window.after(1000, update_timer)

def calculate_score():
    # Calculate score based on attempts, hints, and time
    global score, Global_elapsed_time
    
    elapsed_time = int(time.time() - start_time)

    Global_elapsed_time = elapsed_time
    
    # Base score starts at 1000
    score = 1000
    
    # Deduct points for attempts (50 points per attempt)
    score -= attempts * 50
    
    # Deduct points for hints (100 points per hint)
    score -= hints_used * 100
    
    # Deduct points for time (1 point per second)
    score -= elapsed_time
    
    # Make sure score doesn't go negative
    if score < 0:
        score = 0
    
    score_label.config(text=f"Score: {score}")
    return elapsed_time

def show_hint():
    global hints_used, guess_history, guessed_after_hint
    
    if not game_started or game_over:
        return
    
    # Check if player made a guess after last hint
    if not guessed_after_hint:
        result_label.config(text="❌ Make a guess before using another hint!", fg="orange")
        return
    
    hints_used += 1
    guessed_after_hint = False  # Must guess before next hint
    attempts_label.config(text=f"Attempts: {attempts}/{max_attempts} | Hints: {hints_used}")
    
    # Build hint text
    hint_text = "💡 HINT:\n\n"
    
    # Show history
    if guess_history:
        recent = guess_history[-5:]  # Last 5 guesses
        hint_text += f"Your last guesses: {', '.join(map(str, recent))}\n\n"
    else:
        hint_text += "You haven't made any guesses yet!\n\n"
    
    # Give different hints based on how many hints used
    if hints_used == 1:
        # First hint: even or odd
        if secret_number % 2 == 0:
            hint_text += "The number is EVEN"
        else:
            hint_text += "The number is ODD"
    elif hints_used == 2:
        # Second hint: range narrowing
        mid = (min_range + max_range) // 2
        if secret_number <= mid:
            hint_text += f"The number is in the LOWER half ({min_range}-{mid})"
        else:
            hint_text += f"The number is in the UPPER half ({mid+1}-{max_range})"
    elif hints_used == 3:
        # Third hint: divisibility
        for divisor in [3, 5, 10]:
            if secret_number % divisor == 0:
                hint_text += f"The number is divisible by {divisor}"
                break
        else:
            hint_text += "The number is NOT divisible by 3, 5, or 10"
    else:
        # Additional hints: narrow range more
        if guess_history:
            closest = min(guess_history, key=lambda x: abs(x - secret_number))
            diff = abs(closest - secret_number)
            if diff <= 5:
                hint_text += f"You're VERY close! Within 5 of one of your guesses!"
            elif diff <= 10:
                hint_text += f"You're getting warm! Within 10 of one of your guesses!"
            else:
                hint_text += f"Your closest guess was {closest}"
        else:
            hint_text += "Make some guesses first!"
    hint_label.config(text=hint_text)
    hint_label.pack( pady=10, padx=5, expand=True)

# Hint button
hint_button = tk.Button(center_frame, text="💡 Get Hint", 
                       command=show_hint,
                       font=("Arial", 11, "bold"),
                       bg="#16A085",
                       fg="white",
                       width=12,
                       activebackground="#138D75")
hint_button.pack(pady=5)



# Function to handle number button clicks

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

def ask_player_name(difficulty):
    name_popup = tk.Toplevel(window)
    name_popup.title("New Score!")
    name_popup.geometry("300x150")
    name_popup.config(bg="#2C3E50")
    name_popup.grab_set()
    
    title = tk.Label(name_popup, text=f"🎉 {difficulty} Mode High Score!", 
                    font=("Arial", 13, "bold"), bg="#2C3E50", fg="#F39C12")
    title.pack(pady=15)
    
    name_entry = tk.Entry(name_popup, font=("Arial", 12), width=20)
    name_entry.pack(pady=10)
    name_entry.focus()

    def submit_name():
        player_name = name_entry.get().strip()
        if not player_name:
            player_name = "Anonymous"
        
        final_score_time = Global_elapsed_time
        add_to_leaderboard(player_name, score, final_score_time, difficulty)
        name_popup.destroy()
        
        win_sound.stop()
        pygame.mixer.music.unpause()
        notebook.select(2)  # Switch to leaderboard tab
    
    submit_btn = tk.Button(name_popup, text="Submit", command=submit_name,
                          font=("Arial", 12, "bold"), bg="#2ECC71", fg="white",
                          width=10, activebackground="#27AE60")
    submit_btn.pack(pady=10)
    
    name_entry.bind("<Return>", lambda e: submit_name())

        


def check_guess():
    global current_input, attempts, game_over, guess_history

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
    
    guess_history.append(guess)

    # Increment attempts
    attempts += 1
    attempts_label.config(text=f"Attempts: {attempts}/{max_attempts} | Hints: {hints_used}")

    # Calculate how far off the guess is (for visual feedback)
    difference = abs(guess - secret_number)
    range_size = max_range - min_range
    
    # Check if guess is too low, too high, or correct
    if guess < secret_number:
        result_label.config(text=f"{guess} is too low! Try again.", fg="#E74C3C")
        # Color feedback based on how close
        if difference <= range_size * 0.05:  # Within 5% of range
            display_label.config(bg="#E67E22",text="very close")  # Orange - very close
        elif difference <= range_size * 0.15:  # Within 15% of range
            display_label.config(bg="#F39C12",text="close")  # Yellow - close
        else:
            display_label.config(bg="#34495E",text="far")  # Default - far
    elif guess > secret_number:
        result_label.config(text=f"{guess} is too high! Try again.", fg="#E74C3C")
        if difference <= range_size * 0.05:
            display_label.config(bg="#E67E22",text="very close")  # Orange - very close
        elif difference <= range_size * 0.15:
            display_label.config(bg="#F39C12",text="close")  # Yellow - close
        else:
            display_label.config(bg="#34495E",text="far")  # Default - far
    elif guess > secret_number:
        result_label.config(text=f"{guess} is too high! Try again.", fg="#E74C3C")
        if difference <= range_size * 0.05:
            display_label.config(bg="#E67E22",text="very close")  # Orange - very close
        elif difference <= range_size * 0.15:
            display_label.config(bg="#F39C12",text="close")  # Yellow - close
        else:
            display_label.config(bg="#34495E",text="far")  # Default - far
    else:
       # Correct guess!
        game_over = True
        display_label.config(bg="#2ECC71")  # Green for correct
        result_label.config(text=f"🎉 Correct! You guessed it in {attempts} attempts!", fg="#2ECC71")

        # Determine difficulty for leaderboard
        if min_range == 1 and max_range == 50 and max_attempts == 15:
            difficulty = "Easy"
        elif min_range == 1 and max_range == 100 and max_attempts == 10:
            difficulty = "Medium"
        elif min_range == 1 and max_range == 500 and max_attempts == 12:
            difficulty = "Hard"
        else:
            difficulty = "Custom"

        window.after(500, lambda: ask_player_name(difficulty))

        pygame.mixer.music.pause()

        play_again_button.pack(expand=True, padx=10,)

        
        # Play victory sound!
        if sound_loaded :
            win_sound.play()

    # Check if out of attempts
    if attempts >= max_attempts and not game_over:
        game_over = True
        result_label.config(text=f"😞 Game Over! The number was {secret_number}", fg="#E74C3C")
        play_again_button.pack(pady=10, after=info_frame, side=tk.RIGHT)

    # Update score after each guess
    calculate_score()
    
    # Clear the input for next guess
    current_input = ""
    display_label.config(text="")

def reset_game():
    global secret_number, current_input, attempts, game_over, game_started,guess_history, hints_used, guessed_after_hint, start_time, score
    
    # Reset variables
    current_input = ""
    attempts = 0
    game_over = False
    game_started = False
    guess_history = []
    hints_used = 0
    guessed_after_hint = True
    start_time = 0
    score = 0
    

    # Reset labels
    display_label.config(text="")
    result_label.config(text="Configure settings and click Start Game", fg="white")
    attempts_label.config(text="Attempts: 0/10")
    timer_label.config(text="Time: 0s")
    score_label.config(text="Score: 0")
    hint_label.pack_forget()
    
    # Re-enable settings
    min_entry.config(state=tk.NORMAL)
    max_entry.config(state=tk.NORMAL)
    attempts_entry.config(state=tk.NORMAL)
    start_button.config(state=tk.NORMAL, bg="#9B59B6")

    # Re-enable difficulty buttons
    easy_btn.config(state=tk.NORMAL)
    medium_btn.config(state=tk.NORMAL)
    hard_btn.config(state=tk.NORMAL)

    # Hide play again button
    play_again_button.pack_forget()

    win_sound.stop()  # Stop sound if playing
    pygame.mixer.music.unpause()

    # Switch back to settings tab
    notebook.select(0)
    
number_frame= tk.Frame(center_frame,bg="#1681ED")
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

# Bind number keys using a loop
for num in range(10):  # 0-9
    window.bind(str(num), lambda e, n=num: button_click(n))

# Bind keypad numbers (on numeric keypad)
for num in range(10):
    window.bind(f'<KP_{num}>', lambda e, n=num: button_click(n))

# Bind Enter key
window.bind('<Return>', lambda e: check_guess())
window.bind('<KP_Enter>', lambda e: check_guess())  # Keypad Enter

# Bind Backspace to clear
window.bind('<BackSpace>', lambda e: clear_input())
window.bind('<Delete>', lambda e: clear_input())

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
play_again_button = tk.Button(left_frame, text="Play Again", 
                             command=reset_game,
                             font=("Arial", 14, "bold"),
                             bg="#F39C12",
                             fg="white",
                             width=15,
                             height=1,
                             activebackground="#E67E22",)
                             



# creator label at the bottom
creator_label= tk.Label(window,text="Created by Adekunle Oreoluwa", font=("Arial", 8), bg="#2C3E50", fg="white")
creator_label.pack(side=tk.BOTTOM, pady=0)

window.mainloop()

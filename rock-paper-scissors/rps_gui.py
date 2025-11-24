import tkinter as tk
import random
window = tk.Tk()
window.title("Rock Paper Scissors")
window.geometry("400x600")
window.config(bg="#2C3E50")
window.minsize(400, 500)  # Set minimum window size so it doesn't get too small

wins_count = 0
losses_count = 0
ties_count = 0
rounds_played = 0
max_rounds = 0
move_history = []  # List to store history of moves
history_visible = False  # Track if history is showing or hidden


round_frame = tk.Frame(window, bg="#2C3E50")
round_frame.pack(pady=10,fill=tk.X, padx=20)

round_label = tk.Label(round_frame, text="Number of rounds:", font=("Arial", 12),bg="#2C3E50", fg="white")
round_label.pack(side=tk.LEFT, padx=5)

round_entry = tk.Entry(round_frame, width=5, font=("Arial", 12))
round_entry.insert(0, "5")  # insert() puts default value "5" in the box
round_entry.pack(side=tk.LEFT, padx=5)


def set_rounds():
    global max_rounds, rounds_played, wins_count, losses_count, ties_count,move_history,history_visible
    try:
        # Get the value from entry box and convert to integer
        new_rounds = int(round_entry.get())
        
        # Make sure it's a reasonable number (between 1 and 20)
        if new_rounds < 1 or new_rounds > 20:
            result_label.config(text="Please enter a number between 1 and 20!")
            return
        max_rounds = new_rounds
        rounds_played = 0
        wins_count = 0
        losses_count = 0
        ties_count = 0
        move_history = []  # Clear history when setting new rounds
        history_visible = False  # Reset history visibility
        
        result_label.config(text="Choose your move!")
        score_label.config(text="Wins: 0 | Losses: 0 | Ties: 0")
        rounds_label.config(text=f"Rounds: 0/{max_rounds}")
        reset_button.pack_forget()
        set_button.config(text="Rounds Set!", state=tk.DISABLED)
        set_button.config(bg="#95A5A6", fg="#BDC3C7")
        round_entry.config(state=tk.DISABLED)
        #history_label.config(text="Move History:\nNo moves yet")  # Reset history display
        history_label.pack_forget()  # Hide history initially
        show_history_button.config(text="Show History")
        
    except ValueError:
        # If user enters text instead of number, show error
        result_label.config(text="Please enter a valid number!")

set_button = tk.Button(round_frame, text="Set Rounds", command=set_rounds,font=("Arial", 10), bg="#9B59B6", fg="white",activebackground="#8E44AD")
set_button.pack(side=tk.LEFT, padx=5)


result_label = tk.Label(window,text="Choose your move", font=("Arial",14, "bold"), fg='white', bg="#2C3E50",wraplength=450)
result_label.pack(pady=10,fill=tk.X, padx=20)

score_label = tk.Label(window,text="Wins: 0 | Losses: 0 | Ties: 0", font=("Arial",12), bg="#2C3E50", fg='white')
score_label.pack(pady=10,fill=tk.X, padx=20)

rounds_label = tk.Label(window,text=f"Rounds: 0/{max_rounds}", font=('Arial', 10), bg="#2C3E50", fg='white')
rounds_label.pack(pady=10,fill=tk.X, padx=20)

history_label = tk.Label(window, text="Move History:\nNo moves yet", font=("Arial", 10), bg="#34495E", fg="white", justify=tk.LEFT, padx=10, pady=10,wraplength=450)
#history_label.pack(pady=10, padx=20, fill=tk.BOTH)  # fill=tk.BOTH makes it expand


def toggle_history():
    # Toggle means switch between two states
    global history_visible
    
    if history_visible:
        # If currently visible, hide it
        history_label.pack_forget()
        show_history_button.config(text="Show History")
        history_visible = False
    else:
        # If currently hidden, show it
        update_history()  # Update before showing
        history_label.pack(pady=10, padx=20, fill=tk.BOTH,expand=True)
        show_history_button.config(text="Hide History")
        history_visible = True

show_history_button = tk.Button(window, text="Show History", command=toggle_history,width=30, height=1, font=("Arial", 10),bg="#16A085", fg="white", activebackground="#138D75")
show_history_button.pack(pady=10,padx=100)

def update_history():
    # Show only the last 5 moves
    # [-5:] gets the last 5 items from the list
    recent_history = move_history[-5:]
    
    if not recent_history:
        history_text = "Move History:\nNo moves yet"
    else:
        history_text = "Move History (Last 5):\n"
        # Loop through history and format each round
        for  move in (recent_history):
            history_text += f"Round {move['round']}: {move['player']} vs {move['computer']} - {move['result']}\n"
    
    history_label.config(text=history_text)


def player_choice(choice):
    global wins_count, losses_count, ties_count,rounds_played,max_rounds

    if max_rounds == 0:
        result_label.config(text="Please set the number of rounds first!")
        return
    if rounds_played >= max_rounds:
        result_label.config(text="Game over! Click Play again to Restart.")
        return
    rounds_played += 1

    computer_move = random.choice(['r', 'p', 's'])
    
    move_names ={'r': 'Rock', 'p': 'Paper', 's': 'Scissors'}

    wins_check ={'r':'s', 'p':'r', 's':'p'}

    if choice == computer_move:
        result='it is a tie'
        ties_count+=1
    elif wins_check[choice] == computer_move:
        result='You won'
        wins_count+=1
    else:
        result='Computer won'
        losses_count+=1

    move_history.append({
        'round': rounds_played,
        'player': move_names[choice],
        'computer': move_names[computer_move],
        'result': result
    })

    if history_visible:
        update_history()

    result_label.config(text=f"You ({move_names[choice]})\n vs \nComputer ({move_names[computer_move]})\n\n{result}")

    score_label.config(text=f"wins: {wins_count} | losses: {losses_count} | ties:{ties_count}")

    rounds_label.config(text=f"rounds: {rounds_played}/{max_rounds}")

    if rounds_played >= max_rounds:
        if wins_count > losses_count:
            final_result=" You won the game"
        elif losses_count > wins_count:
            final_result=" You lost the game"
        else:
            final_result="The game is tied"
        result_label.config(text= f"Game Over!\n{final_result}")
        reset_button.pack(pady=20)

def reset_game():
    global wins_count, losses_count, ties_count,rounds_played,max_rounds,move_history
    wins_count = 0
    losses_count = 0
    ties_count = 0
    rounds_played = 0
    max_rounds = 0
    move_history = []

    result_label.config(text=f"Choose your move!")

    score_label.config(text=f"wins: 0 | losses: 0 | ties: 0")

    rounds_label.config(text=f"rounds: 0/{max_rounds}")

    history_label.pack_forget()  # Hide history when resetting
    show_history_button.config(text="Show History")  # Reset button text

    reset_button.pack_forget()
    set_button.config(text="Set Rounds", state=tk.NORMAL)
    set_button.config(bg="#9B59B6", fg="white")
    round_entry.config(state=tk.NORMAL)


rock_button = tk.Button(window,text="💎 Rock",command=lambda: player_choice('r'), width=15, height=2, font=("Arial", 14, "bold"), bg="#E74C3C",fg="white",activebackground="#C0392B",relief="raised",bd=3)
rock_button.pack(pady=10, padx=50)

rock_button = tk.Button(window,text="📄 Paper",command=lambda: player_choice('p'), width=15, height=2, font=("Arial", 14, "bold"), bg="#3498DB",fg="white",activebackground="#2980B9",relief="raised",bd=3)
rock_button.pack(pady=10, padx=50)

rock_button = tk.Button(window,text="✂ Scissors",command=lambda: player_choice('s'), width=15, height=2, font=("Arial", 14, "bold"), bg="#2ECC71",fg="white",activebackground="#27AE60",relief="raised",bd=3)
rock_button.pack(pady=10, padx=50)

reset_button = tk.Button(window,text="Play Again",command=reset_game, bg='#F39C12', font=("Arial", 12, "bold"), width=15, height=2,fg="white",activebackground="#E67E22")

quit_button = tk.Button(window,text="Quit",command=window.destroy, bg='#95A5A6', font=("Arial", 12, "bold"), width=15, height=2,fg="white",activebackground="#7F8C8D")
quit_button.pack(pady=10, padx=80)


window.mainloop()
import tkinter as tk
import random
window = tk.Tk()
window.title("Rock Paper Scissors")
window.geometry("400x400")

wins_count = 0
losses_count = 0
ties_count = 0
rounds_played = 0
max_rounds = 5


result_label = tk.Label(window,text="Choose your move", font=("Arial",14))
result_label.pack(pady=10)

score_label = tk.Label(window,text="Wins: 0 | Losses: 0 | Ties: 0", font=("Arial",12))
score_label.pack(pady=10)

rounds_label = tk.Label(window,text=f"Rounds: 0/{max_rounds}", font=('Arial', 10))
rounds_label.pack(pady=10)


def player_choice(choice):
    global wins_count, losses_count, ties_count,rounds_played,max_rounds

    if rounds_played >= max_rounds:
        result_label.config(text="Game over! Click Play again")
        return
    rounds_played += 1

    computer_move = random.choice(['r', 'p', 's'])
    
    move_names ={'r': 'Rock', 'p': 'Paper', 's': 'Scissors'}

    wins_check ={'r':'s', 'p':'r', 's':'p'}

    if choice == computer_move:
        result='it is a tie'
        ties_count+=1
    elif wins_check[choice] == computer_move:
        result='You win'
        wins_count+=1
    else:
        result='You lose'
        losses_count+=1

    result_label.config(text=f"You: {move_names[choice]}\nComputer: {move_names[computer_move]}\n\n{result}")

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
    global wins_count, losses_count, ties_count,rounds_played,max_rounds
    wins_count = 0
    losses_count = 0
    ties_count = 0
    rounds_played = 0
    max_rounds = 5

    result_label.config(text=f"Choose your move!")

    score_label.config(text=f"wins: 0 | losses: 0 | ties: 0")

    rounds_label.config(text=f"rounds: 0/{max_rounds}")

    reset_button.pack_forget()


rock_button = tk.Button(window,text="💎 Rock",command=lambda: player_choice('r'))
rock_button.pack(pady=10)

rock_button = tk.Button(window,text="📄 Paper",command=lambda: player_choice('p'))
rock_button.pack(pady=10)

rock_button = tk.Button(window,text="✂ Scissors",command=lambda: player_choice('s'))
rock_button.pack(pady=10)

reset_button = tk.Button(window,text="Play Again",command=reset_game, bg='lightblue')

quit_button = tk.Button(window,text="Quit",command=window.destroy, bg="lightcoral")
quit_button.pack(pady=10)


window.mainloop()
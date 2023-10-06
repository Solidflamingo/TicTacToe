# Tic Tac Toe Game with Tkinter and Minimax Algorithm

# Importing Required Libraries

import tkinter as tk
from PIL import Image, ImageTk
import pygame
import winsound

# Initialize Pygame for Sound Effects

pygame.init()

# Load Sound Files

click_sound = pygame.mixer.Sound("click_sound.wav")
win_sound = pygame.mixer.Sound("win_sound.wav")
lose_sound = pygame.mixer.Sound("lose_sound.wav")
tie_sound = pygame.mixer.Sound("tie_sound.wav")

# Initialize Game Variables

board = [' ' for _ in range(9)]  # Board state
current_player = 'O'  # Starting player

# Initialize Tkinter Root Window

root = tk.Tk()
root.title("Tic Tac Toe")

# Screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Center the Window


def center_window(root, width, height):
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2) - 40
    root.geometry(f"{width}x{height}+{x}+{y}")


# Set the window size and position
width = screen_width - 50
height = screen_height - 100
center_window(root, width, height)


# Show the winner message (if the Minimax algorithm works correctly, humans should never win though


def show_winner_dialog(message, image_path):
    # Create a new window
    dialog = tk.Toplevel(root)
    dialog.geometry("1200x800")
    dialog.title("Thanks for playing")

    # Load and display background image
    img = Image.open(image_path)
    img = img.resize((500, 500))
    img = ImageTk.PhotoImage(img)
    panel = tk.Label(dialog, image=img)
    panel.image = img
    panel.pack(side="bottom", fill="both", expand=10)

    # Display winner message
    label = tk.Label(dialog, text=message, fg="black", font=("Arial", 48))
    label.pack()

    # 'OK' button to close the dialog
    button = tk.Button(dialog, text="OK", command=lambda: [dialog.destroy(), reset_game()], width=20, height=2, font=("Helvetica", 24))
    button.pack()

# Mute system sounds from Windows


def mute_system_sound():
    winsound.PlaySound(None, winsound.SND_ASYNC)


# Reset Game automatically when board is full

def reset_game():
    global board, current_player
    board = [' ' for _ in range(9)]
    current_player = 'O'
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text=' ', bg="SystemButtonFace")


# Make Move for human player, to also be called in the Minimax function


def make_move(cell):
    global current_player
    i, j = cell
    index = 3 * i + j
    if board[index] == ' ':
        board[index] = current_player
        buttons[i][j].config(text=current_player, bg="teal")
        click_sound.play()  # Play click sound
        current_player = 'O' if current_player == 'X' else 'X'

# Check Winner using three checks


def check_winner():
    # Horizontal checks
    for i in range(0, 9, 3):
        if board[i] == board[i + 1] == board[i + 2] != ' ':
            return board[i]
    # Vertical checks
    for i in range(3):
        if board[i] == board[i + 3] == board[i + 6] != ' ':
            return board[i]
    # Diagonal checks
    if board[0] == board[4] == board[8] != ' ':
        return board[0]
    if board[2] == board[4] == board[6] != ' ':
        return board[2]
    return None

# Minimax Algorithm for AI


def minimax(board, depth, maximizing):
    scores = {'X': 10, 'O': -10, 'tie': 0}

    winner = check_winner()
    if winner is not None:
        return scores[winner]

    if ' ' not in board:
        return scores['tie']

    if maximizing:
        best_score = float('-inf')
        for i in range(len(board)):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, depth + 1, False)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score

    else:
        best_score = float('inf')
        for i in range(len(board)):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, depth + 1, True)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score

# When tictactoe grid is clicked, events trigger to move the game forward and show winner


def on_click(cell):
    global current_player
    i, j = cell
    index = 3 * i + j
    if board[index] == ' ':
        make_move(cell)
        winner = check_winner()
        if winner:
            if winner == 'X':  # Assuming 'X' is the AI
                show_winner_dialog("The AI wins!", "ai_wins_background.jpg")
                lose_sound.play()  # Play lose sound effect
            else:  # Assuming 'O' is the player
                show_winner_dialog("You win!", "you_win_background.jpg")
                win_sound.play()  # Play win sound effect

        # Check for a tie
        if ' ' not in board:
            mute_system_sound()
            tie_sound.play()  # Play tie sound effect
            show_winner_dialog("It's a tie!", "tie_background.jpg")

        # AI's turn
        if current_player == 'X':  # Make sure it's the AI's turn
            best_score = -float('inf')
            best_move = None

            for i in range(len(board)):
                if board[i] == ' ':
                    board[i] = 'X'
                    score = minimax(board, 0, False)
                    board[i] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = i

            # Make the AI's best move
            if best_move is not None:
                make_move((best_move // 3, best_move % 3))
                winner = check_winner()

                if winner:
                    win_sound.play()
                    show_winner_dialog("The AI has beaten you.", "ai_wins_background.jpg")


# UI Configuration

# Configure rows and columns to expand with the window
for i in range(4):
    root.grid_rowconfigure(i, weight=1 if i > 0 else 0)
for j in range(3):
    root.grid_columnconfigure(j, weight=1)

# Create a top frame with a smaller height
top_frame = tk.Frame(root, height=50, bg='grey')
top_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")
top_frame.grid_propagate(False)

# Create a "Restart" button with adjusted size
reset_button = tk.Button(top_frame, text="Restart", font=("Helvetica", 24), command=reset_game)
reset_button.pack(expand=True, fill=tk.BOTH, side=tk.RIGHT)

# Create a "Mute" button with adjusted size
mute_button = tk.Button(top_frame, text="Mute", font=("Helvetica", 24), command=mute_system_sound)
mute_button.pack(expand=True, fill=tk.BOTH, side=tk.RIGHT)

# Create buttons
buttons = [[None, None, None] for _ in range(3)]
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, text=' ', font=("Helvetica", 48), command=lambda cell=(i, j): on_click(cell))
        buttons[i][j].grid(row=i + 1, column=j, sticky="nsew")


# Start Tkinter Event Loop

root.mainloop()

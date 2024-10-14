import tkinter as tk
from tkinter import messagebox
import random
import time

class TicTacToeAI:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic-Tac-Toe Game")
        self.master.geometry("400x500")
        self.master.configure(bg="#121212")  # Dark background

        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        self.create_dashboard()

    def create_dashboard(self):
        self.clear_frame()
        self.dashboard_frame = tk.Frame(self.master, bg="#121212")  # Match background color
        self.dashboard_frame.pack(pady=20)

        title_label = tk.Label(self.dashboard_frame, text="Tic-Tac-Toe", font=("Helvetica", 28, "bold"), bg="#121212", fg="#00e676")
        title_label.pack(pady=20)

        tagline_label = tk.Label(self.dashboard_frame, text="Challenge Your Mind!", font=("Helvetica", 16), bg="#121212", fg="#ffffff")
        tagline_label.pack(pady=10)

        play_ai_button = tk.Button(self.dashboard_frame, text="Play with AI", font=("Helvetica", 16), width=20, height=2, command=self.show_loading_screen_ai, bg="#00796b", fg="#ffffff", borderwidth=2, relief="solid")
        play_ai_button.pack(pady=10)

        play_pvp_button = tk.Button(self.dashboard_frame, text="Player1 vs Player2", font=("Helvetica", 16), width=20, height=2, command=self.show_loading_screen_pvp, bg="#f57f17", fg="#ffffff", borderwidth=2, relief="solid")
        play_pvp_button.pack(pady=10)

        instructions_button = tk.Button(self.dashboard_frame, text="Instructions", font=("Helvetica", 16), width=20, height=2, command=self.show_instructions, bg="#ff6f00", fg="#ffffff", borderwidth=2, relief="solid")
        instructions_button.pack(pady=10)

        quit_button = tk.Button(self.dashboard_frame, text="Quit", font=("Helvetica", 16), width=20, height=2, command=self.master.quit, bg="#c62828", fg="#ffffff", borderwidth=2, relief="solid")
        quit_button.pack(pady=10)

    def show_loading_screen_ai(self):
        self.show_loading_screen(ai_mode=True)

    def show_loading_screen_pvp(self):
        self.show_loading_screen(ai_mode=False)

    def show_loading_screen(self, ai_mode):
        self.clear_frame()
        loading_frame = tk.Frame(self.master, bg="#121212")
        loading_frame.pack(pady=50)

        heading_label = tk.Label(loading_frame, text="Loading Game...", font=("Helvetica", 24, "bold"), bg="#121212", fg="#00e676")
        heading_label.pack(pady=20)

        progress_bar = tk.Canvas(loading_frame, width=300, height=30, bg="#1e1e1e", bd=2, relief="raised")
        progress_bar.pack(pady=20)
        progress_bar.create_rectangle(0, 0, 0, 30, fill="#2196f3", tags="bar")  # Blue color for the progress bar
        
        # Percentage label
        percentage_label = tk.Label(loading_frame, text="0%", font=("Helvetica", 14), bg="#121212", fg="#00e676")
        percentage_label.pack(pady=5)

        self.master.update()
        self.load_progress(progress_bar, percentage_label, ai_mode)

    def load_progress(self, progress_bar, percentage_label, ai_mode):
        for i in range(0, 300, 10):
            progress_bar.coords("bar", 0, 0, i, 30)
            percentage_label.config(text=f"{i // 3}%")  # Update percentage
            self.master.update()
            time.sleep(0.05)

        self.master.after(500, lambda: self.start_game(ai_mode))

    def start_game(self, ai_mode):
        self.clear_frame()
        self.game_frame = tk.Frame(self.master, bg="#121212")
        self.game_frame.pack(pady=20)

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.game_frame, text="", font=("Helvetica", 24), width=6, height=3, command=lambda row=i, col=j: self.make_move(row, col), bg="#1e1e1e", fg="#ffffff", borderwidth=2, relief="solid")
                self.buttons[i][j].grid(row=i, column=j, padx=5, pady=5)

        mode_heading = "Player1 vs Player2" if not ai_mode else "Player1 vs AI"
        mode_label = tk.Label(self.game_frame, text=mode_heading, font=("Helvetica", 24, "bold"), bg="#121212", fg="#00e676")
        mode_label.grid(row=3, column=0, columnspan=3, pady=20)

        rules_label = tk.Label(self.game_frame, text="Who will claim victory? It's your turn!", font=("Helvetica", 14), bg="#121212", fg="#ffffff")
        rules_label.grid(row=4, column=0, columnspan=3, pady=10)

        self.ai_mode = ai_mode
        if self.ai_mode and random.choice([True, False]):
            self.master.after(2000, self.ai_make_move)  # Delay AI move for 2 seconds

    def show_instructions(self):
        messagebox.showinfo("Instructions", "Tic-Tac-Toe Game Instructions:\n\n1. The game is played on a 3x3 grid.\n2. Player1 is 'X' and Player2 or AI is 'O'.\n3. Players take turns to place their marks in empty cells.\n4. The first player to get 3 of their marks in a row (horizontally, vertically, or diagonally) wins.\n5. If all 9 cells are filled and no player has 3 marks in a row, the game is a draw.\n\nGood luck and may the best player win!")

    def make_move(self, row, col):
        if self.board[row][col] == "" and not self.check_winner():
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player, fg="#00e676" if self.current_player == "X" else "#ff5722")
            if self.check_winner():
                messagebox.showinfo("Game Over", f"🎉 Congratulations! Player {self.current_player} wins! 🎉\n\nPlay Again for More Fun!")
                self.master.after(1000, self.reset_game)  # Delay reset for 1 second
            elif self.check_draw():
                messagebox.showinfo("Game Over", "🤝 It's a draw! 🤝\n\nChallenge Again and Bring Your A-Game!")
                self.master.after(1000, self.reset_game)  # Delay reset for 1 second
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                if self.current_player == "O" and self.ai_mode:
                    self.master.after(1000, self.ai_make_move)  # Delay AI move for 1 second

    def ai_make_move(self):
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ""]
        row, col = random.choice(empty_cells)
        self.make_move(row, col)

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "":
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return True
        return False

    def check_draw(self):
        return all(self.board[i][j] != "" for i in range(3) for j in range(3))

    def reset_game(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", bg="#1e1e1e", fg="#ffffff")
        self.create_dashboard()

    def clear_frame(self):
        for widget in self.master.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    tic_tac_toe = TicTacToeAI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

import tkinter as tk
from tkinter import messagebox
import time

DARK_BG = "#1e1e1e"
CARD_BG = "#2a2a2a"
BTN_BG = "#3c3c3c"
BTN_HOVER = "#505050"
BTN_TEXT = "#ffffff"
TEXT_COLOR = "#e8e8e8"
X_COLOR = "#ff6b6b"
O_COLOR = "#4dabf7"
WIN_COLOR = "#2ecc71"

class CubicUI:
    def __init__(self, root, game, ai):
        self.game = game
        self.ai = ai
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.selected_algo = "alphabeta"  # default algorithm

        self.menu_frame = tk.Frame(root)
        self.game_frame = tk.Frame(root)

        self.create_menu()  
        self.create_game_ui()

        self.show_menu()

        self.start_time = None
        self.timer_running = False
        self.root.configure(bg=DARK_BG)
        self.menu_frame.configure(bg=DARK_BG)
        self.game_frame.configure(bg=DARK_BG)

    # -----------------------------------------------------------
    # MENU
    # -----------------------------------------------------------
    def create_menu(self):
        self.menu_frame.pack(fill="both", expand=True)

        title = tk.Label(
            self.menu_frame, text="3D Tic-Tac-Toe",
            font=("Arial", 28, "bold"), fg=TEXT_COLOR, bg=DARK_BG
        )
        title.pack(pady=40)

        # -------------------------
        # Algorithm selection buttons
        # -------------------------
        algo_label = tk.Label(
            self.menu_frame, text="Choose AI Algorithm:",
            font=("Arial", 16), fg=TEXT_COLOR, bg=DARK_BG
        )
        algo_label.pack(pady=(10, 5))

        algo_frame = tk.Frame(self.menu_frame, bg=DARK_BG)
        algo_frame.pack(pady=10)

        tk.Button(
            algo_frame, text="Minimax + H1", width=15,
            command=lambda: self.set_algorithm("minimax"),
            bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER
        ).pack(side="left", padx=5)

        tk.Button(
            algo_frame, text="AlphaBeta + H1", width=15,
            command=lambda: self.set_algorithm("alphabeta"),
            bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER
        ).pack(side="left", padx=5)

        tk.Button(
            algo_frame, text="Minimax + H2", width=15,
            command=lambda: self.set_algorithm("minimax2"),
            bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER
        ).pack(side="left", padx=5)

        tk.Button(
            algo_frame, text="AlphaBeta + H2", width=15,
            command=lambda: self.set_algorithm("alphabeta2"),
            bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER
        ).pack(side="left", padx=5)

        # -------------------------
        # Menu Buttons
        # -------------------------
        start_button = tk.Button(
            self.menu_frame, text="Start Game", font=("Arial", 16),
            command=self.start_game, width=15, height=2,
            bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER
        )
        start_button.pack(pady=15)

        close_button = tk.Button(
            self.menu_frame, text="Close", font=("Arial", 16),
            command=self.on_close, width=15, height=2,
            bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER
        )
        close_button.pack(pady=15)

    def set_algorithm(self, algo):
        self.selected_algo = algo
        messagebox.showinfo("Algorithm Selected", f"AI will use: {algo}")

    # -----------------------------------------------------------
    # GAME UI
    # -----------------------------------------------------------
    def create_game_ui(self):
        self.game_frame.pack_forget()
        self.game_frame.configure(bg=DARK_BG)

        top_frame = tk.Frame(self.game_frame, bg=DARK_BG)
        top_frame.pack(pady=10)

        self.status_label = tk.Label(
            top_frame, text="Player X's Turn",
            font=("Arial", 16), fg=TEXT_COLOR, bg=DARK_BG
        )
        self.status_label.pack(side="left", padx=20)

        self.timer_label = tk.Label(
            top_frame, text="Time: 00:00",
            font=("Arial", 16), fg=TEXT_COLOR, bg=DARK_BG
        )
        self.timer_label.pack(side="right", padx=20)

        grid_frame = tk.Frame(self.game_frame, bg=DARK_BG)
        grid_frame.pack()

        self.frames = []
        self.buttons = [[[None for _ in range(4)] for _ in range(4)] for _ in range(4)]
        self.create_grid(grid_frame)

        bottom_frame = tk.Frame(self.game_frame, bg=DARK_BG)
        bottom_frame.pack(pady=10)

        reset_button = tk.Button(
            bottom_frame, text="Reset", font=("Arial", 14),
            command=self.reset_game, width=10,
            bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER
        )
        reset_button.pack(side="left", padx=10)

        back_button = tk.Button(
            bottom_frame, text="Back to Menu", font=("Arial", 14),
            command=self.back_to_menu, width=15,
            bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER
        )
        back_button.pack(side="right", padx=10)

    def create_grid(self, parent):
        for z in range(4):
            frame = tk.Frame(parent, borderwidth=2, relief="solid", bg=CARD_BG)
            frame.grid(row=0, column=z, padx=10, pady=10)
            self.frames.append(frame)

            tk.Label(
                frame, text=f"Layer {z+1}", font=("Arial", 12),
                fg=TEXT_COLOR, bg=CARD_BG
            ).grid(row=0, column=0, columnspan=4, pady=5)

            for x in range(4):
                for y in range(4):
                    button = tk.Button(
                        frame, text="", width=4, height=2, font=("Arial", 16),
                        bg=BTN_BG, fg=BTN_TEXT, activebackground=BTN_HOVER,
                        command=lambda x=x, y=y, z=z: self.make_move(x, y, z)
                    )
                    button.grid(row=x+1, column=y, padx=3, pady=3)
                    self.buttons[z][x][y] = button

    # -----------------------------------------------------------
    # GAME LOGIC
    # -----------------------------------------------------------
    def show_menu(self):
        self.game_frame.pack_forget()
        self.menu_frame.pack(fill="both", expand=True)

    def start_game(self):
        self.menu_frame.pack_forget()
        self.game_frame.pack(fill="both", expand=True)
        self.reset_game()
        self.start_timer()

    def reset_game(self):
        self.game.reset_game()
        self.update_grid()
        self.status_label.config(text=f"Player {self.game.current_player}'s Turn")
        self.start_time = time.time()
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

        for z in range(4):
            for x in range(4):
                for y in range(4):
                    self.buttons[z][x][y].config(state="normal", text="", fg="black", bg="white")

    def back_to_menu(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to return to the main menu?"):
            self.timer_running = False
            self.show_menu()

    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
            self.root.destroy()

    def make_move(self, x, y, z):
        if self.game.board[x][y][z] is None and self.timer_running:
            self.game.board[x][y][z] = self.game.current_player
            self.update_grid()

            if self.game.is_winner(self.game.current_player):
                self.status_label.config(text=f"Player {self.game.current_player} Wins")
                self.highlight_winner(self.game.winning_positions)
                self.disable_buttons()
                self.timer_running = False
                return

            elif self.game.is_full():
                self.status_label.config(text="It's a Draw")
                self.disable_buttons()
                self.timer_running = False
                return

            self.game.current_player = "O"
            self.status_label.config(text="Player O's Turn (AI)")
            self.root.after(500, self.ai_move)

    # -----------------------------------------------------------
    # AI MOVE BASED ON SELECTED ALGORITHM
    # -----------------------------------------------------------
    def ai_move(self):
        if not self.timer_running:
            return

        start_time = time.time()

        if self.selected_algo == "minimax":
            move = self.ai.find_best_move_minimax(self.game)
        elif self.selected_algo == "alphabeta":
            move = self.ai.find_best_move_alphabeta(self.game)
        elif self.selected_algo == "minimax2":
            move = self.ai.find_best_move_minimax2(self.game)
        elif self.selected_algo == "alphabeta2":
            move = self.ai.find_best_move_alphabeta2(self.game)
        else:
            move = self.ai.find_best_move_alphabeta(self.game)

        end_time = time.time()
        print(f"Time taken: {end_time - start_time:.2f} seconds")

        if move:
            x, y, z = move
            self.game.board[x][y][z] = self.game.current_player
            self.update_grid()

            if self.game.is_winner(self.game.current_player):
                self.status_label.config(text=f"Player {self.game.current_player} Wins")
                self.highlight_winner(self.game.winning_positions)
                self.disable_buttons()
                self.timer_running = False
                return

            elif self.game.is_full():
                self.status_label.config(text="It's a Draw")
                self.disable_buttons()
                self.timer_running = False
                return

        self.game.current_player = "X"
        self.status_label.config(text="Player X's Turn")

    # -----------------------------------------------------------
    # UI HELPERS
    # -----------------------------------------------------------
    def update_grid(self):
        for z in range(4):
            for x in range(4):
                for y in range(4):
                    symbol = self.game.board[x][y][z]
                    if symbol == "X":
                        self.buttons[z][x][y].config(text=symbol, fg=X_COLOR, bg=BTN_BG)
                    elif symbol == "O":
                        self.buttons[z][x][y].config(text=symbol, fg=O_COLOR, bg=BTN_BG)
                    else:
                        self.buttons[z][x][y].config(text="", fg=TEXT_COLOR, bg=BTN_BG)

    def highlight_winner(self, winning_positions):
        for (x, y, z) in winning_positions:
            self.buttons[z][x][y].config(bg=WIN_COLOR)

    def disable_buttons(self):
        for z in range(4):
            for x in range(4):
                for y in range(4):
                    self.buttons[z][x][y].config(state="disabled")

    def start_timer(self):
        self.start_time = time.time()
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        if not self.timer_running:
            return

        elapsed = int(time.time() - self.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60

        self.timer_label.config(text=f"Time: {minutes:02d}:{seconds:02d}")
        self.root.after(1000, self.update_timer)
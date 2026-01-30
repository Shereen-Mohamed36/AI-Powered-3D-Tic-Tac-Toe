from tkinter import Tk
from game_logic import CubicGame
from ai_player import AIPlayerFast  
from ui import CubicUI
if __name__ == "__main__":
    root = Tk()
    root.title("3D Tic-Tac-Toe")
    root.geometry("1100x500")

    game = CubicGame()
    ai = AIPlayerFast("O")  
    app = CubicUI(root, game, ai)
    root.mainloop()

class CubicGame:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.board = [[[None for _ in range(4)] for _ in range(4)] for _ in range(4)] #board[layer][row][column]
        self.current_player = "X"
         
        self.winning_positions = []  
        

    def is_winner(self, player):
        
        directions = [
            (1, 0, 0), (0, 1, 0), (0, 0, 1),
            (1, 1, 0), (1, 0, 1), (0, 1, 1),
            (1, 1, 1), (1, -1, 0), (1, 0, -1),
            (0, 1, -1), (1, -1, -1)
        ]
        
        self.winning_positions = []  
        for x in range(4):
            for y in range(4):
                for z in range(4):
                    for dx, dy, dz in directions:
                        line = self.check_line(player, x, y, z, dx, dy, dz)#كل مرة نستدعيها عشان هل في ٤ خانات ورا بعض في اتجاه واحد 
                        if line:
                            self.winning_positions = line  
                            return True
                        
        return False
    

    def check_line(self, player, x, y, z, dx, dy, dz): 
        positions = [] 
        try:
            for i in range(4):
                if (
                    x < 0 or y < 0 or z < 0 or 
                    x >= 4 or y >= 4 or z >= 4 or 
                    self.board[x][y][z] != player 
                ):
                    return None   
                positions.append((x, y, z))
                x += dx
                y += dy
                z += dz
                
            return positions
        except IndexError:
            return None  

    def is_full(self): 
        for layer in self.board: 
            for row in layer: 
                if None in row:
                    return False
        return True
    # ---------------------------------------------
    def apply_move(self, x, y, z):
        if self.board[x][y][z] is None:
            self.board[x][y][z] = self.current_player
            self.current_player = "O" if self.current_player == "X" else "X"
            return True
        return False

    
    # ---------------------------------------------
    def undo_move(self, x, y, z):
        if self.board[x][y][z] is not None:
            self.board[x][y][z] = None
            self.current_player = "O" if self.current_player == "X" else "X"

    # ---------------------------------------------
    def get_available_moves(self):
        moves = []
        for x in range(4):
            for y in range(4):
                for z in range(4):
                    if self.board[x][y][z] is None:
                        moves.append((x, y, z))
        return moves

    # ---------------------------------------------
    def clone(self):
        new_game = CubicGame()
        
        new_game.board = [
            [row[:] for row in layer] 
            for layer in self.board
        ]
        new_game.current_player = self.current_player
        return new_game

    
    # ---------------------------------------------
    def print_board(self):
        print("\n========== BOARD ==========")
        for layer in range(4):
            print(f"\nLayer {layer}:")
            for row in self.board[layer]:
                print(row)
        print("===========================\n")
    
    # ---------------------------------------------
    def evaluate(self):
        if self.is_winner("X"):
            return 1000
        if self.is_winner("O"):
            return -1000

        score = 0

        directions = [
            (1, 0, 0), (0, 1, 0), (0, 0, 1),
            (1, 1, 0), (1, 0, 1), (0, 1, 1),
            (1, 1, 1), (1, -1, 0), (1, 0, -1),
            (0, 1, -1), (1, -1, -1)
        ]

        
        for x in range(4):
            for y in range(4):
                for z in range(4):
                    for dx, dy, dz in directions:
                        xs, os = 0, 0
                        for i in range(4):
                            nx, ny, nz = x + dx*i, y + dy*i, z + dz*i
                            if not (0 <= nx < 4 and 0 <= ny < 4 and 0 <= nz < 4):
                                break
                            cell = self.board[nx][ny][nz]
                            if cell == "X":
                                xs += 1
                            elif cell == "O":
                                os += 1

                        
                        if xs > 0 and os == 0:
                            score += xs ** 2  
                        elif os > 0 and xs == 0:
                            score -= os ** 2

        return score

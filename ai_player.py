
import math

class AIPlayerFast:
    def __init__(self, player_symbol):
        self.player_symbol = player_symbol
        self.opponent_symbol = "O" if player_symbol == "X" else "X"
        self.winning_lines =self._generate_winning_lines()
        self.cache ={}

    def get_promising_moves(self, game):
        moves = set()
        directions = [(dx, dy, dz)
                       for dx in [-1, 0, 1] 
                       for dy in [-1, 0, 1] 
                       for dz in [-1, 0, 1] 
                       if not (dx == dy == dz == 0)]
        
        for x in range(4):
            for y in range(4):
                for z in range(4):
                    if game.board[x][y][z] is not None: 
                        for dx, dy, dz in directions:
                            nx, ny, nz = x + dx, y + dy, z + dz
                            if 0 <= nx < 4 and 0 <= ny < 4 and 0 <= nz < 4 :
                                if game.board[nx][ny][nz] is None:
                                    moves.add((nx, ny, nz))
        
            return [(x, y, z) 
                    for x in range(4) 
                    for y in range(4) 
                    for z in range(4) 
                    if game.board[x][y][z] is None]
        
        return list(moves)

    def _generate_winning_lines(self):
        lines = []
        directions = [
            (1, 0, 0), (0, 1, 0), (0, 0, 1),
            (1, 1, 0), (1, 0, 1), (0, 1, 1),
            (1, 1, 1), (1, -1, 0), (1, 0, -1),
            (0, 1, -1), (1, -1, -1)
        ]
        for dx, dy, dz in directions:
            for x in range(4):
                for y in range(4):
                    for z in range(4):
                        line = [(x+i*dx ,y+i*dy ,z+i*dz  ) for i in range(4)]
                        if all(0<=a <4 and 0<=b < 4 and 0<=c < 4 for a,b,c in line) :  # فقط الخطوط الكاملة
                            lines.append(line)
        return lines

    # Heuristic1: 
    def heuristic(self, game, player):
        score = 0
        opp = self.opponent_symbol if player == self.player_symbol else self.player_symbol
        for line in self.winning_lines:
            p = sum(1 for x, y, z in line if game.board[x][y][z] == player)
            o = sum(1 for x, y, z in line if game.board[x][y][z] == opp)
            empty = 4 - p - o

            if p > 0 and o == 0:
                score += p ** 3
                if p == 3 and empty == 1:
                    score += 500
            if o > 0 and p == 0:
                score -= o ** 3
                if p == 3 and empty == 1:
                    score -= 500
        return score

    # Heuristic2: positional + aggressive
    def heuristic2(self, game, player):
        score = 0
        opp = self.opponent_symbol if player == self.player_symbol else self.player_symbol


        for line in self.winning_lines:
            p = sum(1 for pos in line if game.board[pos[0]][pos[1]][pos[2]] == player)
            o = sum(1 for pos in line if game.board[pos[0]][pos[1]][pos[2]] == opp)
            empty = 4 - p - o

            if p > 0 and o == 0:
                if p == 4:
                    return 100000
                score += [0, 10, 100, 1000][p] + empty * 10

            if o > 0 and p == 0:
                if o == 4:
                    return -100000
                score -= [0, 15, 150, 1500][o] + empty * 15


        # Positional bonuses
        centers = [(1,1,1), (1,1,2), (1,2,1), (1,2,2), (2,1,1), (2,1,2), (2,2,1), (2,2,2)]
        corners = [(0,0,0), (0,0,3), (0,3,0), (0,3,3), (3,0,0), (3,0,3), (3,3,0), (3,3,3)]

        for x,y,z in centers:
            if game.board[x][y][z] == player: score += 8
            elif game.board[x][y][z] == opp: score -= 8

        for x,y,z in corners:
            if game.board[x][y][z] == player: score += 6
            elif game.board[x][y][z] == opp: score -= 6

        return score

    def minimax(self, game, depth, maximizing_player):
        if game.is_winner(self.player_symbol):
            return 10000
        if game.is_winner(self.opponent_symbol):
            return -10000
        if depth == 0 or game.is_full():
            return self.heuristic(game, self.player_symbol)

        moves = self.get_promising_moves(game)

        if maximizing_player:
            max_eval = -math.inf
            for x, y, z in moves:
                game.board[x][y][z] = self.player_symbol
                eval = self.minimax(game, depth - 1, False)
                game.board[x][y][z] = None
                max_eval = max(max_eval, eval)
            return max_eval

        else:
            min_eval = math.inf
            for x, y, z in moves:
                game.board[x][y][z] = self.opponent_symbol
                eval = self.minimax(game, depth - 1, True)
                game.board[x][y][z] = None
                min_eval = min(min_eval, eval)
            return min_eval

    def find_best_move_minimax(self, game, depth=2):
        best_val = -math.inf
        best_move = None

        moves = self.get_promising_moves(game)

        for x, y, z in moves:
            game.board[x][y][z] = self.player_symbol
            move_val = self.minimax(game, depth - 1, False)
            game.board[x][y][z] = None

            if move_val > best_val:
                best_val = move_val
                best_move = (x, y, z)

        return best_move

    def minimax2(self, game, depth, maximizing_player):
        if game.is_winner(self.player_symbol):
            return 10000
        if game.is_winner(self.opponent_symbol):
            return -10000
        if depth == 0 or game.is_full():
            return self.heuristic2(game, self.player_symbol)

        moves = self.get_promising_moves(game)

        if maximizing_player:
            max_eval = -math.inf
            for x, y, z in moves:
                game.board[x][y][z] = self.player_symbol
                eval = self.minimax2(game, depth - 1, False)
                game.board[x][y][z] = None
                max_eval = max(max_eval, eval)
            return max_eval

        else:
            min_eval = math.inf
            for x, y, z in moves:
                game.board[x][y][z] = self.opponent_symbol
                eval = self.minimax2(game, depth - 1, True)
                game.board[x][y][z] = None
                min_eval = min(min_eval, eval)
            return min_eval

    def find_best_move_minimax2(self, game, depth=1):
        best_val = -math.inf
        best_move = None

        moves = self.get_promising_moves(game)

        for x, y, z in moves:
            game.board[x][y][z] = self.player_symbol
            move_val = self.minimax2(game, depth - 1, False)
            game.board[x][y][z] = None

            if move_val > best_val:
                best_val = move_val
                best_move = (x, y, z)

        return best_move

    def alpha_beta(self, game, depth, alpha, beta, maximizing_player):
        key =(tuple(tuple(tuple (row) for row in plane ) for plane in game.board) ,
              depth ,
              maximizing_player
        )
        if key in self.cache:
            return self.cache[key]
        
        if game.is_winner(self.player_symbol):
            return 10000
        if game.is_winner(self.opponent_symbol):
            return -10000
        if game.is_full() or depth == 0:
            return self.heuristic(game, self.player_symbol)

        moves = self.get_promising_moves(game)

        if maximizing_player:
            value = -math.inf
            for x, y, z in moves:
                game.board[x][y][z] = self.player_symbol
                value = max(value, self.alpha_beta(game, depth-1, alpha, beta, False))
                game.board[x][y][z] = None
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
        else:
            value = math.inf
            for x, y, z in moves:
                game.board[x][y][z] = self.opponent_symbol
                value = min(value, self.alpha_beta(game, depth-1, alpha, beta, True))
                game.board[x][y][z] = None
                beta = min(beta, value)
                if beta <= alpha:
                    break

        self.cache[key] = value
        return value
       



    def find_best_move_alphabeta(self, game, depth=1):
        best_val = -math.inf
        best_move = None

        moves = self.get_promising_moves(game)

    
        for x, y, z in moves:
            game.board[x][y][z] = self.player_symbol
            val = self.alpha_beta(game, depth-1, -math.inf, math.inf, False)
            game.board[x][y][z] = None

            if val > best_val:
                best_val = val
                best_move = (x,y,z)

        return best_move
    def alpha_beta2(self, game, depth, alpha, beta, maximizing_player):
            key = (tuple(tuple(tuple(row) for row in plane) for plane in game.board),
                   depth,
                   maximizing_player
            )
            if key in self.cache:
                return self.cache[key]
            
            if game.is_winner(self.player_symbol):
                return 10000
            if game.is_winner(self.opponent_symbol):
                return -10000
            if game.is_full() or depth == 0:
                return self.heuristic2(game, self.player_symbol)

            moves = self.get_promising_moves(game)

            if maximizing_player:
                value = -math.inf
                for x, y, z in moves:
                    game.board[x][y][z] = self.player_symbol
                    value = max(value, self.alpha_beta2(game, depth-1, alpha, beta, False))
                    game.board[x][y][z] = None
                    alpha = max(alpha, value)

                    if beta <= alpha:
                       
                       break
            else:
                value = math.inf
                for x, y, z in moves:
                    game.board[x][y][z] = self.opponent_symbol
                    value = min(value, self.alpha_beta2(game, depth-1, alpha, beta, True))
                    game.board[x][y][z] = None
                    beta = min(beta, value)
                    if beta <= alpha:
                        break

            self.cache[key] = value
            return value

    def find_best_move_alphabeta2(self, game, depth=1):
        best_val = -math.inf
        best_move = None

        moves = self.get_promising_moves(game)

       
        for x, y, z in moves:
            game.board[x][y][z] = self.player_symbol
            if game.is_winner(self.player_symbol):
                game.board[x][y][z] = None
                return (x, y, z)
            game.board[x][y][z] = None

    
        for x, y, z in moves:
            game.board[x][y][z] = self.opponent_symbol
            if game.is_winner(self.opponent_symbol):
                game.board[x][y][z] = None
                return (x, y, z)
            game.board[x][y][z] = None

        for x, y, z in moves:
            game.board[x][y][z] = self.player_symbol
            move_val = self.alpha_beta2(game, depth - 1, -math.inf, math.inf, False)
            game.board[x][y][z] = None
            if move_val > best_val:
                best_val = move_val
                best_move = (x, y, z)

        return best_move

    def find_best_move_alphabeta_fast(self, game, depth=1):
        self.cache.clear()
        return self.find_best_move_alphabeta2(game, depth)

    
    def find_best_move(self, game):
        best_val = -math.inf
        best_move = None
        for x in range(4):
            for y in range(4):
                for z in range(4):
                    if game.board[x][y][z] is None:
                        game.board[x][y][z] = self.player_symbol
                        move_val = self.heuristic(game, self.player_symbol) - self.heuristic(game, self.opponent_symbol)
                        game.board[x][y][z] = None
                        if move_val > best_val:
                            best_val = move_val
                            best_move = (x, y, z)
        return best_move
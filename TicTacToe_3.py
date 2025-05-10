import tkinter as tk
from tkinter import messagebox

class TicTacToeGUI:
    def __init__(self, size):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.size = size
        self.board = [['' for _ in range(size)] for _ in range(size)]
        self.buttons = [[None for _ in range(size)] for _ in range(size)]
        self.moves_count = 0
        self.current_player = 'X'

        
        # Status label
        self.status_label = tk.Label(
            self.window, 
            text="Your turn (X)",
            font=('Arial', 14)
        )
        self.status_label.grid(row=size, columnspan=size, pady=10)
        
        # Reset button
        self.reset_button = tk.Button(
            self.window,
            text="New Game",
            font=('Arial', 12),
            command=self.reset_game
        )
        self.reset_button.grid(row=size+1, columnspan=size, pady=10)
        
        # Create the game board
        self.create_board()
    
    def create_board(self):
        for i in range(self.size):
            for j in range(self.size):
                self.buttons[i][j] = tk.Button(
                    self.window,
                    text="",
                    font=('Arial', 20),
                    width=3,
                    height=1,
                    command=lambda row=i, col=j: self.make_move(row, col)
                )
                self.buttons[i][j].grid(row=i, column=j, padx=2, pady=2)
    
    def make_move(self, row, col):
        # Player's move (X)
        if self.board[row][col] == '':
            self.buttons[row][col].config(text='X')
            self.board[row][col] = 'X'
            self.moves_count += 1
            
            result = self.check_winner()
            if result:
                self.handle_game_end(result)
                return
                
            # Computer's move (O)
            self.AI_move()
    
    def get_empty_position(self):
        empty_position = []
        for i in range(self.size):
            for j in range(self.size):
                if(self.board[i][j] == ''):
                    empty_position.append((i,j))
        return empty_position
        
    def AI_move(self):
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        
        empty_positions = self.get_empty_position()
        if not empty_positions:
            return
            
        for i, j in empty_positions:  # Only iterate over empty positions
            if self.board[i][j] == '':  # Additional check to be safe
                self.board[i][j] = 'O'
                score = self.minimax(0, False, alpha, beta)
                self.board[i][j] = ''
                
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
                
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
        
        if best_move:
            i, j = best_move
            self.board[i][j] = 'O'
            self.buttons[i][j].config(text='O')
            self.moves_count += 1
            
            result = self.check_winner()
            if result:
                self.handle_game_end(result)

    def minimax(self, depth, is_maximizing, alpha, beta):
        result = self.check_winner()
        if result:
            if result == 'O':
                return 1
            elif result == 'X':
                return -1  # This was missing a value
            else:  # Tie
                return 0
                
        if depth >= 9:  # Add maximum depth to prevent infinite recursion
            return 0

        empty_positions = self.get_empty_position()
        if not empty_positions:  # No moves left
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i, j in empty_positions:  # Only iterate over empty positions
                if self.board[i][j] == '':
                    self.board[i][j] = 'O'
                    score = self.minimax(depth + 1, False, alpha, beta)
                    self.board[i][j] = ''
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
            return best_score
        else:
            best_score = float('inf')
            for i, j in empty_positions:  # Only iterate over empty positions
                if self.board[i][j] == '':
                    self.board[i][j] = 'X'
                    score = self.minimax(depth + 1, True, alpha, beta)
                    self.board[i][j] = ''
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
            return best_score

    
    def check_winner(self):
        # Check rows, columns and diagonals for a win
        for i in range(self.size):
            for j in range(self.size - 2):
                # Check rows
                if (self.board[i][j] == self.board[i][j+1] == self.board[i][j+2] != ''):
                    return self.board[i][j]
                # Check columns
                if (self.board[j][i] == self.board[j+1][i] == self.board[j+2][i] != ''):
                    return self.board[j][i]
        
        # Check diagonals
        for i in range(self.size - 2):
            for j in range(self.size - 2):
                # Main diagonal
                if (self.board[i][j] == self.board[i+1][j+1] == self.board[i+2][j+2] != ''):
                    return self.board[i][j]
                # Anti-diagonal
                if (j + 2 < self.size and 
                    self.board[i][j+2] == self.board[i+1][j+1] == self.board[i+2][j] != ''):
                    return self.board[i][j+2]
        
        # Check for tie
        if self.moves_count == self.size * self.size:
            return 'Tie'
        
        return None
    
    def handle_game_end(self, result):
        if result == 'Tie':
            messagebox.showinfo("Game Over", "It's a tie!")
        else:
            messagebox.showinfo("Game Over", f"Player {result} wins!")
        self.disable_board()
    
    def disable_board(self):
        for i in range(self.size):
            for j in range(self.size):
                self.buttons[i][j]['state'] = 'disabled'
        self.status_label.config(text="Game Over!")
    
    def reset_game(self):
        self.board = [['' for _ in range(self.size)] for _ in range(self.size)]
        self.moves_count = 0
        for i in range(self.size):
            for j in range(self.size):
                self.buttons[i][j].config(text="", state='normal')
        self.status_label.config(text="Your turn (X)")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToeGUI(3)
    game.run()

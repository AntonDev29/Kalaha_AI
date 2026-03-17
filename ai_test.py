# Author: Anton 
# Minimax AI for Kalaha with alpha-beta pruning

from board import KalahaBoard
import copy


class KalahaAI:
    def __init__(self, max_depth=6):
        """
        Initialize the Kalaha AI with minimax algorithm.
        
        Args:
            max_depth: Maximum depth for minimax search tree
        """
        self.max_depth = max_depth

    def evaluate_board(self, board, ai_player):
        """
        Evaluate the board position.
        Higher score is better for the AI player.
        
        Args:
            board: KalahaBoard instance
            ai_player: The AI player number (1 or 2)
        
        Returns:
            Score representing board advantage
        """
        if ai_player == 1:
            ai_store = board.state[6]
            opponent_store = board.state[13]
        else:
            ai_store = board.state[13]
            opponent_store = board.state[6]
        
        # Score difference between AI and opponent
        return ai_store - opponent_store

    def minimax(self, board, depth, is_maximizing, ai_player, alpha, beta):
        """
        Minimax algorithm with alpha-beta pruning.
        
        Args:
            board: KalahaBoard instance (will be modified during recursion)
            depth: Current depth in the search tree
            is_maximizing: True if maximizing player (AI), False if minimizing (opponent)
            ai_player: The AI player number
            alpha: Alpha value for pruning
            beta: Beta value for pruning
        
        Returns:
            Best score achievable from this position
        """
        # Terminal condition: max depth reached or game over
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board, ai_player)

        current_player = ai_player if is_maximizing else (3 - ai_player)  # Toggle player
        valid_moves = board.get_valid_moves(current_player)

        if not valid_moves:
            # No valid moves, pass turn
            return self.minimax(board, depth - 1, not is_maximizing, ai_player, alpha, beta)

        if is_maximizing:
            max_eval = float('-inf')
            for move in valid_moves:
                # Make a copy of the board to explore this move
                board_copy = self.copy_board(board)
                bonus_turn = board_copy.move(move, current_player)
                
                # If there's a bonus turn, the maximizing player goes again
                next_is_maximizing = True if bonus_turn else False
                eval_score = self.minimax(board_copy, depth - 1, next_is_maximizing, ai_player, alpha, beta)
                
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cutoff
            
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                # Make a copy of the board to explore this move
                board_copy = self.copy_board(board)
                bonus_turn = board_copy.move(move, current_player)
                
                # If there's a bonus turn, the minimizing player goes again
                next_is_maximizing = False if bonus_turn else True
                eval_score = self.minimax(board_copy, depth - 1, next_is_maximizing, ai_player, alpha, beta)
                
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cutoff
            
            return min_eval

    def get_best_move(self, board, ai_player):
        """
        Find the best move for the AI using minimax.
        
        Args:
            board: KalahaBoard instance
            ai_player: The AI player number (1 or 2)
        
        Returns:
            The best pit index to play
        """
        valid_moves = board.get_valid_moves(ai_player)
        
        if not valid_moves:
            return None

        best_move = valid_moves[0]
        best_score = float('-inf')

        for move in valid_moves:
            # Make a copy to simulate this move
            board_copy = self.copy_board(board)
            bonus_turn = board_copy.move(move, ai_player)
            
            # Opponent moves next (unless AI gets bonus turn)
            next_is_maximizing = True if bonus_turn else False
            score = self.minimax(board_copy, self.max_depth - 1, next_is_maximizing, ai_player, 
                                float('-inf'), float('inf'))
            
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    @staticmethod
    def copy_board(board):
        """
        Create a deep copy of the board state.
        
        Args:
            board: KalahaBoard instance
        
        Returns:
            A new KalahaBoard with copied state
        """
        new_board = KalahaBoard()
        new_board.state = board.state.copy()
        return new_board


# Example usage and testing
if __name__ == "__main__":
    from main import print_board
    
    def play_game_with_ai():
        """
        Play Kalaha with AI opponent.
        Player 1 is human, Player 2 is AI.
        """
        game = KalahaBoard()
        ai = KalahaAI(max_depth=6)
        current_player = 1

        while not game.is_game_over():
            print_board(game)
            print(f"Player {current_player}'s turn")

            moves = game.get_valid_moves(current_player)

            if not moves:
                print(f"Player {current_player} has no valid moves!")
                current_player = 2 if current_player == 1 else 1
                continue

            if current_player == 1:
                # Human player
                choice = int(input(f"Choose a pit {moves}: "))
                if choice not in moves:
                    print("Invalid move!")
                    continue
            else:
                # AI player
                choice = ai.get_best_move(game, current_player)
                print(f"AI chooses pit {choice}")

            bonus_turn = game.move(choice, current_player)

            if not bonus_turn:
                current_player = 2 if current_player == 1 else 1

        game.finalize_game()
        print_board(game)
        
        p1_score = game.state[6]
        p2_score = game.state[13]
        print("Game Over!")
        print(f"Player 1 Score: {p1_score}")
        print(f"Player 2 (AI) Score: {p2_score}")
        
        if p1_score > p2_score:
            print("Player 1 wins!")
        elif p2_score > p1_score:
            print("AI wins!")
        else:
            print("It's a tie!")

    # Uncomment to play
    # play_game_with_ai()

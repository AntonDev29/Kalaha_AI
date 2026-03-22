# Author: Anton 
# Minimax AI for Kalaha with alpha-beta pruning

from board import KalahaBoard
import copy


class KalahaAI:
    def __init__(self, max_depth=6):
        self.max_depth = max_depth

    def evaluate_board(self, board, ai_player):
        if ai_player == 1:
            ai_store = board.state[6]
            opponent_store = board.state[13]
        else:
            ai_store = board.state[13]
            opponent_store = board.state[6]
        # Score difference between AI and opponent
        return ai_store - opponent_store

    def minimax(self, board, depth, is_maximizing, ai_player, alpha, beta):
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board, ai_player)
        current_player = ai_player if is_maximizing else (3 - ai_player) 
        valid_moves = board.get_valid_moves(current_player)

        if not valid_moves:
            #No valid moves, pass turn
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
        
        new_board = KalahaBoard()
        new_board.state = board.state.copy()
        return new_board
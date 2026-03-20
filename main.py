# Author: Romel Meza s215212

from board import KalahaBoard
from ai_test import KalahaAI

def print_board(board):
    print("\n          P2 side")
    print("     holes: 12  11  10   9   8   7")
    print("     stones:", end=" ")
    for stones in reversed(board.state[7:13]):
        print(f"{stones:>3}", end=" ")
    print()

    print(f"store {board.state[13]:>2}                      {board.state[6]:<2} store")

    print("     stones:", end=" ")
    for stones in board.state[0:6]:
        print(f"{stones:>3}", end=" ")
    print()
    print("     holes:  0   1   2   3   4   5")
    print("          P1 side\n")


def play_game():
    game = KalahaBoard()
    ai = KalahaAI(max_depth=6)
    current_player = 1  # Human is 1, AI is 2

    while not game.is_game_over():
        print_board(game)
        print(f"Player {current_player}'s turn")

        moves = game.get_valid_moves(current_player)

        if current_player == 1:
            choice = int(input(f"Choose a pit {moves}: "))
            if choice not in moves:
                print("Invalid move!")
                continue
            else:
                choice = ai.get_best_move(game, current_player)
                print(f"AI chooses pit {choice}")

        bonus_turn = game.move(choice, current_player)

        if not bonus_turn:
            current_player = 2 if current_player == 1 else 1

    game.finalize_game()
    print_board(game)
    print("Game Over!")


if __name__ == "__main__":
    play_game()

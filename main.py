# Author: Romel Meza s215212

from board import KalahaBoard
from ai_test import KalahaAI

def print_board(board):
    indent = "        "
    cell = 5

    top_labels = "".join(f"{i:^{cell}}" for i in [6, 5, 4, 3, 2, 1])
    top_stones = "".join(f"{f'[{stones}]':^{cell}}" for stones in reversed(board.state[7:13]))
    bottom_stones = "".join(f"{f'[{stones}]':^{cell}}" for stones in board.state[0:6])
    bottom_labels = "".join(f"{i:^{cell}}" for i in [1, 2, 3, 4, 5, 6])

    middle_width = len(top_stones)
    left_store = f"[P2:{board.state[13]}]"
    right_store = f"[P1:{board.state[6]}]"
    middle_line = left_store + " " * (middle_width - len(left_store) - len(right_store) + 15) + right_store

    print()
    print(indent + top_labels)
    print(indent + top_stones)
    print(middle_line)
    print(indent + bottom_stones)
    print(indent + bottom_labels)
    print()

def play_game():
    game = KalahaBoard()
    ai = KalahaAI(max_depth=6)
    current_player = 1  # Human is 1, AI is 2

    while not game.is_game_over():
        print_board(game)
        print(f"Player {current_player}'s turn")

        moves = game.get_valid_moves(current_player)

        if current_player == 1:
            user_input = input("Choose a pit [1-6]: ")

            if not user_input.isdigit():
                print("Please enter a number.")
                continue

            displayed_choice = int(user_input)

            if displayed_choice < 1 or displayed_choice > 6:
                print("Invalid move!")
                continue

            choice = displayed_choice - 1   # convert 1–6 to 0–5

            if choice not in moves:
                print("Invalid move!")
                continue

        else:
            choice = ai.get_best_move(game, current_player)
            print(f"AI chooses pit {13 - choice}")

        bonus_turn = game.move(choice, current_player)

        if not bonus_turn:
            current_player = 2 if current_player == 1 else 1

    game.finalize_game()
    print_board(game)
    print("Game Over!")


if __name__ == "__main__":
    play_game()

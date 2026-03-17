# Author: Romel Meza s215212

from board import KalahaBoard


def print_board(board):
    print(f"\n   {list(reversed(board.state[7:13]))}")  # P2 Pits
    print(f"{board.state[13]}                  {board.state[6]}")  # Stores
    print(f"   {board.state[0:6]}\n")  # P1 Pits


def play_game():
    game = KalahaBoard()
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
            # Placeholder for AI logic
            choice = moves[0]
            print(f"AI chooses {choice - 6}")

        bonus_turn = game.move(choice, current_player)

        if not bonus_turn:
            current_player = 2 if current_player == 1 else 1

    game.finalize_game()
    print_board(game)
    print("Game Over!")


if __name__ == "__main__":
    play_game()

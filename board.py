# Author: Romel Meza s215212
class KalahaBoard:
    def __init__(self):
        # Indices 0-5: Player 1 pits, 6: P1 Store
        # Indices 7-12: Player 2 pits, 13: P2 Store
        self.state = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        self.p1_indices = range(0, 6)
        self.p2_indices = range(7, 13)

    def is_game_over(self):
        return sum(self.state[0:6]) == 0 or sum(self.state[7:13]) == 0

    def get_valid_moves(self, player):
        indices = self.p1_indices if player == 1 else self.p2_indices
        return [i for i in indices if self.state[i] > 0]

    def move(self, pit_index, player):
        stones = self.state[pit_index]
        self.state[pit_index] = 0

        current_pos = pit_index
        while stones > 0:
            current_pos = (current_pos + 1) % 14

            # Skip opponent's store
            if (player == 1 and current_pos == 13) or (player == 2 and current_pos == 6):
                continue

            self.state[current_pos] += 1
            stones -= 1

        # Rule: Capture
        # If last stone lands in an empty pit on your side
        my_pits = self.p1_indices if player == 1 else self.p2_indices
        if current_pos in my_pits and self.state[current_pos] == 1:
            opposite_pit = 12 - current_pos
            if self.state[opposite_pit] > 0:
                store_idx = 6 if player == 1 else 13
                self.state[store_idx] += self.state[opposite_pit] + 1
                self.state[opposite_pit] = 0
                self.state[current_pos] = 0

        # Rule: Bonus Turn
        # Returns True if the player lands in their own store
        if (player == 1 and current_pos == 6) or (player == 2 and current_pos == 13):
            return True
        return False

    def finalize_game(self):
        # Move remaining stones to respective stores when game ends
        self.state[6] += sum(self.state[0:6])
        self.state[13] += sum(self.state[7:13])
        for i in range(14):
            if i not in [6, 13]:
                self.state[i] = 0

import random

"""This program plays a game of Rock, Paper, Scissors between two Players,
and reports both Player's scores each round."""

moves = ['rock', 'paper', 'scissors']


class Player:
    """The Player class is the parent class for all of the Players
    in this game"""

    def __init__(self):
        self.score = 0

    def move(self):
        return 'rock'

    def learn(self, my_move, their_move):
        pass


class AllRockPlayer(Player):
    """A player that always plays rock"""

    def move(self):
        return 'rock'


class RandomPlayer(Player):
    """A player that chooses moves randomly"""

    def move(self):
        return random.choice(moves)


class HumanPlayer(Player):
    """A player controlled by human input"""

    def move(self):
        while True:
            user_move = input("Rock, paper, or scissors? ").lower()
            if user_move in moves:
                return user_move
            print("Invalid move! Please enter 'rock', 'paper', or 'scissors'.")


class ReflectPlayer(Player):
    """A player that reflects the opponent's previous move"""

    def __init__(self):
        super().__init__()
        self.their_last_move = None

    def move(self):
        if self.their_last_move is None:
            return random.choice(moves)
        return self.their_last_move

    def learn(self, my_move, their_move):
        self.their_last_move = their_move


class CyclePlayer(Player):
    """A player that cycles through moves in order"""

    def __init__(self):
        super().__init__()
        self.my_last_move = None

    def move(self):
        if self.my_last_move is None:
            return random.choice(moves)
        current_index = moves.index(self.my_last_move)
        next_index = (current_index + 1) % len(moves)
        return moves[next_index]

    def learn(self, my_move, their_move):
        self.my_last_move = my_move


def beats(one, two):
    """Determine if move 'one' beats move 'two'"""
    return ((one == 'rock' and two == 'scissors') or
            (one == 'scissors' and two == 'paper') or
            (one == 'paper' and two == 'rock'))


class Game:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def play_round(self):
        move1 = self.p1.move()
        move2 = self.p2.move()
        print(f"Player 1: {move1}  Player 2: {move2}")

        if beats(move1, move2):
            print("Player 1 wins this round!")
            self.p1.score += 1
        elif beats(move2, move1):
            print("Player 2 wins this round!")
            self.p2.score += 1
        else:
            print("It's a tie!")

        print(f"Score: Player 1: {self.p1.score}, "
              f"Player 2: {self.p2.score}\n")

        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)

    def play_game(self, rounds=None):
        print("Rock Paper Scissors Game Start!")
        print("=" * 40)

        round_num = 1
        max_rounds = rounds if rounds else float('inf')

        while round_num <= max_rounds:
            print(f"Round {round_num}:")
            self.play_round()

            score_diff = abs(self.p1.score - self.p2.score)
            if score_diff >= 3 and rounds is None:
                break

            if rounds is None:
                if (isinstance(self.p1, HumanPlayer) or
                        isinstance(self.p2, HumanPlayer)):
                    continue_game = input("Continue playing? "
                                          "(yes/no): ").lower()
                    if continue_game not in ['yes', 'y']:
                        break
                else:
                    if round_num >= 5:
                        break

            round_num += 1

        print("=" * 40)
        print("Game Over!")
        print(f"Final Score - Player 1: {self.p1.score}, "
              f"Player 2: {self.p2.score}")

        if self.p1.score > self.p2.score:
            print("Player 1 wins the game!")
        elif self.p2.score > self.p1.score:
            print("Player 2 wins the game!")
        else:
            print("The game is tied!")
        print("=" * 40)


if __name__ == '__main__':
    players = {
        '1': AllRockPlayer,
        '2': RandomPlayer,
        '3': ReflectPlayer,
        '4': CyclePlayer,
        '5': HumanPlayer
    }

    print("Welcome to Rock Paper Scissors!")
    print("\nPlayer list:")
    for number, player in players.items():
        print(f"{number}. {player.__name__}")

    while (p1 := input("\nChoose player 1: ")) not in players.keys():
        print("Invalid choice, please select player 1 from the list.")

    while (p2 := input("Choose player 2: ")) not in players.keys():
        print("Invalid choice, please select player 2 from the list.")

    while True:
        try:
            rounds = int(input("How many rounds shall we play? "))
            if rounds > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")

    print()
    game = Game(players[p1](), players[p2]())
    game.play_game(rounds)

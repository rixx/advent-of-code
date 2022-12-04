class Round:
    SYMBOLS = {
        "A": "rock",
        "B": "paper",
        "C": "scissors",
        "X": "rock",
        "Y": "paper",
        "Z": "scissors",
    }
    OUTCOMES = {
        ("rock", "paper"): "win",
        ("rock", "scissors"): "lose",
        ("paper", "rock"): "lose",
        ("paper", "scissors"): "win",
        ("scissors", "rock"): "win",
        ("scissors", "paper"): "lose",
    }
    SYMBOL_SCORES = {"rock": 1, "paper": 2, "scissors": 3}
    OUTCOME_SCORES = {"lose": 0, "draw": 3, "win": 6}

    def __init__(self, opponent_choice, own_choice):
        self.opponent_choice = self.SYMBOLS[opponent_choice]
        self.own_choice = self.SYMBOLS[own_choice]
        if self.opponent_choice == self.own_choice:
            self.outcome = "draw"
        else:
            self.outcome = self.OUTCOMES[self.opponent_choice, self.own_choice]
        self.score = (
            self.SYMBOL_SCORES[self.own_choice] + self.OUTCOME_SCORES[self.outcome]
        )


def main_a():
    with open("aoc02.txt") as fp:
        text = fp.readlines()

    rounds = []
    for line in text:
        items = line.split()
        if len(items) > 1:
            rounds.append(Round(*items))
    print(sum([round.score for round in rounds]))


if __name__ == "__main__":
    main_a()

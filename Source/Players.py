import random
from collections import deque
from AIPlayer import Player


class Defector:
    def __init__(self):
        self.name = "Defector"
        self.choice = False

        self.points = 0
        self.final_points = 0

    def reaction(self, stimulus):
        pass

    def reset(self):
        self.points = 0


class Cooperator:
    def __init__(self):
        self.name = "Cooperator"
        self.choice = True

        self.points = 0
        self.final_points = 0

    def reaction(self, stimulus):
        pass

    def reset(self):
        self.points = 0


class Random:
    def __init__(self):
        self.name = "Random"

        if random.randint(0, 1) == 1:
            self.choice = True
        else:
            self.choice = False

        self.points = 0
        self.final_points = 0

    def reaction(self, stimulus):
        if random.randint(0, 1) == 1:
            self.choice = True
        else:
            self.choice = False

    def reset(self):
        self.points = 0


class Coward:
    def __init__(self):
        self.name = "Coward"
        self.choice = False

        self.hiding = False
        self.analysis = []

        self.points = 0
        self.final_points = 0

    def reaction(self, stimulus):
        if stimulus is False and self.hiding is False:
            self.hiding = True
            self.choice = True

        elif self.hiding is True:
            self.analysis.append(stimulus)
            if len(self.analysis) >= 5:
                if sum(self.analysis) >= 3:
                    self.choice = True
                else:
                    self.choice = False
                self.hiding = None
        else:
            pass

    def reset(self):
        self.choice = False
        self.hiding = False
        self.analysis.clear()
        self.points = 0


class Grudge:
    def __init__(self):
        self.name = "Grudge"
        self.choice = True

        self.grudge_held = False

        self.points = 0
        self.final_points = 0

    def reaction(self, stimulus):
        if not self.grudge_held and not stimulus:
            self.choice = False

    def reset(self):
        self.choice = True
        self.grudge_held = False

        self.points = 0


class Detective:
    def __init__(self):
        self.name = "Detective"
        self.choice = True
        self.turn_count = 1
        self.play_nice = None

        self.points = 0
        self.final_points = 0

    def reaction(self, stimulus):
        match self.turn_count:
            case 1:
                self.choice = False
                self.turn_count += 1
            case 2:
                self.choice = True
                self.turn_count += 1
            case 3:
                self.play_nice = not stimulus
                self.turn_count += 1
                if self.play_nice:
                    self.choice = stimulus
                else:
                    self.choice = False
            case _:
                if self.play_nice:
                    self.choice = stimulus
                else:
                    self.choice = False

    def reset(self):
        self.choice = True
        self.play_nice = None
        self.turn_count = 1
        self.points = 0


class TitForTat:
    def __init__(self):
        self.name = "TitForTat"
        self.choice = True

        self.points = 0
        self.final_points = 0

    def reaction(self, stimulus):
        self.choice = stimulus

    def reset(self):
        self.choice = True
        self.points = 0


class Forgiving:
    def __init__(self):
        self.name = "Forgiving"
        self.choice = True

        self.points = 0
        self.final_points = 0

    def reaction(self, stimulus):
        if random.randint(1, 8) == 1:
            self.choice = True
        else:
            self.choice = stimulus

    def reset(self):
        self.choice = True
        self.points = 0


class Sneaky:
    def __init__(self):
        self.name = "Sneaky"
        self.choice = True

        self.points = 0
        self.final_points = 0

    def reaction(self, stimulus):
        if random.randint(1, 8) == 1:
            self.choice = False
        else:
            self.choice = stimulus

    def reset(self):
        self.choice = True
        self.points = 0


class AI:
    def __init__(self):
        self.name = "AI"

        self.player = Player()
        self.previous_rounds = deque(maxlen=5)  # Set previous rounds to the ROUND_MEMORY for the model you're using
        for i in range(self.previous_rounds.maxlen):
            self.previous_rounds.appendleft((2, 2))

        self.choice = self.player.get_action(self.previous_rounds)

        self.points = 0
        self.final_points = 0

    def reaction(self, stimulus):
        self.previous_rounds.appendleft((self.choice, stimulus))
        self.choice = self.player.get_action(self.previous_rounds)

    def reset(self):
        self.previous_rounds.clear()
        for i in range(self.previous_rounds.maxlen):
            self.previous_rounds.appendleft((2, 2))
        self.choice = self.player.get_action(self.previous_rounds)
        self.points = 0

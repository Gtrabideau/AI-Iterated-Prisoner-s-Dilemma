from collections import deque
import random
import Players

# List of players that the AI will face, not including Random, which the AI can't learn from.
player_list = [Players.Defector(), Players.Cooperator(), Players.Grudge(), Players.TitForTat(),
               Players.Detective(), Players.Sneaky(), Players.Forgiving(), Players.Coward()]


class TrainingDilemma:
    def __init__(self, memory):

        # Start player list in a random order
        random.shuffle(player_list)
        self.currentPlayer = 0
        self.player2 = player_list[self.currentPlayer]
        self.rounds = 0

        # Optional AI player points if you want that data
        self.p1points = 0

        # Total score for graphing purposes
        self.score = 0

        # Start past data as all 2's, representing that there is no past data
        self.previous_rounds = deque(maxlen=memory)
        for i in range(self.previous_rounds.maxlen):
            self.previous_rounds.appendleft((2, 2))

    def reset_game(self):
        # Start player list in a random order
        random.shuffle(player_list)
        self.currentPlayer = 0
        self.player2 = player_list[self.currentPlayer]
        self.player2.reset()
        self.rounds = 0

        # Optional AI player points if you want that data
        self.p1points = 0

        # Total score for graphing purposes
        self.score = 0

        # Start past data as all 2's, representing that there is no past data
        self.previous_rounds.clear()
        for i in range(self.previous_rounds.maxlen):
            self.previous_rounds.appendleft((2, 2))

    # Point giver for the second player, which might require points to function correctly
    def give_points(self, player, points):
        player.points += points
        player.final_points += points

    def play_step(self, action):
        reward = 0

        # Get choices from players
        p1choice = bool(action)
        p2choice = self.player2.choice

        # Give points based on player choices (optional way to dispense rewards commented out)
        if (p1choice is True) and (p2choice is True):
            self.score += 3
            reward = 3
            self.p1points += 3

            self.give_points(self.player2, 3)

        elif (p1choice is True) and (p2choice is False):
            self.give_points(self.player2, 5)

        elif (p1choice is False) and (p2choice is True):
            self.score += 5
            reward = 5
            self.p1points += 5

        elif (p1choice is False) and (p2choice is False):
            self.score += 1
            reward = 1
            self.p1points += 5

            self.give_points(self.player2, 1)

        else:
            print('ERROR: Impossible player choices - P1[' + str(p1choice) + '], [' + str(p2choice) + ']')

        # Optional rewards system that works with self.p1points; I believe it improves results.
        # Rewards the AI at the end of each player 2's rounds, but only if the score is 25.
        # The reward is based on the equation so that it is rewarded exponentially the higher above 25 it gets.
        if self.rounds >= 25:
            reward += (1.03 ** (self.p1points - 25)) - 1  # 1.03^(x-500) - 1

        # Update data
        self.previous_rounds.appendleft((p1choice, p2choice))

        # Change player 2's decision based on the AI's decision
        self.player2.reaction(p1choice)

        self.rounds += 1
        # Change player at round 25 and it is not the last player
        if self.rounds >= 25 and self.currentPlayer != len(player_list) - 1:
            self.currentPlayer += 1
            self.player2 = player_list[self.currentPlayer]
            self.player2.reset()

            self.p1points = 0
            self.rounds = 0

        return reward, self.score

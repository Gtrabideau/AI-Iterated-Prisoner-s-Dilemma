import Dilemma
import Players

# Create 2 instances of each player type so each can player can go against itself and every other player type
player_tuple = (Players.Defector(), Players.Cooperator(), Players.Grudge(), Players.Random(), Players.TitForTat(),
                Players.Detective(), Players.Sneaky(), Players.Forgiving(), Players.Coward(), Players.AI())
player_tuple2 = (Players.Defector(), Players.Cooperator(), Players.Grudge(), Players.Random(), Players.TitForTat(),
                 Players.Detective(), Players.Sneaky(), Players.Forgiving(), Players.Coward(), Players.AI())

# Clear data before starting the matches
Dilemma.clear_data()

# Match each player type against every player type on the second list that it already hasn't faced
for player1 in player_tuple:
    for player2 in player_tuple2[player_tuple.index(player1):]:
        current_round = 1

        # Play x rounds with the current match-up
        while current_round <= 200:
            Dilemma.play(player1, player2, current_round)
            current_round += 1

        # Reset the players before moving on
        player1.reset()
        player2.reset()

# Print out the final scores
Dilemma.final_scores(player_tuple, player_tuple2)
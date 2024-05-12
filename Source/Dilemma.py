import csv


# Function to give out points
def give_points(player, points):
    player.points += points
    player.final_points += points


# Play one round of the dilemma
def play(player1, player2, current_round):
    p1choice = bool(player1.choice)
    p2choice = bool(player2.choice)

    # Give points based on player choices
    if p1choice and p2choice:
        give_points(player1, 3)
        give_points(player2, 3)
    elif p1choice and not p2choice:
        give_points(player2, 5)
    elif p2choice and not p1choice:
        give_points(player1, 5)
    else:
        give_points(player1, 1)
        give_points(player2, 1)

    # Store choices in data file
    with open('Data/matchData.csv', mode='a') as csvfile:
        csvfile.write(player1.name + ',' + player2.name + "," + str(current_round) + "," +
                      str(p1choice) + "," + str(p2choice) + "," +
                      str(player1.points) + "," + str(player2.points) + "\n")

    # Have players react to the results
    player1.reaction(p2choice)
    player2.reaction(p1choice)


# Function for printing final scores to a file
def final_scores(player_list, player_list2):
    for i in range(len(player_list)):
        with open('Data/finalScores.csv', mode='a') as csvfile:
            csvfile.write(player_list[i].name + "," + str(player_list[i].final_points + player_list2[i].final_points)
                          + "\n")


# Function for clearing data so that new data can be entered
def clear_data():
    # Replace the actual match data with the blank data
    with open("Data/blankMatchData.csv", "r") as example, open("Data/matchData.csv", "w") as data:
        for line in example:
            data.write(line)

    # Replace the actual final scores data with the blank data
    with open("Data/blankFinalScores.csv", "r") as example, open("Data/finalScores.csv", "w") as data:
        for line in example:
            data.write(line)

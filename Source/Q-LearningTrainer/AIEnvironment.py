import itertools
import numpy as np
from AIDilemma import TrainingDilemma
import pickle
from matplotlib import style
from Plotter import plot

style.use('ggplot')

HM_EPISODES = 50_000  # Total episodes
epsilon = 0.99  # The closer to 1, the more random it starts as
EPS_DECAY = 0.9998  # The rate at which the randomness decays
SHOW_EVERY = 5000  # Update graph every x episodes

start_q_table = None  # None or filename if you want to continue training a model
export_q_table = "../Data/qtable.pickle"  # The location and name of the end q-table

CHOICES = 3  # Number of stimuli (True, False, and no stimuli)
LEARNING_RATE = 0.01
DISCOUNT = 0.95  # For adjusting how much it cares about future rewards

ROUND_MEMORY = 5  # Number of rounds back that AI keeps track of

# Create a q-table if there is none
if start_q_table is None:
    def fill():
        tups = []
        for x1 in range(CHOICES):
            for y1 in range(CHOICES):
                tups.append((x1, y1))
        return tups


    # Initialize q table as a dictionary
    q_table = {}

    tuples = []
    cartesian_products = []

    for i in range(ROUND_MEMORY):
        # Get a number of tuples equal to the amount of rounds you want remembered
        tuples.append(tuple(fill()))
    for element in itertools.product(*tuples):
        # Get the cartesian products, so you have all the possible combinations of actions and stimuli
        cartesian_products.append(element)
    for i in cartesian_products:
        # Give two random negative weights to the possible actions the AI can make (true or false)
        q_table[i] = [np.random.uniform(-10, -5) for j in range(2)]

# Load already made q-table
else:
    with open(start_q_table, 'rb') as f:
        q_table = pickle.load(f)

# Variables for graphing
plot_scores = []
plot_avgscores = []
section_score = 0
total_score = 0
highest_score = 0

# Create the dilemma the AI will practice on with the number of rounds it wants to be returned
dilemma = TrainingDilemma(ROUND_MEMORY)

for episode in range(HM_EPISODES):
    # Start the dilemma from a blank slate
    dilemma.reset_game()

    # Play 200 rounds in the dilemma, with player 2 switching every 25 rounds
    for i in range(200):

        # Current data
        obs = tuple(dilemma.previous_rounds)

        # Choose action based on q-table or make a random choice for exploration
        if np.random.random() > epsilon:
            action = np.argmax(q_table[obs])
        else:
            action = np.random.randint(0, 2)

        # Get the reward and score from the dilemma
        reward, score = dilemma.play_step(action)

        # Save the new data
        new_obs = tuple(dilemma.previous_rounds)

        # Get q-scores for calculation
        max_future_q = np.max(q_table[new_obs])
        current_q = q_table[obs][action]

        # Equation for filling spot in q table
        new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)

        # Put value in q-table at the intersection of the observation and the action taken
        q_table[obs][action] = new_q

    # Decay epsilon to reduce random choices over time
    epsilon *= EPS_DECAY

    # Store total score for average score calculation
    total_score += dilemma.score
    section_score += dilemma.score

    # Plot progress
    if episode % SHOW_EVERY == 0:
        # Average score of all scores in all episodes
        avg_score = total_score / (episode + 1)
        plot_avgscores.append(avg_score)

        # Average score of SHOW_EVERY episodes
        section_score = section_score / SHOW_EVERY
        plot_scores.append(section_score)
        plot(plot_scores, plot_avgscores)
        print(section_score)

        # Optional code to export the best scoring q-table only if it has an average score of 560 or higher.
        # if section_score >= highest_score and section_score >= 560:
        #     highest_score = section_score
        #     with open("../Data/qtable-Highest.pickle", "wb") as f:
        #         pickle.dump(q_table, f)

        # reset dilemma score
        section_score = 0

# Save q-table when finished, can change output name as needed
with open(export_q_table, "wb") as f:
    pickle.dump(q_table, f)

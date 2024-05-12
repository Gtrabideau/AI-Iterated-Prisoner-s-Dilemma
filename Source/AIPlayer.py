import pickle
import numpy as np

# the location and name of the q-table you want to use
qtable_name = "Data/qtable-Final.pickle"


class Player:
    def __init__(self):
        # Load the q-table based on its name
        with open(qtable_name, "rb") as f:
            self.q_table = pickle.load(f)

    def get_action(self, previous_rounds):
        # Turns the previous round data into a tuple and accesses the Q-table to get the action
        obs = tuple(previous_rounds)
        action = np.argmax(self.q_table[obs])
        return action

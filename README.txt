AI Iterated Prisoner's Dilemma

Description:
This project was inspired by Axelrod's Tournament, an experiment that tested different approached to the iterated prisoner's dilemma.
Robert Axelrod's paper on this tournament can be found here: https://www.jstor.org/stable/173932

This project acts both as a smaller version of Axelrod's tournament as well as a test for a q-learning AI that will participate in the tournament. New stratagies for the tournament can be added in the 'Players.py' file and a new q-table can be trained in the 'AITrainer.py' file in the 'Q-LearningTrainer' folder. It is reccomended that this project be opened in an IDE such as PyCharm in order to more easily install the correct imports as well as navigate the files. It is also recommended that you first read about Axelrod's Tournament or at least quickly google the Iterated Prisoner's Dilemma.


Project Contents:
'Data' Folder: This contains the .csv files for the final scores and match data of a single run-through of the iterated prisoner's dilemma as well as the blank versions of these csv files. It also contains a pre-trained qtable for the AI player, titled 'qtable-Final.pickle'.

'Q-LearningTrainer' Folder: This folder contains 'AITrainer.py', a python script which is used to create and train the q-table used by the AI; 'AIDIlemma.py', a python script which is used by 'AITrainer.py' to simulate the iterated prisoner's dilemma in order to train the q-table; 'Plotter.py' a python script which is used by 'AITrainer.py' in order to plot data from the trainer as it trains.

'Main.py': The main python file which runs the dilemma with the strategies contained in 'Players.py'.

'Players.py': Python file which contains a class for each of the strategies to be used in the dilemma. Each strategy is listed and explained later in the README.

'AIPlayer.py': A python program which holds the Player class for the AI, also where you replace the file location and name if you want to use a q-table that is different from the pre-trained table. You will also need to change self.round_memory in the 'Players.py' file for the AI if you train a q-table with less memory.

'Dilemma.py': A python program which contains all the tools to run the dilemma, this file is used by 'Main.py'.


How To Use 'AITrainer.py':
1: Enter the location of the q-table you want to continue training into start_q_table, or put None if you are starting are starting a new q-table.
2: Enter the location of where you want to export the q-table, the default location is to the 'Data' folder.
3: Adjust the HM_EPISODES, epsilon, EPS_DECAY, SHOW_EVERY, LEARNING_RATE, DISCOUNT, and ROUND_MEMORY to your preferences. I believe the default settings are near optimal.
4: Run the python file and then then start again from step 1, replacing start_q_table with the path to your file. Make sure ROUND_MEMORY is set to same number it was when that q-table file was trained. For best results train the same q-table multiple times.


How To Use 'Main.py':
1: Simply run 'Main.py' and the results data will be output to the .csv files in Data

The pre-trained q-table, 'qtable-final.pickle', was able to an average score of over 560 in the AIDilemma simulation for a 5000 round sample and was trained multiple times in order to reach this point. This q-table is the default one used by AIPlayer, and often gets the highest score of all the strategies.


The Strategies:
Defector: Will always 'defect' (return false)

Cooperator: Will always 'cooperate' (return true)

Random: Will randomly defect or cooperate

Grudge: Will always cooperate until its opponent defects, at which point Grudge will always defect no matter what

TitForTat: Will start with cooperate, but will make the same choice as its opponent last choice.

Forgiving: Will act like TitForTat, but will sometimes cooperate instead of defecting, even if the opponent defected last round. 

Sneaky: Will act like TitforTat, but will sometimes defect instead of cooperating, even if the opponent cooperated last round.

Detective: Will start with the pattern cooperate, defect, cooperate in order to try and guess its opponents actions, then it will either act as TitForTat if it thinks its opponent will retaliate against defections or always defect if it thinks its opponent is vulnerable.

Coward: Will start with defect, but will enter a 'hiding' state if the opponent responds harshly to any of its defections. In its 'hiding' state, it will cooperate for 5 rounds and see how the opponent responds. If the opponent seems to forgive the Coward, it will always cooperate, if the the opponent doesn't forgive the Coward, it will always defect.

AI: This will act differently based on the q-table loaded. The pre-trained table will act as follows: Will often start with two rounds of cooperating, and will respond to defections with defections and cooperations with cooperations. It will also sense the Coward and take advantage of its pattern in order to trick the Coward into cooperating and then will defect against the Coward.


Feel free to add your own strategy class to the 'Players.py' file using the same format as the others. You will also need to add this new strategy to the player_tuple and and player_tuple2 in 'Main.py' as well as the player_list in 'AIDilemma.py' if you wish to train a q-table against your strategy.
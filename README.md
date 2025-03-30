# Project Penney

This project focuses on simulating many games of penney. Penney is a game where two players each choose a certain 3-bit sequence based on a combination of black and red. The deck is then drawn until there is a sequence that matches with one of the player's chosen sequence. The player also gets to keep the previously drawn cards that led to their matching sequence. The process repeats until you run out of cards. The sequence each player chooses cannot be the same. The game is scored by two methods: tricks and totals by cards. A trick is where the player found a matching sequence to their desired sequence, which counts as one trick. Totals by cards is scored by how many cards a player received for each trick.

---
# How to Play the Game (step-by-step)

1. Start with a shuffled 52 card standard deck. And get another person to play with you.
2. Each player chooses a 3 letter combination of Reds and/or Blacks as their sequence of choice. Both players cannot have the same sequence.
3. Decide which scoring method you will use (tricks or total cards).
4. Flip cards one at a time from the deck until you see a sequence that matches a player's chosen sequence (eg., Red, Black, Black). The player who got the match gets one point (trick) and also gets to keep any previous cards flipped in addition to the matching sequence of cards.
5. Repeat step 3 until you run out of cards.
6. Score based on the chosen method. If scoring by tricks, the player with the most tricks wins. If scoring by total cards, the player with the most cards wins. All other cases will result in a draw for both methods.
---
Files that are included:

'src/' (Source Code)

- datagen.py: This file contains the code that generates and shuffles the decks. It also contains code that generates all the possible combinations of sequences both players can choose.

- helpers.py: This file contains your debugger function.

- processing.py: This file contains code that plays all the games for each deck.

- visualization.py: This file contains code that visualizes all the winning/drawing probabilites using both methods (tricks and totals by cards).

'stored_results/' (Stored probabilites)

- results_results.csv: This file contains the probability results for each deck.

'stored_seeds/' (Stored seeds)

- results_seeds.csv: This file contains all the seeds used for each deck.

'visualizations/' (Heatmap Visualizations)

- heatmap_player_2_Win_%_(Total).svg: This file shows the heatmap that was produced from the visulization.py file. Specifically, it shows a heatmap visualization containing the winning/drawing probabilites using the total cards method.
- heatmap_player_2_Win_%_(Trick).svg: This file shows the heatmap that was produced from the visulization.py file. Specifically, it shows a heatmap visualization containing the winning/drawing probabilites using the trick method.

Main.py: This file contains testing code that produces the visualizations and the list of seeds used.

ProjectPenney#1.ipynb: This is just an extra file that contains the full code all in one file for your convenience.

---

Steps to analyze the probabilities:

1. Download all the files in the 'src/' folder. Or just the ProjectPenney#1.ipynb if you want to run it in one file.
2. Use the code in test.py to run the 1,000,000 simulations of Penney's game and to test the visualizations of those results. If using the ipynb file, run each block of code to get the desired results.

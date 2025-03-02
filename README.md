# ProjectPenney1

This project focuses on simulating many games of penney. Penney is a game where two players each choose a certain 3-bit sequence based on a combination of black and red. The deck is then drawn until there is a sequence that matches with one of the player's chosen sequence. The player also gets to keep the previously drawn cards that led to their matching sequence. The process repeats until you run out of cards. The sequence each player chooses cannot be the same. The game is scored by two methods: tricks and totals by cards. A trick is where the player found a matching sequence to their desired sequence, which counts as one trick. Totals by cards is scored by how many cards a player received for each trick.

---

Files that are included:

'src (Source code)'

- datagen.py: This file contains the code that generates and shuffles the decks. It also contains code that generates all the possible combinations of sequences both players can choose.

- helpers.py: This file contains your debugger function.

- processing.py: This file contains code that plays all the games for each deck.

- visualization.py: This file contains code that visualizes all the winning/drawing probabilites for player 2 using both methods (tricks and totals by cards).
- test.py: This file contains 
- ProjectPenney1.ipynb: This is just an extra file that contains the full code all in one file for your convenience.

---

Steps to analyze the probabilities:

1. Download all the files in the 'src' folder. Or just the ProjectPenney1.ipynb if you want to run it in one file.
2. Use the code in test.py to run the 100,000 simulations of Penney's game and to test the visualizations of those results. If using the ipynb file, run each block of code to get the desired results.

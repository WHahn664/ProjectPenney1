from processing import simulate_games
from visualization import visualize_heatmap

# This will simulate 1000000 games of penney
results1, seeds1 = simulate_games(num_decks=1000000)
visualize_heatmap(results1, ["Player 2 Win % (Trick)", "Player 2 Win % (Total)"], num_decks=1000000)
#Augment with more decks (put any number of decks in num_decks). Uncomment all the code below. Then comment the two lines of code above.
#Also, update num_decks in visualize_heatmap to the expected amount of total decks each time you want to add new decks.
#results2, seeds2 = simulate_games(
    #num_decks=100,
    #existing_results=results1,
    #existing_seeds=seeds1
    
#)

#visualize_heatmap(results2, ["Player 2 Win % (Trick)", "Player 2 Win % (Total)"], num_decks=1000100)

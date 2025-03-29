from processing import simulate_games
from visualization import visualize_heatmap

# This will simulate 1000000 games of penney
num_decks_to_generate = 1000000
results1, seeds1 = simulate_games(num_decks_to_generate)

# This will visualize our results with heatmaps
visualize_heatmap(results1, ["Player 2 Win % (Trick)", "Player 2 Win % (Total)"])

# Augment existing data with more decks (put any number of decks in num_decks). Comment out all of the lines of code below.
#results2, seeds2 = simulate_games(
#    num_decks=100,
#    existing_results=results1,
#    existing_seeds=seeds1,
#    save_prefix="test_aug",
#    save_to_file=True
#)
# visualize_heatmap(results2, ["Player 2 Win % (Trick)", "Player 2 Win % (Total)"])

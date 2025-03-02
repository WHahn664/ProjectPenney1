from processing import simulate_games
from visualization import visualize_heatmap

# This will simulate 100000 games of penney
num_decks_to_generate = 100000
results, seeds = simulate_games(num_decks_to_generate)

# This will visualize our results with heatmaps
visualize_heatmap(results, ["Player 2 Win % (Trick)", "Player 2 Win % (Total)"])

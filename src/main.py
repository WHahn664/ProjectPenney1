from processing import play_all_games
from visualization import visualize_heatmap

# Running Simulation for 100000 decks
num_decks_to_generate = 100000
results, seeds = play_all_games(num_decks_to_generate)

# Creating heatmaps for Player 2 probabilities
visualize_heatmap(results, ["Player 2 Win %", "Draw %"])

from processing import play_all_games
from visualization import visualize_heatmap

# Run Simulation
num_decks_to_generate = 100000
results, seeds = play_all_games(num_decks_to_generate)

# Visualize heatmaps for Player 2 probabilities and Draws
visualize_heatmap(results, ["Player 2 Win %", "Draw %"])
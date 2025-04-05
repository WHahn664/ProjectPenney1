from processing import simulate_games
from visualization import visualize_heatmap

#The two lines of commented code below is for when you want to create new decks from scratch without augmenting the existing data.
#Uncomment these two lines of code if you want to do so. Also, comment out the rest of the code below it.
#results1, seeds1 = simulate_games(num_decks=1000000)
#visualize_heatmap(results1, ["Player 2 Win % (Trick)", "Player 2 Win % (Total)"], num_decks=1000000)

#These two lines of code allows us to load our existing data for augmentation.
results_old = load_results_from_csv("results_results.csv")
seeds_old = load_seeds_from_csv("results_seeds.csv")

#These 4 lines of code below allows us to augment our existing data with any number of new decks. Simply change num_decks to whichever number you desire.
results_new, seeds_new = simulate_games(
    num_decks=100,
    existing_results=results_old,
    existing_seeds=seeds_old
)
#These two lines of code will allows us to update our heatmaps with the new decks.
total_decks = len(seeds_new)
visualize_heatmap(results_new, ["Player 2 Win % (Trick)", "Player 2 Win % (Total)"], num_decks=total_decks)

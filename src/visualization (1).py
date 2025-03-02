import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datagen import generate_sequences
from helpers import debugger_factory
from typing import Dict, Tuple, List

@debugger_factory()  
def visualize_heatmap(results: Dict[Tuple, Dict[str, float]], metrics: List[str]):
    """
    This function displays two heatmaps of player 2's win probabilites and draws. The left heatmap is based on using tricks, and the 
    right heatmap is based on using total cards. 
    """
    # This will create all possible sequences
    sequences = generate_sequences()

    # This will tell us how many heatmaps we need to create.
    num_metrics = len(metrics)

    # Set up the figure with subplots, one for each metric
    fig, axes = plt.subplots(1, num_metrics, figsize=(8 * num_metrics, 8))

    # If there's only one metric, make sure axes is a list (for consistent handling later)
    if num_metrics == 1:
        axes = [axes]

    # Convert sequences into a more readable label format
    # e.g., (0,0,1) becomes 'BBR' (B for 0, R for 1)
    formatted_labels = [''.join(['B' if x == 0 else 'R' for x in seq]) for seq in sequences]

    # Loop over each requested metric (one heatmap per metric)
    for idx, metric in enumerate(metrics):
        # This will create an empty square matrix
        matrix = np.zeros((len(sequences), len(sequences)))

        # This will create an annotation matrix that will hols the text labels in each heatmap cell.
        annotations = np.empty((len(sequences), len(sequences)), dtype=object)

        # This loop will fill the matrix and annotations with the probability data
        for (p1_seq, p2_seq), stats in results.items():
            # This will find the index for each sequence.
            i, j = sequences.index(p1_seq), sequences.index(p2_seq)

            # These two lines will get the value for the current metric such as win percentage
            win_pct = int(stats.get(metric, 0) * 100)  # This line converts the win decimal into a percentage
            draw_pct = int(stats.get("Draw %", 0) * 100)  # This line converts the draw decimal to a percentage

            # This will set the annotation for each cell, which is something like "65% (5%)". The draw percentage is in the parenthesis, and the other value is the win percentage
            annotations[i, j] = f"{win_pct}% ({draw_pct}%)"

            # This will set the matrix value
            matrix[i, j] = win_pct

        # This will create a heatmap using seaborn
        sns.heatmap(
            matrix,                                
            annot=annotations,                     
            fmt="",                                
            xticklabels=formatted_labels,          
            yticklabels=formatted_labels,          
            cmap="coolwarm",                       
            linewidths=0.5,                        
            annot_kws={"size": 9},                 
            ax=axes[idx]                           
        )
        axes[idx].set_title(f"Heatmap of {metric}", fontsize=14) # This sets the title of each heatmap
        axes[idx].set_xlabel("Player 2 Choices", fontsize=12) # This sets the label for the x-axis
        axes[idx].set_ylabel("Player 1 Choices", fontsize=12) # This sets the label for the y-axis

        # These two lines of code rotate the labels for better redability
        plt.setp(axes[idx].get_xticklabels(), rotation=45, ha="right")
        plt.setp(axes[idx].get_yticklabels(), rotation=0)

    # This line adjusts the layout so that the plots don't overlap with each other   
    plt.tight_layout()

    # This will show all heat maps
    plt.show()

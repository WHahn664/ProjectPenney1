import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datagen import generate_sequences
from helpers import debugger_factory
from typing import Dict, Tuple, List
import itertools
import matplotlib.colors as mcolors

@debugger_factory()  
def visualize_heatmap(results: Dict[Tuple, Dict[str, float]], metrics: List[str], save_path: str = "heatmap", num_decks: int=1000000):
    """
    Visualizes win and draw percentages. Outputs two different heatmaps (one scoring by tricks and the other scoring by total cards).
    """
    #This will generate all possible 3-letter red/black sequences.
    sequences = generate_sequences()
    #This will allow us to convert each sequence from a tuple to a string when labeling the axes for our heatmaps.
    formatted_labels = [''.join(seq) for seq in sequences]

    #These three lines of code below allow us to title each of our heatmaps with the appropriate title.
    custom_titles = {
        "Player 2 Win % (Trick)": f"My Chance of Win(Draw)\nby Tricks\nN = {num_decks:,}",
        "Player 2 Win % (Total)": f"My Chance of Win(Draw)\nby Cards\nN = {num_decks:,}"
    }
    
    for idx, metric in enumerate(metrics):
        
        matrix = np.zeros((len(sequences), len(sequences)))
        annotations = np.empty((len(sequences), len(sequences)), dtype=object)
        mask = np.zeros_like(matrix, dtype=bool)

        
        for (p1_seq, p2_seq), stats in results.items():
            i, j = sequences.index(p1_seq), sequences.index(p2_seq)

            if i == j:  
                matrix[i, j] = np.nan  
                annotations[i, j] = ""  
                mask[i, j] = True  
            else:
                win_pct = round(stats.get(metric, 0) * 100)
                draw_metric = "Draw % (Trick)" if "Trick" in metric else "Draw % (Total)"
                draw_pct = int(stats.get(draw_metric, 0) * 100)
                annotations[i, j] = f"{win_pct} ({draw_pct})"
                matrix[i, j] = win_pct

        
        cmap = sns.color_palette("Blues", as_cmap=True) 
        cmap.set_bad(color='lightgrey')  

        
        fig, ax = plt.subplots(figsize=(10, 8))

        sns.heatmap(
            matrix,
            annot=annotations,
            fmt="",
            xticklabels=formatted_labels,
            yticklabels=formatted_labels,
            cmap=cmap,
            linewidths=0.5,
            annot_kws={"size": 9},
            mask=mask,  
            cbar=False,  
            ax=ax
        )

        #These two lines of code will label the axes.
        ax.set_xlabel("Player 1 Sequence", fontsize=14, labelpad=15)
        ax.set_ylabel("Player 2 Sequence", fontsize=14, labelpad=15)

        #These two lines of code will allow us to put ticks on our heatmaps.
        ax.set_xticklabels(formatted_labels, rotation=0, ha="center")
        ax.set_yticklabels(formatted_labels, rotation=0)

        #This line of code will allow us to use our custom titles when labeling our heatmaps.
        ax.set_title(custom_titles.get(metric, f"Win Probability by {metric}\nN = 1,000,000"), fontsize=16)

        #These lines of save each plot as a SVG file. One heatmap is based on the Tricks scoring method and the other heatmap is based
        #on the Total Cards scoring method. There should be a total of two SVG files.
        filename = f"{save_path}_{metric.replace(' ', '_')}.svg"
        plt.tight_layout()
        plt.savefig(filename, format="svg")
        print(f"Saved: {filename}")
        plt.close(fig)



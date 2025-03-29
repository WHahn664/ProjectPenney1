import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datagen import generate_sequences
from helpers import debugger_factory
from typing import Dict, Tuple, List
import itertools
@debugger_factory()  
def visualize_heatmap(results: Dict[Tuple, Dict[str, float]], metrics: List[str], save_path: str = "heatmap"):
    """
    Visualizes win and draw percentages
    """
    sequences = list(itertools.product('BR', repeat=3))
    num_metrics = len(metrics)
    fig, axes = plt.subplots(1, num_metrics, figsize=(8 * num_metrics, 8))
    if num_metrics == 1:
        axes = [axes]
    formatted_labels = [''.join(seq) for seq in sequences]

    for idx, metric in enumerate(metrics):
        matrix = np.zeros((len(sequences), len(sequences)))
        annotations = np.empty((len(sequences), len(sequences)), dtype=object)

        for (p1_seq, p2_seq), stats in results.items():
            i, j = sequences.index(p1_seq), sequences.index(p2_seq)
            win_pct = int(stats.get(metric, 0) * 100)
            draw_metric = "Draw % (Trick)" if "Trick" in metric else "Draw % (Total)"
            draw_pct = int(stats.get(draw_metric, 0) * 100)
            
            annotations[i, j] = f"{win_pct} ({draw_pct})"
            matrix[i, j] = win_pct

        sns.heatmap(
            matrix,
            annot=annotations,
            fmt="",
            xticklabels=formatted_labels,
            yticklabels=formatted_labels,
            cmap="Blues",
            linewidths=0.5,
            annot_kws={"size": 9},
            ax=axes[idx],
            cbar=False
        )
        axes[idx].set_title(f"My Chance of Win (Draw) by {metric}", fontsize=14)
        if idx == 0:  # First heatmap (for Player 2's Win % based on Tricks)
            axes[idx].set_title("My Chance of Win (Draw) \n by Tricks \n N = 1,000,000", fontsize=14)
        elif idx == 1:  # Second heatmap (for Player 2's Win % based on Total Cards)
            axes[idx].set_title("My chance of Win (Draw) \n by Cards \n N = 1,000,000", fontsize=14)
        axes[idx].set_xlabel("Player 2 Choices", fontsize=12)
        axes[idx].set_ylabel("Player 1 Choices", fontsize=12)
        plt.setp(axes[idx].get_xticklabels(), rotation=0, ha="right")
        plt.setp(axes[idx].get_yticklabels(), rotation=0)

    plt.tight_layout()
    filename = f"{save_path}_{metric.replace(' ', '_')}.svg"
    plt.savefig(filename, format="svg")
    print(f"Saved: {filename}")

        # Close the figure to free memory
    plt.close(fig)
    plt.show()

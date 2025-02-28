import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from typing import Dict, Tuple, List
from processing import generate_sequences
from helpers import debugger_factory

@debugger_factory()
def visualize_heatmap(results: Dict[Tuple, Dict[str, float]], metrics: List[str]):
    sequences = generate_sequences()
    num_metrics = len(metrics)
    
    fig, axes = plt.subplots(1, num_metrics, figsize=(6 * num_metrics, 6))
    
    if num_metrics == 1:
        axes = [axes]
    
    def format_sequence(seq):
        return ''.join(['B' if x == 0 else 'R' for x in seq])
    
    formatted_labels = [format_sequence(seq) for seq in sequences]
    
    for idx, metric in enumerate(metrics):
        matrix = np.zeros((len(sequences), len(sequences)))
        
        for (p1_seq, p2_seq), stats in results.items():
            i, j = sequences.index(p1_seq), sequences.index(p2_seq)
            matrix[i, j] = stats[metric]
        
        sns.heatmap(matrix, annot=True, xticklabels=formatted_labels, yticklabels=formatted_labels, cmap="coolwarm", ax=axes[idx])
        axes[idx].set_title("{metric}")
        axes[idx].set_xlabel("Player 2 Sequence")
        axes[idx].set_ylabel("Player 1 Sequence")
        axes[idx].tick_params(axis='y', rotation=0)
    
    plt.tight_layout()
    plt.show()

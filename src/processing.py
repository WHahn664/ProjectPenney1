from typing import Dict, List, Tuple
import itertools
from datagen import generate_sequences, get_n_decks
from helpers import debugger_factory
from datagen import HALF_DECK_SIZE
import numpy as np
from typing import Dict, Tuple, List, Optional
import csv

def generate_1_game(deck: np.ndarray, player1_seq: Tuple[str, str, str], player2_seq: Tuple[str, str, str]) -> Tuple[int, int, int, int]:
    """
    Simulates one game of Penney.
    - Players choose their sequences.
    - Flip cards one at a time until a player's sequence occurs.
    - The player who gets a match is awarded one trick and all previous cards plus the 3 matching cards.
    """

    p1_str, p2_str = ''.join(player1_seq), ''.join(player2_seq)
    p1_tricks, p2_tricks = 0, 0
    p1_total_cards, p2_total_cards = 0, 0
    collected_cards = 0
    current_sequence = []

    for card in deck:
        current_sequence.append('B' if card == 0 else 'R')
        collected_cards += 1

        if len(current_sequence) >= 3:
            trick_str = ''.join(current_sequence[-3:])

            if trick_str == p1_str:
                p1_tricks += 1
                p1_total_cards += collected_cards
                collected_cards = 0
                current_sequence = []
                continue

            if trick_str == p2_str:
                p2_tricks += 1
                p2_total_cards += collected_cards
                collected_cards = 0
                current_sequence = []
                continue

    return p1_tricks, p2_tricks, p1_total_cards, p2_total_cards

@debugger_factory()
def simulate_games(
    num_decks: int,
    existing_results: Dict[Tuple, Dict[str, float]] = None,
    existing_seeds: List[int] = None,
    save_prefix: str = "results",
    save_to_file: bool = True
) -> Tuple[Dict[Tuple, Dict[str, float]], List[int]]:
    """
    Simulates multiple games of Penney.
    """

    sequences = generate_sequences()
    if existing_results is None:
        results = {(p1, p2): {"Player 2 Win % (Trick)": 0.0,
                              "Player 2 Win % (Total)": 0.0,
                              "Draw % (Trick)": 0.0,
                              "Draw % (Total)": 0.0}
                   for p1 in sequences for p2 in sequences}
        used_seeds = []
    else:
        results = existing_results
        used_seeds = existing_seeds

    decks = get_n_decks(num_decks)
    for seed, deck in decks:
        used_seeds.append(seed)
        for p1 in sequences:
            for p2 in sequences:
                p1_tricks, p2_tricks, p1_cards, p2_cards = generate_1_game(deck, p1, p2)

                total_tricks = p1_tricks + p2_tricks
                total_cards = p1_cards + p2_cards
                if p1_tricks > p2_tricks:
                    results[(p1, p2)]["Draw % (Trick)"] += 0
                elif p1_tricks < p2_tricks:
                    results[(p1, p2)]["Player 2 Win % (Trick)"] += 1
                else:
                    results[(p1, p2)]["Draw % (Trick)"] += 1
                
                if p1_cards > p2_cards:
                    results[(p1, p2)]["Draw % (Total)"] += 0
                elif p1_cards < p2_cards:
                    results[(p1, p2)]["Player 2 Win % (Total)"] += 1
                else:
                    results[(p1, p2)]["Draw % (Total)"] += 1
    for key in results:
        for metric in results[key]:
            results[key][metric] /= num_decks

    if save_to_file:
        csv_filename = f"{save_prefix}_results.csv"
        with open(csv_filename, mode='w', newline='') as csvfile:
            fieldnames = ["Player 1", "Player 2", "Player 2 Win % (Trick)", "Player 2 Win % (Total)", "Draw % (Trick)", "Draw % (Total)"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for (p1, p2), stats in results.items():
                row = {
                    "Player 1": ''.join(p1),
                    "Player 2": ''.join(p2),
                    **stats
                }
                writer.writerow(row)

        seeds_filename = f"{save_prefix}_seeds.csv"
        with open(seeds_filename, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Seed"])
            for seed in used_seeds:
                writer.writerow([seed])

    return results, used_seeds

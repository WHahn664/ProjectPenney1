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

    #This line of code converts each player's sequences into strings.
    p1_str, p2_str = ''.join(player1_seq), ''.join(player2_seq)
    #These two lines of code help us keep track of how many tricks and cards each player won.
    p1_tricks, p2_tricks = 0, 0
    p1_total_cards, p2_total_cards = 0, 0
    #This will allow us to keep track of the number of cards flipped before a sequence match.
    collected_cards = 0
    #This will us to keep track of the running sequence of the flipped cards.
    current_sequence = []
    
    #This loop allows us to play the game of Penney by flipping one card at a time. Also, keeps track of number of tricks and total cards won for each player.
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
    Simulates multiple games of Penney. This function can also augmenting existing results if you so choose. 
    Outputs the results and seeds used.
    """
    #This will generate all possible 3-letter red/black sequences.
    sequences = generate_sequences()

    # If there is no existing data, then it will initialize new dictionaries. Otherwise, it will use the existing results and seeds.
    if existing_results is None:
        results = {(p1, p2): {"Player 2 Win % (Trick)": 0.0,
                              "Player 2 Win % (Total)": 0.0,
                              "Draw % (Trick)": 0.0,
                              "Draw % (Total)": 0.0}
                   for p1 in sequences for p2 in sequences}
        used_seeds = []
    else:
        results = existing_results
        used_seeds = existing_seeds.copy() if existing_seeds else []
        existing_total = len(used_seeds)
        for key in results:
            for metric in results[key]:
                results[key][metric] *= existing_total
        

    #This will allow us to generate new decks and seeds.
    decks = get_n_decks(num_decks)
    
    #These loops will allow us to loop over each deck. These loops will also allow us to play multiple games of Penney for each deck.
    #These loops will also allow us to determine the winner based on the number tricks or the number of total cards for each deck.
    for seed, deck in decks:
        used_seeds.append(seed)
        for p1 in sequences:
            for p2 in sequences:
                p1_tricks, p2_tricks, p1_cards, p2_cards = generate_1_game(deck, p1, p2)

                if (p1, p2) not in results:
                    results[(p1, p2)] = {
                        "Player 2 Win % (Trick)": 0.0,
                        "Player 2 Win % (Total)": 0.0,
                        "Draw % (Trick)": 0.0,
                        "Draw % (Total)": 0.0
                    }
                
                if p1_tricks > p2_tricks:
                    pass
                elif p1_tricks < p2_tricks:
                    results[(p1, p2)]["Player 2 Win % (Trick)"] += 1
                else:
                    results[(p1, p2)]["Draw % (Trick)"] += 1
                
                if p1_cards > p2_cards:
                    pass
                elif p1_cards < p2_cards:
                    results[(p1, p2)]["Player 2 Win % (Total)"] += 1
                else:
                    results[(p1, p2)]["Draw % (Total)"] += 1


    #These 4 lines of code will allow us to determine the probabilities.
    total_decks = len(used_seeds)
    for key in results:
        for metric in results[key]:
            results[key][metric] /= total_decks
    

    #These blocks of code will save our probabilities/results as a 'results_results.csv' file. 
    #These blocks of code will also save our used seeds as a 'results_seeds.csv' file
    if save_to_file:
        csv_filename = f"{save_prefix}_results.csv"
        with open(csv_filename, mode='w', newline='') as csvfile:
            fieldnames = ["Player 1", "Player 2", "Player 2 Win % (Trick)", "Player 2 Win % (Total)", "Draw % (Trick)", "Draw % (Total)"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for (p1, p2), stats in results.items():
                stats_rounded = {metric: round(value, 3) if isinstance(value, float) else value for metric, value in stats.items()}
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

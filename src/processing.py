from typing import Dict, List, Tuple
import itertools
from datagen import generate_sequences, get_n_decks
from helpers import debugger_factory
from datagen import HALF_DECK_SIZE
import numpy as np
import json
from typing import Dict, Tuple, List, Optional
import csv

def generate_1_game(deck: np.ndarray, player1_seq: Tuple[str, str, str], player2_seq: Tuple[str, str, str]) -> Tuple[int, int, int, int]:
    """
    Simulates one game of Penney.
    - Players choose their sequences.
    - Flip cards one at a time until a player's sequence occurs.
    - The player who gets a match is awarded one trick and all previous cards plus the 3 matching cards.
    """
    if player1_seq == player2_seq:
        raise ValueError("Players cannot choose the same sequence.")

    p1_str, p2_str = ''.join(player1_seq), ''.join(player2_seq)
    p1_tricks, p2_tricks = 0, 0
    p1_total_cards, p2_total_cards = 0, 0
    collected_cards = 0  
    current_sequence = []

    for card in deck:
        current_sequence.append(card)
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
    num_decks: int = 1000000,
    existing_results: Optional[Dict[Tuple, Dict[str, float]]] = None,
    existing_seeds: Optional[List[int]] = None,
    save_prefix: Optional[str] = None,
    save_to_file: bool = False
) -> Tuple[Dict[Tuple, Dict[str, float]], List[int]]:
    """
    Simulates multiple games of Penney.
    """
    sequences = list(itertools.product('BR', repeat=3))
    results = existing_results if existing_results else {}
    seeds = existing_seeds if existing_seeds else []

    new_seeds = []

    for i in range(num_decks):
        seed = np.random.randint(0, 2**32 - 1)
        new_seeds.append(seed)
        rng = np.random.default_rng(seed)
        deck = rng.choice(['B', 'R'], size=52)

        for player1_seq, player2_seq in itertools.combinations(sequences, 2):
            p1_count, p2_count, p1_cards, p2_cards = generate_1_game(deck, player1_seq, player2_seq)

            for a, b, p1, p2 in [(player1_seq, player2_seq, p1_count, p2_count),
                                 (player2_seq, player1_seq, p2_count, p1_count)]:

                key = (a, b)
                if key not in results:
                    results[key] = {
                        "Player 2 Win % (Trick)": 0,
                        "Player 2 Win % (Total)": 0,
                        "Draw % (Trick)": 0,
                        "Draw % (Total)": 0,
                        "games": 0
                    }

                res = results[key]
                res["Player 2 Win % (Trick)"] += int(p2 > p1)
                res["Player 2 Win % (Total)"] += int(p2_cards > p1_cards)
                res["Draw % (Trick)"] += int(p2 == p1)
                res["Draw % (Total)"] += int(p2_cards == p1_cards)
                res["games"] += 1

    
    for stats in results.values():
        g = stats["games"]
        if g > 0:
            stats["Player 2 Win % (Trick)"] /= g
            stats["Player 2 Win % (Total)"] /= g
            stats["Draw % (Trick)"] /= g
            stats["Draw % (Total)"] /= g

    seeds += new_seeds

    
    if save_to_file and save_prefix:
        with open(f"{save_prefix}_results.json", "w") as f:
            json.dump({str(k): v for k, v in results.items()}, f, indent=2)

        with open(f"{save_prefix}_seeds.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["seed"])
            writer.writerows([[s] for s in seeds])

        print(f"Saved {len(seeds)} seeds and results to: {save_prefix}_*.json/csv")

    return results, seeds

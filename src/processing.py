import itertools
import numpy as np
from typing import List, Tuple, Dict
from datagen import get_n_decks
from helpers import debugger_factory

def generate_sequences() -> List[Tuple[int, int, int]]:
    return list(itertools.product([0, 1], repeat=3))

def generate_1_game(deck: np.ndarray, player1_seq: Tuple[int, int, int], player2_seq: Tuple[int, int, int]) -> Tuple[int, int, int, int]:
    if player1_seq == player2_seq:
        raise ValueError("Players cannot choose the same sequence.")
    
    deck_str = ''.join(map(str, deck))
    p1_str, p2_str = ''.join(map(str, player1_seq)), ''.join(map(str, player2_seq))
    
    p1_count = deck_str.count(p1_str)
    p2_count = deck_str.count(p2_str)
    
    p1_first, p2_first = deck_str.find(p1_str), deck_str.find(p2_str)
    
    if p1_first != -1 and (p2_first == -1 or p1_first < p2_first):
        winner = 1
    elif p2_first != -1 and (p1_first == -1 or p2_first < p1_first):
        winner = 2
    else:
        winner = 0
    
    return winner, p1_count, p2_count, max(p1_first, p2_first, len(deck))

@debugger_factory()
def play_all_games(num_decks: int = 100000) -> Tuple[Dict[Tuple, Dict[str, float]], Dict[Tuple, List[int]]]:
    sequences = generate_sequences()
    results = {}
    seeds = {}
    
    for player1_seq, player2_seq in itertools.combinations(sequences, 2):
        decks = get_n_decks(num_decks)
        
        outcomes = []
        p1_trick_counts, p2_trick_counts = [], []
        total_cards_used = []
        seed_list = []
        
        for seed, deck in decks:
            winner, p1_count, p2_count, total_cards = generate_1_game(deck, player1_seq, player2_seq)
            outcomes.append(winner)
            p1_trick_counts.append(p1_count)
            p2_trick_counts.append(p2_count)
            total_cards_used.append(total_cards)
            seed_list.append(seed)
        
        results[(player1_seq, player2_seq)] = {
            "Player 1 Win %": outcomes.count(1) / num_decks,
            "Player 2 Win %": outcomes.count(2) / num_decks,
            "Draw %": outcomes.count(0) / num_decks,
            "Player 1 Avg Tricks": np.mean(p1_trick_counts),
            "Player 2 Avg Tricks": np.mean(p2_trick_counts),
            "Avg Cards Used": np.mean(total_cards_used)
        }
        
        seeds[(player1_seq, player2_seq)] = seed_list
    
    return results, seeds
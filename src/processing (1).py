from typing import Dict, List, Tuple
import itertools
from datagen import generate_sequences, get_n_decks
from helpers import debugger_factory
from datagen import HALF_DECK_SIZE
import numpy as np


def generate_1_game(deck: np.ndarray, player1_seq: Tuple[int, int, int], player2_seq: Tuple[int, int, int]) -> Tuple[int, int, int, int]:
    """
    This function plays one game. Each player chooses a sequence. And the player whose sequence appears first in the deck is the winner.
    """
    if player1_seq == player2_seq:
        raise ValueError("Players cannot choose the same sequence.") # This ensures that both players cannot choose the same sequence

    # These two lines convert the deck and sequences into strings so that we can easily search within them.
    deck_str = ''.join(map(str, deck)) 
    p1_str, p2_str = ''.join(map(str, player1_seq)), ''.join(map(str, player2_seq))

    # These two lines count how many times each player's desired sequence shows up in the deck (tricks).
    p1_count = deck_str.count(p1_str)
    p2_count = deck_str.count(p2_str)

    # These two lines counts the total amount of cards used for each player's desired sequence (totals cards)
    p1_total_cards = sum(len(p1_str) for i in range(len(deck) - 2) if deck_str[i:i+3] == p1_str)
    p2_total_cards = sum(len(p2_str) for i in range(len(deck) - 2) if deck_str[i:i+3] == p2_str)

    return p1_count, p2_count, p1_total_cards, p2_total_cards


@debugger_factory()
def simulate_games(num_decks: int = 100000) -> Tuple[Dict[Tuple, Dict[str, float]], Dict[Tuple, List[int]]]:
    """
    This function simulates all games for each deck in num_decks. It also calculates win percentages and draw percentages.
    """
    sequences = generate_sequences()    # Creates all 3-bit sequences
    results = {}                        # Stores win and draw probabilities
    seeds = {}                          # Stores each deck's seed

    # This loop will help us iterate over all possible pairs of sequences (56 possible combinations).
    for player1_seq, player2_seq in itertools.combinations(sequences, 2):
        decks = get_n_decks(num_decks)  # This allows us to get the shuffled decks

        # These four lines will help us keep track of the tricks, total cards, and draws
        p1_wins_trick, p2_wins_trick = 0, 0
        p1_wins_total, p2_wins_total = 0, 0
        draws1 = 0
        draws2 = 0

        # This loop plays all each deck
        for seed, deck in decks:
            p1_count, p2_count, p1_cards, p2_cards = generate_1_game(deck, player1_seq, player2_seq)

            # These five linese determine the winner based on the number of tricks
            if p1_count > p2_count:
                p1_wins_trick += 1
            elif p2_count > p1_count:
                p2_wins_trick += 1
            else:
                draws1 += 1

            # These four lines determine the winner by comparing the total amount of cards used by each player
            if p1_cards > p2_cards:
                p1_wins_total += 1
            elif p2_cards > p1_cards:
                p2_wins_total += 1
            else:
                draws2 += 1

        # These two blocks of code help us store our probabilities.
        results[(player1_seq, player2_seq)] = {
            "Player 2 Win % (Trick)": p2_wins_trick / num_decks,
            "Player 2 Win % (Total)": p2_wins_total / num_decks,
            "Draw %": draws1 / num_decks
        }
        results[(player2_seq, player1_seq)] = {
            "Player 2 Win % (Trick)": p1_wins_trick / num_decks,
            "Player 2 Win % (Total)": p1_wins_total / num_decks,
            "Draw %": draws2 / num_decks
        }

    return results, seeds

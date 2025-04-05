import numpy as np
import itertools
import random
from typing import List, Tuple, Dict
from helpers import debugger_factory

HALF_DECK_SIZE = 26

def get_init_deck(half_deck_size: int) -> np.ndarray:
    """
    This function creates an initial decks of 0s (Blacks) and 1s (Reds)
    
    """
    return np.array([0] * half_deck_size + [1] * half_deck_size)

def shuffle_deck(seed: int, deck: np.ndarray) -> np.ndarray:
    """
    This function shuffles a deck using a specific random seed. Shuffles a given deck using a specified seed.
    
    """
    np.random.seed(seed)
    shuffled_deck = deck.copy()
    np.random.shuffle(shuffled_deck)
    return shuffled_deck

@debugger_factory()    
def get_n_decks(num_decks: int, num_cards: int = HALF_DECK_SIZE) -> List[Tuple[int, np.ndarray]]:
    """
    This function creates a list of shuffled decks each with unique random seeds. Also, each deck has a tuple containing (seed, deck).
    """
    init_deck = get_init_deck(num_cards)
    decks = []
    for _ in range(num_decks):
        seed = np.random.randint(0, 2**32-1)
        shuffled_deck = shuffle_deck(seed, init_deck)
        decks.append((seed, shuffled_deck))
    return decks
    

def generate_sequences() -> List[Tuple[str, str, str]]:
     """This function creates all possible combinations of 0s and 1s Generates all possible three-card sequences of Bs and Rs."""
     return list(itertools.product('BR', repeat=3))


def load_results_from_csv(filepath: str) -> Dict[Tuple[str, str], Dict[str, float]]:
    """
    This function allows us to load the results_results.csv file containing all the results from multiple games of Penney.
    This function is only used if we want augment existing data.
    """
    results = {}
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            p1 = tuple(row["Player 1"])  
            p2 = tuple(row["Player 2"])  
            if len(p1) != 3 or len(p2) != 3:
                print(f"Skipping invalid row: {row}")
                continue
            results[(p1, p2)] = {
                "Player 2 Win % (Trick)": float(row["Player 2 Win % (Trick)"]),
                "Player 2 Win % (Total)": float(row["Player 2 Win % (Total)"]),
                "Draw % (Trick)": float(row["Draw % (Trick)"]),
                "Draw % (Total)": float(row["Draw % (Total)"])
            }
    return results
def load_seeds_from_csv(filepath: str) -> List[int]:
    """
    This function allows us to load the results_seeds.csv file containg all the seeds used for each deck.
    This function is only used if we want to augment existing data.
    """
    seeds = []
    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  
        for row in reader:
            seeds.append(int(row[0]))
    return seeds


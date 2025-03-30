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
     """This function creates all possible combinations of 0s and 1s Generates all possible three-card sequences of 0s and 1s."""
     return list(itertools.product('BR', repeat=3))

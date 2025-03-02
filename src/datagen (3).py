import numpy as np
import itertools
import random
from typing import List, Tuple, Dict
from helpers import debugger_factory

HALF_DECK_SIZE = 26

def get_init_deck(HALF_DECK_SIZE: int) -> np.ndarray:
    """
    This function creates an initial decks of 0s (Blacks) and 1s (Reds)
    
    """
    return np.array([0] * HALF_DECK_SIZE + [1] * HALF_DECK_SIZE)

def shuffle_deck(seed: int, deck: np.ndarray) -> np.ndarray:
    """
    This function shuffles a deck using a specific random seed. Shuffles a given deck using a specified seed.
    
    """
    np.random.seed(seed)             # Allows us to store a random seed
    shuffled_deck = deck.copy()      # Making a copy of the deck
    np.random.shuffle(shuffled_deck) # Allows us to shuffle the deck
    return shuffled_deck             # Returns the shuffled deck


@debugger_factory()
def get_n_decks(num_decks: int, num_cards: int = HALF_DECK_SIZE) -> List[Tuple[int, np.ndarray]]:
    """
    This function creates a list of shuffled decks each with unique random seeds. Also, each deck has a tuple containing (seed, deck).
    """
    init_deck = get_init_deck(num_cards)  # This creates the initial deck
    decks = []                            # This creates a list to store the decks

    for _ in range(num_decks):
        seed = random.randint(0, 2**31 - 1)          # This generates a random seed from 0 to 2,147,483,648
        shuffled_deck = shuffle_deck(seed, init_deck) # This shuffles the deck using that assigned random seed
        decks.append((seed, shuffled_deck))           # This stores the seeds and the shuffled decks

    return decks


def generate_sequences() -> List[Tuple[int, int, int]]:
    """This function creates all possible combinations of 0s and 1s Generates all possible three-card sequences of 0s and 1s."""
    return list(itertools.product([0, 1], repeat=3))  # This creates all possible combinations of 3-bit sequences 3-bit binary sequence

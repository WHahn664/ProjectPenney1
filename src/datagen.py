import numpy as np
import random
from typing import List, Tuple
from helpers import HALF_DECK_SIZE

def get_init_deck(half_deck_size: int = HALF_DECK_SIZE) -> np.ndarray:
    return np.array([0] * half_deck_size + [1] * half_deck_size)

def shuffle_deck(seed: int, deck: np.ndarray) -> np.ndarray:
    np.random.seed(seed)
    shuffled_deck = deck.copy()
    np.random.shuffle(shuffled_deck)
    return shuffled_deck

def get_n_decks(num_decks: int, num_cards: int = HALF_DECK_SIZE) -> List[Tuple[int, np.ndarray]]:
    init_deck = get_init_deck(num_cards)
    decks = []
    
    for _ in range(num_decks):
        seed = random.randint(0, 2**31 - 1)
        shuffled_deck = shuffle_deck(seed, init_deck)
        decks.append((seed, shuffled_deck))
    
    return decks

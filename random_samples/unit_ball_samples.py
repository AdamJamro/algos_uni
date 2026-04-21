from typing import TypeAlias

from randomness_config import *

def pivot_with_mask(vec: np.ndarray, mask: np.ndarray):
    """expects 2dim vector array"""

    size = mask.sum()
    new_samples = np.random.random_sample(size * vec.shape[1]).reshape(size, vec.shape[1])
    vec[mask] = new_samples
    vec[:] = np.concatenate((vec[~mask], new_samples))


def generate_samples(quantity: int = 10, dimension: int = 2, p_norm: int | float = 2) -> np.ndarray:
    """Generate random points in a unit ball of given dimension."""

    def p_norm_to_p(_vec):
        """calculates (||vec||_p) ^ p"""
        return np.power(np.abs(_vec), p_norm).sum(axis=-1)

    sample_vec = random_sample(quantity * dimension).reshape((quantity, dimension))

    while np.any(mask := (p_norm_to_p(sample_vec) >= 1.0)):
        pivot_with_mask(sample_vec, mask)

    return sample_vec.reshape(quantity, dimension)


# code specialized for p generator samples
# TODO delete?

Mask: TypeAlias = np.ndarray[bool]
def generate_samples_with_mask_callback(quantity: int, dimension: int, mask_callback: Callable[[np.ndarray], Mask]) -> np.ndarray:
    sample_vec = random_sample(quantity * dimension).reshape((quantity, dimension))

    while any(mask := mask_callback(sample_vec)):
        pivot_with_mask(sample_vec, mask)

    return sample_vec

def generate_samples_p1(quantity: int = 10, dimension: int = 2) -> np.ndarray:
    sample_vec = random_sample(quantity * dimension).reshape(quantity, dimension)

    while any(mask := (sample_vec.sum(axis=-1) >= 1.0)):
        pivot_with_mask(sample_vec, mask)

    return sample_vec


def generate_samples_pmax(quantity: int = 10, dimension: int = 2) -> np.ndarray:
    sample_vec = random_sample(quantity * dimension).reshape(quantity, dimension)

    while any(mask := (np.abs(sample_vec).max(axis=-1) >= 1.0)):
        pivot_with_mask(sample_vec, mask)

    return sample_vec

def generate_samples_p2(quantity: int = 10, dimension: int = 2) -> np.ndarray:
    sample_vec = random_sample(quantity * dimension).reshape(quantity, dimension)

    while any(mask := ((sample_vec * sample_vec).sum(axis=-1) >= 1.0)):
        pivot_with_mask(sample_vec, mask)

    return sample_vec



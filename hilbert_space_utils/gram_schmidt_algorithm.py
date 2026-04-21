from typing import Iterable

from hilbert_space_utils import *
from normalization import normalize
from dot_product import dot_product

np.array([1, 2, 3])


def gram_schmidt_algorithm(vectors: Iterable[np.ndarray]):
    """
    Apply the Gram-Schmidt algorithm to a set of vectors to produce an orthonormal basis.

    Parameters:
    vectors (array-like): A list of input vectors.

    Returns:
    numpy.ndarray: An array of orthonormal vectors.
    """
    orthonormal_basis = []

    for v in vectors:
        w = v.copy()
        for u in orthonormal_basis:
            proj = dot_product(w, u) * u
            w = w - proj

        if np.linalg.norm(w) > 1e-10:
            orthonormal_basis.append(normalize(w))

    return np.array(orthonormal_basis)


if __name__ == "__main__":
    vectors = [np.array([1, 1, 0]), np.array([1, 0, 1]), np.array([0, 1, 1])]
    orthonormal_basis = gram_schmidt_algorithm(vectors)
    print("Orthonormal basis:")
    for vec in orthonormal_basis:
        print(f"{vec=}")
        print(f"{dot_product(vec, vec)=}")
        print(f"{[dot_product(vec, other) for other in orthonormal_basis]=}")
        print()
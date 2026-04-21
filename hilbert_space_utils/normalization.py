from hilbert_space_utils import np
from dot_product import dot_product


def normalize(vector):
    """
    Normalize a vector to have unit length.

    Parameters:
    vector (array-like): The input vector to be normalized.

    Returns:
    numpy.ndarray: The normalized vector with unit length.
    """
    vector = np.array(vector)
    norm = np.sqrt(dot_product(vector, vector))
    if norm == 0:
        raise ValueError("Cannot normalize a zero vector.")

    return vector / norm


if __name__ == "__main__":
    v = [3, 4]
    normalized_v = normalize(v)
    print("Normalized vector:", normalized_v)
    print(
        "Norm of the normalized vector:",
        np.sqrt(dot_product(normalized_v, normalized_v)),
    )

    v = [1 + 1j, 2 + 2j]
    normalized_v = normalize(v)
    print("Normalized vector:", normalized_v)
    print(
        "Norm of the normalized vector:",
        np.sqrt(dot_product(normalized_v, normalized_v)),
    )

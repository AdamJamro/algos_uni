from hilbert_space_utils import np

def dot_product(vector_a, vector_b):
    """
    Compute the dot product of two vectors.

    Returns:
    float: The dot product of the two vectors.
    """
    return np.dot(np.array(vector_a), np.conjugate(np.array(vector_b)))


if __name__ == "__main__":
    a = [1, 2, 3]
    b = [4, 5, 6]
    print(dot_product(a, b))

    a = [1, 2, 3]
    b = [4 + 1j, 5 + 1j, 6 + 1j]
    print(dot_product(a, b))
